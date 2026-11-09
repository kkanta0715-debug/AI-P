
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ページ設定
st.set_page_config(
    page_title="World MBTI Statistics",
    page_icon="📊",
    layout="wide"
)

st.title("World MBTI Statistics")
st.write("国を選択すると、その国の16種類のMBTI割合を表示します。")

# CSVファイルの読み込み
# pagesフォルダの1つ上の階層を指定
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "countriesMBTI_16types.csv"

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()

    if "Country" not in data.columns:
        raise ValueError("CSVにCountry列がありません。")

    mbti_columns = [
        col for col in data.columns if col != "Country"
    ]

    for col in mbti_columns:
        data[col] = pd.to_numeric(
            data[col], errors="coerce"
        )

    data = data.dropna(subset=["Country"])

    return data, mbti_columns

try:
    df, mbti_columns = load_data(DATA_FILE)

except FileNotFoundError:
    st.error("CSVファイルが見つかりません。")
    st.stop()

except Exception as error:
    st.error(f"データ読み込みエラー: {error}")
    st.stop()

# 国の選択
countries = sorted(
    df["Country"].astype(str).unique().tolist()
)

if not countries:
    st.error("国のデータがありません。")
    st.stop()

default_country = (
    "South Korea"
    if "South Korea" in countries
    else countries[0]
)

selected_country = st.selectbox(
    "国を選択してください",
    countries,
    index=countries.index(default_country)
)

country_row = df[
    df["Country"].astype(str) == selected_country
].iloc[0]

# MBTIデータを取得して降順に並べ替え
chart_data = pd.DataFrame({
    "MBTI": mbti_columns,
    "Percentage": [
        float(country_row[col]) * 100
        for col in mbti_columns
    ]
})

chart_data = chart_data.dropna(
    subset=["Percentage"]
)

chart_data = chart_data.sort_values(
    "Percentage",
    ascending=False
).reset_index(drop=True)

# 色の変換関数
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(
        int(hex_color[i:i+2], 16)
        for i in (0, 2, 4)
    )

def blend_color(start_hex, end_hex, ratio):
    start = hex_to_rgb(start_hex)
    end = hex_to_rgb(end_hex)

    blended = tuple(
        round(
            start[i] +
            (end[i] - start[i]) * ratio
        )
        for i in range(3)
    )

    return "#{:02X}{:02X}{:02X}".format(*blended)

# グラデーションカラー
# 1位は赤、2位以下は青から薄い青
bar_colors = ["#E53935"]

remaining_count = len(chart_data) - 1

for rank in range(remaining_count):
    ratio = rank / max(remaining_count - 1, 1)

    color = blend_color(
        "#2457A6",
        "#DCEBFA",
        ratio
    )

    bar_colors.append(color)

# 棒グラフの作成
fig = go.Figure(
    go.Bar(
        x=chart_data["Percentage"],
        y=chart_data["MBTI"],
        orientation="h",
        marker=dict(
            color=bar_colors,
            line=dict(width=0)
        ),
        text=[
            f"{value:.2f}%"
            for value in chart_data["Percentage"]
        ],
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "割合: %{x:.2f}%"
            "<extra></extra>"
        )
    )
)

fig.update_layout(
    title=f"{selected_country} - MBTI Distribution",
    xaxis_title="割合 (%)",
    yaxis_title="MBTIタイプ",
    yaxis=dict(autorange="reversed"),
    xaxis=dict(rangemode="tozero"),
    template="plotly_white",
    height=650,
    showlegend=False
)

# 統計情報
top_type = chart_data.iloc[0]
total_value = chart_data["Percentage"].sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "最も割合が高いMBTI",
    top_type["MBTI"]
)

col2.metric(
    "最高割合",
    f'{top_type["Percentage"]:.2f}%'
)

col3.metric(
    "16タイプの合計",
    f"{total_value:.2f}%"
)

# グラフ表示
st.plotly_chart(
    fig,
    use_container_width=True
)

# データ一覧
with st.expander("MBTI割合の一覧を見る"):

    display_data = chart_data.copy()

    display_data["Percentage"] = (
        display_data["Percentage"]
        .map(lambda x: f"{x:.2f}%")
    )

    display_data.insert(
        0,
        "順位",
        range(1, len(display_data) + 1)
    )

    st.dataframe(
        display_data,
        hide_index=True,
        use_container_width=True
    )

st.caption(
    "注：元データの数値をそのまま百分率に換算しています。"
    "合計が必ずしも100%にならない場合があります。"
)
