import streamlit as st
import google.generativeai as genai

# 1. API 설정
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Secrets에 'GEMINI_API_KEY'가 없습니다!")
    else:
        # 새로 발급받은 키를 적용
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"설정 불러오기 실패: {e}")

st.title("🥦 냉장고 파먹기 AI: Single-Chef")

ingredients = st.text_input("남은 재료를 입력하세요 (예: 두부, 대파)")

if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('AI 셰프가 응답 중입니다...'):
            try:
                # [중요] 'models/'를 붙이지 않고 모델명만 정확히 입력합니다.
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 프롬프트 전달
                response = model.generate_content(f"{ingredients}를 주재료로 간단한 요리 레시피 1개 알려줘.")
                
                st.success("레시피를 찾았습니다!")
                st.markdown(response.text)
                
            except Exception as e:
                # 여기서도 404가 나면 gemini-pro로 한 번 더 시도 (자동 페일오버)
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(f"{ingredients} 레시피 알려줘.")
                    st.success("성공 (안정화 모델 사용)")
                    st.markdown(response.text)
                except Exception as final_e:
                    st.error(f"서버 연결 오류: {final_e}")
                    st.info("구글 API 서버의 일시적인 경로 오류입니다. 1분 뒤 다시 시도해 보세요.")
    else:
        st.warning("재료를 입력해 주세요!")
