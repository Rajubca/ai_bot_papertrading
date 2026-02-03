import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Paper Trading Analytics", layout="wide")
st.title("📊 Paper Trading – Analytics Dashboard")

# ----------------------------
# AUTH TOKEN (URL → Sidebar)
# ----------------------------

# 1️⃣ Read token from URL (if present)
query_params = st.query_params
url_token = query_params.get("token", [""])[0]

# 2️⃣ Sidebar input (fallback / override)
st.sidebar.header("🔐 Authentication")
input_token = st.sidebar.text_input(
    "Paste JWT Token",
    type="password",
    value=url_token
).strip()

# 3️⃣ Final token decision
token = input_token

if not token:
    st.info(
        "Login at http://localhost:3000/login and paste your JWT token here.\n\n"
        "This analytics panel is for internal/admin use."
    )
    st.stop()

HEADERS = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

# ----------------------------
# Backend Health + Core Stats
# ----------------------------
st.subheader("🔌 Backend Status")

try:
    stats = requests.get(
        f"{API_BASE}/api/analytics",
        headers=HEADERS,
        timeout=5
    ).json()

    pnl = requests.get(
        f"{API_BASE}/api/pnl/today",
        headers=HEADERS,
        timeout=5
    ).json()

    st.success("Authenticated & connected to backend")

except Exception as e:
    st.error("Authentication failed or backend unreachable")
    st.code(str(e))
    st.stop()

# ----------------------------
# PnL Summary
# ----------------------------
st.subheader("💰 PnL Summary")

p1, p2, p3, p4 = st.columns(4)

p1.metric("Realized PnL", pnl.get("realized_pnl", 0))
p2.metric("Unrealized PnL", pnl.get("unrealized_pnl", 0))
p3.metric("Total PnL", pnl.get("total_pnl", 0))
p4.metric("Win Rate (%)", stats.get("win_rate", 0))

# ----------------------------
# Analytics Section
# ----------------------------
st.subheader("📈 Trade Analytics")

a1, a2, a3, a4 = st.columns(4)

a1.metric("Total Trades", stats.get("total_trades", 0))
a2.metric("Avg Win", stats.get("avg_win", 0))
a3.metric("Expectancy", stats.get("expectancy", 0))
a4.metric("Max Win Streak", stats.get("max_win_streak", 0))

# ----------------------------
# AI Chat Section
# ----------------------------
st.subheader("🤖 AI Trading Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask the AI about performance, risk, or trades")

if st.button("Send") and user_input:
    try:
        res = requests.post(
            f"{API_BASE}/api/agent/chat",
            headers=HEADERS,
            json={"message": user_input},
            timeout=10,
        ).json()

        st.session_state.chat.append(("You", user_input))

        ai_reply = (
            res.get("reply")
            or res.get("summary")
            or res.get("message")
            or str(res)
        )

        st.session_state.chat.append(("AI", ai_reply))

    except Exception as e:
        st.error(f"AI error: {e}")

for role, msg in st.session_state.chat:
    st.markdown(f"**{role}:** {msg}")
