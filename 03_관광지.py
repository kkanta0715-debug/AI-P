
import streamlit as st
import folium
from streamlit_folium import st_folium

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

st.title("서울 외국인 인기 관광지 TOP 10")
st.markdown("""
서울을 방문하는 외국인 관광객을 위한 주요 관광지 10곳과
1박 2일 추천 여행 코스를 소개합니다.
""")

st.info(
    "관광지 TOP 10은 외국인에게 잘 알려진 대표 관광지를 바탕으로 "
    "구성한 추천 목록입니다. 공식적인 선호도 통계 순위는 아닙니다."
)

# ==========================================
# 2. 관광지 데이터
# ==========================================

places = [
    {
        "rank": 1,
        "name": "경복궁",
        "english": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "description": "조선 왕조의 대표 궁궐입니다. 웅장한 전통 건축과 한국의 역사를 경험할 수 있습니다.",
        "tip": "한복을 입고 궁궐을 관람하는 것도 추천합니다."
    },
    {
        "rank": 2,
        "name": "명동",
        "english": "Myeong-dong",
        "lat": 37.5636,
        "lon": 126.9850,
        "description": "화장품, 패션 매장, 길거리 음식이 모여 있는 서울의 대표 쇼핑 거리입니다.",
        "tip": "저녁 시간에 길거리 음식과 쇼핑을 즐겨보세요."
    },
    {
        "rank": 3,
        "name": "N서울타워",
        "english": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "description": "남산에 위치한 전망 명소로 서울의 아름다운 전경과 야경을 감상할 수 있습니다.",
        "tip": "일몰 시간에 방문하는 것을 추천합니다."
    },
    {
        "rank": 4,
        "name": "북촌한옥마을",
        "english": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "description": "전통 한옥이 이어지는 골목에서 한국의 옛 주거 문화를 느낄 수 있습니다.",
        "tip": "주민이 거주하는 곳이므로 조용히 관람해 주세요."
    },
    {
        "rank": 5,
        "name": "홍대",
        "english": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "description": "거리 공연과 음악, 개성 있는 카페와 상점으로 유명한 젊은 문화 거리입니다.",
        "tip": "저녁에는 거리 공연과 다양한 먹거리를 즐겨보세요."
    },
    {
        "rank": 6,
        "name": "동대문디자인플라자",
        "english": "Dongdaemun Design Plaza",
        "lat": 37.5671,
        "lon": 127.0095,
        "description": "독특한 곡선형 건축물과 전시, 디자인 행사를 즐길 수 있는 복합 문화 공간입니다.",
        "tip": "건축물의 외관과 야간 조명을 감상해 보세요."
    },
    {
        "rank": 7,
        "name": "코엑스·별마당도서관",
        "english": "COEX & Starfield Library",
        "lat": 37.5126,
        "lon": 127.0590,
        "description": "대형 쇼핑몰과 전시장, 높은 서가가 인상적인 별마당도서관이 있는 공간입니다.",
        "tip": "쇼핑과 실내 관광을 함께 즐기기 좋습니다."
    },
    {
        "rank": 8,
        "name": "남대문시장",
        "english": "Namdaemun Market",
        "lat": 37.5592,
        "lon": 126.9770,
        "description": "먹거리와 의류, 생활용품 등을 만날 수 있는 오랜 역사의 전통시장입니다.",
        "tip": "한국의 전통시장 분위기와 다양한 음식을 경험해 보세요."
    },
    {
        "rank": 9,
        "name": "인사동",
        "english": "Insadong",
        "lat": 37.5740,
        "lon": 126.9850,
        "description": "전통 공예품과 갤러리, 찻집, 기념품 가게가 모여 있는 문화 거리입니다.",
        "tip": "전통차를 마시고 한국적인 기념품을 구경해 보세요."
    },
    {
        "rank": 10,
        "name": "성수동",
        "english": "Seongsu-dong",
        "lat": 37.5445,
        "lon": 127.0557,
        "description": "개성 있는 카페와 편집숍, 팝업스토어로 유명한 트렌디한 지역입니다.",
        "tip": "다양한 카페와 팝업스토어를 둘러보세요."
    }
]

# ==========================================
# 3. 서울 지도 생성
# ==========================================

st.header("서울 주요 관광지 지도")

m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap",
    control_scale=True
)

# 관광지 마커 표시

for place in places:

    popup_html = f"""
    <div style="width:240px; font-family:Arial;">
        <h4>{place['rank']}. {place['name']}</h4>
        <p><b>{place['english']}</b></p>
        <p>{place['description']}</p>
        <p><b>방문 팁:</b> {place['tip']}</p>
    </div>
    """

    folium.Marker(
        location=[place["lat"], place["lon"]],
        tooltip=place["name"],
        popup=folium.Popup(
            popup_html,
            max_width=300
        ),
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background-color:#1769aa;
                color:white;
                border:2px solid white;
                border-radius:50%;
                width:30px;
                height:30px;
                line-height:26px;
                text-align:center;
                font-weight:bold;
                box-shadow:0 1px 5px rgba(0,0,0,0.4);
            ">
                {place['rank']}
            </div>
            """,
            icon_size=(30, 30),
            icon_anchor=(15, 15)
        )
    ).add_to(m)

# 지도 출력

st_folium(
    m,
    width=None,
    height=600,
    use_container_width=True,
    returned_objects=[]
)

# ==========================================
# 4. 관광지 설명
# ==========================================

st.header("주요 관광지 소개")

for place in places:

    with st.expander(
        f"{place['rank']}. {place['name']} / {place['english']}"
    ):

        st.write(place["description"])

        st.success(
            "방문 추천 팁: " + place["tip"]
        )

# ==========================================
# 5. 1박 2일 여행 일정
# ==========================================

st.divider()

st.header("서울 1박 2일 추천 여행 일정")

st.markdown("""
서울의 전통문화와 현대적인 도시 분위기를 모두 경험할 수 있도록
대중교통 중심의 여행 코스를 구성했습니다.
""")

# ==========================================
# DAY 1
# ==========================================

st.subheader("DAY 1 - 서울의 전통문화와 야경")

st.image(
    "https://images.unsplash.com/photo-1590301157890-4810ed352733?w=1200",
    caption="경복궁과 서울의 전통문화",
    use_container_width=True
)

day1 = [
    ("09:00 ~ 11:00", "경복궁",
     "조선 왕조의 궁궐을 관람하고 한국의 전통 건축을 감상합니다."),

    ("11:00 ~ 12:00", "북촌한옥마을",
     "전통 한옥이 있는 골목길을 산책합니다."),

    ("12:00 ~ 13:00", "점심 식사",
     "인사동 주변에서 한국 음식을 즐깁니다."),

    ("13:00 ~ 14:30", "인사동",
     "전통 찻집과 공예품점, 기념품 가게를 둘러봅니다."),

    ("14:30 ~ 16:00", "남대문시장",
     "한국의 전통시장과 다양한 길거리 음식을 경험합니다."),

    ("16:00 ~ 18:00", "명동",
     "쇼핑과 화장품 매장, 길거리 음식을 즐깁니다."),

    ("18:00 ~ 20:00", "N서울타워",
     "남산에서 서울의 아름다운 야경을 감상합니다.")
]

for time, location, description in day1:

    with st.container(border=True):

        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown(f"**{time}**")

        with col2:
            st.markdown(f"**{location}**")
            st.write(description)

# ==========================================
# DAY 2
# ==========================================

st.subheader("DAY 2 - 현대적인 서울과 트렌디한 거리")

st.image(
    "https://images.unsplash.com/photo-1535189043414-47a3c49a0bed?w=1200",
    caption="서울의 현대적인 도시 풍경",
    use_container_width=True
)

day2 = [
    ("09:00 ~ 10:30", "동대문디자인플라자",
     "독특한 건축물과 디자인 전시 공간을 둘러봅니다."),

    ("10:30 ~ 12:00", "성수동",
     "감각적인 카페와 편집숍, 팝업스토어를 방문합니다."),

    ("12:00 ~ 13:00", "점심 식사",
     "성수동 주변 맛집에서 점심을 즐깁니다."),

    ("13:00 ~ 15:00", "코엑스·별마당도서관",
     "쇼핑몰과 별마당도서관을 구경합니다."),

    ("15:00 ~ 17:30", "홍대",
     "거리 공연과 카페, 다양한 상점을 즐기며 여행을 마무리합니다.")
]

for time, location, description in day2:

    with st.container(border=True):

        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown(f"**{time}**")

        with col2:
            st.markdown(f"**{location}**")
            st.write(description)

# ==========================================
# 6. 여행 안내
# ==========================================

st.divider()

st.header("여행 안내")

st.markdown("""
- 추천 숙박 지역: 명동, 종로, 을지로
- 주요 이동 수단: 지하철 및 버스
- 추천 여행 시기: 봄과 가을
- 궁궐 휴무일과 관광지 운영 시간은 방문 전에 확인하세요.
- 실제 이동 시간은 교통 상황에 따라 달라질 수 있습니다.
""")

st.caption("""
지도 데이터: OpenStreetMap
관광지 좌표: 각 관광지의 대표 위치
관광지 TOP 10: 외국인에게 잘 알려진 대표 명소를 바탕으로 한 추천 목록
""")

st.success("서울 1박 2일 여행 코스 안내가 완료되었습니다!")
