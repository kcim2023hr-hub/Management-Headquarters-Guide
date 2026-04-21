import streamlit as st
from openai import OpenAI
import datetime

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="육아지원제도 가이드", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f9f9fb; }
    .stCard {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #e1e4e8;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .title-text { color: #2c3e50; font-weight: 800; font-size: 32px; text-align: center; margin-bottom: 30px; }
    .highlight { color: #ff4b6b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. 사이드바 구성
with st.sidebar:
    st.markdown("### 🍼 육아지원 센터")
    st.write(f"📅 **기준일:** {datetime.date.today().strftime('%Y-%m-%d')}")
    st.divider()
    
    st.markdown("#### 📑 주요 바로가기")
    st.link_button("정부 '6+6' 부모육아휴직제 안내", "https://www.ei.go.kr")
    st.button("신청 서식 다운로드 (사내)")
    st.button("복직 지원 프로그램 신청")
    
    st.sidebar.markdown("---")
    st.sidebar.info("📞 **문의: 인사총무팀 (내선 102)**")

# 3. 메인 화면 타이틀
st.markdown("<div class='title-text'>💖 경영관리본부 육아지원제도 가이드</div>", unsafe_allow_html=True)

# 4. 정보 카드 섹션 (이미지 레이아웃 참고)
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="stCard">
            <h3>🤰 임신기 지원 제도</h3>
            <p>• <b>단축 근무:</b> 임신 전체 기간 2시간 단축 가능</p>
            <p>• <b>태아검진 휴가:</b> 매월 1회 유급 휴가 제공</p>
            <p class="highlight">⚠️ 신청 방법: 그룹웨어 '근무 신청' 메뉴 활용</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stCard">
            <h3>👨‍👩‍👧‍👦 육아기 지원 제도</h3>
            <p>• <b>육아휴직:</b> 자녀당 최대 1년 (남/녀 공통)</p>
            <p>• <b>유연근무제:</b> 시차출퇴근제 적극 권장</p>
            <p><b>"일과 가정의 양립, 경영관리본부가 함께합니다."</b></p>
        </div>
    """, unsafe_allow_html=True)

# 5. ChatGPT API 연동 Q&A 섹션
st.divider()
st.markdown("### 🤖 무엇이든 물어보세요 (육아휴직, 급여 계산 등)")

# Secrets에서 API 키 불러오기 (배포 시 설정 필요)
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except:
    st.error("API Key가 설정되지 않았습니다. Streamlit Cloud의 Secrets 설정을 확인해주세요.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "너는 경영관리본부의 육아지원제도 전문 상담사야. 규정에 기반해 친절하게 답변해줘."}
    ]

# 채팅 이력 표시
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("예: 육아휴직 급여는 어떻게 계산되나요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
