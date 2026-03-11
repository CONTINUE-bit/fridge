import streamlit as st
import google.generativeai as genai

def get_available_models():
    """
    ListModels API를 사용하여 사용 가능한 모델 목록을 가져옵니다.
    """
    try:
        model_list = genai.list_models()
        return [model.name for model in model_list]
    except Exception as e:
        st.error(f"모델 목록 가져오기 실패: {e}")
        return []

def validate_ingredients(ingredients):
    """
    입력된 재료가 유효한지 확인합니다.
    """
    if not ingredients.strip():
        return False, "재료를 입력해주세요."
    
    ingredient_list = [ingredient.strip() for ingredient in ingredients.split(",")]
    if len(ingredient_list) < 2:
        return False, "2개 이상의 재료를 입력해주세요."
    
    return True, None

def generate_recipe(ingredients):
    """
    입력된 재료로 레시피를 생성합니다.
    """
    try:
        available_models = get_available_models()
        if "gemini-1.5-flash" in available_models:
            model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            st.error("'gemini-1.5-flash' 모델을 찾을 수 없습니다. 사용 가능한 모델 목록을 확인해 주세요.")
            return

        response = model.generate_content(f"{ingredients}를 주재료로 간단한 자취 요리 레시피 1개 추천해줘.")
        return response.text
    except Exception as e:
        st.error(f"레시피 생성 중 오류 발생: {e}")
        return None

# 1. API 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Settings -> Secrets에 'GEMINI_API_KEY'를 등록해주세요.")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="냉장고 파먹기 AI", page_icon="🥦")
st.title("🥦 냉장고 파먹기 AI")

ingredients = st.text_input("남은 재료를 입력하세요", placeholder="예: 두부, 계란, 스팸")

if st.button("레시피 추천받기"):
    is_valid, error_message = validate_ingredients(ingredients)
    if is_valid:
        with st.spinner('AI 셰프가 응답 중입니다...'):
            recipe = generate_recipe(ingredients)
            if recipe:
                st.success("레시피 생성 완료!")
                st.markdown(recipe)
    else:
        st.warning(error_message)
