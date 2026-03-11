import streamlit as st
import google.generativeai as genai

# 1. Gemini API 설정 (발급받은 키를 여기에 넣으세요)
GOOGLE_API_KEY = "AIzaSyCVGHYea0bb6hMYiRX0cN0b6raTTtin01Y"
genai.configure(api_key=GOOGLE_API_KEY)
try:
    # 가장 표준적이고 최신인 명칭입니다.
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except:
    # 만약 위 설정이 실패하면 이전 세대 안정화 모델로 자동 전환합니다.
    model = genai.GenerativeModel('models/gemini-pro')

# 2. 화면 구성 (프론트엔드)
st.set_page_config(page_title="냉장고 파먹기 AI", page_icon="🥦")
st.title("🥦 냉장고 파먹기 AI: Single-Chef")
st.markdown("---")
st.write("냉장고에 남은 재료들을 입력하시면 최적의 레시피를 추천해 드립니다.")

# 입력창
ingredients = st.text_input("남은 재료를 입력하세요 (예: 두부, 스팸, 대파)", placeholder="재료를 쉼표로 구분해 주세요")

# 3. 메인 로직
if st.button("레시피 추천받기"):
    if ingredients:
        with st.spinner('AI 셰프가 레시피를 생각 중입니다...'):
            try:
                # 프롬프트 설계 (중요!)
                prompt = f"""
                너는 1인 가구를 위한 전문 요리사야. 
                사용자가 입력한 [{ingredients}]를 주재료로 사용해서 만들 수 있는 맛있는 요리 1가지를 추천해줘.
                형식은 다음과 같이 출력해줘:
                1. 요리 이름
                2. 간단한 요리 설명
                3. 필요한 추가 양념 (집에 있을 법한 기본 양념 위주)
                4. 조리 단계 (번호를 매겨서)
                5. AI 셰프의 팁 1가지
                """
                
                # API 호출
                response = model.generate_content(prompt)
                
                # 결과 출력
                st.success("레시피 작성이 완료되었습니다!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("재료를 입력해 주세요!")






