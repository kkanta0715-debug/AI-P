    "国を選択してください",
    countries,
    index=default_index
)

country_row = df.loc[df["Country"].astype(str) == selected_country].iloc[0]

# Convert proportions (e.g. 0.1339) into percentages (13.39%).
chart_data = pd.DataFrame({
    "MBTI": mbti_columns,
    "Percentage": [float(country_row[col]) * 100 for col in mbti_columns]
})

chart_data = chart_data.sort_values(
    "Percentage",
    ascending=False
).reset_index(drop=True)

# --------------------------------------------------
# Create bar colors:
# 1st place = red
# Remaining places = blue shades that gradually fade.
# --------------------------------------------------
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def blend_color(start_hex, end_hex, ratio):
    start = hex_to_rgb(start_hex)
    end = hex_to_rgb(end_hex)
    blended = tuple(
        round(start[i] + (end[i] - start[i]) * ratio)
        for i in range(3)
    )
    return rgb_to_hex(blended)

bar_colors = ["#E53935"]  # Highest percentage: red

remaining_count = max(len(chart_data) - 1, 1)
for rank in range(remaining_count):
    # Dark blue near the top, gradually fading to pale blue.
    ratio = rank / max(remaining_count - 1, 1)
    bar_colors.append(
        blend_color("#2457A6", "#DCEBFA", ratio)
    )

# Horizontal chart: reverse the order so the highest value appears at the top.
fig = go.Figure(
    go.Bar(
        x=chart_data["Percentage"],
        y=chart_data["MBTI"],
        orientation="h",
        marker=dict(
            color=bar_colors[:len(chart_data)],
            line=dict(color="rgba(0,0,0,0)", width=0)
        ),
        text=[f"{value:.2f}%" for value in chart_data["Percentage"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>割合: %{x:.2f}%<extra></extra>"
    )
)

fig.update_layout(
    title=dict(
        text=f"{selected_country} — MBTI Distribution",
        x=0.02,
        xanchor="left"
    ),
    xaxis=dict(
        title="割合 (%)",
        rangemode="tozero",
        showgrid=True,
        gridcolor="rgba(128,128,128,0.18)"
    ),
    yaxis=dict(
        title="MBTIタイプ",
        autorange="reversed"
    ),
    template="plotly_white",
    height=650,
    margin=dict(l=35, r=75, t=75, b=55),
    showlegend=False
)

# --------------------------------------------------
# Summary metrics
# --------------------------------------------------
top_type = chart_data.iloc[0]
average_value = chart_data["Percentage"].mean()
total_value = chart_data["Percentage"].sum()

metric1, metric2, metric3 = st.columns(3)
metric1.metric("最も割合が高いMBTI", top_type["MBTI"])
metric2.metric("最高割合", f'{top_type["Percentage"]:.2f}%')
metric3.metric("16タイプの合計", f"{total_value:.2f}%")

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Data table
# --------------------------------------------------
with st.expander("割合の一覧を見る"):
    display_data = chart_data.copy()
    display_data["Percentage"] = display_data["Percentage"].map(
        lambda value: f"{value:.2f}%"
    )
    display_data.insert(0, "順位", range(1, len(display_data) + 1))
    st.dataframe(display_data, hide_index=True, use_container_width=True)

st.caption(
    "注：元データの数値をそのまま百分率に換算して表示しています。"
    "合計が必ずしも100%にならない場合があります。"
)
