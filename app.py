import math

import streamlit as st


st.set_page_config(
    page_title="피자를 활용해 분수의 크기 비교하기",
    page_icon="🍕",
    layout="centered",
)


def pizza_svg(parts: int, colored_parts: int, label: str) -> str:
    center = 140
    radius = 112
    prefix = "pizza-left" if label == "왼쪽 피자" else "pizza-right"
    slices = []
    toppings = []
    crust_marks = []

    for index in range(parts):
        start_degrees = -90 + index * 360 / parts
        end_degrees = -90 + (index + 1) * 360 / parts
        middle_angle = math.radians((start_degrees + end_degrees) / 2)
        start_angle = math.radians(start_degrees)
        end_angle = math.radians(end_degrees)
        start_x = center + radius * math.cos(start_angle)
        start_y = center + radius * math.sin(start_angle)
        end_x = center + radius * math.cos(end_angle)
        end_y = center + radius * math.sin(end_angle)
        fill = f"url(#{prefix}-orange)" if index < colored_parts else f"url(#{prefix}-cream)"

        slices.append(
            f'<path d="M {center} {center} L {start_x:.3f} {start_y:.3f} '
            f'A {radius} {radius} 0 0 1 {end_x:.3f} {end_y:.3f} Z" '
            f'fill="{fill}" stroke="#FFF8E9" stroke-width="2.5"/>'
        )

        pepperoni_x = center + 70 * math.cos(middle_angle)
        pepperoni_y = center + 70 * math.sin(middle_angle)
        basil_x = center + 43 * math.cos(middle_angle + 0.12)
        basil_y = center + 43 * math.sin(middle_angle + 0.12)
        if index % 3 == 0:
            toppings.append(
                f'<circle cx="{pepperoni_x:.2f}" cy="{pepperoni_y:.2f}" r="7" '
                'fill="#C94F35" stroke="#963622" stroke-width="1.5"/>'
                f'<circle cx="{pepperoni_x - 2.2:.2f}" '
                f'cy="{pepperoni_y - 2.2:.2f}" r="1.8" fill="#F5A17B"/>'
            )
        elif index % 3 == 1:
            toppings.append(
                f'<circle cx="{pepperoni_x:.2f}" cy="{pepperoni_y:.2f}" r="7" '
                'fill="#F4D887" stroke="#477342" stroke-width="3"/>'
                f'<circle cx="{pepperoni_x:.2f}" cy="{pepperoni_y:.2f}" r="2" '
                'fill="#6E984D"/>'
            )
        else:
            toppings.append(
                f'<ellipse cx="{pepperoni_x:.2f}" cy="{pepperoni_y:.2f}" '
                'rx="6.5" ry="4.5" fill="#46332A" stroke="#2D211B" '
                'stroke-width="1"/>'
                f'<ellipse cx="{pepperoni_x:.2f}" cy="{pepperoni_y:.2f}" '
                'rx="2.5" ry="1.5" fill="#F4D887"/>'
            )
        toppings.append(
            f'<ellipse cx="{basil_x:.2f}" cy="{basil_y:.2f}" '
            'rx="3" ry="6" '
            f'transform="rotate({math.degrees(middle_angle):.1f} '
            f'{basil_x:.2f} {basil_y:.2f})" fill="#558044" '
            'stroke="#3E6335" stroke-width="0.8"/>'
        )

    for index in range(16):
        angle = math.radians(-78.75 + index * 22.5)
        mark_x = center + 120 * math.cos(angle)
        mark_y = center + 120 * math.sin(angle)
        crust_marks.append(
            f'<circle cx="{mark_x:.2f}" cy="{mark_y:.2f}" '
            f'r="{1.5 if index % 2 == 0 else 1.1}" fill="#9A552C" opacity="0.7"/>'
        )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 280" '
        f'role="img" aria-label="{label}" '
        'style="width:min(100%, 300px);height:auto;display:block;margin:0 auto">'
        '<defs>'
        f'<radialGradient id="{prefix}-crust" cx="40%" cy="32%" r="75%">'
        '<stop offset="0%" stop-color="#F6D291"/>'
        '<stop offset="72%" stop-color="#D89149"/>'
        '<stop offset="100%" stop-color="#A9572D"/>'
        '</radialGradient>'
        f'<linearGradient id="{prefix}-cheese" x1="15%" y1="0%" x2="85%" y2="100%">'
        '<stop offset="0%" stop-color="#FFE9A8"/>'
        '<stop offset="100%" stop-color="#E9B856"/>'
        '</linearGradient>'
        f'<radialGradient id="{prefix}-orange" cx="40%" cy="30%" r="85%">'
        '<stop offset="0%" stop-color="#F3913B"/>'
        '<stop offset="100%" stop-color="#D85A1B"/>'
        '</radialGradient>'
        f'<radialGradient id="{prefix}-cream" cx="40%" cy="30%" r="85%">'
        '<stop offset="0%" stop-color="#FFF8E7"/>'
        '<stop offset="100%" stop-color="#F0D8A7"/>'
        '</radialGradient>'
        '</defs>'
        f'<circle cx="{center}" cy="{center}" r="124" '
        f'fill="url(#{prefix}-crust)" stroke="#8F4A26" stroke-width="3"/>'
        f'<circle cx="{center}" cy="{center}" r="117" '
        f'fill="url(#{prefix}-cheese)" stroke="#E6B967" stroke-width="2"/>'
        f'{"".join(crust_marks)}'
        f'{"".join(slices)}'
        f'{"".join(toppings)}'
        f'<circle cx="{center}" cy="{center}" r="{radius}" '
        'fill="none" stroke="#A9562B" stroke-width="2"/>'
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


st.title("피자를 활용해 분수의 크기 비교하기")
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
