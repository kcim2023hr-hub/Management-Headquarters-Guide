import streamlit as st
from openai import OpenAI
import datetime

# 1. 페이지 설정
st.set_page_config(
    page_title="Kcim 육아지원 실무 대응 시스템",
    page_icon="⚖️",
    layout="wide"
)

# Kcim 브랜드 컬러
KCIM_DARK = "#193D52"
KCIM_MEDIUM = "#00A8C0"
KCIM_LIGHT = "#8CCEE7"
WHITE = "#FFFFFF"

# 2. 고도화된 레이아웃 CSS (이레 안심 가이드 스타일 이식)
st.markdown(f"""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * {{ font-family: 'Pretendard', sans-serif; }}
    
    /* 전체 스크롤 억제 및 배경 */
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: #F8F9FA;
        overflow: hidden;
    }}

    /* 사이드바 디자인 (글씨 색상 및 라운드 처리) */
    [data-testid="stSidebar"] {{
        background-color: {KCIM_DARK};
        padding: 2rem 1rem;
    }}
    [data-testid="stSidebar"] .stMarkdown p {{
        color: #FFFFFF !important;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
    [data-testid="stSidebar"] .stRadio label {{
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px 15px;
        margin-bottom: 5px;
        color: #E2E8F0 !important;
        transition: 0.3s;
    }}
    [data-testid="stSidebar"] .stRadio label:hover {{
        background-color: rgba(255, 255, 255, 0.15);
    }}
    /* 라디오 선택 시 강조 */
    div[data-testid="stRadio"] div[role="radiogroup"] > label[data-baseweb="radio"] {{
        font-size: 1.1rem !important;
    }}

    /* 메인 타이틀 구역 */
    .main-title {{
        text-align: center;
        color: #FF4B6B; /* 포인트 핑크 대신 Kcim 톤 유지 시 아래 컬러 사용 */
        color: {KCIM_DARK};
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
    }}

    /* 정보 카드 (중앙 정렬 및 부드러운 그림자) */
    .info-card-container {{
        max-width: 850px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        height: 50vh;
        overflow-y: auto;
        padding: 10px;
    }}
    .info-card {{
        background: white;
        border-radius: 20px;
        padding: 1.5rem 2rem;
        border: 2px solid #FFE5E9; /* 부드러운 테두리 */
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .card-header {{
        color: {KCIM_MEDIUM};
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .card-content {{
        font-size: 1.05rem;
        color: #334155;
        line-height: 1.7;
    }}
    .card-content b {{ color: {KCIM_DARK}; }}

    /* 하단 통합 검색/상담창 (고정) */
    .fixed-footer {{
        position: fixed;
        bottom: 20px;
        left: 20%; /* 사이드바 공간 제외 */
        right: 5%;
        max-width: 850px;
        margin: 0 auto;
        background: white;
        border-radius: 25px;
        padding: 10px 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.05);
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 (정보 업데이트)
with st.sidebar:
    st.markdown(f"### 💖 Kcim 실무 가이드")
    st.write(f"2026년 04월 22일 (수)")
    st.divider()
    
    st.markdown("📂 **응대 카테고리**")
    category = st.radio(
        "",
        ["전체 가이드", "🤰 임신기 지침", "👨‍🍼 배우자 휴가", "🤱 육아기 정책", "💰 급여/복직"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("📞 **지원팀 직통**")
    st.info("• 인사지원: 내선 102\n• 마더세이프: 1588-7309")

# 4. 메인 콘텐츠
st.markdown(f'<div class="main-title">✨ Kcim 육아지원 실무 대시보드</div>', unsafe_allow_html=True)

# 선택 데이터 필터링
faq_pool = [
    {"cat": "🤰 임신기 지침", "title": "임신 초기 단축근무 대응", "content": "임신 <b>12주 이내 또는 32주 이후</b>인지 확인하십시오[cite: 13, 76]. 하루 2시간 단축이 가능하며 고위험 임신부는 전 기간 사용 가능합니다[cite: 13, 77]."},
    {"cat": "👨‍🍼 배우자 휴가", "title": "배우자 출산휴가 핵심", "content": "25.2.23.부터 <b>유급 20일</b>로 확대되었습니다[cite: 27, 103]. 출산일로부터 120일 내 총 4회(분할 3회) 사용 가능함을 안내하십시오[cite: 30, 105, 106]."},
    {"cat": "🤱 육아기 정책", "title": "자녀 연령 확대 안내", "content": "대상 자녀 연령이 <b>만 12세(초6)</b>로 대폭 확대되었습니다[cite: 48, 118, 119]. 육휴 미사용분 포함 시 최대 3년까지 사용 가능합니다[cite: 45, 119]."},
    {"cat": "💰 급여/복직", "title": "사후지급금 폐지 관련", "content": "2025년 1월 1일 사용분부터 <b>사후지급금 제도가 폐지</b>되었습니다[cite: 41, 113, 257]. 복직 대기 없이 휴직 중 100% 수령 가능함을 안내하십시오[cite: 113, 297]."}
]

display_data = faq_pool if category == "전체 가이드" else [d for d in faq_pool if d['cat'] in category]

st.markdown('<div class="info-card-container">', unsafe_allow_html=True)
for item in display_data:
    st.markdown(f"""
        <div class="info-card">
            <div class="card-header">📌 {item['title']}</div>
            <div class="card-content">{item['content']}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. 하단 상담/검색창 (레이아웃 동일화)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 상담 내용이 표시될 공간
chat_box = st.container(height=150)
with chat_box:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 검색바 (이레 안심 가이드 스타일)
if prompt := st.chat_input("증상, 제도, 법령 등 무엇이든 물어보세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_box:
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "너는 Kcim 전문 노무사야. 2025년 개정안(초6 자녀연령, 급여 250만 등)을 바탕으로 친절히 답변해."}] + st.session_state.messages
                )
                res = response.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("API Key를 확인해 주세요.")
