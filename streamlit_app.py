import streamlit as st
from openai import OpenAI
import datetime

# 1. 페이지 설정: 타이틀 및 레이아웃 최적화
st.set_page_config(
    page_title="Kcim 경영관리본부 육아지원 가이드",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kcim 브랜드 컬러 정의
KCIM_DARK = "#193D52"    # 메인 네이비 (신뢰감)
KCIM_MEDIUM = "#00A8C0"  # 포인트 사이언 (활력)
KCIM_LIGHT = "#8CCEE7"   # 소프트 블루 (편안함)
BG_SOFT = "#F8FAFC"      # 배경색

# 2. 커스텀 CSS: 레이아웃 및 디자인 고도화
st.markdown(f"""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * {{ font-family: 'Pretendard', sans-serif; }}
    
    .stApp {{ background-color: {BG_SOFT}; }}
    
    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {{ background-color: {KCIM_DARK}; border-right: 1px solid rgba(255,255,255,0.1); }}
    [data-testid="stSidebar"] .stMarkdown {{ color: white; }}
    
    /* 메인 배너 */
    .main-banner {{
        background: linear-gradient(135deg, {KCIM_DARK} 0%, {KCIM_MEDIUM} 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(25, 61, 82, 0.15);
    }}
    
    /* 가이드 카드 스타일 */
    .guide-card {{
        background: white;
        padding: 1.8rem;
        border-radius: 15px;
        border-top: 6px solid {KCIM_MEDIUM};
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        height: 100%;
        transition: transform 0.2s;
    }}
    .guide-card:hover {{ transform: translateY(-5px); }}
    
    /* 강조 텍스트 */
    .highlight {{ color: {KCIM_MEDIUM}; font-weight: 700; }}
    .law-ref {{ font-size: 0.85rem; color: #64748b; margin-top: 0.5rem; }}
    
    /* 탭 스타일 최적화 */
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: white;
        border-radius: 8px 8px 0 0;
        padding: 10px 25px;
        font-weight: 600;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바: 핵심 정보 및 퀵 메뉴
with st.sidebar:
    st.image("https://www.kcim.co.kr/img/common/logo_w.png", width=150) # Kcim 로고 (URL은 예시)
    st.markdown("### 🏢 경영관리본부\n**디지털 노무사 서비스**")
    st.divider()
    
    st.markdown("#### 📅 2025 법령 시행 캘린더")
    st.success("**01.01 시행**\n- 육아휴직 급여 인상\n- 사후지급금 폐지")
    st.warning("**02.23 시행**\n- 기간 연장 (1.5년)\n- 배우자 휴가 20일\n- 단축 자녀연령 초6")
    
    st.divider()
    st.markdown("#### ☎️ 내부 지원 센터")
    st.write("• 인사팀(본사): 내선 102")
    st.write("• 노무 상담: 내선 105")

# 4. 메인 대시보드 상단
st.markdown(f"""
    <div class="main-banner">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">⚖️ 2025 육아지원제도 스마트 가이드</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">전문 노무사가 검토한 고용노동부 최신 개정안 지침</p>
    </div>
    """, unsafe_allow_html=True)

# 5. 탭 메뉴: 정보 구조화
tab1, tab2, tab3 = st.tabs(["📑 제도 핵심 요약", "💰 급여 시뮬레이션", "🤖 AI 전문 상담"])

with tab1:
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="guide-card">
                <h3 style="color:{KCIM_DARK};">🤱 육아기 지원 <small style="font-size:0.6em; color:gray;">(25.02.23 시행)</small></h3>
                <p>• <b>육아기 근로시간 단축 자녀 연령:</b> <span class="highlight">만 12세(초6) 이하</span>로 확대</p>
                <p>• <b>단축 기간:</b> 최대 <span class="highlight">3년</span> (휴직 미사용분 가산)</p>
                <p>• <b>육아휴직 기간:</b> 최대 <span class="highlight">1.5년</span> (부모 각 3개월 사용 시)</p>
                <p class="law-ref">※ 근거: 남녀고용평등법 제19조 및 제19조의2</p>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="guide-card" style="border-top-color:{KCIM_DARK};">
                <h3 style="color:{KCIM_DARK};">🤰 임신·출산기 보호 <small style="font-size:0.6em; color:gray;">(25.02.23 시행)</small></h3>
                <p>• <b>배우자 출산휴가:</b> <span class="highlight">20일</span> (분할 사용 4회 확대)</p>
                <p>• <b>임신기 근로시간 단축:</b> 12주 이내 ~ <span class="highlight">32주 이후</span></p>
                <p>• <b>난임치료휴가:</b> 연간 6일 (유급 2일 포함)</p>
                <p class="law-ref">※ 근거: 근로기준법 제74조</p>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.write("")
    st.markdown(f"""
        <div class="guide-card">
            <h3 style="text-align:center; color:{KCIM_DARK};">💳 2025 육아휴직 급여 체계 (1.1 시행)</h3>
            <div style="background:{BG_SOFT}; padding:1.5rem; border-radius:10px; margin:1rem 0;">
                <p>• <b>1~3개월:</b> 월 상한 <span class="highlight">250만 원</span> (통상임금 100%)</p>
                <p>• <b>4~6개월:</b> 월 상한 <span class="highlight">200만 원</span> (통상임금 100%)</p>
                <p>• <b>7~12개월:</b> 월 상한 <span class="highlight">160만 원</span> (통상임금 80%)</p>
            </div>
            <p style="text-align:center; font-weight:bold; color:red;">[핵심 변경] 사후지급금(25%) 폐지 → 휴직 중 전액 지급</p>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.write("")
    st.markdown(f"### 🤖 '든든매니저' 전문 노무 상담")
    st.caption("고용노동부 최신 지침과 법령을 기반으로 답변하는 전문 페르소나입니다.")

    # 오류 최적화: OpenAI 클라이언트 초기화 및 메시지 관리
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": f"""너는 Kcim 경영관리본부 소속의 '전문 노무사'야. 
            반드시 2025년 개정된 최신 법령에 근거하여 답변해. 

            [노무사 상담 핵심 원칙]
            1. 육아기 근로시간 단축 자녀 연령: **만 12세 또는 초등학교 6학년** 이하 (가장 중요한 변경사항).
            2. 육아기 단축 기간: 최대 **3년** 가능.
            3. 육아휴직 기간: 부모 모두 3개월 이상 사용 시 최대 **1.5년** 연장.
            4. 급여 상한: 1-3개월(250만), 4-6개월(200만), 7개월 이후(160만). 사후지급금은 폐지됨.
            5. 배우자 휴가: **20일**, 120일 이내 **4회(분할 3회)** 사용 가능.
            
            사용자에게 전문적이면서도 따뜻한 어조로 법률적 신뢰감을 제공해줘."""}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("노무사에게 질문하세요 (예: 육아기 단축근무 자녀 연령이 어떻게 바뀌나요?)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"상담 연결에 실패했습니다. (Error: {str(e)})")
