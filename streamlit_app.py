# ──────────────────────────────────────────
# 스텝 프로그레스 (클릭 가능한 버튼형, 계산기 모드에서는 숨김)
# ──────────────────────────────────────────
if not is_calc:
    with st.container(key="stepper_wrap_box"):
        with st.container(horizontal=True, gap="small"):
            for i, s in enumerate(STEPS):
                is_done = i in st.session_state.completed_steps
                is_active = i == active_idx
                icon = "✓" if is_done else str(s["id"])
                key_state = "step_active" if is_active else ("step_done" if is_done else "step_todo")
                if st.button(
                    f"{icon}. {s['short']}",
                    key=f"{key_state}_{i}",
                    help=f"STEP {s['id']}. {s['short']}로 이동",
                ):
                    st.session_state.active_step = i
                    st.session_state.mode = "steps"
                    st.rerun()

# ──────────────────────────────────────────
# 상단 컨트롤 행: 계산기 ↔ 가이드 전환 버튼 (항상 우측에 고정 노출)
# ──────────────────────────────────────────
ctrl_spacer, ctrl_btn = st.columns([5.5, 1.4])
with ctrl_btn:
    calc_toggle_label = "📋 가이드로" if is_calc else "📊 계산기"
    if st.button(calc_toggle_label, key="btn_calc", use_container_width=True,
                 type="primary" if is_calc else "secondary"):
        st.session_state.mode = "steps" if is_calc else "calc"
        st.rerun()

# ──────────────────────────────────────────
# 플로팅 액션 버튼 (좌하단: AI 챗봇 열기)
# CSS로 position:fixed 처리되어 레이아웃 흐름에서 완전히 벗어나므로
# block-container에 별도 강제 여백이 필요하지 않습니다.
# ──────────────────────────────────────────
if st.button("💬", key="chat_toggle_btn", help="AI 챗봇 육아지원박사에게 질문하기"):
    st.session_state.chat_open = True
    st.rerun()

# ──────────────────────────────────────────
# 메인 레이아웃 — 메뉴 없이 본문이 항상 전체 폭 사용
# ──────────────────────────────────────────
col_center = st.container()
