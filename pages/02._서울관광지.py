
import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

st.title("서울 외국인 인기 관광지 TOP 10")
st.write("외국인 관광객이 많이 방문하는 서울의 주요 관광지를 지도에서 확인해 보세요.")

# 관광지 데이터
places = [
    {
        "rank": 1,
        "name": "명동",
        "english": "Myeong-dong",
        "lat": 37.5636,
        "lon": 126.9850,
        "description": "화장품 매장, 쇼핑 거리, 길거리 음식으로 유명한 서울의 대표 관광지입니다."
    },
    {
        "rank": 2,
        "name": "N서울타워",
        "english": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "description": "남산 정상에서 서울의 아름다운 전경과 야경을 감상할 수 있습니다."
    },
    {
        "rank": 3,
        "name": "코엑스",
        "english": "COEX",
        "lat": 37.5126,
        "lon": 127.0590,
        "description": "쇼핑몰, 별마당도서관, 전시장 등이 있는 복합 문화 공간입니다."
    },
    {
        "rank": 4,
        "name": "강남역",
        "english": "Gangnam Station",
        "lat": 37.4979,
        "lon": 127.0276,
        "description": "다양한 음식점과 카페, 쇼핑 시설이 모여 있는 번화가입니다."
    },
    {
        "rank": 5,
        "name": "홍대",
        "english": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "description": "거리 공연과 음악, 개성 있는 카페와 상점으로 유명합니다."
    },
    {
        "rank": 6,
        "name": "남대문시장",
        "english": "Namdaemun Market",
        "lat": 37.5592,
        "lon": 126.9770,
        "description": "다양한 한국 음식과 의류, 생활용품을 만날 수 있는 전통시장입니다."
    },
    {
        "rank": 7,
        "name": "동대문디자인플라자",
        "english": "DDP",
        "lat": 37.5671,
        "lon": 127.0095,
        "description": "독특한 건축 디자인과 전시, 문화 행사를 즐길 수 있는 공간입니다."
    },
    {
        "rank": 8,
        "name": "북촌한옥마을",
        "english": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "description": "한국 전통 한옥과 아름다운 골목길을 감상할 수 있습니다."
    },
    {
        "rank": 9,
        "name": "경복궁",
        "english": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "description": "조선 왕조의 대표 궁궐로 한국의 역사와 전통 건축을 경험할 수 있습니다."
    },
    {
        "rank": 10,
        "name": "서울숲·성수",
        "english": "Seoul Forest & Seongsu",
        "lat": 37.5444,
        "lon": 127.0374,
        "description": "넓은 공원과 감각적인 카페, 편집숍이 어우러진 인기 지역입니다."
    }
]

# 서울 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11,
    tiles="OpenStreetMap"
)

# 관광지 마커 표시
for place in places:

    popup_text = f"""
    <h4>{place['rank']}. {place['name']}</h4>
    <p>{place['english']}</p>
    <p>{place['description']}</p>
    """

    folium.Marker(
        location=[place["lat"], place["lon"]],
        tooltip=place["name"],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(
            color="red",
            icon="info-sign"
        )
    ).add_to(m)

# 지도 출력
st.subheader("서울 관광지 지도")

st_folium(
    m,
    width=None,
    height=600,
    use_container_width=True
)

# 관광지 설명
st.subheader("주요 관광지 소개")

for place in places:

    with st.expander(
        f"{place['rank']}. {place['name']} ({place['english']})"
    ):
        st.write(place["description"])

# 하단 안내
st.divider()

st.caption(
    "※ 관광지 위치는 대표 좌표이며, 순위는 추천 목록입니다. "
    "공식 방문객 순위와 동일한 통계 순위는 아닙니다."
)
