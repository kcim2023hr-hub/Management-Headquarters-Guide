import streamlit as st
from openai import OpenAI
import datetime

# 1. 페이지 설정 및 브랜드 컬러 (Kcim 로고 가이드라인 반영)
st.set_page_config(
    page_title="경영관리본부 육아지원 가이드",
    page_icon="🏢",
    layout="wide"
)

# Kcim 공식 컬러 팔레트
KCIM_DARK = "#193D52"    # PANTONE 2153C (Main Navy)
KCIM_MEDIUM = "#00A8C0"  # PANTONE 2201C (Point Cyan)
KCIM_LIGHT = "#8CCEE7"   # PANTONE 297C (Soft Blue)

# 2. 커스텀 CSS (전문 노무사 스타일의 신뢰감 있는 레이아웃)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #F7FBFE; }}
    [data-testid="stSidebar"] {{ background-color: {KCIM_DARK}; }}
    [data-testid="stSidebar"] * {{ color: white !important; }}
    .main-banner {{
        background: linear-gradient(135deg, {KCIM_DARK} 0%, {KCIM_MEDIUM} 100%);
        padding: 40px; border-radius: 15px; text-align: center; color: white; margin-bottom: 30px;
    }}
    .info-card {{
        background-color: white; padding: 25px; border-radius: 12px;
        border: 1px solid {KCIM_LIGHT}; border-top: 5px solid {KCIM_MEDIUM};
        box-shadow: 0 4px 10px rgba(0,0,0,0.03); height: 100%;
    }}
    .status-badge {{
        background-color: {KCIM_LIGHT}; color: {KCIM_DARK};
        padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 (법규 시행 일정 및 안내)
with st.sidebar:
    st.markdown(f"## Kcim 경영관리본부")
    st.markdown("<p style='opacity:0.8;'>전문 노무사 상담 지원 서비스</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### 📅 주요 법령 시행일")
    st.info("**2025.01.01 시행**\n- 육아휴직 급여 인상\n- 사후지급금 전면 폐지")
    st.warning("**2025.02.23 시행**\n- 휴직 기간 1.5년 연장\n- 배우자 휴가 20일 확대\n- 단축근무 자녀연령 초6 확대")
    st.divider()
    st.write("📞 사내 노무 상담: 내선 102")

# 4. 메인 배너
st.markdown(f"""
    <div class="main-banner">
        <h1>💼 2025 육아지원제도 전문 가이드</h1>
        <p style="color: {KCIM_LIGHT}; font-size: 1.2rem;">고용노동부 최신 개정 법령 및 지침 100% 반영</p>
    </div>
    """, unsafe_allow_html=True)

# 5. 콘텐츠 영역 (노무사 관점의 탭 구성)
tabs = st.tabs(["📑 핵심 개정 요약", "💰 급여 및 수당 체계", "🤖 전문 노무 상담(AI)"])

with tabs[0]:
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="info-card">
                <h3>🤰 임신·출산기 보호 <span class="status-badge">2.23 시행</span></h3>
                <ul>
                    <li><b>배우자 출산휴가:</b> <span class='highlight'>20일</span> 확대 (총 4회 분할 사용 가능) [cite: 27, 103, 106]</li>
                    <li><b>임신기 근로시간 단축:</b> 임신 후 12주 이내 ~ <span class='highlight'>32주 이후</span>로 확대 [cite: 13, 76]</li>
                    <li><b>난임치료휴가:</b> 연간 6일(유급 2일)로 대폭 확대 [cite: 82, 85]</li>
                    <li><b>유산·사산휴가:</b> 11주 이내 유산 시 <span class='highlight'>10일</span> 부여 [cite: 96]</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="info-card">
                <h3>🤱 육아기 지원 강화 <span class="status-badge">1.1 / 2.23 시행</span></h3>
                <ul>
                    <li><b>육아휴직 기간:</b> 부모 각 3개월 사용 시 <span class='highlight'>최대 1.5년</span> [cite: 35, 111]</li>
                    <li><b>육아기 근로시간 단축:</b> 대상 자녀 <span class='highlight'>만 12세(초6)</span> 이하로 확대 [cite: 48, 118]</li>
                    <li><b>단축 기간:</b> 휴직 미사용분 포함 최대 <span class='highlight'>3년</span>까지 가능 [cite: 45, 119]</li>
                    <li><b>분할 사용:</b> 육아휴직 <span class='highlight'>3회(4번)</span> 분할 가능 [cite: 113]</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

with tabs[1]:
    st.write("")
    st.markdown(f"""
        <div class="info-card">
            <h3 style="text-align:center; color:{KCIM_DARK};">💰 2025년 육아휴직 급여 지급 기준 (1.1 시행)</h3>
            <table style="width:100%; border-collapse: collapse; margin-top:20px; border-radius:10px; overflow:hidden;">
                <tr style="background-color:{KCIM_DARK}; color:white;">
                    <th style="padding:15px; text-align:left;">휴직 기간</th>
                    <th style="padding:15px; text-align:left;">상한액 (통상임금 100%/80%)</th>
                    <th style="padding:15px; text-align:left;">비고</th>
                </tr>
                <tr style="border-bottom:1px solid #eee;">
                    <td style="padding:15px;">1 ~ 3개월</td>
                    <td style="padding:15px; font-weight:bold; color:{KCIM_MEDIUM};">월 250만원</td>
                    <td style="padding:15px;">사후지급금 폐지</td>
                </tr>
                <tr style="border-bottom:1px solid #eee;">
                    <td style="padding:15px;">4 ~ 6개월</td>
                    <td style="padding:15px; font-weight:bold; color:{KCIM_MEDIUM};">월 200만원</td>
                    <td style="padding:15px;">[cite: 38, 39, 113]</td>
                </tr>
                <tr>
                    <td style="padding:15px;">7 ~ 12개월</td>
                    <td style="padding:15px; font-weight:bold; color:{KCIM_MEDIUM};">월 160만원</td>
                    <td style="padding:15px;">[cite: 40, 113]</td>
                </tr>
            </table>
            <p style="color:red; font-size:0.9rem; margin-top:15px; text-align:center;">※ 2025년 이후 사용분부터는 <b>사후지급금(25%) 없이 휴직 기간 중 전액 지급</b>됩니다. [cite: 41, 113, 257]</p>
        </div>
        """, unsafe_allow_html=True)

with tabs[2]:
    st.write("")
    st.markdown(f"### 🤖 전문 노무 상담 AI '든든매니저'")
    st.info("본 AI는 고용노동부 2025 개편 가이드 및 관계 법령(남녀고용평등법 등)을 학습한 전문 노무사 페르소나를 가지고 있습니다.")
    
    # 6. AI 챗봇 설정 (노무사 페르소나 및 최신 법령 강제 주입)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": f"""너는 Kcim 경영관리본부의 '전문 노무사' 어시스턴트야. 
            반드시 2025년 개정된 최신 법령(남녀고용평등법, 고용보험법 시행령)에 근거하여 답변해.

            [전문 노무사 지식 베이스]
            1. 육아기 근로시간 단축: 대상 자녀 연령이 **만 12세 또는 초등학교 6학년** 이하로 확대됨. [cite: 48, 118]
            2. 육아기 근로시간 단축 기간: 최대 **3년**까지 확대됨. [cite: 45, 119]
            3. 육아휴직 기간 연장: 부모가 각각 3개월 이상 사용 시 최대 **1년 6개월**로 확대됨. [cite: 35, 111, 306]
            4. 육아휴직 급여: 1~3개월(250만), 4~6개월(200만), 7개월 이후(160만) 상한액 적용. [cite: 113]
            5. 사후지급금: 2025년 사용분부터 **전면 폐지**되어 휴직 중 100% 지급됨. [cite: 41, 257]
            6. 배우자 출산휴가: **20일**로 확대, 출산일로부터 120일 내 **3회 분할(총 4회 사용)** 가능. [cite: 103, 105, 106]
            7. 임신기 단축: 임신 후 12주 이내 및 **32주 이후**부터 사용 가능. [cite: 13, 76]

            답변 시 "개정된 법령에 따르면"이라는 표현을 사용하여 신뢰감을 주고, 정확한 기간과 금액을 명시해줘."""}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("노무 상담 질문을 입력하세요 (예: 육아기 단축근무 자녀 연령 기준은?)"):
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
                res = response.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("API Key 설정이 필요합니다 (Secrets).")
