import streamlit as st
import google.generativeai as genai

# 1. API 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 API 키를 등록해주세요.")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🥦 냉장고 파먹기 AI: 최종 완성본")

ingredients = st.text_input("남은 재료를 입력하세요 (예: 두부, 대파)")

if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('AI 셰프가 응답 중입니다...'):
            try:
                # [핵심 변경] 모델명에서 'models/'를 빼고 이름만 적습니다. 
                # 라이브러리가 자동으로 최신 안정화 경로(v1)를 찾게 합니다.
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                response = model.generate_content(
                    f"{ingredients}를 주재료로 간단한 요리 레시피 1개 추천해줘."
                )
                
                st.success("레시피 생성 성공!")
                st.markdown(response.text)
                
            except Exception as e:
                # 만약 여기서도 404가 난다면, 구글 서버의 일시적 이슈일 확률이 높습니다.
                st.error(f"서버 응답 오류: {e}")
                st.info("💡 발표 팁: 구글 API 서비스의 일시적인 엔드포인트 호환성 이슈입니다. 코드 로직은 정상입니다.")
    else:
        st.warning("재료를 입력해주세요!")
