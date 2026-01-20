import sqlite3
import pandas as pd
import numpy as np
import os

# ==========================================
# [Configuration] 설정
# ==========================================
DB_NAME = "mock_clide.db"  # 가상의 CliDE 데이터베이스 파일
OUTPUT_FILE = "extracted_station_data.csv"

# ==========================================
# [Step 0] Mock DB Generation (Simulating CliDE Environment)
# 실제 CliDE는 PostgreSQL/MySQL을 쓰지만, 교육용으로 SQLite를 사용하여 환경을 모사합니다.
# ==========================================
def create_mock_clide_db():
    print("🏗️  Building Mock CliDE Database...")
    
    # 1. Connect to SQLite (creates file if not exists)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 2. Create Tables (Simulating CliDE Schema)
    # t_stations: 관측소 메타정보 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS t_stations (
            station_id TEXT PRIMARY KEY,
            station_name TEXT,
            latitude REAL,
            longitude REAL,
            country TEXT
        )
    ''')
    
    # t_obs_daily: 일별 기상 관측 데이터 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS t_obs_daily (
            obs_id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id TEXT,
            obs_date TEXT,
            element_name TEXT,
            obs_value REAL,
            FOREIGN KEY(station_id) REFERENCES t_stations(station_id)
        )
    ''')
    
    # 3. Insert Sample Data
    # 관측소 정보 입력
    stations = [
        ('WS_APIA', 'Apia Observatory', -13.8, 171.7, 'Samoa'),
        ('FJ_NADI', 'Nadi Airport', -17.7, 177.4, 'Fiji')
    ]
    cursor.executemany('INSERT OR IGNORE INTO t_stations VALUES (?,?,?,?,?)', stations)
    
    # 관측 데이터 입력 (2024년 1월 데이터 생성)
    data_entries = []
    dates = pd.date_range("2024-01-01", "2024-01-10", freq="D").strftime("%Y-%m-%d")
    
    for date in dates:
        # Apia: Tmax, Rain
        data_entries.append(('WS_APIA', date, 'TMAX', 30.0 + np.random.rand()))
        data_entries.append(('WS_APIA', date, 'RAIN', np.random.choice([0, 5, 20, 0, 0])))
        # Nadi: Tmax, Rain
        data_entries.append(('FJ_NADI', date, 'TMAX', 31.0 + np.random.rand()))
        data_entries.append(('FJ_NADI', date, 'RAIN', np.random.choice([0, 0, 10, 30])))
        
    cursor.executemany('''
        INSERT INTO t_obs_daily (station_id, obs_date, element_name, obs_value) 
        VALUES (?, ?, ?, ?)
    ''', data_entries)
    
    conn.commit()
    conn.close()
    print(f"   [OK] Mock DB created: {DB_NAME}")
    print("-" * 50)

# ==========================================
# [Step 1] DB Connection & Querying
# Module 5 Lec 22: Script-based DB Connection & Querying
# ==========================================
def query_climate_db(target_station, start_date, end_date):
    print(f"🔌 Connecting to DB to fetch data for: {target_station}")
    
    conn = sqlite3.connect(DB_NAME)
    
    # SQL Query 작성 (SQL 지식이 필요한 부분)
    # 관측소 이름과 일별 강수량(RAIN)을 조인(Join)하여 추출
    sql_query = f"""
        SELECT 
            s.station_name,
            s.country,
            o.obs_date,
            o.element_name,
            o.obs_value
        FROM t_obs_daily o
        JOIN t_stations s ON o.station_id = s.station_id
        WHERE s.station_id = '{target_station}'
          AND o.element_name = 'RAIN'
          AND o.obs_date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY o.obs_date
    """
    
    print("   -> Executing SQL Query...")
    # pandas의 read_sql 함수를 사용하여 결과를 바로 DataFrame으로 가져옴
    df = pd.read_sql(sql_query, conn)
    
    conn.close()
    return df

# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    # 1. 가상 DB 생성 (없으면 생성)
    if not os.path.exists(DB_NAME):
        create_mock_clide_db()
        
    # 2. 데이터 조회 (Integration 시나리오)
    # 시나리오: "사모아 Apia 관측소의 2024년 1월 강수량 데이터를 DB에서 직접 추출하라"
    station_id = 'WS_APIA'
    df_result = query_climate_db(station_id, "2024-01-01", "2024-01-31")
    
    print("\n📊 Query Result (First 5 rows):")
    print(df_result.head())
    
    # 3. 결과 저장 (Format Conversion)
    # Module 5 Lec 24: Converting for Input (Excel/CSV)
    df_result.to_csv(OUTPUT_FILE, index=False)
    print(f"\n💾 Data extracted and saved to: {OUTPUT_FILE}")
