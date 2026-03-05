import streamlit as st
import google.generativeai as genai
import os

# 1. API 설정
API_KEY = "AIzaSyAsahOu0AatP8A_zAvU4H6jCJS0_9Npe_c"
genai.configure(api_key=API_KEY)

# 최신 모델 설정
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="영문학 거장 스무고개", page_icon="📚")
st.title("📚 AI 자유 질문 스무고개")
st.write("제가 생각한 인물은 누구일까요? 질문을 던져보세요!")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if not st.session_state.game_over:
    if prompt := st.chat_input("질문을 입력하세요 (예: 한국 사람인가요?)"):
        # 사용자 질문 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답 생성 (에러 방지를 위해 문자열 구조 최적화)
        try:
            system_instruction = (
                "너는 스무고개 게임의 사회자야. 정답은 '소설가 한강'이야. "
                "사용자의 질문에 대해 오직 '예', '아니오', '모르겠습니다' 중 하나로만 아주 짧게 대답해줘. "
                "사용자가 '한강'을 맞추면 '정답입니다!'라고 대답해야 해."
            )
            
            # 내용을 리스트가 아닌 단일 문자열로 구성하여 전달
            full_prompt = f"{system_instruction}\n\n사용자 질문: {prompt}\n답변:"
            response = model.generate_content(full_prompt)
            ai_answer = response.text.strip()

            # AI 응답 표시
            st.session_state.messages.append({"role": "assistant", "content": ai_answer})
            with st.chat_message("assistant"):
                st.markdown(ai_answer)

            # 정답 판정 및 이미지 표시
            if "정답입니다" in ai_answer:
                st.balloons()
                st.success("🎉 축하합니다! 정답은 '소설가 한강'입니다.")
                if os.path.exists("han_kang.jpg"):
                    st.image("han_kang.jpg", caption="한강 (소설가)")
                st.session_state.game_over = True
                
        except Exception as e:
            st.error(f"대답을 생성하는 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요. (에러: {e})")

# 다시 시작 버튼
if st.session_state.game_over:
    if st.button("게임 다시 시작하기"):
        st.session_state.messages = []
        st.session_state.game_over = False
        st.rerun()
