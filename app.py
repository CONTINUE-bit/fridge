import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# 1. API 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets에 API 키를 등록해주세요.")
else:
    # API 키를 설정합니다.
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🥦 냉장고 파먹기 AI: 최종 해결 모드")

ingredients = st.text_input("남은 재료를 입력하세요 (예: 두부, 계란)")

if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('서버와 직접 통신 중...'):
            try:
                # [필살기] v1beta가 아닌 'v1' API 버전을 쓰라고 강제로 옵션을 줍니다.
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # RequestOptions를 사용하여 API 버전을 v1으로 고정합니다.
                response = model.generate_content(
                    f"{ingredients}로 자취생용 요리 레시피 1개 추천해줘.",
                    request_options=RequestOptions(api_version='v1')
                )
                
                st.success("드디어 성공!")
                st.markdown(response.text)
                
            except Exception as e:
                # 만약 이래도 안된다면, 모델명에서 models/를 붙여서 마지막 시도
                try:
                    model = genai.GenerativeModel('models/gemini-1.5-flash')
                    response = model.generate_content(
                        f"{ingredients} 레시피 알려줘.",
                        request_options=RequestOptions(api_version='v1')
                    )
                    st.success("성공 (경로 강제 지정)")
                    st.markdown(response.text)
                except Exception as final_e:
                    st.error(f"기술적 한계 발생: {final_e}")
                    st.info("이 오류는 현재 계정이 구글의 최신 API 엔드포인트에 접근이 제한된 상태임을 의미합니다.")
    else:
        st.warning("재료를 입력해주세요!")
