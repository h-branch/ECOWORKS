import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm, Normalize
import pandas as pd
import cartopy.crs as ccrs
import pyproj


#0. 피해지점
location=pd.read_csv('D:/이현지/2. 진종훈 팀장님/#2. 내배수/241008 피해지점 및 인근 관측소 매칭/location.csv', encoding='euc-kr')
loc_df=pd.DataFrame(location)
loc_df.drop(columns=loc_df.columns[7:11], inplace=True)
loc_df.rename(columns={'Unnamed: 5':'lat', 'Unnamed: 6':'lon'}, inplace=True)
loc_df


#1-1. HSR 데이터 전처리
f_path='D:/이현지/2. 진종훈 팀장님/#2. 내배수/241008 피해지점 및 인근 관측소 매칭/241010 사례집 다운로드/1hrPCPH_2019071515.bin'
nx, ny = 2305, 2881
with open(f_path, 'rb') as f:
    file=f.read()
rdr=np.frombuffer(file, dtype=np.int16, offset=4).astype(np.float32).reshape(ny, nx)
null=(rdr<=-20000)
rdr[null]=np.nan
rdr /= 100
rdr.shape


#1-2. AI-HQPE 데이터 전처리
f_path='D:/이현지/2. 진종훈 팀장님/#2. 내배수/241115 IRPS 결과/Downloads/rain_fcst_202309201600_acc_1h.bin' #ai-hqpe
nx, ny = 2305, 2881
with open(f_path, 'rb') as f:
    file=f.read()
rdr=np.frombuffer(file, dtype=np.int16).astype(np.float32).reshape(ny, nx)
rdr /= 100
rain_rate=np.where(rdr>0.21, rdr, -9999.) #1hr=0.03, 3hr=0.10, 6hr=0.21
rain_rate.shape


#2. 반사도-강우강도 변환(HSR)
ZRa = 200.
ZRb = 1.6
def dbz_to_rain(dbz):
    # za와 zb 계산
    za = 0.1 / ZRb
    zb = np.log10(ZRa) / ZRb
    # 강수량 계산
    rain = dbz * za - zb
    rain = 10.0 ** rain
    return rain
dbz_val=rdr
rain_val=dbz_to_rain(dbz_val)
rain_val.shape


#3. pyproj 라이브러리 사용하여 위경도 변환
cell_size=500
center_lat=38
center_lon=126
center_grid=(1681, 1121)
# 프로젝션 정의
projection = pyproj.Proj(proj='lcc', lat_1=30, lat_2=60, lat_0=center_lat, lon_0=center_lon, datum='WGS84')
# 격자 위치 계산
j_indices, i_indices = np.meshgrid(np.arange(nx), np.arange(ny))
x = (j_indices - center_grid[1]) * cell_size
y = (i_indices - center_grid[0]) * cell_size
# 프로젝션 변환 (벡터화된 함수 사용)
lon, lat = projection(x, y, inverse=True)
# 결과 확인
print(lon.shape)
print(lat.shape)


#4. 컬러바 생성 및 처리
kma_color=['#00c8ff', '#009bf5', '#0049f5', #청색
           '#00ff00', '#00be00', '#008c00', '#005a00', #녹색
           '#ffff00', '#ffdd1f', '#f9cb00', '#e0b900', '#ccaa00', #황색
           '#ff6600', '#ff3300', '#d20000', '#b40000', #적색
           '#dfa9ff', '#c969ff', '#b429ff', '#9300e4', #자색
           '#b3b4de', '#4c4eb1', '#000390' #남색
]
colormap_rain=ListedColormap(kma_color).with_extremes(over='#333333', under='#ffffff')
colormap_rain.set_bad([0,0,0,0])
bounds=np.array([
    0., 0.1, 0.5, 1.,
    2., 3., 4., 5., 
    6., 7., 8., 9., 10., 
    15., 20., 25., 30., 
    40., 50., 60., 70., 
    90., 110., 150.
])
norm=BoundaryNorm(boundaries=bounds, ncolors=len(colormap_rain.colors))
colormap_rain
ticks=bounds[:]


#5. HSR 강우강도 표출
fig = plt.figure(figsize=(10, 7.8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
# coastline 추가
ax.coastlines()
# 한반도 범위 설정
ax.set_extent([124.5, 129.8, 33., 39.], crs=ccrs.PlateCarree())
# 위경도 그리기
gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, color='gray', alpha=0.5)
gl.top_labels = False
gl.right_labels = False
# 레이더 데이터 시각화
contour = ax.contourf(lon, lat,
                      rain_val, #HSR
                      #rain_rate, #AI-HQRE
                       cmap=colormap_rain, levels=bounds, extend='both',
                       transform=ccrs.PlateCarree(), norm=norm)
# 중심 좌표 표시
center_lon = loc_df.iloc[0]['lon']
center_lat = loc_df.iloc[0]['lat']
ax.scatter(center_lat, center_lon, color='black', marker='x', s=800, label='피해 지역', linewidths=10, zorder=5, edgecolors=1)
# 범례 추가
ax.legend(facecolor='white', edgecolor='black', fontsize='large', framealpha=1, markerscale=0.07, scatterpoints=1)
# 색상 막대 추가
cbar = plt.colorbar(contour, ax=ax, ticks=ticks, orientation='vertical', pad=0.02, extend='both', extendrect=True)
# 플롯 보여주기
plt.show()


#6. 피해지점 ZOOM
# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')  # Windows에서는 Malgun Gothic 사용
# 또는 다른 폰트를 사용할 수 있습니다. (예: 'AppleGothic' for Mac)
# 중심 좌표
center_lon = loc_df.iloc[0]['lon']
center_lat = loc_df.iloc[0]['lat']
# 주변 범위 (100 km)
radius = 100 * 1000  # km를 m로 변환
# 지구의 반지름 (m)
earth_radius = 6371000
# 경도, 위도 범위 계산
delta_lon = np.degrees(radius / (earth_radius * np.cos(np.radians(center_lat))))
delta_lat = np.degrees(radius / earth_radius)
lon_min = center_lon - delta_lon
lon_max = center_lon + delta_lon
lat_min = center_lat - delta_lat
lat_max = center_lat + delta_lat
# 새로운 맵 생성
fig = plt.figure(figsize=(10, 6.5), dpi=100)
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
# coastline 추가
ax.coastlines(resolution='10m')
# 축 범위 설정
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
# 위경도 그리기
gl=ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, color='gray', alpha=0.5)
gl.top_labels = False  # 위쪽 레이블 숨기기
gl.right_labels = False  # 오른쪽 레이블 숨기기
# 레이더 데이터 시각화 (contourf 사용)
contour = ax.contourf(lon, lat,
                      rain_val, #HSR
                      #rain_rate, #AI-HQRE
                       cmap=colormap_rain, levels=bounds, extend='both',
                       transform=ccrs.PlateCarree(), norm=norm)
ax.scatter(center_lon, center_lat, color='black', marker='x', s=800, label='피해 지역', linewidths=8)
ax.legend(facecolor='white', edgecolor='black', fontsize='large', framealpha=1, markerscale=0.07, scatterpoints=1)
# 색상 막대 추가
cbar = plt.colorbar(contour, ax=ax, ticks=ticks, orientation='vertical', pad=0.02, extend='both', extendrect=True)
# 플롯 보여주기
plt.show()
