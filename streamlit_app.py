import streamlit as st
from openai import OpenAI
import datetime

# 1. 페이지 설정 및 브랜드 컬러 정의
st.set_page_config(
    page_title="경영관리본부 육아지원 가이드",
    page_icon="🏢",
    layout="wide"
)

# 브랜드 컬러 설정 (보내주신 이미지의 네이비/블루 반영)
PRIMARY_COLOR = "#002060"  # 짙은 네이비
SECONDARY_COLOR = "#e7efff" # 연한 블루 배경
ACCENT_COLOR = "#0050ef"    # 포인트 블루

# 2. 커스텀 CSS: 신뢰감을 주는 경영관리본부 톤앤매너
st.markdown(f"""
    <style>
    /* 기본 배경색 */
    .stApp {{ background-color: #ffffff; }}
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {{
        background-color: {PRIMARY_COLOR};
        color: white;
    }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    
    /* 카드 스타일 */
    .guide-card {{
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        border-top: 4px solid {ACCENT_COLOR};
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        height: 100%;
    }}
    
    /* 메인 타이틀 배너 */
    .main-banner {{
        background-color: {PRIMARY_COLOR};
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }}
    
    /* 탭 디자인 */
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #f0f2f6;
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background-color: {ACCENT_COLOR} !important;
        color: white !important;
    }}
    
    /* 강조 텍스트 */
    .highlight {{ color: {ACCENT_COLOR}; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 구성
with st.sidebar:
    st.markdown(f"<h2 style='text-align:center;'>🏢 경영관리본부</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.8;'>Smart HR Support</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### 📢 2025 핵심 개편")
    st.info("**1월 1일 시행**\n- 휴직급여 최대 250만원\n- 사후지급금 완전 폐지")
    st.warning("**2월 23일 시행**\n- 육아휴직 1년 6개월 연장\n- 배우자 출산휴가 20일")
    
    st.divider()
    st.markdown("### 📞 Contact")
    st.write("• HR팀: 내선 806")
    st.write("• IT지원: 내선 850")

# 4. 메인 화면 상단 배너
st.markdown(f"""
    <div class="main-banner">
        <h1 style="color: white; margin: 0;">2025 육아지원제도 스마트 가이드</h1>
        <p style="color: #cbdcf7; margin-top: 10px; font-size: 1.1rem;">경영관리본부 임직원을 위한 고용노동부 최신 지침 100% 반영</p>
    </div>
    """, unsafe_allow_html=True)

# 5. 제도 상세 안내 (Tabs)
tabs = st.tabs(["📑 임신기", "👶 출산기", "🤱 육아기", "💬 FAQ"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="guide-card">
            <h3>임신기 근로시간 단축 <span style='font-size:0.8rem; color:gray;'>(2.23 시행)</span></h3>
            <p>• <b>시기:</b> 12주 이내 ~ 32주 이후 (4주 확대)</p>
            <p>• <b>대상:</b> 전 임신부 (고위험군 전 기간)</p>
            <p class="highlight">※ 임금 삭감 없이 하루 2시간 단축</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="guide-card">
            <h3>난임치료휴가 확대 <span style='font-size:0.8rem; color:gray;'>(2.23 시행)</span></h3>
            <p>• <b>기간:</b> 연간 6일 (기존 3일)</p>
            <p>• <b>유급:</b> 최초 2일 유급 (기존 1일)</p>
        </div>""", unsafe_allow_html=True)

with tabs[1]:
    st.markdown(f"""<div class="guide-card">
        <h3>배우자 출산휴가 확대 <span style='font-size:0.8rem; color:gray;'>(2.23 시행)</span></h3>
        <p>• <b>휴가기간:</b> <span class="highlight">20일</span> (기존 10일)</p>
        <p>• <b>분할사용:</b> 총 4회 분할 가능</p>
        <p>• <b>청구기한:</b> 출산일로부터 120일 이내</p>
    </div>""", unsafe_allow_html=True)

with tabs[2]:
    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown(f"""<div class="guide-card">
            <h3>육아휴직 급여 인상 <span style='font-size:0.8rem; color:gray;'>(1.1 시행)</span></h3>
            <p>• <b>1~3개월:</b> 월 250만원 상한</p>
            <p>• <b>4~6개월:</b> 월 200만원 상한</p>
            <p>• <b>7개월 이후:</b> 월 160만원 상한</p>
            <p class="highlight">※ 사후지급금 제도 전면 폐지</p>
        </div>""", unsafe_allow_html=True)
    with c_b:
        st.markdown(f"""<div class="guide-card">
            <h3>육아휴직 기간 연장 <span style='font-size:0.8rem; color:gray;'>(2.23 시행)</span></h3>
            <p>• <b>기존:</b> 1년 → <b>개정:</b> <span class="highlight">1년 6개월</span></p>
            <p>• <b>조건:</b> 부모 모두 3개월 이상 육아휴직 사용 시</p>
        </div>""", unsafe_allow_html=True)

with tabs[3]:
    st.markdown("### ❓ 자주 묻는 질문")
    faq = {
        "Q. 육아휴직 중 전직하면 급여는 어떻게 되나요?": "전직 전 사용 기간에 대해서는 개정된 급여가 적용되며, 자세한 고용보험 승계는 인사팀 문의 바랍니다.",
        "Q. 2024년에 시작한 육아휴직도 인상된 급여를 받나요?": "2025년 1월 1일 이후 사용하는 기간에 대해서만 인상된 상한액이 적용됩니다."
    }
    for q, a in faq.items():
        with st.expander(q):
            st.write(a)

# 6. AI 챗봇 섹션 (Primary Color 톤 유지)
st.divider()
st.subheader("🤖 든든매니저 AI 상담")
st.info("2025년 고용노동부 '달라지는 육아지원제도' 가이드북을 학습한 AI입니다.")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("API Key를 Secrets에 설정해주세요.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"""너는 경영관리본부의 전문 상담사 '든든매니저'야. 
        사용자의 질문에 2025년 고용노동부 개정안을 바탕으로 답변해. 
        브랜드 컬러인 네이비와 블루 톤에 어울리는 신뢰감 있고 전문적인 말투를 사용해줘."""}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("질문을 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        full_res = response.choices[0].message.content
        st.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
