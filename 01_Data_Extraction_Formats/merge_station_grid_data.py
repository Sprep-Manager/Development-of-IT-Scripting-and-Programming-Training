import xarray as xr
import pandas as pd
import numpy as np
import os

# ==========================================
# [Configuration] 설정
# ==========================================
STATION_FILE = "station_data_sample.csv"
GRID_FILE = "satellite_grid_sample.nc"
OUTPUT_FILE = "merged_climate_data.csv"

# Target Station: Apia, Samoa (Example)
TARGET_LAT = -13.83
TARGET_LON = 171.75

# ==========================================
# [Step 0] Mock Data Generation (For Training)
# 실습을 위한 가상 데이터 생성 함수 (실제 데이터가 없을 때 작동)
# ==========================================
def generate_mock_data():
    print("🔄 Generating mock data for training...")
    
    # 1. Create Station Data (CSV)
    # 2024년 1월 1일부터 10일간의 일별 관측 데이터
    dates = pd.date_range(start="2024-01-01", periods=10, freq="D")
    df_station = pd.DataFrame({
        "date": dates,
        "station_id": "APIA_OBS_01",
        "observed_temp": [28.5, 29.1, 28.8, 27.5, 28.2, 29.5, 30.1, 29.8, 28.9, 29.0]
    })
    df_station.to_csv(STATION_FILE, index=False)
    print(f"   [OK] Created {STATION_FILE}")

    # 2. Create Grid Data (NetCDF)
    # 위도 -15 ~ -12, 경도 170 ~ 173 범위의 4D 데이터 (Time, Lat, Lon)
    lats = np.linspace(-15, -12, 10)
    lons = np.linspace(170, 173, 10)
    
    # 랜덤 온도 데이터 생성 (실제 데이터 흉내)
    temp_data = 28 + np.random.randn(10, 10, 10)  # Time x Lat x Lon
    
    ds = xr.Dataset(
        {"model_temp": (("time", "lat", "lon"), temp_data)},
        coords={
            "time": dates,
            "lat": lats,
            "lon": lons
        }
    )
    # SPREP 교육 커리큘럼에서 강조하는 메타데이터 추가
    ds.attrs["description"] = "Mock Satellite Temperature Data for SPREP Training"
    ds.to_netcdf(GRID_FILE)
    print(f"   [OK] Created {GRID_FILE}")
    print("-" * 50)

# ==========================================
# [Step 1] Data Loading
# ==========================================
def process_data():
    # 데이터가 없으면 생성
    if not os.path.exists(STATION_FILE) or not os.path.exists(GRID_FILE):
        generate_mock_data()

    print("🚀 Starting Data Integration Process...")

    # 1. Load Station Data (Pandas)
    print(f"1️⃣  Loading Station Data: {STATION_FILE}")
    df_station = pd.read_csv(STATION_FILE)
    df_station['date'] = pd.to_datetime(df_station['date']) # 날짜 형식 변환
    
    # 2. Load Grid Data (Xarray)
    # Module 2 Lec 8: Multidimensional I/O with xarray
    print(f"2️⃣  Loading Grid Data: {GRID_FILE}")
    ds_grid = xr.open_dataset(GRID_FILE)

    # ==========================================
    # [Step 2] Spatial Extraction (Nearest Neighbor)
    # 관측소 위치와 가장 가까운 격자점(Grid Point) 데이터 추출
    # ==========================================
    print(f"3️⃣  Extracting Grid Data for Location: Lat {TARGET_LAT}, Lon {TARGET_LON}")
    
    # method='nearest': 가장 가까운 격자점을 자동으로 찾음
    # tolerance=0.5: 0.5도 이상 차이나면 데이터 없음 처리 (Data Quality Control의 일환)
    point_data = ds_grid.sel(lat=TARGET_LAT, lon=TARGET_LON, method='nearest', tolerance=0.5)
    
    # Xarray 데이터를 Pandas DataFrame으로 변환
    df_grid = point_data.to_dataframe().reset_index()
    
    # 필요한 컬럼만 선택 ('time', 'model_temp')
    df_grid = df_grid[['time', 'model_temp']]

    # ==========================================
    # [Step 3] Merging (Integration)
    # ==========================================
    print("4️⃣  Merging Station and Grid Data...")
    
    # 날짜를 기준으로 두 데이터 병합 (Merge)
    # Module 3 Lec 10: Merging Station and Grid Data
    df_merged = pd.merge(
        df_station, 
        df_grid, 
        left_on='date', 
        right_on='time', 
        how='inner' # 두 데이터 모두 존재하는 날짜만 남김
    )

    # 불필요한 중복 컬럼 정리
    df_merged.drop(columns=['time'], inplace=True)

    # Bias 계산 (관측값 - 모델값)
    df_merged['bias'] = df_merged['observed_temp'] - df_merged['model_temp']

    print("\n✅ Integration Complete! Sample Data:")
    print(df_merged.head())

    # ==========================================
    # [Step 4] Save Result
    # ==========================================
    df_merged.to_csv(OUTPUT_FILE, index=False)
    print(f"\n💾 Result saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_data()
