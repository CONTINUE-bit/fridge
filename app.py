import streamlit as st
from google import genai

# 1. API 설정
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
                # [수정 1] 모델명을 gemini-1.5-flash로 변경 (무료 할당량 최적화)
                response = client.models.generate_content(
                    model="gemini-1.5-flash-002", 
                    contents=f"{ingredients}를 주재료로 자취생용 요리 레시피 1개를 추천해줘."
                )
                
                # [수정 2] 응답 객체에서 텍스트를 추출하는 방식 안전하게 변경
                # 최신 SDK에서는 response.text로 바로 접근이 가능하지만, 
                # 간혹 빈 응답이 올 경우를 대비해 아래와 같이 출력합니다.
                if response:
                    st.success("레시피 생성 완료!")
                    st.markdown(response.text)
                else:
                    st.error("AI로부터 응답을 받지 못했습니다. 다시 시도해 주세요.")
                
            except Exception as e:
                # 429 에러가 발생했을 때 사용자에게 안내 메시지 강화
                if "429" in str(e):
                    st.error("현재 요청이 너무 많습니다. 30초만 기다렸다가 다시 버튼을 눌러주세요!")
                else:
                    st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("재료를 입력해 주세요!")


