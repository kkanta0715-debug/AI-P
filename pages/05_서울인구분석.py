
import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ==================================================
# 1. 페이지 기본 설정
# ==================================================

st.set_page_config(
    page_title="서울시 자치구 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("서울시 자치구별 인구 분석")

st.write(
    "연도와 자치구를 선택해 남녀 연령별 인구를 비교하고, "
    "연령대를 선택해 자치구별 인구 순위를 확인할 수 있습니다."
)


# ==================================================
# 2. CSV 파일 경로
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "population.csv"


# ==================================================
# 3. CSV 데이터 불러오기
# ==================================================

@st.cache_data
def load_data(path):

    try:
        data = pd.read_csv(
            path,
            encoding="utf-8-sig"
        )

    except UnicodeDecodeError:
        data = pd.read_csv(
            path,
            encoding="cp949"
        )

    data.columns = data.columns.astype(str).str.strip()

    if "행정구역" not in data.columns:
        raise ValueError(
            "CSV 파일에 '행정구역' 열이 없습니다."
        )

    # 행정구역 코드 제거
    data["행정구역명"] = (
        data["행정구역"]
        .astype(str)
        .str.replace(
            r"\s*\(\d+\)\s*$",
            "",
            regex=True
        )
        .str.strip()
    )

    # 서울특별시 종로구 -> 종로구
    data["구"] = (
        data["행정구역명"]
        .str.replace(
            r"^서울특별시\s*",
            "",
            regex=True
        )
        .str.strip()
    )

    # 인구 데이터 숫자형 변환
    for column in data.columns:

        if column not in [
            "행정구역",
            "행정구역명",
            "구"
        ]:

            data[column] = pd.to_numeric(
                data[column]
                .astype(str)
                .str.replace(",", "", regex=False),
                errors="coerce"
            )

    return data


if not CSV_PATH.exists():

    st.error(
        "population.csv 파일을 찾을 수 없습니다. "
        "pages 폴더의 상위 폴더에 CSV 파일을 넣어주세요."
    )

    st.stop()


try:

    df = load_data(str(CSV_PATH))

except Exception as error:

    st.error(
        f"CSV 파일을 불러오는 중 오류가 발생했습니다: {error}"
    )

    st.stop()


# ==================================================
# 4. 연도 추출
# ==================================================

years = sorted({

    int(match.group(1))

    for column in df.columns

    if (
        match := re.match(
            r"^(\d{4})년_",
            column
        )
    )

})


# ==================================================
# 5. 연령대 추출
# ==================================================

age_pattern = re.compile(
    r"(\d{1,3}~\d{1,3}세|100세 이상)$"
)

age_groups = []

for column in df.columns:

    match = age_pattern.search(column)

    if match:

        age = match.group(1)

        if age not in age_groups:

            age_groups.append(age)


def age_sort_key(age):

    if age == "100세 이상":

        return 100

    return int(age.split("~")[0])


age_groups = sorted(
    age_groups,
    key=age_sort_key
)


if not years or not age_groups:

    st.error(
        "CSV에서 연도 또는 연령대 열을 찾을 수 없습니다."
    )

    st.stop()


# ==================================================
# 6. 서울시 전체 제외 및 자치구 목록
# ==================================================

district_df = df[
    df["구"] != "서울특별시"
].copy()

district_df = district_df[
    district_df["구"].str.endswith("구", na=False)
].copy()

districts = sorted(
    district_df["구"].dropna().unique().tolist()
)


if not districts:

    st.error("자치구 데이터를 찾을 수 없습니다.")

    st.stop()


# ==================================================
# 7. 첫 번째 그래프
#    남녀 연령별 인구 비교
# ==================================================

st.header("1. 자치구별 남녀 연령대 인구 비교")

st.caption(
    "서울시 전체는 제외했습니다. "
    "연도와 자치구를 선택하면 남성은 분홍색, "
    "여성은 초록색 선으로 표시됩니다."
)


# 선택 메뉴
control1, control2 = st.columns(2)


with control1:

    selected_year = st.selectbox(
        "연도 선택",
        years,
        index=len(years) - 1,
        key="line_year"
    )


with control2:

    selected_district = st.selectbox(
        "자치구 선택",
        districts,
        key="line_district"
    )


# 선택한 자치구 데이터
selected_rows = district_df[
    district_df["구"] == selected_district
]


if selected_rows.empty:

    st.warning(
        "선택한 자치구 데이터가 없습니다."
    )

    st.stop()


selected_row = selected_rows.iloc[0]


# 남녀 연령별 데이터 생성
male_values = []
female_values = []


for age in age_groups:

    male_column = (
        f"{selected_year}년_남_거주자_{age}"
    )

    female_column = (
        f"{selected_year}년_여_거주자_{age}"
    )

    male_value = (
        selected_row[male_column]
        if male_column in df.columns
        else None
    )

    female_value = (
        selected_row[female_column]
        if female_column in df.columns
        else None
    )

    male_values.append(
        int(male_value)
        if pd.notna(male_value)
        else None
    )

    female_values.append(
        int(female_value)
        if pd.notna(female_value)
        else None
    )


# 꺾은선 그래프 생성
line_fig = go.Figure()


# 남성: 분홍색
line_fig.add_trace(

    go.Scatter(

        x=age_groups,

        y=male_values,

        mode="lines+markers",

        name="남성",

        line=dict(
            color="#E879A9",
            width=3
        ),

        marker=dict(
            color="#E879A9",
            size=8
        ),

        hovertemplate=(
            "연령대: %{x}<br>"
            "남성: %{y:,.0f}명"
            "<extra></extra>"
        )

    )

)


# 여성: 초록색
line_fig.add_trace(

    go.Scatter(

        x=age_groups,

        y=female_values,

        mode="lines+markers",

        name="여성",

        line=dict(
            color="#168A45",
            width=3
        ),

        marker=dict(
            color="#168A45",
            size=8
        ),

        hovertemplate=(
            "연령대: %{x}<br>"
            "여성: %{y:,.0f}명"
            "<extra></extra>"
        )

    )

)


# 그래프 디자인
line_fig.update_layout(

    title=(
        f"{selected_district} · "
        f"{selected_year}년 남녀 연령대별 인구"
    ),

    xaxis_title="나이(연령대)",

    yaxis_title="인구수(명)",

    font=dict(
        family="sans-serif",
        size=14
    ),

    hovermode="x unified",

    legend_title="성별",

    margin=dict(
        l=25,
        r=25,
        t=70,
        b=25
    )

)


# 세로축 1,000명 단위
line_fig.update_yaxes(

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


line_fig.update_xaxes(

    showgrid=False,

    categoryorder="array",

    categoryarray=age_groups

)


# 그래프 출력
st.plotly_chart(
    line_fig,
    use_container_width=True
)


# ==================================================
# 8. 두 번째 그래프
#    연령대별 자치구 인구 순위
# ==================================================

st.divider()

st.header("2. 연령대별 자치구 인구 순위")

st.caption(
    "연도와 10세 단위 연령대를 선택하면 "
    "해당 연령대의 남녀 합계 인구가 많은 "
    "자치구부터 내림차순으로 표시됩니다."
)


# 선택 메뉴
rank_control1, rank_control2 = st.columns(2)


with rank_control1:

    rank_year = st.selectbox(
        "순위 그래프 연도",
        years,
        index=len(years) - 1,
        key="rank_year"
    )


with rank_control2:

    selected_age = st.selectbox(
        "연령대 선택",
        age_groups,
        key="rank_age"
    )


# 전체 성별 합계 인구 열 선택
rank_column = (
    f"{rank_year}년_거주자_{selected_age}"
)


if rank_column not in district_df.columns:

    st.error(
        f"'{rank_column}' 열을 CSV에서 찾을 수 없습니다."
    )

    st.stop()


# 자치구별 인구 데이터
rank_df = district_df[
    ["구", rank_column]
].copy()


rank_df = rank_df.rename(

    columns={
        "구": "자치구",
        rank_column: "인구수"
    }

)


rank_df["인구수"] = pd.to_numeric(
    rank_df["인구수"],
    errors="coerce"
)


rank_df = rank_df.dropna(
    subset=["인구수"]
)


# 인구가 많은 순서대로 정렬
rank_df = rank_df.sort_values(

    by="인구수",

    ascending=False

).reset_index(drop=True)


# 순위 생성
rank_df["순위"] = rank_df.index + 1


# 가로 막대그래프
# 1위가 위쪽에 오도록 역순 정렬
bar_df = rank_df.sort_values(
    by="인구수",
    ascending=True
)


bar_fig = go.Figure()


bar_fig.add_trace(

    go.Bar(

        x=bar_df["인구수"],

        y=bar_df["자치구"],

        orientation="h",

        marker_color="#168A45",

        text=bar_df["인구수"].map(
            lambda value: f"{int(value):,}명"
        ),

        textposition="outside",

        hovertemplate=(
            "자치구: %{y}<br>"
            "인구수: %{x:,.0f}명"
            "<extra></extra>"
        )

    )

)


# 막대그래프 디자인
bar_fig.update_layout(

    title=(
        f"{rank_year}년 {selected_age} "
        "자치구별 인구 순위"
    ),

    xaxis_title="인구수(명)",

    yaxis_title="자치구",

    font=dict(
        family="sans-serif",
        size=13
    ),

    margin=dict(
        l=25,
        r=80,
        t=70,
        b=25
    ),

    height=750

)


bar_fig.update_xaxes(

    tickformat=",",

    showgrid=True,

    gridcolor="#D9E2DC"

)


bar_fig.update_yaxes(
    title="자치구",
    automargin=True
)


# 그래프 출력
st.plotly_chart(
    bar_fig,
    use_container_width=True
)


# ==================================================
# 9. 자치구별 순위 표
# ==================================================

with st.expander("자치구별 인구 순위 데이터 보기"):

    display_rank_df = rank_df[
        ["순위", "자치구", "인구수"]
    ].copy()

    display_rank_df["인구수"] = (
        display_rank_df["인구수"]
        .map(lambda value: f"{int(value):,}명")
    )

    st.dataframe(
        display_rank_df,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# 10. 안내
# ==================================================

st.caption(
    "자료의 연령대는 0~9세, 10~19세 등 10세 단위입니다. "
    "첫 번째 그래프는 남성과 여성을 각각 표시하고, "
    "두 번째 그래프는 남녀 합계 인구를 기준으로 "
    "자치구 순위를 계산합니다."
)
