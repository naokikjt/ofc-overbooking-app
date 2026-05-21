import streamlit as st
from scipy.stats import beta, binom

st.set_page_config(page_title="8枠日まとめ推定", layout="centered")

st.title("8枠の日 オーバーブッキング推定")
st.caption("過去2週間の8枠日合計から推奨算出")

mode = st.radio("安全モード", ["標準（実測値）", "慎重（安全側推定）"])

risk_threshold = 0.20

# 2週間分の8枠日合計入力
total_slots = st.number_input(
    "過去2週間の8枠日 総実施枠数",
    min_value=1,
    value=48  # 8枠 × 3日 × 2週 = 48
)

cancels = st.number_input(
    "過去2週間の8枠日 総キャンセル数",
    min_value=0,
    value=0
)

if cancels > total_slots:
    st.error("キャンセル数が総枠数を超えています")
else:

    alpha = cancels + 1
    beta_post = total_slots - cancels + 1

    if mode == "慎重（安全側推定）":
        p_use = beta.ppf(0.05, alpha, beta_post)
    else:
        p_use = cancels / total_slots if total_slots > 0 else 0

    st.write(f"使用キャンセル率: {p_use*100:.1f}%")

    results = []

    for k in range(0, 9):
        prob_break = binom.cdf(k - 1, 8, p_use)
        results.append((k, prob_break))

    safe_options = [k for k, prob in results if prob < risk_threshold]
    recommended = max(safe_options) if safe_options else 0

    st.success(f"8枠日の推奨オーバーブッキング：＋{recommended}枠")

    st.subheader("各追加枠での破綻確率")

    for k, prob in results:
        mark = "🟢" if k == recommended else ""
        st.write(f"{mark} +{k}枠 → 破綻確率 {prob*100:.1f}%")
