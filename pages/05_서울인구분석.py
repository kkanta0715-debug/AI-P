
import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =====================================
# 1. 기본 설정
# =====================================

st.set_page_config(
    page_title="서울시 연령별 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("서울시 연령별 인구 분석")

st.write(
    "행정구역, 연도, 성별을 선택하면 "
    "연령대별 인구수를 꺾은선 그래프로 확인할 수 있습니다."
)


# =====================================
# 2. CSV 파일 경로
# =====================================

# 현재 파일은 pages 폴더에 있음
# CSV는 pages의 상위 폴더에 있음

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "population.csv"


# =====================================
# 3. CSV 파일 읽기
# =====================================

@st.cache_data
def load_data(path):

    try:
        df = pd.read_csv(
            path,
            encoding="utf-8-sig"
        )

    except UnicodeDecodeError:
        df = pd.read_csv(
            path,
            encoding="cp949"
        )

    # 열 이름 정리
    df.columns = df.columns.astype(str).str.strip()

    # 행정구역명 정리
    df["행정구역"] = df["행정구역"].astype(str).str.strip()

    df["행정구역명"] = (
        df["행정구역"]
        .str.replace(r"\s*\(\d+\)\s*$", "", regex=True)
        .str.strip()
    )

    # 숫자 데이터 변환
    for col in df.columns:

        if col not in ["행정구역", "행정구역명"]:

            df[col] = pd.to_numeric(
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False),
                errors="coerce"
            )

    return df


# =====================================
# 4. 데이터 불러오기
# =====================================

if not CSV_PATH.exists():

    st.error(
        "population.csv 파일을 찾을 수 없습니다. "
        "프로젝트 최상위 폴더에 CSV 파일을 넣어주세요."
    )

    st.stop()


try:

    df = load_data(str(CSV_PATH))

except Exception as e:

    st.error(f"데이터 읽기 오류: {e}")

    st.stop()


# =====================================
# 5. 연도 추출
# =====================================

years = sorted({

    int(match.group(1))

    for col in df.columns

    if (match := re.match(r"^(\d{4})년_", col))

})


# =====================================
# 6. 연령대 추출
# =====================================

age_pattern = re.compile(
    r"(\d{1,3}~\d{1,3}세|100세 이상)$"
)

age_groups = []

for col in df.columns:

    match = age_pattern.search(col)

    if match:

        age = match.group(1)

        if age not in age_groups:

            age_groups.append(age)


def age_sort_key(age):

    if age == "100세 이상":

        return 100

    return int(age.split("~")[0])


age_groups.sort(key=age_sort_key)


# =====================================
# 7. 행정구역 추출
# =====================================

districts = (
    df["행정구역명"]
    .dropna()
    .unique()
    .tolist()
)

districts.sort(
    key=lambda x: (x != "서울특별시", x)
)


# =====================================
# 8. 선택 메뉴
# =====================================

st.subheader("분석 조건 선택")

col1, col2, col3 = st.columns(3)


with col1:

    selected_district = st.selectbox(
        "행정구역",
        districts
    )


with col2:

    selected_year = st.selectbox(
        "연도",
        years,
        index=len(years) - 1
    )


with col3:

    selected_gender = st.selectbox(
        "성별",
        ["전체", "남성", "여성"]
    )


# =====================================
# 9. 성별에 따른 컬럼 선택
# =====================================

prefix_map = {

    "전체": f"{selected_year}년_거주자_",

    "남성": f"{selected_year}년_남_거주자_",

    "여성": f"{selected_year}년_여_거주자_"

}

column_prefix = prefix_map[selected_gender]


# =====================================
# 10. 선택한 행정구역 데이터
# =====================================

selected_data = df[
    df["행정구역명"] == selected_district
]


if selected_data.empty:

    st.warning("선택한 행정구역 데이터가 없습니다.")

    st.stop()


selected_row = selected_data.iloc[0]


# =====================================
# 11. 연령별 인구 데이터 생성
# =====================================

chart_data = []

for age in age_groups:

    column_name = column_prefix + age

    if column_name in df.columns:

        value = selected_row[column_name]

        if pd.notna(value):

            chart_data.append({

                "나이": age,

                "인구수": int(value)

            })


chart_df = pd.DataFrame(chart_data)


if chart_df.empty:

    st.warning(
        "선택한 조건에 해당하는 데이터가 없습니다."
    )

    st.stop()


# =====================================
# 12. 주요 지표
# =====================================

total_population = chart_df["인구수"].sum()

max_age = chart_df.loc[
    chart_df["인구수"].idxmax(),
    "나이"
]


metric1, metric2 = st.columns(2)


metric1.metric(
    "연령대별 인구 합계",
    f"{total_population:,}명"
)


metric2.metric(
    "인구가 가장 많은 연령대",
    max_age
)


# =====================================
# 13. 꺾은선 그래프
# =====================================

fig = go.Figure()


fig.add_trace(

    go.Scatter(

        x=chart_df["나이"],

        y=chart_df["인구수"],

        mode="lines+markers",

        name="인구수",

        # 초록색 선
        line=dict(
            color="#168A45",
            width=3
        ),

        # 초록색 점
        marker=dict(
            color="#168A45",
            size=9
        ),

        hovertemplate=
        "나이: %{x}<br>"
        "인구수: %{y:,.0f}명"
        "<extra></extra>"

    )

)


# =====================================
# 14. 그래프 디자인
# =====================================

fig.update_layout(

    title=f"{selected_district} "
          f"{selected_year}년 "
          f"{selected_gender} 인구",

    xaxis_title="나이",

    yaxis_title="인구수(명)",

    font=dict(
        family="sans-serif",
        size=14
    ),

    hovermode="x unified",

    showlegend=False,

    margin=dict(
        l=25,
        r=25,
        t=70,
        b=25
    )

)


# =====================================
# 15. 세로축 1,000명 단위 설정
# =====================================

fig.update_yaxes(

    rangemode="tozero",

    tickmode="linear",

    tick0=0,

    dtick=1000,

    tickformat=",",

    showgrid=True,

    gridcolor="#D9E2DC",

    gridwidth=1,

    zeroline=True

)


# 가로축 설정
fig.update_xaxes(

    showgrid=False,

    categoryorder="array",

    categoryarray=age_groups

)


# =====================================
# 16. 그래프 출력
# =====================================

st.subheader("연령대별 인구 꺾은선 그래프")

st.plotly_chart(
    fig,
    use_container_width=True
)


# =====================================
# 17. 데이터 표 출력
# =====================================

with st.expander("상세 인구 데이터 확인"):

    display_df = chart_df.copy()

    display_df["인구수"] = (
        display_df["인구수"]
        .map(lambda x: f"{x:,}")
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# =====================================
# 18. 안내
# =====================================

st.caption(
    "자료의 연령 구간은 0~9세, 10~19세 등 "
    "10세 단위입니다. "
    "세로축 구분선은 1,000명 간격입니다."
)
