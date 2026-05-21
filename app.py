import streamlit as st
from scipy.stats import beta, binom

st.set_page_config(page_title="OFC Overbooking App", layout="centered")
st.title("OFC オーバーブッキング予測（曜日別＋8枠統合）")

mode = st.radio("安全モード", ["標準（実測値）", "慎重（安全側推定）"])

risk_threshold = 0.20

days = {
    "月曜日": 4,
    "火曜日": 8,
    "水曜日": 4,
    "木曜日": 8,
    "金曜日": 8
}

eight_slot_cancel_sum = 0
eight_slot_total_sum = 0

st.header("曜日別推奨")

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

    alpha = cancels + 1
    beta_post = total_slots - cancels + 1

    if mode == "慎重（安全側推定）":
        p_use = beta.ppf(0.05, alpha, beta_post)
    else:
        p_use = cancels / total_slots if total_slots > 0 else 0

    results = []
    for k in range(0, slots + 1):
        prob_break = binom.cdf(k - 1, slots, p_use)
        results.append((k, prob_break))

    safe_options = [k for k, prob in results if prob < risk_threshold]
    recommended = max(safe_options) if safe_options else 0

    st.success(f"推奨：＋{recommended}枠")

    for k, prob in results:
        mark = "🟢" if k == recommended else ""
        st.write(f"{mark} +{k}枠 → 破綻確率 {prob*100:.1f}%")

    st.divider()

    # 8枠日を合算
    if slots == 8:
        eight_slot_cancel_sum += cancels
        eight_slot_total_sum += total_slots


# =========================
# 🔵 8枠日 統合推奨
# =========================

if eight_slot_total_sum > 0:

    st.header("🔵 8枠の日（火・木・金）統合推定")

    alpha = eight_slot_cancel_sum + 1
    beta_post = eight_slot_total_sum - eight_slot_cancel_sum + 1

    if mode == "慎重（安全側推定）":
        p_use = beta.ppf(0.05, alpha, beta_post)
    else:
        p_use = eight_slot_cancel_sum / eight_slot_total_sum

    st.write(f"使用キャンセル率: {p_use*100:.1f}%")

    results = []
    for k in range(0, 9):
        prob_break = binom.cdf(k - 1, 8, p_use)
        results.append((k, prob_break))

    safe_options = [k for k, prob in results if prob < risk_threshold]
    recommended = max(safe_options) if safe_options else 0

    st.success(f"8枠の日 推奨オーバーブッキング：＋{recommended}枠")

    for k, prob in results:
        mark = "🟢" if k == recommended else ""
        st.write(f"{mark} +{k}枠 → 破綻確率 {prob*100:.1f}%")
