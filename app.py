import streamlit as st
import google.generativeai as genai

# 1. API 설정
try:
    key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=key)
except Exception as e:
    st.error(f"Secrets 설정 에러: {e}")

st.title("🥦 냉장고 파먹기 AI: Single-Chef")

ingredients = st.text_input("남은 재료를 입력하세요 (예: 두부, 대파)")

if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('AI 셰프가 요리를 연구 중입니다...'):
            try:
                # [중요] 모델 이름 앞에 'models/'를 생략하고 시도합니다.
                # 만약 안되면 'models/gemini-1.5-flash'로 한 번 더 시도하는 로직입니다.
                model_name = 'gemini-1.5-flash' 
                model = genai.GenerativeModel(model_name)
                
                response = model.generate_content(f"{ingredients}를 주재료로 자취생용 요리 레시피 1개 추천해줘.")
                
                st.success("레시피 완성!")
                st.markdown(response.text)
                
            except Exception as e:
                # 404 에러 대응: 다른 명칭으로 재시도
                try:
                    model = genai.GenerativeModel('models/gemini-1.5-flash')
                    response = model.generate_content(f"{ingredients} 레시피 알려줘.")
                    st.success("성공 (표준 경로 사용)")
                    st.markdown(response.text)
                except Exception as final_e:
                    st.error(f"서버 연결 오류: {final_e}")
    else:
        st.warning("재료를 입력해 주세요!")
