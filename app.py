import math

import streamlit as st


st.set_page_config(page_title="피자 분수 실험실", page_icon="🍕", layout="centered")


def pizza_svg(parts: int, colored_parts: int, label: str) -> str:
    center = 130
    radius = 112
    slices = []

    for index in range(parts):
        start_angle = math.radians(-90 + index * 360 / parts)
        end_angle = math.radians(-90 + (index + 1) * 360 / parts)
        start_x = center + radius * math.cos(start_angle)
        start_y = center + radius * math.sin(start_angle)
        end_x = center + radius * math.cos(end_angle)
        end_y = center + radius * math.sin(end_angle)
        fill = "#E87522" if index < colored_parts else "#FFF1D6"

        slices.append(
            f'<path d="M {center} {center} L {start_x:.3f} {start_y:.3f} '
            f'A {radius} {radius} 0 0 1 {end_x:.3f} {end_y:.3f} Z" '
            f'fill="{fill}" stroke="#FFFFFF" stroke-width="2.5"/>'
        )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 260" '
        f'role="img" aria-label="{label}" '
        'style="width:min(100%, 300px);height:auto;display:block;margin:0 auto">'
        f'{"".join(slices)}'
        f'<circle cx="{center}" cy="{center}" r="{radius}" '
        'fill="none" stroke="#71451F" stroke-width="3"/>'
        "</svg>"
    )


def on_pizza_change(side: str) -> None:
    st.session_state["comparison_result"] = None
    parts_key = f"{side}_parts"
    colored_key = f"{side}_colored"
    if parts_key in st.session_state and colored_key in st.session_state:
        st.session_state[colored_key] = min(
            st.session_state[colored_key], st.session_state[parts_key]
        )


def compare_fractions(
    left_colored: int, left_parts: int, right_colored: int, right_parts: int
) -> str:
    left_cross_product = left_colored * right_parts
    right_cross_product = right_colored * left_parts

    if left_cross_product == right_cross_product:
        return "두 피자에서 색칠한 양은 같아요"
    if left_cross_product > right_cross_product:
        return "왼쪽이 더 많아요"
    return "오른쪽이 더 많아요"


st.title("🍕 피자 분수 실험실")
st.write("피자를 나누고 색칠해 보세요. 두 피자에서 색칠한 양은 같을까요?")

st.markdown(
    """
    <style>
    .fraction-display {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        margin: 0.25rem 0 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.session_state.setdefault("comparison_result", None)
st.session_state.setdefault("left_parts", 2)
st.session_state.setdefault("left_colored", 1)
st.session_state.setdefault("right_parts", 8)
st.session_state.setdefault("right_colored", 4)
left_column, right_column = st.columns(2, gap="large")

with left_column:
    st.subheader("왼쪽 피자")
    left_parts = st.slider(
        "몇 등분할까요?",
        min_value=2,
        max_value=12,
        key="left_parts",
        on_change=on_pizza_change,
        args=("left",),
    )
    left_colored = st.slider(
        "몇 조각을 색칠할까요?",
        min_value=0,
        max_value=left_parts,
        key="left_colored",
        on_change=on_pizza_change,
        args=("left",),
    )
    st.markdown(
        pizza_svg(left_parts, left_colored, "왼쪽 피자"),
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="fraction-display">{left_colored}/{left_parts}</div>',
        unsafe_allow_html=True,
    )

with right_column:
    st.subheader("오른쪽 피자")
    right_parts = st.slider(
        "몇 등분할까요?",
        min_value=2,
        max_value=12,
        key="right_parts",
        on_change=on_pizza_change,
        args=("right",),
    )
    right_colored = st.slider(
        "몇 조각을 색칠할까요?",
        min_value=0,
        max_value=right_parts,
        key="right_colored",
        on_change=on_pizza_change,
        args=("right",),
    )
    st.markdown(
        pizza_svg(right_parts, right_colored, "오른쪽 피자"),
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="fraction-display">{right_colored}/{right_parts}</div>',
        unsafe_allow_html=True,
    )

if st.button("비교 결과 보기", type="primary", use_container_width=True):
    st.session_state["comparison_result"] = compare_fractions(
        left_colored, left_parts, right_colored, right_parts
    )

if st.session_state["comparison_result"]:
    st.success(st.session_state["comparison_result"])
