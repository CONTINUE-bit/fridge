import streamlit as st
import google.generativeai as genai

# API 설정
try:
    key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=key)
except Exception as e:
    st.error(f"Secrets 설정 에러: {e}")

st.title("🥦 냉장고 파먹기 AI: 최종 테스트")

ingredients = st.text_input("남은 재료를 입력하세요")

if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('분석 중...'):
            try:
                # 가장 확실한 모델 하나만 시도합니다.
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{ingredients} 요리 레시피 1개 추천해줘.")
                
                st.success("성공!")
                st.markdown(response.text)
            except Exception as e:
                # 여기에 뜨는 영어 메시지가 진짜 범인입니다!
                st.error(f"진짜 에러 원인: {e}")
    else:
        st.warning("재료를 입력하세요.")
