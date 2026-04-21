import streamlit as st
from openai import OpenAI
import datetime

# 1. 페이지 설정 및 디자인 고도화
st.set_page_config(
    page_title="경영관리본부 육아지원 가이드",
    page_icon="🍼",
    layout="wide"
)

# 커스텀 CSS
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
    st.error("**1월 1일 시행**\n- 육아휴직 급여 인상 (최대 250만) [cite: 38, 43, 113]\n- 사후지급금 폐지 [cite: 41, 113, 257]")
    st.warning("**2월 23일 시행**\n- 육아휴직 기간 연장 (최대 1.5년) [cite: 35, 113, 263]\n- 배우자 출산휴가 (20일) [cite: 27, 103, 265]\n- 육아기 근로시간 단축 자녀연령 확대 (초6) [cite: 48, 118, 119]")
    
    st.divider()
    st.info("💡 **문의처**\n인사총무팀: 내선 102\n고용노동부 콜센터: 1350 [cite: 520]")

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
                <h3>임신기 근로시간 단축 (2.23 시행) [cite: 267]</h3>
                <ul>
                    <li><b>확대:</b> 임신 후 12주 이내, 32주 이후로 사용 기간 확대 (기존 36주 이후) [cite: 13, 75, 76]</li>
                    <li><b>고위험 임신부:</b> 의사 진단 시 임신 전 기간 사용 가능 [cite: 13, 77]</li>
                    <li><b>특징:</b> 1일 최대 2시간 단축 가능하며 임금 삭감 불가 [cite: 74]</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="guide-card" style="border-left-color: #4b6bff;">
                <h3>난임치료휴가 확대 (2.23 시행) [cite: 264]</h3>
                <ul>
                    <li><b>기간:</b> 연간 6일로 확대 (기존 3일) [cite: 15, 82, 85]</li>
                    <li><b>유급:</b> 최초 2일 유급 (기존 1일) [cite: 16, 85]</li>
                    <li><b>비밀유지:</b> 사업주의 난임치료 정보 비밀유지 의무 신설 [cite: 86, 255]</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
        <div class="guide-card">
            <h3>배우자 출산휴가 (2.23 시행) [cite: 265]</h3>
            <p>산모와 신생아를 충분히 돌볼 수 있도록 휴가 기간 및 급여 지원이 확대됩니다. [cite: 100]</p>
            <div style="display: flex; justify-content: space-around;">
                <div class="stat-box"><b>휴가 기간</b><br><span style="font-size:20px; color:#ff4b6b;">20일(유급)</span><br>(기존 10일) [cite: 27, 103]</div>
                <div class="stat-box"><b>분할 사용</b><br><span style="font-size:20px; color:#ff4b6b;">3회 분할</span><br>(총 4회 사용) [cite: 30, 106]</div>
                <div class="stat-box"><b>사용 기한</b><br><span style="font-size:20px; color:#ff4b6b;">120일 이내</span><br>(출산일 기준) [cite: 105]</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="guide-card" style="border-left-color: #9c27b0;">
            <h3>출산전후휴가 확대 (2.23 시행) [cite: 268]</h3>
            <ul>
                <li><b>미숙아 출산:</b> 휴가 기간이 100일로 확대 (기존 90일) [cite: 18, 89, 93]</li>
                <li><b>유산·사산휴가:</b> 임신 11주 이내 유산·사산 시 휴가 기간 10일로 확대 (기존 5일) [cite: 96, 462]</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
            <div class="guide-card">
                <h3>육아휴직 급여 인상 (1.1 시행) [cite: 257]</h3>
                <ul>
                    <li><b>1~3개월:</b> 월 상한 250만원 [cite: 38, 43, 113, 287]</li>
                    <li><b>4~6개월:</b> 월 상한 200만원 [cite: 39, 113, 288]</li>
                    <li><b>7개월~12개월:</b> 월 상한 160만원 [cite: 40, 113, 289]</li>
                    <li><b>사후지급금 폐지:</b> 육아휴직 중 전액 지급으로 개편 [cite: 41, 113, 257]</li>
                    <li><b>기간 연장:</b> 부모 각각 3개월 이상 사용 시 최대 1.5년으로 연장 (2.23 시행) [cite: 35, 113, 263, 306]</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
            <div class="guide-card" style="border-left-color: #4caf50;">
                <h3>육아기 근로시간 단축 (2.23 시행) [cite: 266]</h3>
                <ul>
                    <li><b>대상 자녀:</b> 만 12세 이하 또는 초등학교 6학년 이하 [cite: 48, 118, 119, 274]</li>
                    <li><b>사용 기간:</b> 최대 3년까지 사용 가능 (1년 + 육아휴직 미사용분 × 2) [cite: 45, 46, 119]</li>
                    <li><b>최소 사용:</b> 1개월 단위로 사용 가능 (기존 3개월) [cite: 50, 119]</li>
                    <li><b>급여 지원:</b> 매주 최초 10시간 단축분 기준금액 상한 220만원으로 상향 [cite: 119, 259]</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

with tab4:
    st.markdown("### 💡 자주 묻는 질문 (FAQ) [cite: 4]")
    with st.expander("Q. 이미 육아휴직 중인데 인상된 급여를 받을 수 있나요?"):
        st.write("A. 네, 적용됩니다. 제도 개편 시행일('25.1.1.) 이전에 육아휴직을 시작했더라도 시행일 이후 '사용 기간'에 대해서는 인상된 급여를 받을 수 있습니다. [cite: 280, 281, 282]")
    with st.expander("Q. 육아휴직 기간 연장(1.5년)을 위한 조건은 무엇인가요?"):
        st.write("A. 부모가 각각 육아휴직을 3개월 이상 사용한 경우 각각 6개월씩 기간이 연장됩니다. 또한 한부모 가족이거나 중증 장애아동의 부모인 경우에도 6개월 연장 혜택을 받을 수 있습니다. [cite: 35, 36, 111, 308, 332]")
    with st.expander("Q. 육아기 근로시간 단축 대상 자녀 연령이 육아휴직에도 적용되나요?"):
        st.write("A. 아니요. 육아기 근로시간 단축 대상은 만 12세(초6) 이하로 확대되지만, 육아휴직은 기존과 동일하게 만 8세(초2) 이하 자녀를 대상으로 합니다. [cite: 274, 275]")

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
        1. 2025.1.1 시행(급여 인상, 사후지급금 폐지 등)과 2025.2.23 시행(기간 연장, 배우자 출산휴가 확대 등) 제도를 엄격히 구분해서 안내할 것.
        2. 육아휴직 급여 인상 상한액(1~3개월 250만, 4~6개월 200만, 7개월 이후 160만)을 정확히 전달할 것.
        3. 육아휴직 기간 연장(1년→1.5년)은 부모 모두 3개월 이상 사용 시에만 적용됨을 명시할 것.
        4. 배우자 출산휴가가 20일로 늘어나고 120일 이내에 3회 분할(총 4회 사용) 가능함을 안내할 것.
        5. 육아기 근로시간 단축은 만 12세(초6) 이하 자녀까지 확대되나, 육아휴직은 만 8세(초2) 기준이 유지됨을 주의해서 답변할 것."""}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("궁금한 제도를 입력하세요 (예: 배우자 출산휴가는 며칠인가요?)"):
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
