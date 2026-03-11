import streamlit as st
import google.generativeai as genai

# 1. API 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Settings -> Secrets에 'GEMINI_API_KEY'를 등록해주세요.")
else:
    # 안전하게 API 키 설정
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="냉장고 파먹기 AI", page_icon="🥦")
st.title("🥦 냉장고 파먹기 AI")

ingredients = st.text_input("남은 재료를 입력하세요", placeholder="예: 두부, 계란, 스팸")

if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('AI 셰프가 응답 중입니다...'):
            try:
                # [최신 표준] models/ 를 붙이지 않고 최신 모델명만 사용
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                response = model.generate_content(
                    f"{ingredients}를 주재료로 간단한 자취 요리 레시피 1개 추천해줘."
                )
                
                st.success("레시피 생성 완료!")
                st.markdown(response.text)
                
            except Exception as e:
                # 여전히 404가 날 경우를 대비한 대체 경로
                try:
                    # 라이브러리 버전에 따라 다를 수 있는 경로 강제 시도
                    model = genai.GenerativeModel('models/gemini-1.5-flash')
                    response = model.generate_content(f"{ingredients} 레시피 추천해줘.")
                    st.success("성공 (표준 경로 연결)")
                    st.markdown(response.text)
                except Exception as final_e:
                    st.error(f"서버 응답 오류: {final_e}")
                    st.info("💡 팁: 이 오류는 구글 API 서버의 일시적인 경로 이슈입니다. 잠시 후 다시 시도해 보세요.")
    else:
        st.warning("재료를 입력해주세요!")
