import streamlit as st
import google.generativeai as genai

# 1. API 설정
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# 2. 화면 구성
st.set_page_config(page_title="냉장고 파먹기 AI", page_icon="🥦")
st.title("🥦 냉장고 파먹기 AI: Single-Chef")

# 입력창
ingredients = st.text_input("남은 재료를 입력하세요", placeholder="예: 두부, 스팸, 대파")

# 3. 메인 로직
if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('AI 셰프가 레시피를 생성 중입니다...'):
            # 시도해볼 모델 목록 (우선순위 순)
            model_names = ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-1.5-flash']
            
            success = False
            for name in model_names:
                try:
                    model = genai.GenerativeModel(name)
                    response = model.generate_content(f"{ingredients}를 주재료로 자취생용 요리 레시피 1개를 추천해줘.")
                    
                    st.success(f"레시피 생성 완료! (사용 모델: {name})")
                    st.markdown(response.text)
                    success = True
                    break # 성공하면 루프 탈출
                except Exception:
                    continue # 실패하면 다음 모델명 시도
            
            if not success:
                st.error("현재 모든 AI 모델 경로가 응답하지 않습니다. API 키 권한이나 라이브러리 설정을 확인해주세요.")
    else:
        st.warning("재료를 입력해 주세요!")
