import streamlit as st
from google import genai

# 1. API 설정
# Secrets에 저장했다면 st.secrets["GEMINI_API_KEY"]를 사용하세요.
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GOOGLE_API_KEY)

# 2. 화면 구성
st.set_page_config(page_title="냉장고 파먹기 AI", page_icon="🥦")
st.title("🥦 냉장고 파먹기 AI: Single-Chef")
st.write("냉장고에 남은 재료를 입력하면 최신 Gemini AI가 레시피를 제안합니다.")

# 입력창
ingredients = st.text_input("남은 재료를 입력하세요 (예: 두부, 스팸, 대파)", placeholder="재료를 쉼표로 구분")

# 3. 메인 로직
if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('AI 셰프가 최신 레시피를 가져오는 중...'):
            try:
                # 최신 라이브러리 호출 방식
                response = client.models.generate_content(
                    model="gemini-2.0-flash", # 가장 최신 모델 사용
                    contents=f"{ingredients}를 주재료로 자취생용 요리 레시피 1개를 추천해줘."
                )
                
                st.success("레시피 생성 완료!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("재료를 입력해 주세요!")

