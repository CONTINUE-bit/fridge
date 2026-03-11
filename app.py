import streamlit as st
import google.generativeai as genai # 다시 이 라이브러리를 안정적으로 사용합니다.

# 1. API 설정
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# 2. 화면 구성
st.set_page_config(page_title="냉장고 파먹기 AI", page_icon="🥦")
st.title("🥦 냉장고 파먹기 AI: Single-Chef")
st.write("냉장고에 남은 재료를 입력하면 AI가 레시피를 제안합니다.")

# 입력창
ingredients = st.text_input("남은 재료를 입력하세요 (예: 두부, 스팸, 대파)", placeholder="재료를 쉼표로 구분")

# 3. 메인 로직
if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('AI 셰프가 레시피를 생각 중입니다...'):
            try:
                # 가장 안정적인 모델 호출 방식입니다.
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{ingredients}를 주재료로 자취생용 요리 레시피 1개를 추천해줘.")
                
                st.success("레시피 생성 완료!")
                st.markdown(response.text)
                
            except Exception as e:
                if "429" in str(e):
                    st.error("현재 요청이 너무 많습니다. 30초만 기다렸다가 다시 시도해 주세요!")
                else:
                    st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("재료를 입력해 주세요!")
