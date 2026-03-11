import streamlit as st
import google.generativeai as genai

# 1. API 설정
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Secrets 설정에서 'GEMINI_API_KEY'를 확인해주세요!")
    else:
        # 새로 발급받은 키가 적용되도록 설정
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"설정 불러오기 실패: {e}")

st.title("🥦 냉장고 파먹기 AI: Single-Chef")
st.write("안정적인 서버 모드로 연결 중입니다.")

ingredients = st.text_input("남은 재료를 입력하세요 (예: 두부, 대파)")

if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('AI 셰프가 응답 중...'):
            try:
                # 404 에러를 피하기 위해 가장 검증된 초기 모델명을 사용합니다.
                model = genai.GenerativeModel('gemini-pro')
                
                # 안전한 응답 생성을 위한 설정
                response = model.generate_content(
                    f"{ingredients}를 주재료로 간단한 요리 레시피 1개 알려줘.",
                    generation_config=genai.types.GenerationConfig(
                        candidate_count=1,
                        stop_sequences=['x'],
                        max_output_tokens=500,
                        temperature=0.7)
                )
                
                if response.text:
                    st.success("레시피를 찾았습니다!")
                    st.markdown(response.text)
                else:
                    st.warning("AI가 답변을 생성하지 못했습니다. 다시 시도해주세요.")
                    
            except Exception as e:
                # 만약 여기서도 404가 난다면, 구글 AI 스튜디오의 모델 사용 권한 자체의 문제입니다.
                st.error(f"최종 확인된 에러: {e}")
                st.info("이 오류는 구글 계정의 API 사용 권한 문제입니다. 다른 구글 계정으로 키를 새로 발급받는 것을 추천합니다.")
    else:
        st.warning("재료를 입력해 주세요!")
