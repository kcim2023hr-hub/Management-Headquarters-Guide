import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(
    page_title="Kcim 육아지원 실무 대응 시스템",
    page_icon="⚖️",
    layout="wide"
)

# [Kcim 브랜드 컬러 팔레트]
KCIM_DARK = "#193D52"
KCIM_MEDIUM = "#00A8C0"
KCIM_LIGHT = "#8CCEE7"

# 2. 가독성 극대화 CSS (글씨 크기 대폭 상향)
st.markdown(f"""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 전체 기본 폰트 크기 상향 */
    html, body, [class*="css"] {{
        font-family: 'Pretendard', sans-serif;
        font-size: 18px; /* 기본 폰트 크기를 18px로 상향 */
    }}

    .stApp {{ background-color: #F8FAFC; }}
    
    /* 사이드바 글씨 크기 */
    [data-testid="stSidebar"] {{ background-color: {KCIM_DARK}; }}
    [data-testid="stSidebar"] .stMarkdown p {{ font-size: 18px !important; color: white !important; }}
    [data-testid="stSidebar"] .stRadio label {{ font-size: 19px !important; color: white !important; }}
    
    /* 헤더 배너 */
    .header-banner {{
        background: linear-gradient(135deg, {KCIM_DARK} 0%, {KCIM_MEDIUM} 100%);
        padding: 3rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2.5rem;
    }}
    .header-banner h1 {{ font-size: 3rem !important; }}
    .header-banner p {{ font-size: 1.4rem !important; }}
    
    /* 섹션 타이틀 */
    .section-title {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {KCIM_DARK};
        border-left: 8px solid {KCIM_MEDIUM};
        padding-left: 20px;
        margin-bottom: 2rem;
    }}

    /* 실무 응대 카드 (글씨 크기 및 간격 최적화) */
    .manual-card {{
        background: white;
        padding: 2.2rem;
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        margin-bottom: 2rem;
        box-shadow: 0 6px 10px rgba(0,0,0,0.04);
    }}
    .category-tag {{
        background: {KCIM_LIGHT};
        color: {KCIM_DARK} !important;
        padding: 6px 15px;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 800;
        margin-bottom: 1.2rem;
        display: inline-block;
    }}
    .manual-q {{ 
        font-size: 1.5rem; /* 질문 크기 상향 */
        font-weight: 800; 
        color: {KCIM_DARK}; 
        margin-bottom: 1.2rem; 
        display: block; 
        line-height: 1.4;
    }}
    .manual-a {{ 
        font-size: 1.25rem; /* 답변 크기 상향 */
        color: #1e293b; 
        line-height: 1.9; /* 줄 간격 확대 */
    }}
    .point {{ 
        color: {KCIM_MEDIUM}; 
        font-weight: 900; 
        background-color: #f0f9ff;
        padding: 0 4px;
    }}

    /* 하단 검색창 영역 */
    .search-area {{
        background: white;
        padding: 3rem;
        border-radius: 25px;
        border: 3px solid {KCIM_DARK};
        margin-top: 5rem;
    }}
    
    /* 스트림릿 기본 텍스트 입력창 크기 상향 */
    .stChatInput textarea {{
        font-size: 1.2rem !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 (실무 네비게이션)
with st.sidebar:
    st.markdown("## 📂 응대 카테고리")
    category = st.radio(
        "",
        ["전체 보기", "🤰 임신기 단축근무", "👨‍🍼 배우자 출산휴가", "🤱 육아휴직 및 단축", "💰 급여 및 복직 가이드"]
    )
    st.divider()
    st.markdown("### 📞 실무 지원")
    st.write("• 인사지원팀: 102")
    st.write("• IT 시스템: 105")

# 4. 메인 헤더
st.markdown(f"""
    <div class="header-banner">
        <h1>⚖️ 2025 육아지원 실무 대응</h1>
        <p>Kcim 경영관리본부 | {category} 실전 매뉴얼</p>
    </div>
    """, unsafe_allow_html=True)

# 5. 메인 콘텐츠
st.markdown(f'<p class="section-title">📍 {category} 지침 확인</p>', unsafe_allow_html=True)

faq_pool = [
    {
        "cat": "🤰 임신기 단축근무", 
        "q": "임신 초기 직원이 단축근무를 요청할 때 필수 확인사항은?", 
        "a": "현재 임신 <span class='point'>12주 이내</span> 또는 <span class='point'>32주 이후</span>인지 우선 확인하십시오[cite: 12, 13]. 임금 삭감 없이 <span class='point'>하루 2시간</span> 단축이 가능하며, 의사 진단이 있는 고위험 임신부는 전 기간 사용 가능함을 반드시 안내하십시오[cite: 13, 77]."
    },
    {
        "cat": "👨‍🍼 배우자 출산휴가", 
        "q": "배우자 출산휴가 기간과 분할 사용에 대해 묻는다면?", 
        "a": "2025년 2월 23일 이후 <span class='point'>유급 20일</span>로 확대되었습니다[cite: 27, 103]. 출산일로부터 120일 이내에 사용을 완료해야 하며, <span class='point'>총 4회(분할 3회)</span>까지 나누어 쓸 수 있어 유연한 육아 참여가 가능함을 안내하십시오[cite: 30, 105, 106]."
    },
    {
        "cat": "🤱 육아휴직 및 단축", 
        "q": "초등 고학년 자녀를 둔 직원의 단축근무가 가능한가요?", 
        "a": "<b>네, 가능합니다.</b> 2025년 개정으로 대상 자녀 연령이 <span class='point'>만 12세 또는 초등 6학년 이하</span>로 확대되었습니다[cite: 48, 118, 119]. 육아휴직 미사용분 포함 시 최대 3년까지 사용 가능함을 적극 안내하십시오[cite: 45, 119]."
    },
    {
        "cat": "💰 급여 및 복직 가이드", 
        "q": "복직 예정자가 사후지급금(25%) 수령 시점을 문의한다면?", 
        "a": "2025년 1월 1일 이후 사용분부터 <span class='point'>사후지급금 제도가 폐지</span>되었습니다[cite: 41, 113, 257]. 이제 복직 후 6개월 대기 없이 휴직 중에 <span class='point'>급여 100%를 전액 수령</span>하게 됨을 안내하여 경제적 안정을 강조하십시오[cite: 113, 297]."
    }
]

display_data = faq_pool if category == "전체 보기" else [d for d in faq_pool if d['cat'] == category]

col1, col2 = st.columns(2)
for i, item in enumerate(display_data):
    with (col1 if i % 2 == 0 else col2):
        st.markdown(f"""
            <div class="manual-card">
                <span class="category-tag">{item['cat']}</span>
                <span class="manual-q">Q. {item['q']}</span>
                <p class="manual-a">A. {item['a']}</p>
            </div>
        """, unsafe_allow_html=True)

# 6. 최하단 상담창 (검색)
st.markdown('<div class="search-area">', unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center; color:{KCIM_DARK};'>🤖 실시간 노무 자문 (상세 검색)</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_placeholder = st.container(height=300)
with chat_placeholder:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(f"<div style='font-size:1.15rem;'>{msg['content']}</div>", unsafe_allow_html=True)

if prompt := st.chat_input("노무사에게 상세 내용을 문의하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(f"<div style='font-size:1.15rem;'>{prompt}</div>", unsafe_allow_html=True)
        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "너는 Kcim 전문 노무사야. 2025년 육아지원법 개정안을 바탕으로 답변해."}] + st.session_state.messages
                )
                res = response.choices[0].message.content
                st.markdown(f"<div style='font-size:1.15rem;'>{res}</div>", unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("API 연동을 확인하세요.")

st.markdown('</div>', unsafe_allow_html=True)

# 7. 푸터
st.markdown("<br><center style='color:#94a3b8; font-size:1rem;'>© 2025 Kcim Management Support Division | HR Practical Dashboard</center>", unsafe_allow_html=True)
