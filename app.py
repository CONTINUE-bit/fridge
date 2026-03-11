import streamlit as st
import google.generativeai as genai

# 1. API 설정
try:
    if "GEMINI_API_KEY" in st.secrets:
        key = st.secrets["GEMINI_API_KEY"]
        # 최신 SDK 설정 방식
        genai.configure(api_key=key)
    else:
        st.error("Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다.")
except Exception as e:
    st.error(f"환경 설정 오류: {e}")

st.title("🥦 냉장고 파먹기 AI: 최신 모드")

ingredients = st.text_input("남은 재료를 입력하세요 (예: 두부, 계란)")

if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('최신 AI 모델에 연결 중...'):
            try:
                # [핵심] 최신 라이브러리에서 권장하는 모델 경로 명시
                # gemini-1.5-flash는 현재 가장 빠르고 안정적인 모델입니다.
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                
                response = model.generate_content(
                    f"{ingredients}를 주재료로 간단한 요리 레시피 1개 알려줘."
                )
                
                if response.text:
                    st.success("레시피 생성 완료!")
                    st.markdown(response.text)
                
            except Exception as e:
                # 여기서도 404가 난다면 모델명을 gemini-pro로 교체해봅니다.
                try:
                    model = genai.GenerativeModel('models/gemini-pro')
                    response = model.generate_content(f"{ingredients} 레시피 추천해줘.")
                    st.success("성공 (안정 모델 연결)")
                    st.markdown(response.text)
                except Exception as final_e:
                    st.error(f"최종 연결 실패: {final_e}")
                    st.info("구글 API 계정의 'Generative Language API' 사용 설정이 활성화되었는지 확인이 필요합니다.")
    else:
        st.warning("재료를 입력해주세요!")
