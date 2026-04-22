import streamlit as st
from openai import OpenAI
import datetime

# 1. 페이지 설정
st.set_page_config(
    page_title="Kcim 육아지원 실무 안심 대시보드",
    page_icon="⚖️",
    layout="wide"
)

# [Kcim 브랜드 컬러 설정]
KCIM_DARK = "#193D52"  # 신뢰의 네이비
KCIM_MEDIUM = "#00A8C0" # 활력의 사이언
KCIM_POINT = "#E63946"  # 강조/경고의 레드
BG_COLOR = "#F4F7F9"    # 부드러운 배경

# 2. 가독성 중심 고도화 CSS
st.markdown(f"""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * {{ font-family: 'Pretendard', sans-serif; }}
    
    .stApp {{ background-color: {BG_COLOR}; }}
    
    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {{
        background-color: {KCIM_DARK};
        padding: 2.5rem 1rem;
    }}
    [data-testid="stSidebar"] .stMarkdown p {{
        color: white !important;
        font-size: 1.1rem;
        font-weight: 500;
    }}

    /* 메인 타이틀 구역 */
    .dashboard-header {{
        background-color: white;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }}

    /* 상황별 응대 카드 (핵심) */
    .manual-card {{
        background: white;
        border-radius: 18px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }}
    .manual-card:hover {{ transform: translateY(-5px); }}

    /* 카드 내 텍스트 디자인 */
    .status-badge {{
        display: inline-block;
        padding: 6px 14px;
        border-radius: 8px;
        background-color: {KCIM_MEDIUM}15;
        color: {KCIM_MEDIUM};
        font-weight: 800;
        font-size: 0.95rem;
        margin-bottom: 1.2rem;
    }}
    .situation-q {{
        font-size: 1.6rem;
        font-weight: 800;
        color: {KCIM_DARK};
        margin-bottom: 1.5rem;
        line-height: 1.3;
    }}
    .action-a {{
        font-size: 1.2rem;
        color: #1E293B;
        line-height: 1.8;
        padding: 1.5rem;
        background-color: #F8FAFC;
        border-radius: 12px;
        border-left: 6px solid {KCIM_MEDIUM};
    }}
    
    /* 핵심 수치 강조 */
    .highlight {{
        color: {KCIM_POINT};
        font-weight: 800;
        background-color: #FFF5F5;
        padding: 2px 6px;
        border-radius: 4px;
    }}

    /* 챗봇 입력창 하단 고정 느낌 유지 */
    .chat-container {{
        max-width: 900px;
        margin: 0 auto;
        padding-top: 2rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바: 관리자 전용 상황 필터
with st.sidebar:
    st.markdown("## 🛡️ 관리자 메뉴")
    st.caption("문의 직원의 상황에 따라 가이드가 변경됩니다.")
    
    menu = st.radio(
        "상황 선택",
        ["🏠 전체 가이드 보기", "🤰 임신 초기/고위험군", "👨‍🍼 출산 및 배우자 휴가", "🤱 육아기 돌봄 및 단축", "💰 휴직 급여 및 복직"],
        index=0
    )
    st.divider()
    st.markdown("### 💡 관리자 Tip")
    st.info("2025년부터 모든 지원 제도가 '부모 동반 육아'를 장려하는 방향으로 확대되었습니다.")
    st.write(f"📅 업데이트: {datetime.date.today()}")

# 4. 메인 콘텐츠
st.markdown('<div class="dashboard-header">', unsafe_allow_html=True)
st.markdown(f'<h1 style="color:{KCIM_DARK}; margin:0;">⚖️ 육아지원제도 즉각 응대 매뉴얼</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#64748B; font-size:1.2rem; margin-top:0.5rem;">경영진 및 팀장용 실전 가이드 (2025년 개정판)</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. 응대 시나리오 데이터 (가이드북 내용 100% 반영)
scenarios = [
    {
        "cat": "🤰 임신 초기/고위험군",
        "q": "직원이 임신 초기라 출퇴근길이 너무 힘들고 조산 위험이 있다고 합니다.",
        "a": f"먼저 축하와 함께 <span class='highlight'>임신기 근로시간 단축</span>을 안내하세요. [cite: 13, 76] 임신 후 <span class='highlight'>12주 이내 및 32주 이후</span> 근로자는 임금 삭감 없이 하루 2시간 일찍 퇴근 가능합니다. [cite: 13, 75] 고위험 임신부는 기간 제한 없이 사용 가능하므로 안심시켜 주세요. [cite: 13, 77]"
    },
    {
        "cat": "👨‍🍼 출산 및 배우자 휴가",
        "q": "남성 직원이 아내의 출산으로 휴가를 길게 쓰고 싶어 합니다.",
        "a": f"올해부터 <span class='highlight'>배우자 출산휴가가 유급 20일</span>로 대폭 늘어났음을 알려주세요. [cite: 27, 103] 특히 한 번에 다 쓰지 않고 <span class='highlight'>총 4번까지 나누어 사용</span> 가능하므로, [cite: 30, 106] 산후조리원 퇴소 시기 등에 맞춰 유연하게 사용하도록 권장해 주세요. [cite: 100]"
    },
    {
        "cat": "🤱 육아기 돌봄 및 단축",
        "q": "초등학생 자녀를 둔 직원이 아이 등하교 문제로 고민이 많습니다.",
        "a": f"2025년부터 <span class='highlight'>육아기 단축근무 자녀 연령이 초6(만 12세)</span>까지 확대되었습니다. [cite: 48, 118] 육아휴직 미사용분까지 합쳐 <span class='highlight'>최대 3년</span>까지 쓸 수 있으니, [cite: 45, 119] 회사를 그만두지 않고도 커리어를 유지하며 아이를 돌볼 수 있다고 격려해 주세요. [cite: 118]"
    },
    {
        "cat": "💰 휴직 급여 및 복직",
        "q": "육아휴직 중 경제적 부담 때문에 복직을 고민하는 직원이 있다면?",
        "a": f"2025년부터 급여가 인상되어 <span class='highlight'>첫 3개월은 월 최대 250만 원</span>이 지급됩니다. [cite: 38, 113] 특히 복직 후 6개월 뒤에나 주던 <span class='highlight'>사후지급금 제도가 폐지</span>되어, [cite: 41, 113] 이제 휴직 중에 100% 다 받을 수 있어 훨씬 안심할 수 있다고 전해 주세요. [cite: 113, 297]"
    }
]

# 필터링 및 출력 영역
st.markdown('<div class="main-container">', unsafe_allow_html=True)

display_guides = scenarios if menu == "🏠 전체 가이드 보기" else [s for s in scenarios if s['cat'] == menu]

for s in display_guides:
    st.markdown(f"""
        <div class="manual-card">
            <span class="status-badge">{s['cat']}</span>
            <div class="situation-q">Q. {s['q']}</div>
            <div class="action-a">A. {s['a']}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 6. 하단 지능형 상담 기능
st.divider()
st.subheader("🤖 상세 법령 및 특수 사례 상담")
st.caption("위 시나리오 외에 구체적인 급여 계산이나 법적 예외 상황이 궁금하시면 질문하세요.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("예: 쌍둥이 출산 시 배우자 휴가 일수는?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "너는 Kcim 경영관리본부의 전문 노무 상담사야. 사장님과 팀장님께 2025년 개정된 법령을 기반으로 실무적인 조언을 해줘. 답변은 정중하고 신뢰감 있게 구성해."}] + st.session_state.messages
            )
            res = response.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except:
            st.error("상세 상담을 위해서는 OpenAI API 설정이 필요합니다.")
