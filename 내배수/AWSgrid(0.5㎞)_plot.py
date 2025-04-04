#0. 데이터 구조 확인
aws_grid=pd.read_csv('D:/이현지/2. 진종훈 팀장님/#2. 내배수/241008 피해지점 및 인근 관측소 매칭/241010 사례집 다운로드/1hrAwsGrid_201907151515.txt', header=None, skiprows=1)
aws_grid
aws_grid.iloc[:, 1361].unique()
aws_rain=aws_grid.iloc[:,:-1]
aws_rain


#1. DataFrame을 NumPy 배열로 변환
rain_array = aws_rain.values  # 또는 rain_array = aws_rain.to_numpy()
# 결과 확인
print(rain_array)
print(lat.shape)
print(lon.shape)


#2. pyproj 라이브러리 사용하여 위경도 변환(0.5㎞ 기준)
cell_size=500
center_lat=38
center_lon=126
center_grid=(1162, 310)
# 프로젝션 정의
projection = pyproj.Proj(proj='lcc', lat_1=30, lat_2=60, lat_0=center_lat, lon_0=center_lon, datum='WGS84')
# 격자 위치 계산
j_indices, i_indices = np.meshgrid(np.arange(1361), np.arange(1361))
x = (j_indices - center_grid[1]) * cell_size
y = (i_indices - center_grid[0]) * cell_size
# 프로젝션 변환 (벡터화된 함수 사용)
lon, lat = projection(x, y, inverse=True)
# 결과 확인
print("위도 배열:\n", lat)
print("경도 배열:\n", lon)


#3. 객관분석 표출
fig = plt.figure(figsize=(10, 7.8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
# coastline 추가
ax.coastlines()
# 한반도 범위 설정 - 경계: W 124.19583333, E 131.87222222, S 33.11111111, N 43.00972222
ax.set_extent([124.5, 129.8, 33., 39.], crs=ccrs.PlateCarree())
# 위경도 그리기
gl=ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, color='gray', alpha=0.5)
gl.top_labels = False  # 위쪽 레이블 숨기기
gl.right_labels = False  # 오른쪽 레이블 숨기기
# 레이더 데이터 시각화 (contourf 사용)
contour = ax.contourf(lon, lat,
                       rain_array, cmap=colormap_rain, levels=bounds, extend='both',
                       transform=ccrs.PlateCarree(), norm=norm)
# 중심 좌표
center_lon = loc_df.iloc[0]['lon']
center_lat = loc_df.iloc[0]['lat']
ax.scatter(center_lon, center_lat, color='black', marker='x', s=800, label='피해 지역', linewidths=10, zorder=5, edgecolors=1)
# 범례 추가
ax.legend(facecolor='white', edgecolor='black', fontsize='large', framealpha=1, markerscale=0.07, scatterpoints=1)
# 색상 막대 추가
cbar = plt.colorbar(contour, ax=ax, ticks=ticks, orientation='vertical', pad=0.02, extend='both', extendrect=True)
# 플롯 보여주기
plt.show()


#4. 피해지점 ZOOM
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
fig = plt.figure(figsize=(10, 6.5))
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
                       rain_array, cmap=colormap_rain, levels=bounds, extend='both',
                       transform=ccrs.PlateCarree(), norm=norm)
ax.scatter(center_lon, center_lat, color='black', marker='x', s=800, label='피해 지역', linewidths=8)
ax.legend(facecolor='white', edgecolor='black', fontsize='large', framealpha=1, markerscale=0.07, scatterpoints=1)
# 색상 막대 추가
cbar = plt.colorbar(contour, ax=ax, ticks=ticks, orientation='vertical', pad=0.02, extend='both', extendrect=True)
# 플롯 보여주기
plt.show()
