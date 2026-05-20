import streamlit as st
from scipy.stats import beta, binom

st.set_page_config(page_title="OFC Overbooking App", layout="centered")
st.title("OFC オーバーブッキング予測（曜日別）")
st.caption("過去2週間データから曜日別推奨")

days = {
    "月曜日": 4,
    "火曜日": 8,
    "水曜日": 4,
    "木曜日": 8,
    "金曜日": 4
}

st.header("過去2週間のキャンセル入力")

results_summary = {}

for day, slots in days.items():
    st.subheader(day)

    total_slots = slots * 2
    cancels = st.number_input(
        f"{day} のキャンセル数（2週間合計）",
        min_value=0,
        max_value=total_slots,
        value=0,
        key=day
    )

    if cancels > total_slots:
        st.error("キャンセル数が枠数を超えています")
    else:
        alpha = cancels + 1
        beta_post = total_slots - cancels + 1

        # 安全側（5%下限）
        p_lower = beta.ppf(0.05, alpha, beta_post)

        st.write(f"推定キャンセル率（安全側）: {p_lower*100:.1f}%")

        st.write("オーバーブッキングごとの破綻確率:")

        for k in range(0, slots + 1):
            prob_cancel_less = binom.cdf(k - 1, slots, p_lower)
            prob_break = prob_cancel_less
            st.write(f"+{k}枠 → 破綻確率 {prob_break*100:.1f}%")

        st.divider()
