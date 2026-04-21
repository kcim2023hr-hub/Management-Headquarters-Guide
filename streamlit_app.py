import streamlit as st
from openai import OpenAI

# 1. 페이지 설정 (전체 화면 활용)
st.set_page_config(
    page_title="Kcim 육아지원 실무 대응 시스템",
    page_icon="⚖️",
    layout="wide"
)

# [Kcim 브랜드 컬러]
KCIM_DARK = "#193D52"
KCIM_MEDIUM = "#00A8C0"
KCIM_LIGHT = "#8CCEE7"

# 2. 원페이지 & 글씨 색상 최적화 CSS
st.markdown(f"""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 폰트 및 스크롤 억제 */
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        overflow: hidden; /* 전체 페이지 스크롤 방지 */
    }}

    /* 사이드바 글씨 색상 및 디자인 */
    [data-testid="stSidebar"] {{
        background-color: {KCIM_DARK};
    }}
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] h2 {{
        color: #FFFFFF !important; /* 명도 높은 순백색으로 변경 */
        font-weight: 600;
    }}
    [data-testid="stSidebar"] .stRadio label {{
        color: #E2E8F0 !important; /* 약간 밝은 회색으로 가독성 확보 */
        font-size: 17px !important;
    }}
    [data-testid="stSidebar"] .stRadio label[data-shortid="selected"] {{
        color: {KCIM_LIGHT} !important; /* 선택된 항목은 라이트 블루 */
        font-weight: 800;
    }}

    /* 메인 배너 컴팩트화 */
    .header-banner {{
        background: linear-gradient(135deg, {KCIM_DARK} 0%, {KCIM_MEDIUM} 100%);
        padding: 1rem 2rem;
        border-radius: 12px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }}
    
    /* FAQ 카드 높이 고정 및 스크롤 */
    .content-area {{
        height: 45vh; /* 화면의 약 45% 차지 */
        overflow-y: auto;
        padding-right: 10px;
    }}
    
    .manual-card {{
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }}
    .manual-q {{ font-size: 1.2rem; font-weight: 700; color: {KCIM_DARK}; margin-bottom: 0.5rem; }}
    .manual-a {{ font-size: 1.05rem; color: #334155; line-height: 1.6; }}
    .point {{ color: {KCIM_MEDIUM}; font-weight: 800; }}

    /* 하단 고정 검색창 구역 */
    .search-area {{
        height: 30vh; /* 화면 하단 고정 */
        background: #F1F5F9;
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid {KCIM_DARK};
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 (글씨 색상 체크 완료)
with st.sidebar:
    st.markdown("## 📂 실무 카테고리")
    category = st.radio(
        "메뉴를 선택하세요",
        ["전체 보기", "🤰 임신기 단축", "👨‍🍼 배우자 휴가", "🤱 육아기 지침", "💰 급여/복직"],
        label_visibility="collapsed"
    )
    st.divider()
    st.markdown("### 📞 긴급 지원\n- 인사지원: 102\n- IT시스템: 105")

# 4. 메인 화면 (컴팩트 배너)
st.markdown(f"""
    <div class="header-banner">
        <h2 style="margin:0; font-size:1.8rem;">⚖️ 2025 육아지원 실무 대응</h2>
        <p style="margin:0; font-weight:600;">{category} 매뉴얼</p>
    </div>
    """, unsafe_allow_html=True)

# 5. FAQ 콘텐츠 영역 (높이 고정형)
st.markdown(f'<div class="content-area">', unsafe_allow_html=True)

faq_pool = [
    {"cat": "🤰 임신기 단축", "q": "임신 단축근무 필수 확인사항?", "a": "임신 <span class='point'>12주 이내/32주 이후</span> 확인. 삭감 없이 1일 2시간 단축 가능."},
    {"cat": "👨‍🍼 배우자 휴가", "q": "배우자 출산휴가 기간?", "a": "25.2.23. 이후 <span class='point'>유급 20일</span> 확대. 120일 내 총 4회 분할 가능."},
    {"cat": "🤱 육아기 지침", "q": "초등 6학년 자녀 단축근무?", "a": "<b>가능함.</b> 자녀 연령 <span class='point'>만 12세 이하</span>로 확대. 최대 3년 사용 가능."},
    {"cat": "💰 급여/복직", "q": "사후지급금 폐지 안내?", "a": "25.1.1. 이후 사용분부터 <span class='point'>100% 즉시 지급</span>. 복직 후 대기 불필요."}
]

display_data = faq_pool if category == "전체 보기" else [d for d in faq_pool if d['cat'] in category]

cols = st.columns(2)
for i, item in enumerate(display_data):
    with cols[i % 2]:
        st.markdown(f"""
            <div class="manual-card">
                <div class="manual-q">Q. {item['q']}</div>
                <div class="manual-a">A. {item['a']}</div>
            </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 6. 하단 고정 검색/상담창 (스크롤 없이 노출)
st.markdown('<div class="search-area">', unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; font-weight:bold; color:{KCIM_DARK}; margin-bottom:10px;'>🤖 실시간 전문 노무 상담 (상세 검색)</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 상담 내역 (작은 창)
chat_sub = st.container(height=120)
with chat_sub:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("문의 내용을 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_sub:
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "너는 Kcim 노무사야."}] + st.session_state.messages
                )
                res = response.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("API 연결 확인 요망")

st.markdown('</div>', unsafe_allow_html=True)
