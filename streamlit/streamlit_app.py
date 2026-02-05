import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AI Paper Trading",
    layout="wide"
)

st.title("📊 AI Paper Trading Platform")

# ----------------------------
# SESSION STATE
# ----------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "chat" not in st.session_state:
    st.session_state.chat = []

# ----------------------------
# AUTH SIDEBAR
# ----------------------------
st.sidebar.header("🔐 Authentication")

if not st.session_state.token:
    tab_login, tab_register = st.sidebar.tabs(["Login", "Register"])

    # -------- LOGIN --------
    with tab_login:
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input(
            "Password", type="password", key="login_password"
        )

        if st.button("Login"):
            res = requests.post(
                f"{API_BASE}/api/auth/login",
                json={
                    "email": login_email,
                    "password": login_password,
                },
                timeout=5,
            )

            if res.status_code == 200:
                data = res.json()
                st.session_state.token = data["access_token"]
                st.success("Login successful")
                st.rerun()
            else:
                try:
                    st.error(res.json().get("detail", "Login failed"))
                except Exception:
                    st.error("Login failed")

    # -------- REGISTER --------
    with tab_register:
        reg_name = st.text_input("Name", key="reg_name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input(
            "Password", type="password", key="reg_password"
        )

        if st.button("Register"):
            res = requests.post(
                f"{API_BASE}/api/auth/register",
                json={
                    "name": reg_name,
                    "email": reg_email,
                    "password": reg_password,
                },
                timeout=5,
            )

            if res.status_code == 200:
                st.success("Registration successful. Please login.")
            else:
                try:
                    st.error(res.json().get("detail", "Registration failed"))
                except Exception:
                    st.error("Registration failed")

    st.stop()

# ----------------------------
# AUTH HEADERS
# ----------------------------
HEADERS = {
    "Authorization": f"Bearer {st.session_state.token}",
    "Content-Type": "application/json",
}

# ----------------------------
# LOGOUT
# ----------------------------
if st.sidebar.button("Logout"):
    st.session_state.token = None
    st.session_state.chat = []
    st.rerun()

# ----------------------------
# BACKEND HEALTH
# ----------------------------
st.subheader("🔌 Backend Status")

try:
    analytics_res = requests.get(
        f"{API_BASE}/api/analytics",
        headers=HEADERS,
        timeout=5,
    )

    pnl_res = requests.get(
        f"{API_BASE}/api/pnl/today",
        headers=HEADERS,
        timeout=5,
    )

    if analytics_res.status_code != 200:
        st.error("Unauthorized or session expired")
        st.stop()

    analytics = analytics_res.json()
    pnl = pnl_res.json()

    st.success("Authenticated & connected")

except Exception as e:
    st.error("Backend unreachable")
    st.code(str(e))
    st.stop()

# ----------------------------
# PNL SUMMARY
# ----------------------------
st.subheader("💰 PnL Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Realized PnL", pnl.get("realized_pnl", 0))
c2.metric("Unrealized PnL", pnl.get("unrealized_pnl", 0))
c3.metric("Total PnL", pnl.get("total_pnl", 0))
c4.metric("Win Rate (%)", analytics.get("win_rate", 0))

# ----------------------------
# ANALYTICS
# ----------------------------
st.subheader("📈 Trade Analytics")

a1, a2, a3, a4 = st.columns(4)

a1.metric("Total Trades", analytics.get("total_trades", 0))
a2.metric("Avg Win", analytics.get("avg_win", 0))
a3.metric("Expectancy", analytics.get("expectancy", 0))
a4.metric("Max Win Streak", analytics.get("max_win_streak", 0))

# ----------------------------
# AI CHAT
# ----------------------------
st.subheader("🤖 AI Trading Assistant")

user_input = st.text_input("Ask about performance, risk, or trades")

if st.button("Send") and user_input:
    try:
        res = requests.post(
            f"{API_BASE}/api/agent/chat",
            headers=HEADERS,
            json={"message": user_input},
            timeout=10,
        )

        st.session_state.chat.append(("You", user_input))

        if res.status_code == 200:
            data = res.json()
            reply = (
                data.get("reply")
                or data.get("summary")
                or data.get("message")
                or str(data)
            )
            st.session_state.chat.append(("AI", reply))
        else:
            st.session_state.chat.append(
                ("AI", "AI service error")
            )

    except Exception as e:
        st.error(f"AI error: {e}")

for role, msg in st.session_state.chat:
    st.markdown(f"**{role}:** {msg}")
