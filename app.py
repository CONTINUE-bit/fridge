import streamlit as st
import google.generativeai as genai

# 1. API 설정
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Secrets에 'GEMINI_API_KEY'를 추가해 주세요!")
    else:
        key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=key)
except Exception as e:
    st.error(f"설정 에러: {e}")

st.title("🥦 냉장고 파먹기 AI")

ingredients = st.text_input("남은 재료를 입력하세요 (예: 계란, 대파)")

if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('AI 셰프가 레시피를 생성 중입니다...'):
            try:
                # 404 에러를 피하기 위한 가장 안정적인 모델 호출 (gemini-pro)
                # 현재 환경에서 1.5-flash 경로가 꼬여있으므로, 검증된 gemini-pro를 우선 사용합니다.
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"{ingredients}를 주재료로 자취생용 요리 레시피 1개를 추천해줘.")
                
                st.success("레시피 생성 성공!")
                st.markdown(response.text)
                
            except Exception as e:
                # 만약 gemini-pro도 안된다면 최신 이름을 한 번 더 시도
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash-latest')
                    response = model.generate_content(f"{ingredients} 레시피 추천해줘.")
                    st.success("성공!")
                    st.markdown(response.text)
                except Exception as final_e:
                    st.error(f"최종 에러 발생: {final_e}")
                    st.info("이 에러는 구글 API 서버와 현재 라이브러리 간의 일시적인 경로 불일치입니다. 잠시 후 다시 시도해 주세요.")
    else:
        st.warning("재료를 입력해 주세요!")
