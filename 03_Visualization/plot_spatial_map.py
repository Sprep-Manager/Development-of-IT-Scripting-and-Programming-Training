import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import warnings

# 경고 메시지 숨기기 (깔끔한 출력을 위해)
warnings.filterwarnings("ignore")

# ==========================================
# [Step 0] Mock Data Generation
# (실습용: 태평양 지역의 가상 기온 및 바람 데이터 생성)
# ==========================================
def generate_spatial_data():
    print("🎨 Generating mock spatial data for the Pacific region...")
    
    # 태평양 지역 위경도 범위 (Pacific Region focus)
    lons = np.linspace(160, 200, 100) # 160E ~ 160W
    lats = np.linspace(-30, 10, 80)   # 30S ~ 10N
    lon2d, lat2d = np.meshgrid(lons, lats)
    
    # 1. Temperature (가상의 기온 패턴)
    # 적도 부근이 따뜻하고 남쪽으로 갈수록 추워지도록 생성
    temp = 28 - 0.5 * (np.abs(lat2d)) + np.sin(lon2d/10)
    
    # 2. Wind Vectors (U, V components)
    # 무역풍(Trade winds) 흉내: 동풍 계열
    u_wind = -5 + np.cos(lat2d/5) * 2
    v_wind = np.sin(lon2d/10) * 2
    
    return lons, lats, temp, u_wind, v_wind

# ==========================================
# [Step 1] Visualization Routine (Cartopy)
# Module 4 Lec 18: Geographic Mapping with Cartopy
# Module 4 Lec 19: Advanced Contour & Vector Plotting
# ==========================================
def plot_climate_map():
    # 데이터 생성
    lons, lats, temp, u, v = generate_spatial_data()
    
    # 1. 캔버스 설정 (Projection: PlateCarree - 일반적인 위경도 도법)
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    
    print("🗺️  Drawing base map features...")
    # 2. 지도 배경 추가 (해안선, 국가 경계, 바다 색상)
    ax.add_feature(cfeature.COASTLINE, linewidth=1.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, color='lightgray')
    ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
    
    # 그리드(Gridlines) 추가
    gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False
    
    # 3. 데이터 시각화 - 기온 (Contour Fill)
    print("🌡️  Plotting Temperature Contours...")
    # levels: 등고선 단계 설정
    levels = np.arange(15, 32, 1) 
    contour = ax.contourf(lons, lats, temp, levels=levels, 
                          cmap='RdYlBu_r', # Red-Yellow-Blue (Reverse)
                          transform=ccrs.PlateCarree(),
                          extend='both')
    
    # 컬러바(Colorbar) 추가
    cbar = plt.colorbar(contour, ax=ax, orientation='vertical', pad=0.02, shrink=0.8)
    cbar.set_label('Surface Temperature (°C)', fontsize=12)
    
    # 4. 데이터 시각화 - 바람 벡터 (Quiver)
    print("💨  Plotting Wind Vectors...")
    # 가독성을 위해 데이터 간격을 띄워서 표시 (skip)
    skip = 5
    ax.quiver(lons[::skip], lats[::skip], u[::skip, ::skip], v[::skip, ::skip],
              transform=ccrs.PlateCarree(),
              color='black', alpha=0.7, scale=200)

    # 5. 제목 및 저장
    plt.title('Pacific Region Climate Analysis\nTemperature & Wind Vectors (Simulated)', fontsize=15, pad=15)
    
    output_file = "pacific_climate_map.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✅ Visualization saved to: {output_file}")
    
    # (Optional) 화면에 띄우기
    # plt.show()

if __name__ == "__main__":
    plot_climate_map()
