import streamlit as st
import google.generativeai as genai

# 1. API 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets에 API 키를 등록해주세요.")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🥦 냉장고 파먹기 AI: 성공 모드")

ingredients = st.text_input("남은 재료를 입력하세요 (예: 계란, 참치)")

if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('AI 셰프가 응답 중입니다...'):
            try:
                # [해결책] 모델 이름에 버전을 직접 명시하거나, 가장 표준적인 이름을 사용합니다.
                # v1beta 에러를 피하기 위해 'models/gemini-1.5-flash' 경로를 사용합니다.
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                
                response = model.generate_content(
                    f"{ingredients}로 만드는 간단한 자취 요리 레시피 1개 추천해줘."
                )
                
                st.success("레시피 생성 성공!")
                st.markdown(response.text)
                
            except Exception as e:
                # 만약 위 방식도 안된다면, 가장 기초적인 모델로 마지막 시도
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(f"{ingredients} 레시피 알려줘.")
                    st.success("성공 (안정 모델 모드)")
                    st.markdown(response.text)
                except Exception as final_e:
                    st.error(f"서버 응답 오류: {final_e}")
                    st.info("💡 팁: 이 오류는 라이브러리와 구글 서버 간의 버전 미스매치입니다. 발표 시 '인프라 호환성 이슈 해결 과정'으로 설명하기 좋습니다.")
    else:
        st.warning("재료를 입력해주세요!")
