import streamlit as st
from openai import OpenAI
import datetime

# 1. 페이지 설정: 넓은 화면 사용 및 타이틀 설정
st.set_page_config(
    page_title="Kcim 육아지원 실무 안심 대시보드",
    page_icon="⚖️",
    layout="wide"
)

# [Kcim 브랜드 컬러]
KCIM_DARK = "#193D52"  # 신뢰감을 주는 네이비
KCIM_MEDIUM = "#00A8C0" # 전문적인 사이언
KCIM_POINT = "#FF4B6B"  # 주의/강조용 포인트 색상

# 2. UI/UX 최적화 CSS (가독성 및 심리적 안정감 강조)
st.markdown(f"""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * {{ font-family: 'Pretendard', sans-serif; }}
    
    /* 배경 및 전체 레이아웃 */
    .stApp {{ background-color: #F4F7F9; }}
    
    /* 사이드바 스타일: 어두운 배경에 흰색 글씨로 시인성 확보 */
    [data-testid="stSidebar"] {{
        background-color: {KCIM_DARK};
        padding: 2rem 1rem;
    }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    
    /* 중앙 집중형 카드 레이아웃 */
    .main-container {{
        max-width: 900px;
        margin: 0 auto;
        padding-bottom: 100px;
    }}
    
    /* 섹션 타이틀 */
    .st-title {{
        font-size: 2.2rem;
        font-weight: 800;
        color: {KCIM_DARK};
        text-align: center;
        margin-bottom: 0.5rem;
    }}
    .st-subtitle {{
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }}

    /* 응대 카드 디자인 */
    .guide-card {{
        background: white;
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    .guide-tag {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 700;
        background-color: {KCIM_MEDIUM}20;
        color: {KCIM_MEDIUM};
        margin-bottom: 1rem;
    }}
    .guide-q {{
        font-size: 1.3rem;
        font-weight: 700;
        color: {KCIM_DARK};
        margin-bottom: 1rem;
    }}
    .guide-a {{
        font-size: 1.1rem;
        color: #334155;
        line-height: 1.8;
        padding: 1rem;
        background-color: #F8FAFC;
        border-radius: 10px;
        border-left: 4px solid {KCIM_MEDIUM};
    }}
    .highlight {{ color: {KCIM_POINT}; font-weight: 700; }}

    /* 하단 검색창 고정 스타일 */
    .footer-search {{
        position: fixed;
        bottom: 0;
        left: 20rem; /* 사이드바 너비 고려 */
        right: 0;
        background: white;
        padding: 1.5rem 3rem;
        border-top: 1px solid #E2E8F0;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.05);
        z-index: 100;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바: 상황별 빠른 메뉴
with st.sidebar:
    st.markdown("## 🛡️ 관리자 메뉴")
    st.caption("문의 직원의 상황을 선택하세요")
    
    menu = st.radio(
        "",
        ["🏠 전체 한눈에 보기", "🤰 임신 사실을 알렸을 때", "👨‍🍼 출산이 임박했을 때", "🤱 본격적인 육아기", "💰 급여/복직 문의"],
        index=0
    )
    
    st.divider()
    st.markdown("### 💡 실무 Tip")
    st.info("임직원에게 '축하'를 먼저 건네는 것이 원활한 노무 관리의 시작입니다.")
    st.write(f"📅 기준일: {datetime.date.today()}")

# 4. 메인 콘텐츠 영역
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown('<div class="st-title">⚖️ 육아지원제도 즉각 응대 가이드</div>', unsafe_allow_html=True)
st.markdown('<div class="st-subtitle">사장님과 팀장님을 위한 2025년 최신판 실무 매뉴얼</div>', unsafe_allow_html=True)

# 데이터 정의 (최신 법령 기반 요약)
guides = [
    {
        "cat": "🤰 임신 사실을 알렸을 때",
        "q": "직원이 임신 초기라 몸이 힘들다고 합니다. 어떤 혜택이 있죠?",
        "a": "가장 먼저 <span class='highlight'>'임신기 근로시간 단축'</span>을 안내하세요. 12주 이내라면 임금 삭감 없이 하루 2시간 일찍 퇴근할 수 있습니다. 2025년부터는 32주 이후에도 동일하게 적용됩니다."
    },
    {
        "cat": "👨‍🍼 출산이 임박했을 때",
        "q": "남성 직원이 아내 출산으로 자리를 비워야 한다면?",
        "a": "최근 법 개정으로 <span class='highlight'>'배우자 출산휴가'가 유급 20일</span>로 대폭 늘어났습니다. 한 번에 다 안 써도 되며, 120일 내에 4번까지 나누어 쓸 수 있다고 알려주시면 매우 좋아할 것입니다."
    },
    {
        "cat": "🤱 본격적인 육아기",
        "q": "초등학교 다니는 자녀가 있는데 단축근무가 되나요?",
        "a": "네, 가능합니다. 대상 자녀 연령이 <span class='highlight'>초등학교 6학년(만 12세)</span>까지 확대되었습니다. 육아기 근로시간 단축은 최대 3년까지 가능하니 업무 스케줄 조정을 함께 논의해 보세요."
    },
    {
        "cat": "💰 급여/복직 문의",
        "q": "육아휴직 들어가면 돈은 어떻게 나오나요?",
        "a": "2025년부터 급여가 인상되었습니다. <span class='highlight'>첫 3개월은 최대 250만 원</span>까지 나옵니다. 특히 복직 후에 주던 사후지급금 제도가 폐지되어, 이제 휴직 중에 100% 다 받을 수 있어 걱정 덜어주셔도 됩니다."
    }
]

# 필터링 및 출력
display_guides = guides if menu == "🏠 전체 한눈에 보기" else [g for g in guides if g['cat'] == menu]

for guide in display_guides:
    st.markdown(f"""
        <div class="guide-card">
            <div class="guide-tag">{guide['cat']}</div>
            <div class="guide-q">{guide['q']}</div>
            <div class="guide-a">{guide['a']}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 5. 하단 고정 AI 상담창 (전문 내용 확인용)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 이력 표시 컨테이너
with st.container():
    st.markdown("<br><br><br>", unsafe_allow_html=True) # 하단 여백
    if prompt := st.chat_input("더 구체적인 사례나 법령 근거가 궁금하시면 질문하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # AI 상담 로직 (OpenAI 연결 가정)
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "너는 Kcim 경영진을 보좌하는 전문 노무사야. 친절하고 명확하게 실무 답변을 해줘."}] + st.session_state.messages
            )
            ans = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except:
            st.warning("상세 답변을 위해 API 설정이 필요합니다. (기본 매뉴얼은 위 카드를 참고하세요)")

# 채팅 메시지 출력
for msg in reversed(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
