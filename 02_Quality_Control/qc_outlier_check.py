import pandas as pd
import numpy as np
import os

# ==========================================
# [Configuration] 설정
# ==========================================
RAW_FILE = "raw_climate_data.csv"
CLEAN_FILE = "clean_climate_data.csv"

# QC Thresholds (물리적 한계값 설정 - 현업 기준 예시)
TEMP_MIN = -50.0
TEMP_MAX = 50.0
PRECIP_MIN = 0.0
PRECIP_MAX = 500.0  # Daily max realistic limit

# ==========================================
# [Step 0] Mock Dirty Data Generation
# (실습용: 결측치, 이상치, 에러가 포함된 '지저분한' 데이터 생성)
# ==========================================
def generate_dirty_data():
    print("⚠️  Generating 'Dirty' Mock Data with errors...")
    
    dates = pd.date_range(start="2024-01-01", periods=15, freq="D")
    
    # 정상 데이터 + 의도적인 오류 주입
    temps = [25.0, 26.2, 25.8, 999.9, 27.0, np.nan, 26.5, 25.9, 26.1, 150.0, 24.8, 25.5, -100.0, 26.0, 26.3]
    precips = [0.0, 5.0, 10.2, -5.0, 0.0, 0.0, 20.5, np.nan, 0.0, 800.0, 15.0, 0.0, 0.0, 2.5, 0.0]
    
    # 999.9: 장비 에러 코드, np.nan: 결측, 150.0/800.0: 이상치, -5.0: 물리적 불가능값
    
    df = pd.DataFrame({
        "date": dates,
        "temperature": temps,
        "precipitation": precips
    })
    
    df.to_csv(RAW_FILE, index=False)
    print(f"   [OK] Created {RAW_FILE} with intended errors.")
    print("-" * 50)

# ==========================================
# [Step 1] Physical Limit Check (Range Check)
# Module 3 Lec 11: Error Detection
# ==========================================
def apply_physical_qc(df):
    print("1️⃣  Applying Physical Limit QC...")
    
    # Create QC Flag columns (0: Good, 1: Bad/Suspect)
    df['qc_flag_temp'] = 0
    df['qc_flag_precip'] = 0
    
    # 1. Temperature Check
    # 범위를 벗어나거나 999.9 같은 에러 코드는 NaN 처리 및 Flagging
    mask_temp_bad = (df['temperature'] < TEMP_MIN) | (df['temperature'] > TEMP_MAX)
    df.loc[mask_temp_bad, 'qc_flag_temp'] = 1  # Mark as Bad
    df.loc[mask_temp_bad, 'temperature'] = np.nan # Treat as missing for interpolation later
    
    # 2. Precipitation Check
    mask_precip_bad = (df['precipitation'] < PRECIP_MIN) | (df['precipitation'] > PRECIP_MAX)
    df.loc[mask_precip_bad, 'qc_flag_precip'] = 1
    df.loc[mask_precip_bad, 'precipitation'] = np.nan
    
    print("   -> Limit checks applied. Out of bound values set to NaN.")
    return df

# ==========================================
# [Step 2] Statistical Outlier Detection (Z-Score)
# Module 3 Lec 11: Outlier Control using statistical methods
# ==========================================
def apply_statistical_qc(df):
    print("2️⃣  Applying Statistical QC (Z-Score)...")
    
    # Calculate Z-score for temperature (ignoring NaNs)
    mean_temp = df['temperature'].mean()
    std_temp = df['temperature'].std()
    
    # Z-score가 3 이상(표준편차의 3배)이면 이상치로 간주
    z_scores = (df['temperature'] - mean_temp) / std_temp
    outliers = np.abs(z_scores) > 3
    
    if outliers.any():
        print(f"   -> Detected {outliers.sum()} statistical outliers in Temperature.")
        df.loc[outliers, 'qc_flag_temp'] = 2  # Flag 2 = Statistical Outlier
        df.loc[outliers, 'temperature'] = np.nan
        
    return df

# ==========================================
# [Step 3] Missing Data Interpolation
# Module 3 Lec 12: Spatio-temporal Interpolation
# ==========================================
def fill_missing_values(df):
    print("3️⃣  Filling Missing Values (Interpolation)...")
    
    # Temperature: Linear Interpolation (선형 보간 - 기온은 연속적이므로 적합)
    df['temp_filled'] = df['temperature'].interpolate(method='linear')
    
    # Precipitation: Fill with 0 or Nearest (강수량은 선형보간이 위험할 수 있음, 여기선 단순화하여 ffill 사용)
    # 현업에서는 주변 관측소 데이터를 사용하지만, 단일 관측소 예제이므로 Forward Fill 사용
    df['precip_filled'] = df['precipitation'].fillna(method='ffill').fillna(0)
    
    print("   -> Missing values filled.")
    return df

# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    if not os.path.exists(RAW_FILE):
        generate_dirty_data()
        
    df_raw = pd.read_csv(RAW_FILE)
    print("📊 Raw Data Preview:")
    print(df_raw.head(10))
    print("\n" + "="*30 + "\n")
    
    # Run QC Pipeline
    df_qc = apply_physical_qc(df_raw)
    df_qc = apply_statistical_qc(df_qc)
    df_clean = fill_missing_values(df_qc)
    
    # Save Results
    df_clean.to_csv(CLEAN_FILE, index=False)
    
    print("\n✅ QC Process Complete!")
    print(f"💾 Clean data saved to: {CLEAN_FILE}")
    print("\n📊 Final Data Preview (Comparison):")
    print(df_clean[['date', 'temperature', 'temp_filled', 'qc_flag_temp']].head(15))
