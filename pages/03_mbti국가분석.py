import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# 페이지 기본 설정
st.set_page_config(
    page_title="국가별 MBTI 비율 분석 대시보드",
    page_icon="🌍",
    layout="centered"
)

# 1. 데이터 로드 (스트림릿 클라우드 최적화 캐싱)
@st.cache_data
def load_data():
    # 깃허브에 업로드할 때 파일명을 'countries_mbti.csv'로 변경하시는 것을 권장합니다.
    # 기존 파일명 그대로 쓰신다면 'countriesMBTI_16types (1).csv'로 수정해주세요.
    file_path = "countries_mbti.csv"
    df = pd.read_csv(file_path)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일을 불러오지 못했습니다. 파일 이름을 확인해주세요. (에러: {e})")
    st.stop()

# 타이틀 및 설명
st.title("🌍 국가별 MBTI 비율 비교 대시보드")
st.markdown("원하는 국가를 선택하여 16가지 MBTI 유형별 분포와 순위를 확인해보세요!")

# 2. 국가 선택 드롭다운
countries = sorted(df['Country'].unique())
selected_country = st.sidebar.selectbox("국가를 선택하세요:", countries)

# 선택한 국가의 데이터 가공 (비율 높은 순으로 정렬)
country_row = df[df['Country'] == selected_country].melt(
    id_vars=['Country'], 
    var_name='MBTI', 
    value_name='Ratio'
).sort_values(by='Ratio', ascending=False).reset_index(drop=True)

# 백분율(%) 형태로 변환
country_row['Percentage'] = country_row['Ratio'] * 100

st.subheader(f"📌 [{selected_country}]의 MBTI 분포")

# 3. 색상 설정 조건 (1등: 빨간색, 나머지: 파란색 계열 그라데이션)
# 정렬된 상태이므로 index 0이 1등입니다.
colors = []
num_bars = len(country_row)

# 파란색 계열의 흐려지는 그라데이션 색상 생성 (2등부터 끝등까지)
# matplotlib의 'Blues' colormap 활용 (너무 연해지지 않도록 범위 조절)
cmap = plt.cm.Blues
# 2등~마지막 항목 개수만큼 파란색 컬러 추출 (진한 파랑 -> 연한 파랑)
blue_shades = [mcolors.to_hex(cmap(val)) for val in [i / (num_bars + 2) for i in range(num_bars + 2, 2, -1)]]

for i in range(num_bars):
    if i == 0:
        colors.append('#FF4B4B')  # 1등: 강렬한 빨간색
    else:
        colors.append(blue_shades[i - 1])  # 나머지: 순위가 낮아질수록 연해지는 파란색 그라데이션

# 막대그래프 시각화
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(country_row['MBTI'], country_row['Percentage'], color=colors)

# 그래프 디자인 꾸미기
ax.set_title(f"{selected_country} - MBTI Distribution (1st Highlighted)", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("MBTI Type", fontsize=12)
ax.set_ylabel("Ratio (%)", fontsize=12)
plt.xticks(rotation=45, ha='right')

# 막대 위에 정확한 퍼센트 값 표시
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3포인트 위로 오프셋
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

st.pyplot(fig)

# 하단 상세 데이터 표 제공
with st.expander("📊 상세 데이터 표 보기"):
    display_df = country_row[['MBTI', 'Percentage']].copy()
    display_df['Percentage'] = display_df['Percentage'].round(2).astype(str) + '%'
    display_df.columns = ['MBTI 유형', '비율']
    st.dataframe(display_df, use_container_width=True)
