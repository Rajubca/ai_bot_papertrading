import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Paper Trading Analytics",
    layout="wide"
)

st.title("📊 Paper Trading – Analytics Dashboard")

# ----------------------------
# Backend health check
# ----------------------------
st.subheader("🔌 Backend Status")

try:
    r = requests.get(f"{API_BASE}/api/analytics", timeout=5)
    backend_ok = r.status_code == 200
except Exception as e:
    backend_ok = False
    st.error(f"Backend not reachable: {e}")

if backend_ok:
    st.success("Backend is running")
else:
    st.stop()

# ----------------------------
# Analytics Section
# ----------------------------
st.subheader("📈 Trade Analytics")

try:
    analytics = r.json()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Trades", analytics.get("total_trades", 0))
    col2.metric("Win Rate (%)", analytics.get("win_rate", 0))
    col3.metric("Expectancy", analytics.get("expectancy", 0))
    col4.metric("Max Win Streak", analytics.get("max_win_streak", 0))

except Exception as e:
    st.warning("No analytics data available yet")
    st.text(str(e))

# ----------------------------
# AI Chat Section
# ----------------------------
st.subheader("🤖 AI Trading Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask the AI about your trades, risk, or performance")

if st.button("Send") and user_input:
    try:
        res = requests.post(
            f"{API_BASE}/api/agent/chat",
            json={"message": user_input},
            timeout=10
        ).json()

        st.session_state.chat.append(("You", user_input))
        st.session_state.chat.append(("AI", res.get("summary", str(res))))

    except Exception as e:
        st.error(f"AI error: {e}")

for role, msg in st.session_state.chat:
    st.markdown(f"**{role}:** {msg}")
