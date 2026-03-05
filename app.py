import streamlit as st
import google.generativeai as genai
import os

# 1. API 설정
API_KEY = "AIzaSyDdBePmdkBA5TMMWO1rDG3sXgev_6-QEju"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="영문학 거장 스무고개", page_icon="📚")
st.title("📚 AI 자유 질문 스무고개")
st.write("제가 생각한 인물은 누구일까요? 질문을 던져보세요!")

# 세션 상태 초기화 (대화 기록 저장용)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if not st.session_state.game_over:
    if prompt := st.chat_input("질문을 입력하세요 (예: 한국 사람인가요?)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답 생성
        system_instruction = "당신은 스무고개 사회자입니다. 정답은 '소설가 한강'입니다. '예', '아니오', '모르겠습니다'로만 답하세요. 정답을 맞히면 '정답입니다!'라고 하세요."
        response = model.generate_content(f"{system_instruction}\n\n질문: {prompt}")
        ai_answer = response.text.strip()

        st.session_state.messages.append({"role": "assistant", "content": ai_answer})
        with st.chat_message("assistant"):
            st.markdown(ai_answer)

        # 정답 판정
        if "정답입니다" in ai_answer:
            st.balloons()
            st.image("han_kang.jpg", caption="정답: 소설가 한강")
            st.success("🎉 정답을 맞히셨습니다!")
            st.session_state.game_over = True
