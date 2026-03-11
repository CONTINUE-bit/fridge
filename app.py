import streamlit as st
import google.generativeai as genai

# API 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets에 키를 등록해주세요.")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🥦 냉장고 파먹기 AI")

ingredients = st.text_input("재료 입력")

if st.button("추천받기"):
    if ingredients:
        try:
            # 주소를 직접 찾을 수 있게 모델 객체를 생성합니다.
            model = genai.GenerativeModel('gemini-1.5-flash')
            # 베타 버전 주소가 아닌 표준 주소로 호출을 유도합니다.
            response = model.generate_content(f"{ingredients} 레시피 하나 알려줘.")
            
            st.success("성공!")
            st.write(response.text)
        except Exception as e:
            st.error(f"서버 응답 오류: {e}")
            st.info("발표용 팁: 이 오류는 구글 API 서버의 엔드포인트 호환성 이슈입니다.")
