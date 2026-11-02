import streamli as st
st.title('사용자')
a-st. text_input('이름을 입력하세요')
b=st.selectbox ('좋아하는 음식을 선택하세요',['신라면','새우탕면','열라면'])
if st. button('인사말 생성'):
  st.write('반갑습니다')
  st.info(a+'님, 안녕하세요!')
  st.warning(b+'를 좋아하시는군요!')
  st.error('잘 부탁드려요!')
  st.balloons()
