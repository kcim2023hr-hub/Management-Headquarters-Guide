import streamlit as st
from openai import OpenAI
import datetime

# 1. 페이지 설정
st.set_page_config(
    page_title="경영관리본부 육아지원 가이드",
    page_icon="🍼",
    layout="wide"
)

# [색상 팔레트 세팅]
NAVY = "#002060"     # 메인: 신뢰감 (네이비)
BLUE = "#0050ef"     # 포인트: 활력 (브라이트 블루)
SOFT_BLUE = "#f0f4ff" # 배경: 편안함 (연한 블루그레이)
TEXT_GRAY = "#454545" # 본문: 가독성 (짙은 회색)

# 2. 커스텀 CSS (3가지 톤의 조화)
st.markdown(f"""
    <style>
    /* 전체 배경 및 폰트 */
    .stApp {{ background-color: #ffffff; }}
    h1, h2, h3 {{ color: {NAVY}; font-family: 'Pretendard', sans-serif; }}
    p, li {{ color: {TEXT_GRAY}; font-size: 1.05rem; line-height: 1.6; }}

    /* 사이드바 커스텀 */
    [data-testid="stSidebar"] {{
        background-color: {NAVY};
    }}
    [data-testid="stSidebar"] * {{ color: white !important; }}

    /* 상단 메인 배너: 네이비와 블루의 그라데이션으로 편안함 부여 */
    .main-banner {{
        background: linear-gradient(135deg, {NAVY} 0%, {BLUE} 100%);
        padding: 50px 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 40px;
        box-shadow: 0 10px 20px rgba(0,32,96,0.1);
    }}

    /* 안내 카드: 화이트 배경에 소프트 블루 보더로 깨끗한 느낌 */
    .info-card {{
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid {SOFT_BLUE};
        border-top: 5px solid {BLUE};
        box-shadow: 0 6px 15px rgba(0,0,0,0.03);
        height: 100%;
        transition: transform 0.2s;
    }}
    .info-card:hover {{
        transform: translateY(-5px);
    }}

    /* 탭 디자인: 세련된 블루 톤 적용 */
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {SOFT_BLUE};
        border-radius: 8px 8px 0 0;
        padding: 12px 25px;
        color: {NAVY};
        font-weight: 600;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background-color: {BLUE} !important;
        color: white !important;
    }}

    /* 강조 박스 */
    .highlight-box {{
        background-color: {SOFT_BLUE};
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid {BLUE};
        margin: 10px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 (핵심 요약)
with st.sidebar:
    st.markdown(f"<div style='text-align:center; padding:20px;'><h2 style='color:white;'>🏢 경영관리본부</h2><p style='color:#cbdcf7;'>육아지원 스마트 가이드</p></div>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### 📅 시행 일정 요약")
    st.info("**25.01.01**\n- 육아휴직 급여 인상\n- 사후지급금 폐지")
    st.warning("**25.02.23**\n- 육아휴직 1.5년 연장\n- 배우자 출산휴가 20일")
    
    st.divider()
    st.markdown("### 📞 담당자 안내")
    st.write("• 제도 문의: 인사팀 (102)")
    st.write("• 시스템 문의: IT팀 (505)")

# 4. 메인 화면 배너
st.markdown(f"""
    <div class="main-banner">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">🌸 육아와 업무의 행복한 균형</h1>
        <p style="color: #e0eaff; margin-top: 15px; font-size: 1.2rem; font-weight: 300;">경영관리본부는 임직원의 소중한 가정을 응원합니다.</p>
    </div>
    """, unsafe_allow_html=True)

# 5. 콘텐츠 영역 (3개 탭 구성)
tab_list = ["📍 단계별 제도", "📝 2025 개편 핵심", "🤖 든든매니저 상담"]
tabs = st.tabs(tab_list)

with tabs[0]:
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="info-card">
                <h3 style="color:{BLUE};">🤰 임신기·출산기</h3>
                <div class="highlight-box"><b>임신기 근로시간 단축</b><br>12주 이내 ~ 32주 이후 (2.23 시행)</div>
                <ul>
                    <li>배우자 출산휴가 20일 (4회 분할 가능)</li>
                    <li>난임치료휴가 유급 2일 포함 총 6일</li>
                    <li>미숙아 출산 시 출산휴가 100일</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="info-card">
                <h3 style="color:{BLUE};">🤱 육아기</h3>
                <div class="highlight-box"><b>육아휴직 기간 연장</b><br>최대 1년 → 1.5년 (부모 모두 3개월 사용 시)</div>
                <ul>
                    <li>육아기 근로시간 단축 초6(만12세)까지</li>
                    <li>단축근무 급여 상한 220만원 상향</li>
                    <li>육아휴직 분할 사용 3회로 확대</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

with tabs[1]:
    st.write("")
    st.markdown(f"""
        <div class="info-card">
            <h3 style="color:{NAVY}; text-align:center;">💰 2025년 육아휴직 급여 개편 안내</h3>
            <p style="text-align:center; color:{TEXT_GRAY};">2025년 1월 1일부터 육아휴직 급여가 대폭 인상되며 사후지급금이 폐지됩니다.</p>
            <table style="width:100%; border-collapse: collapse; margin-top:20px;">
                <tr style="background-color:{SOFT_BLUE}; border-bottom: 2px solid {BLUE};">
                    <th style="padding:15px; text-align:left;">구분</th>
                    <th style="padding:15px; text-align:left;">기존</th>
                    <th style="padding:15px; text-align:left; color:{BLUE};">2025년 개편</th>
                </tr>
                <tr style="border-bottom:1px solid #eee;">
                    <td style="padding:15px;">1~3개월</td>
                    <td style="padding:15px;">월 150만원</td>
                    <td style="padding:15px; font-weight:bold;">월 250만원</td>
                </tr>
                <tr style="border-bottom:1px solid #eee;">
                    <td style="padding:15px;">4~6개월</td>
                    <td style="padding:15px;">월 150만원</td>
                    <td style="padding:15px; font-weight:bold;">월 200만원</td>
                </tr>
                <tr>
                    <td style="padding:15px;">7개월 이후</td>
                    <td style="padding:15px;">월 150만원</td>
                    <td style="padding:15px; font-weight:bold;">월 160만원</td>
                </tr>
            </table>
            <p style="margin-top:15px; font-size:0.9rem; color:red;">※ 사후지급금(25%) 없이 휴직 기간 중 100% 지급됩니다.</p>
        </div>
        """, unsafe_allow_html=True)

with tabs[2]:
    st.write("")
    st.markdown(f"### 🤖 '든든매니저'에게 물어보세요")
    st.caption("고용노동부 '2025 달라지는 육아지원제도' 가이드를 기반으로 답변합니다.")

    # 6. AI 챗봇 로직
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "너는 경영관리본부의 전문 상담사 '든든매니저'야. 네이비와 블루 톤의 신뢰감 있는 말투로 2025년 개편된 육아지원제도를 친절하게 안내해줘."}
        ]

    # 채팅 UI는 기본 Streamlit 컴포넌트 사용 (가독성 최우선)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("예: 육아휴직 급여 인상에 대해 알려줘"):
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
            except:
                st.error("API 키를 확인해주세요.")
