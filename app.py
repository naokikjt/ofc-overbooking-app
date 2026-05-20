import streamlit as st
from scipy.stats import beta, binom

st.set_page_config(page_title="OFC Overbooking App", layout="centered")
st.title("OFC オーバーブッキング予測アプリ")
st.caption("週1日・通常4枠 / 事前キャンセルのみ考慮")

st.header("前月データ入力")
col1, col2 = st.columns(2)
with col1:
    n_prev = st.number_input("前月OFC総数", min_value=1, value=100, step=1)
with col2:
    c_prev = st.number_input("前月キャンセル数", min_value=0, value=12, step=1)

confidence = st.slider("安全水準（%）", min_value=80, max_value=99, value=95, step=1)

if c_prev > n_prev:
    st.error("キャンセル数は総数以下にしてください。")
else:
    alpha_post = c_prev + 1
    beta_post = n_prev - c_prev + 1
    alpha_level = 1 - confidence / 100
    p_lower = beta.ppf(alpha_level, alpha_post, beta_post)

    n_slots = 4
    st.header("結果")
    st.write(f"安全側キャンセル率推定: **{p_lower*100:.2f}%**")

    results = []
    for k in range(0, n_slots + 1):
        prob = 1 - binom.cdf(k - 1, n_slots, p_lower)
        results.append((k, prob))

    safe_candidates = [k for k, prob in results if prob >= confidence / 100]
    max_safe = max(safe_candidates) if safe_candidates else 0

    st.subheader(f"推奨オーバーブッキング枠: +{max_safe}")
    st.divider()
    st.subheader("各オーバーブッキング枠の相殺確率")
    for k, prob in results:
        st.write(f"+{k}枠 : 相殺確率 {prob*100:.1f}%")

    st.caption("判定基準: P(キャンセル数 ≥ オーバーブッキング枠) ≥ 安全水準")
