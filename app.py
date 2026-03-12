import streamlit as st
import google.generativeai as genai

# 1. API 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets에 API 키를 등록해주세요.")

st.title("🥦 냉장고 파먹기 AI: Next-Gen")

ingredients = st.text_input("남은 재료를 입력하세요 (예: 스팸, 계란)")

if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('최신 Gemini 2.0 모델로 레시피를 생성 중...'):
            try:
                # 리스트에서 확인된 정확한 모델명을 사용합니다.
                model = genai.GenerativeModel('models/gemini-2.5-flash')
                
                response = model.generate_content(
                    f"{ingredients}를 주재료로 간단한 자취 요리 레시피 1개 추천해줘."
                )
                
                st.success("레시피 생성 성공!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"모델 연결 오류: {e}")
    else:
        st.warning("재료를 입력해주세요!")




