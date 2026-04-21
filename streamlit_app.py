import streamlit as st
from openai import OpenAI
import datetime

# 1. 페이지 설정 및 디자인 고도화
st.set_page_config(
    page_title="경영관리본부 육아지원 가이드",
    page_icon="🍼",
    layout="wide"
)

# 커스텀 CSS: 이미지의 부드러운 톤과 전문적인 레이아웃 재현
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 10px 10px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .guide-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #ff4b6b;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .stat-box {
        text-align: center;
        padding: 10px;
        background-color: #fff0f3;
        border-radius: 10px;
        border: 1px solid #ffccd5;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 사이드바: 퀵 인포 및 시행일정
with st.sidebar:
    st.markdown("## 🏢 경영관리본부\n**육아지원 스마트 센터**")
    st.write(f"📅 오늘 날짜: {datetime.date.today()}")
    st.divider()
    
    st.markdown("### 🔔 2025년 주요 시행일")
    st.error("**1월 1일 시행**\n- 휴직급여 인상 (최대 250만)\n- 사후지급금 폐지")
    st.warning("**2월 23일 시행**\n- 휴직기간 연장 (1.5년)\n- 배우자 출산휴가 (20일)\n- 단축근무 자녀연령 확대 (초6)")
    
    st.divider()
    st.info("💡 **문의처**\n인사총무팀: 내선 102\n고용노동부 콜센터: 1350")

# 3. 메인 상단 배너
st.markdown("""
    <div style="background: linear-gradient(to right, #ffafbd, #ffc3a0); padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 25px;">
        <h1 style="color: white; margin: 0;">💖 스마트 육아지원제도 가이드</h1>
        <p style="color: white; opacity: 0.9; font-size: 18px;">2025년 달라지는 고용노동부 지침 100% 반영</p>
    </div>
    """, unsafe_allow_html=True)

# 4. 제도별 상세 안내 (Tabs 활용)
tab1, tab2, tab3, tab4 = st.tabs(["🤰 임신기", "👶 출산기", "🤱 육아기", "❓ FAQ"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="guide-card">
                <h3>임신기 근로시간 단축 (2.23 시행)</h3>
                <ul>
                    <li><b>확대:</b> 12주 이내 ~ 32주 이후 (기존 36주) [cite: 13, 76]</li>
                    <li><b>고위험 임신부:</b> 임신 전 기간 사용 가능 [cite: 13, 77]</li>
                    <li><b>임금:</b> 근로시간 단축을 이유로 임금 삭감 불가</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="guide-card" style="border-left-color: #4b6bff;">
                <h3>난임치료휴가 확대 (2.23 시행)</h3>
                <ul>
                    <li><b>기간:</b> 연간 6일 (기존 3일) [cite: 15, 85]</li>
                    <li><b>유급:</b> 최초 2일 유급 (기존 1일) [cite: 16, 85]</li>
                    <li><b>비밀유지:</b> 사업주의 비밀유지 의무 신설 [cite: 86]</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
        <div class="guide-card">
            <h3>배우자 출산휴가 (2.23 시행)</h3>
            <p>신생아와 산모를 충분히 돌볼 수 있도록 대폭 확대됩니다.</p>
            <div style="display: flex; justify-content: space-around;">
                <div class="stat-box"><b>휴가 기간</b><br><span style="font-size:20px; color:#ff4b6b;">20일</span> (기존 10일) [cite: 27, 103]</div>
                <div class="stat-box"><b>분할 사용</b><br><span style="font-size:20px; color:#ff4b6b;">3회</span> (총 4회 분할) [cite: 30, 106]</div>
                <div class="stat-box"><b>급여 지원</b><br><span style="font-size:20px; color:#ff4b6b;">20일 전체</span> (중소기업) [cite: 29, 107]</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
            <div class="guide-card">
                <h3>육아휴직 급여 인상 (1.1 시행)</h3>
                <ul>
                    <li><b>1~3개월:</b> 월 상한 250만원 [cite: 38, 43, 113]</li>
                    <li><b>4~6개월:</b> 월 상한 200만원 [cite: 39, 113]</li>
                    <li><b>7개월~:</b> 월 상한 160만원 [cite: 40, 113]</li>
                    <li><b>사후지급금 폐지:</b> 휴직 중 전액 지급 [cite: 41, 113, 257]</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
            <div class="guide-card" style="border-left-color: #4caf50;">
                <h3>육아기 근로시간 단축 (2.23 시행)</h3>
                <ul>
                    <li><b>대상:</b> 만 12세 또는 초6 이하 [cite: 48, 118, 119]</li>
                    <li><b>기간:</b> 최대 3년 (휴직 미사용분 가산) [cite: 45, 118, 119]</li>
                    <li><b>급여:</b> 기준금액 상한 220만원으로 상향 [cite: 119, 259]</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

with tab4:
    st.markdown("### 💡 자주 묻는 질문 (FAQ)")
    with st.expander("Q. 이미 육아휴직 중인데 인상된 급여를 받을 수 있나요?"):
        st.write("A. 네, 가능합니다. 2025년 1월 1일 이후 사용하는 기간에 대해서는 인상된 급여 기준이 적용됩니다. [cite: 280, 281, 282]")
    with st.expander("Q. 육아휴직 1년 6개월 연장 조건은 무엇인가요?"):
        st.write("A. 부모가 각각 육아휴직을 3개월 이상 사용했거나, 한부모 또는 중증장애아동 부모인 경우에 가능합니다. [cite: 35, 36, 111, 308]")

# 5. AI 챗봇 섹션
st.divider()
st.markdown("### 🤖 육아지원 AI 어시스턴트 '든든매니저'")
st.caption("고용노동부 2025 개편 가이드북 데이터를 기반으로 답변합니다.")

# API 설정 및 페르소나 주입
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("API Key 설정이 필요합니다 (Settings > Secrets).")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """너는 경영관리본부의 '든든매니저'야. 
        사용자에게 2025년 개편된 육아지원제도를 안내하는 전문가이며, 반드시 제공된 고용노동부 PDF 가이드북 내용에 기반해 답변해야 해.
        
        [주요 규칙]
        1. 2025.1.1 시행과 2025.2.23 시행 제도를 엄격히 구분해서 안내할 것.
        2. 육아휴직 급여 인상(최대 250만)과 기간 연장(1.5년) 조건을 정확히 설명할 것.
        3. 배우자 출산휴가가 20일로 늘어난 점과 4회 분할 가능함을 강조할 것.
        4. 말투는 부드럽고 따뜻하게 하되, 수치는 정확하게 전달할 것."""}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("궁금한 제도를 입력하세요 (예: 육아휴직 급여 인상 얼마인가요?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        ans = response.choices[0].message.content
        st.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
