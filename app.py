import streamlit as st
from scipy.stats import beta, binom

st.set_page_config(page_title="OFC Overbooking App", layout="centered")
st.title("OFC オーバーブッキング予測（曜日別）")
st.caption("過去2週間のキャンセル実績から曜日別推奨を算出")

# 安全モード選択
mode = st.radio("安全モードを選択", ["標準（実測値）", "慎重（安全側推定）"])

days = {
    "月曜日": 4,
    "火曜日": 8,
    "水曜日": 4,
    "木曜日": 8,
    "金曜日": 4
}

risk_threshold = 0.20  # 破綻確率20%未満を推奨

for day, slots in days.items():

    st.subheader(f"📅 {day}（通常{slots}枠）")

    total_slots = slots * 2
    cancels = st.number_input(
        f"{day} のキャンセル数（過去2週間合計）",
        min_value=0,
        max_value=total_slots,
        value=0,
        key=day
    )

    if total_slots == 0:
        continue

    alpha = cancels + 1
    beta_post = total_slots - cancels + 1

    # キャンセル率の選択
    if mode == "慎重（安全側推定）":
        p_use = beta.ppf(0.05, alpha, beta_post)
    else:
        p_use = cancels / total_slots

    st.write(f"使用キャンセル率: {p_use*100:.1f}%")

    results = []

    for k in range(0, slots + 1):
        prob_break = binom.cdf(k - 1, slots, p_use)
        results.append((k, prob_break))

    # 推奨枠算出
    safe_options = [k for k, prob in results if prob < risk_threshold]
    recommended = max(safe_options) if safe_options else 0

    st.success(f"推奨オーバーブッキング枠：＋{recommended}枠")

    st.write("各追加枠での破綻確率：")

    for k, prob in results:
        color = "🟢" if k == recommended else ""
        st.write(f"{color} +{k}枠 → 破綻確率 {prob*100:.1f}%")

    st.divider()
