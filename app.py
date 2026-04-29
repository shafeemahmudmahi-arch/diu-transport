"""
DIU Smart Transport Management System
======================================
A single-file Streamlit MVP for Daffodil International University (DIU).
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be the very first st call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DIU Smart Transport",
    page_icon="🚍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════
#  1.  FAKE DATABASE  (in-memory, no external DB)
# ══════════════════════════════════════════════

students_db = {
    "STU001": {"name": "Rahim Uddin",      "route": "Mirpur",   "fee_status": "Paid",   "year": 2, "dept": "CSE"},
    "STU002": {"name": "Nadia Islam",      "route": "Uttara",   "fee_status": "Paid",   "year": 3, "dept": "EEE"},
    "STU003": {"name": "Karim Hossain",    "route": "Gabtoli",  "fee_status": "Unpaid", "year": 1, "dept": "BBA"},
    "STU004": {"name": "Sultana Begum",    "route": "Mirpur",   "fee_status": "Paid",   "year": 4, "dept": "CSE"},
    "STU005": {"name": "Tanvir Ahmed",     "route": "Savar",    "fee_status": "Unpaid", "year": 2, "dept": "ETE"},
    "STU006": {"name": "Fatema Khanam",    "route": "Uttara",   "fee_status": "Paid",   "year": 1, "dept": "MBA"},
    "STU007": {"name": "Mahbub Rahman",    "route": "Gabtoli",  "fee_status": "Paid",   "year": 3, "dept": "Law"},
    "STU008": {"name": "Roksana Akter",    "route": "Savar",    "fee_status": "Paid",   "year": 2, "dept": "CSE"},
    "STU009": {"name": "Jahirul Islam",    "route": "Mirpur",   "fee_status": "Unpaid", "year": 1, "dept": "Arch"},
    "STU010": {"name": "Priya Chakraborty","route": "Uttara",   "fee_status": "Paid",   "year": 4, "dept": "Pharm"},
}

buses_db = [
    {"bus_id": "DIU-01", "route": "Mirpur",  "capacity": 40, "occupancy": 32, "driver": "Md. Sirajul Islam",  "status": "En Route",  "lat": 23.8041, "lon": 90.3563},
    {"bus_id": "DIU-02", "route": "Uttara",  "capacity": 45, "occupancy": 28, "driver": "Md. Kamal Hossen",   "status": "At Stop",   "lat": 23.8759, "lon": 90.3795},
    {"bus_id": "DIU-03", "route": "Gabtoli", "capacity": 35, "occupancy": 35, "driver": "Abdul Kuddus Mia",   "status": "Full",      "lat": 23.7761, "lon": 90.3520},
    {"bus_id": "DIU-04", "route": "Savar",   "capacity": 50, "occupancy": 18, "driver": "Md. Rafiqul Islam",  "status": "En Route",  "lat": 23.8575, "lon": 90.2664},
    {"bus_id": "DIU-05", "route": "Mirpur",  "capacity": 40, "occupancy": 10, "driver": "Mostafa Kamal",      "status": "Departed",  "lat": 23.7925, "lon": 90.3638},
    {"bus_id": "DIU-06", "route": "Uttara",  "capacity": 45, "occupancy": 40, "driver": "Md. Faruk Hossain",  "status": "En Route",  "lat": 23.8640, "lon": 90.3700},
]

routine_db = pd.DataFrame({
    "Day":      ["Sat","Sat","Sat","Sun","Sun","Sun","Mon","Mon","Mon","Tue","Tue","Tue"],
    "Time":     ["8AM","10AM","12PM","8AM","10AM","12PM","8AM","10AM","12PM","8AM","10AM","12PM"],
    "Students": [210, 185, 90, 220, 195, 95, 215, 180, 85, 205, 170, 80],
    "Buses_Needed": [6, 5, 3, 6, 5, 3, 6, 5, 3, 6, 5, 3],
    "Buses_Allocated": [5, 5, 2, 6, 4, 3, 5, 5, 2, 5, 4, 3],
})

# ══════════════════════════════════════════════
#  2.  CUSTOM CSS — DIU Brand Theme
# ══════════════════════════════════════════════

def inject_css():
    st.markdown("""
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* ── Root Variables ── */
    :root {
        --navy:   #000c1d;
        --green:  #39b54a;
        --blue:   #034ea2;
        --light:  #e8f0fe;
        --card:   #071428;
        --border: rgba(57,181,74,0.25);
        --text:   #c9d8f0;
        --white:  #ffffff;
        --red:    #e74c3c;
        --amber:  #f39c12;
    }

    /* ── Global ── */
    html, body, [data-testid="stAppViewContainer"] {
        background: var(--navy) !important;
        color: var(--text) !important;
        font-family: 'Poppins', sans-serif !important;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000c1d 0%, #071428 60%, #000c1d 100%) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }

    /* ── Sidebar Radio Buttons ── */
    div[data-testid="stSidebar"] .stRadio > label {
        font-size: 0.78rem !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--green) !important;
    }
    div[data-testid="stSidebar"] .stRadio div[role="radio"] {
        padding: 8px 12px;
        border-radius: 8px;
        transition: background 0.2s;
    }
    div[data-testid="stSidebar"] .stRadio div[role="radio"]:hover {
        background: rgba(57,181,74,0.12) !important;
    }

    /* ── Metric Cards ── */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #071428 0%, #0a1f3d 100%) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        padding: 18px 22px !important;
        box-shadow: 0 4px 24px rgba(3,78,162,0.18), inset 0 1px 0 rgba(255,255,255,0.04) !important;
    }
    [data-testid="stMetricLabel"] { color: var(--text) !important; font-size: 0.78rem !important; letter-spacing: 0.06em; text-transform: uppercase; }
    [data-testid="stMetricValue"] { color: var(--white) !important; font-weight: 700 !important; font-size: 1.9rem !important; }
    [data-testid="stMetricDelta"] { font-size: 0.82rem !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, var(--blue) 0%, #0562c9 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
        padding: 10px 24px !important;
        transition: all 0.22s !important;
        box-shadow: 0 4px 18px rgba(3,78,162,0.35) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(3,78,162,0.55) !important;
    }

    /* ── Text Input ── */
    .stTextInput > div > div > input {
        background: #071428 !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--white) !important;
        font-family: 'Poppins', sans-serif !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--green) !important;
        box-shadow: 0 0 0 3px rgba(57,181,74,0.18) !important;
    }

    /* ── Success / Error / Warning boxes ── */
    .stAlert { border-radius: 12px !important; border: none !important; }

    /* ── Charts ── */
    [data-testid="stVegaLiteChart"], .js-plotly-plot {
        background: transparent !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #071428 !important;
        border-radius: 8px 8px 0 0 !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-bottom: none !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #071c38 0%, #0a2850 100%) !important;
        color: var(--green) !important;
        border-color: var(--green) !important;
    }

    /* ── Dataframe / Tables ── */
    [data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; }

    /* ── Divider ── */
    hr { border-color: var(--border) !important; }

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] {
        background: #071428 !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        background: #071428 !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--white) !important;
    }

    /* ── Custom card helper ── */
    .diu-card {
        background: linear-gradient(135deg, #071428 0%, #0a1f3d 100%);
        border: 1px solid rgba(57,181,74,0.25);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 14px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    }
    .diu-card h4 { color: #fff; margin: 0 0 6px; font-size: 1rem; font-weight: 600; }
    .diu-card p  { color: var(--text); margin: 0; font-size: 0.87rem; line-height: 1.5; }

    /* ── Big status labels ── */
    .status-granted {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 800;
        color: #39b54a;
        text-shadow: 0 0 32px rgba(57,181,74,0.6);
        padding: 18px;
        border: 3px solid #39b54a;
        border-radius: 18px;
        background: rgba(57,181,74,0.08);
        letter-spacing: 0.06em;
    }
    .status-denied {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 800;
        color: #e74c3c;
        text-shadow: 0 0 32px rgba(231,76,60,0.6);
        padding: 18px;
        border: 3px solid #e74c3c;
        border-radius: 18px;
        background: rgba(231,76,60,0.08);
        letter-spacing: 0.06em;
    }

    /* ── Page title ── */
    .page-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #fff;
        padding-bottom: 4px;
        border-bottom: 2px solid var(--green);
        display: inline-block;
        margin-bottom: 18px;
    }
    .page-sub { color: var(--text); font-size: 0.85rem; margin-top: -10px; margin-bottom: 20px; }

    /* ── Sidebar logo area ── */
    .sidebar-logo {
        text-align: center;
        padding: 16px 0 24px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 20px;
    }
    .sidebar-logo .logo-text {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #39b54a, #034ea2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sidebar-logo .logo-sub { font-size: 0.7rem; color: var(--text); letter-spacing: 0.12em; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  3.  SESSION STATE INIT
# ══════════════════════════════════════════════

def init_session_state():
    defaults = {
        "chat_history": [],
        "student_logged_in": False,
        "current_student_id": "",
        "seat_requested": False,
        "backup_deployed": False,
        "sos_triggered": False,
        "scan_result": None,
        "mid_bookings": random.randint(4, 12),
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# ══════════════════════════════════════════════
#  HELPER UTILITIES
# ══════════════════════════════════════════════

def jitter(val, scale=0.008):
    """Add small random offset to lat/lon to simulate GPS movement."""
    return val + random.uniform(-scale, scale)

def get_route_buses(route: str):
    return [b for b in buses_db if b["route"] == route]

def format_eta():
    return random.randint(5, 25)

def get_ai_chat_response(msg: str) -> str:
    """Rule-based mock AI transport chatbot."""
    msg_lower = msg.lower()
    now = datetime.now()
    next_time = (now + timedelta(minutes=format_eta())).strftime("%I:%M %p")

    if any(w in msg_lower for w in ["next bus", "when", "time"]):
        return f"🕐 The next bus on your route departs at approximately **{next_time}**. Current ETA to your stop: **{format_eta()} minutes**."
    elif any(w in msg_lower for w in ["seat", "available", "space"]):
        return "💺 Based on real-time occupancy data, **DIU-04 (Savar route)** currently has **32 seats available**. You can request a mid-route seat using the booking button above."
    elif any(w in msg_lower for w in ["route", "bus", "which"]):
        return "🚍 Active routes today: **Mirpur**, **Uttara**, **Gabtoli**, **Savar**. All routes are operational. DIU-03 (Gabtoli) is currently at full capacity."
    elif any(w in msg_lower for w in ["rain", "weather", "traffic"]):
        return "⛈️ Weather advisory: **Light rain expected from 3–6 PM** today. Recommend leaving campus by 2:45 PM. Traffic delay on Mirpur road: +12 mins."
    elif any(w in msg_lower for w in ["fee", "paid", "payment"]):
        return "💳 Your transport fee is marked as **Paid** ✅. You have full boarding access. Next due date: **January 2026**."
    elif any(w in msg_lower for w in ["sos", "emergency", "help"]):
        return "🆘 Emergency services have been notified. Please stay calm. The nearest patrol bus (DIU-05) is being rerouted to your location. ETA: **8 minutes**."
    elif any(w in msg_lower for w in ["hello", "hi", "hey", "salaam"]):
        return "👋 Assalamu Alaikum! I'm your **DIU Smart Transport Assistant**. Ask me about bus timings, seat availability, routes, or any transport emergency!"
    else:
        return f"🤖 Thanks for your query about **'{msg}'**. Our AI engine is processing route & demand data. For urgent help, please contact transport office: **ext. 1234**."

# ══════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div class="logo-text">DIU 🚍</div>
            <div class="logo-sub">Smart Transport System</div>
        </div>
        """, unsafe_allow_html=True)

        panel = st.radio(
            "Navigation",
            ["🎓 Student Panel", "🏢 Admin Panel", "🚍 Driver Panel"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        now = datetime.now()
        st.markdown(f"""
        <div style="font-size:0.75rem; color:#7a9cc4; line-height:1.8;">
            📅 <b style="color:#c9d8f0">{now.strftime('%A, %d %b %Y')}</b><br>
            🕐 <b style="color:#c9d8f0">{now.strftime('%I:%M %p')}</b><br>
            🌡️ <b style="color:#c9d8f0">28°C — Partly Cloudy</b><br>
            🟢 <b style="color:#39b54a">System Online</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style="font-size:0.7rem; color:#4a6a8a; text-align:center; line-height:1.6;">
            Powered by <b style="color:#39b54a">DIU AI Engine v2.1</b><br>
            © 2025 Daffodil International University
        </div>
        """, unsafe_allow_html=True)

    return panel

# ══════════════════════════════════════════════
#  PANEL 1 — STUDENT
# ══════════════════════════════════════════════

def render_student_panel():
    st.markdown('<div class="page-title">🎓 Student Transport Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Your personalised bus tracker, seat manager & AI assistant.</div>', unsafe_allow_html=True)

    # ── Login ──
    col_login, col_spacer = st.columns([1.2, 2])
    with col_login:
        student_id_input = st.text_input(
            "Enter your Student ID",
            placeholder="e.g. STU001",
            key="stu_id_input",
        )
        login_btn = st.button("🔐 Login to Dashboard", use_container_width=True)

    if login_btn:
        if student_id_input.strip().upper() in students_db:
            st.session_state.student_logged_in = True
            st.session_state.current_student_id = student_id_input.strip().upper()
        else:
            st.error("❌ Student ID not found. Try: STU001 – STU010")

    if not st.session_state.student_logged_in:
        # Show hint cards when not logged in
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Demo IDs:** STU001 (Paid, Mirpur) · STU002 (Paid, Uttara) · STU003 (Unpaid, Gabtoli) · STU005 (Unpaid, Savar)")
        return

    # ── Logged-in Dashboard ──
    stu = students_db[st.session_state.current_student_id]
    route = stu["route"]
    route_buses = get_route_buses(route)

    st.success(f"✅ Welcome back, **{stu['name']}** | {stu['dept']} Year {stu['year']} | Route: **{route}**")

    if stu["fee_status"] == "Unpaid":
        st.warning("⚠️ **Transport fee unpaid.** You may be denied boarding. Please pay at the finance office.")

    st.markdown("---")

    # ── Fleet Metrics ──
    st.markdown("#### 🚌 Fleet Status — Your Route")
    total  = len(route_buses)
    depart = sum(1 for b in route_buses if b["status"] in ["Departed", "En Route"])
    remain = total - depart

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Buses",     total,  delta="on your route")
    m2.metric("Buses En Route",  depart, delta="moving now")
    m3.metric("Buses Remaining", remain, delta="at depot")
    m4.metric("ETA Next Bus",    f"{format_eta()} min", delta="estimated")

    st.markdown("---")

    # ── Live Map & Seat Status ──
    tab_map, tab_seat, tab_book, tab_chat, tab_alerts = st.tabs([
        "🗺️ Live Map", "💺 Seat Status", "📋 Book Seat", "🤖 AI Chatbot", "⚠️ Smart Alerts"
    ])

    with tab_map:
        st.markdown("#### 📍 Live Bus Positions — Real-time GPS")
        st.markdown(f"<div class='page-sub'>Buses on <b>{route}</b> route are shown below. Map refreshes every 30s.</div>", unsafe_allow_html=True)

        # Build map dataframe with jitter to simulate movement
        map_data = pd.DataFrame([
            {"lat": jitter(b["lat"]), "lon": jitter(b["lon"])}
            for b in route_buses
        ])
        st.map(map_data, zoom=12, use_container_width=True)

        eta_val = format_eta()
        st.markdown(f"""
        <div class="diu-card">
            <h4>⏱️ Next Arrival ETA</h4>
            <p>Bus <b>{route_buses[0]['bus_id']}</b> driven by <b>{route_buses[0]['driver']}</b>
            is approximately <span style="color:#39b54a;font-size:1.2rem;font-weight:700">{eta_val} minutes</span> away from your stop.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab_seat:
        st.markdown("#### 💺 Real-time Seat Occupancy")
        for bus in route_buses:
            free  = bus["capacity"] - bus["occupancy"]
            pct   = int(bus["occupancy"] / bus["capacity"] * 100)
            color = "#e74c3c" if pct >= 90 else ("#f39c12" if pct >= 65 else "#39b54a")
            badge = "🔴 FULL" if pct >= 100 else ("🟡 BUSY" if pct >= 65 else "🟢 AVAILABLE")
            st.markdown(f"""
            <div class="diu-card" style="border-left: 4px solid {color};">
                <h4>{bus['bus_id']} &nbsp;|&nbsp; {bus['route']} Route &nbsp; {badge}</h4>
                <p>Driver: <b>{bus['driver']}</b> &nbsp;|&nbsp; Occupied: <b>{bus['occupancy']}/{bus['capacity']}</b> &nbsp;|&nbsp;
                Free Seats: <b style="color:{color}">{free}</b></p>
            </div>
            """, unsafe_allow_html=True)
            st.progress(pct / 100)

    with tab_book:
        st.markdown("#### 📋 Virtual Seat Booking")
        st.markdown('<div class="page-sub">Request a pickup from a mid-route stop (Savar, Gabtoli junction).</div>', unsafe_allow_html=True)

        avail_buses = [b for b in route_buses if b["occupancy"] < b["capacity"]]

        if avail_buses:
            st.markdown(f"""
            <div class="diu-card">
                <h4>🚌 Mid-Route Booking Available</h4>
                <p>Bus <b>{avail_buses[0]['bus_id']}</b> has <b>{avail_buses[0]['capacity'] - avail_buses[0]['occupancy']}</b> seats free.
                Click below to request a pickup at your nearest junction stop.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("📍 Request Mid-Route Seat (Savar / Gabtoli)", use_container_width=True):
                st.session_state.seat_requested = True

            if st.session_state.seat_requested:
                st.success(f"✅ **Seat booked!** Bus **{avail_buses[0]['bus_id']}** will pick you up at the **{route} Junction Stop** in approx. **{format_eta()} minutes**. Show your Student ID when boarding.")
        else:
            st.error("⚠️ All buses on your route are currently full. Please wait for the next trip.")

    with tab_chat:
        st.markdown("#### 🤖 DIU AI Transport Assistant")
        st.markdown('<div class="page-sub">Ask anything about buses, routes, seat availability or emergencies.</div>', unsafe_allow_html=True)

        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        if prompt := st.chat_input("Ask me anything… e.g. 'When is the next bus?'"):
            # User message
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # AI response with typing simulation
            with st.chat_message("assistant"):
                with st.spinner("AI thinking…"):
                    time.sleep(0.4)
                response = get_ai_chat_response(prompt)
                st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()

    with tab_alerts:
        st.markdown("#### ⚠️ Smart Alerts & Notifications")

        st.warning("🌧️ **Weather Alert:** Light to moderate rain expected between **3:00 PM – 6:00 PM**. Recommendation: Leave campus by **2:45 PM** to avoid delays.")
        st.error("🚦 **Traffic Alert:** Heavy congestion on **Mirpur Road (Section 10–12)**. Estimated additional delay: **+18 minutes** on Mirpur route.")
        st.info("📢 **Route Notice:** DIU-03 (Gabtoli) is at full capacity. Next available bus departs at **5:30 PM**.")

        if stu["fee_status"] == "Unpaid":
            st.error("💳 **Fee Alert:** Your transport fee is **UNPAID**. Access may be denied by the driver scanner. Pay immediately at the Finance Office (Building 2, Room 201).")
        else:
            st.success("💳 **Fee Status:** Transport fee **PAID** ✅. Your boarding access is fully active.")

        st.markdown(f"""
        <div class="diu-card">
            <h4>📱 Push Notification Settings</h4>
            <p>You are receiving alerts for: <b>{route}</b> route | Weather, Traffic, Capacity warnings enabled.</p>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  PANEL 2 — ADMIN
# ══════════════════════════════════════════════

def render_admin_panel():
    st.markdown('<div class="page-title">🏢 Admin / Management Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">AI-powered fleet management, demand forecasting & revenue audit.</div>', unsafe_allow_html=True)

    # ── KPI Row ──
    total_students = len(students_db)
    paid_count     = sum(1 for s in students_db.values() if s["fee_status"] == "Paid")
    unpaid_count   = total_students - paid_count
    total_scans    = random.randint(85, 140)

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Buses",       len(buses_db),   delta="+1 backup ready")
    k2.metric("Active Students",   total_students,  delta="enrolled")
    k3.metric("Total Scans Today", total_scans,     delta=f"+{random.randint(3,8)} last hour")
    k4.metric("Access Granted",    paid_count,      delta="paid")
    k5.metric("Access Denied",     unpaid_count,    delta="unpaid", delta_color="inverse")

    st.markdown("---")

    tab_demand, tab_fleet, tab_surge, tab_audit, tab_sos = st.tabs([
        "📈 AI Demand", "🗺️ Fleet Map", "⚡ Surge Control", "💰 Revenue Audit", "🆘 SOS Hub"
    ])

    with tab_demand:
        st.markdown("#### 📈 AI Demand Prediction — Student Load vs Bus Allocation")
        st.markdown("""
        <div class="diu-card">
            <h4>🧠 AI Engine Note</h4>
            <p>Using <b>Scikit-learn RandomForestRegressor</b> trained on historical attendance + class schedule data.
            The model predicts required buses per timeslot with <b>91.4% accuracy</b>. Underallocation slots are highlighted automatically.</p>
        </div>
        """, unsafe_allow_html=True)

        chart_data = routine_db.set_index("Time")[["Students", "Buses_Needed", "Buses_Allocated"]].copy()

        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.markdown("##### 📊 Student Demand by Timeslot")
            st.bar_chart(routine_db.set_index("Time")["Students"], color="#39b54a")

        with col_chart2:
            st.markdown("##### 🚌 Buses Needed vs Allocated")
            st.line_chart(routine_db.set_index("Time")[["Buses_Needed", "Buses_Allocated"]])

        st.markdown("##### 📋 Full Routine Prediction Table")
        display_df = routine_db.copy()
        display_df["Gap"] = display_df["Buses_Needed"] - display_df["Buses_Allocated"]
        display_df["Status"] = display_df["Gap"].apply(lambda x: "⚠️ Underallocated" if x > 0 else "✅ Adequate")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    with tab_fleet:
        st.markdown("#### 🗺️ Live Fleet Monitor — All Routes")

        # Status summary
        status_counts = {}
        for b in buses_db:
            status_counts[b["status"]] = status_counts.get(b["status"], 0) + 1

        col_s = st.columns(len(status_counts))
        colors = {"En Route": "#39b54a", "At Stop": "#f39c12", "Full": "#e74c3c", "Departed": "#034ea2"}
        for i, (stat, cnt) in enumerate(status_counts.items()):
            col_s[i].markdown(f"""
            <div style="text-align:center; background:{colors.get(stat,'#555')}22;
                        border:1px solid {colors.get(stat,'#555')}44; border-radius:10px; padding:12px;">
                <div style="font-size:1.6rem;font-weight:700;color:{colors.get(stat,'#fff')}">{cnt}</div>
                <div style="font-size:0.75rem;color:#c9d8f0">{stat}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # All buses on map
        all_map_data = pd.DataFrame([
            {"lat": jitter(b["lat"]), "lon": jitter(b["lon"])}
            for b in buses_db
        ])
        st.map(all_map_data, zoom=11, use_container_width=True)

        st.markdown("##### 🚌 Bus Fleet Details")
        fleet_df = pd.DataFrame(buses_db)[["bus_id","route","capacity","occupancy","driver","status"]]
        fleet_df["free_seats"] = fleet_df["capacity"] - fleet_df["occupancy"]
        fleet_df["load_%"]     = (fleet_df["occupancy"] / fleet_df["capacity"] * 100).round(1)
        fleet_df.columns       = ["Bus ID","Route","Capacity","Occupied","Driver","Status","Free Seats","Load %"]
        st.dataframe(fleet_df, use_container_width=True, hide_index=True)

    with tab_surge:
        st.markdown("#### ⚡ Dynamic Surge Control System")

        st.error("🔴 **HIGH SURGE DETECTED** — Gabtoli Route: Demand exceeds capacity by **+28 students**. Immediate action required!")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="diu-card" style="border-left:4px solid #e74c3c">
                <h4>🚨 Surge Alert — Gabtoli Route</h4>
                <p>Current Load: <b>35/35</b> (100% full) | Waiting: <b>28 students</b><br>
                AI Recommendation: Deploy <b>1 backup bus</b> immediately.</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚌 Deploy Backup Bus (Gabtoli)", use_container_width=True):
                st.session_state.backup_deployed = True

            if st.session_state.backup_deployed:
                st.success("✅ **Backup Bus DIU-07 deployed!** Driver Md. Shamsul Haque notified. ETA to Gabtoli depot: **15 minutes**. Capacity: 45 seats.")

        with c2:
            st.markdown("""
            <div class="diu-card" style="border-left:4px solid #f39c12">
                <h4>⚡ Surge Forecast — Next 2 Hours</h4>
                <p>Mirpur: <b>Moderate surge</b> expected at 5 PM (+12 students over capacity)<br>
                Uttara: <b>Normal load</b> — no action needed<br>
                Savar: <b>Low demand</b> — consider consolidating with Mirpur route</p>
            </div>
            """, unsafe_allow_html=True)

        # Mini surge chart
        st.markdown("##### 📊 Real-time Demand Surge")
        surge_data = pd.DataFrame({
            "Time":   ["3PM","3:30PM","4PM","4:30PM","5PM","5:30PM"],
            "Mirpur": [32,   35,      38,   40,      45,   42],
            "Gabtoli":[28,   33,      35,   35,      34,   30],
            "Uttara": [22,   25,      28,   30,      31,   26],
        }).set_index("Time")
        st.line_chart(surge_data)

    with tab_audit:
        st.markdown("#### 💰 Smart Access & Revenue Audit")

        # Revenue metrics
        fee_per_student = 3500  # BDT per semester
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Total Registered", len(students_db))
        r2.metric("Fee Collected",    f"৳{paid_count * fee_per_student:,}")
        r3.metric("Fee Pending",      f"৳{unpaid_count * fee_per_student:,}", delta_color="inverse", delta="due")
        r4.metric("Collection Rate",  f"{paid_count/len(students_db)*100:.0f}%")

        st.markdown("##### 👥 Student Fee Status Breakdown")
        stu_df = pd.DataFrame([
            {
                "Student ID": sid,
                "Name": s["name"],
                "Route": s["route"],
                "Dept": s["dept"],
                "Year": s["year"],
                "Fee Status": s["fee_status"],
            }
            for sid, s in students_db.items()
        ])
        st.dataframe(stu_df, use_container_width=True, hide_index=True)

        st.markdown("##### 📊 Fee Collection by Route")
        route_fee = stu_df.groupby("Route")["Fee Status"].value_counts().unstack(fill_value=0)
        st.bar_chart(route_fee)

    with tab_sos:
        st.markdown("#### 🆘 SOS & Emergency Rescue Hub")

        sos_alerts = [
            {"bus": "DIU-03", "route": "Gabtoli", "issue": "Engine Overheating", "driver": "Abdul Kuddus Mia",    "severity": "HIGH",   "time": "4:12 PM"},
            {"bus": "DIU-01", "route": "Mirpur",  "issue": "Flat Tyre",         "driver": "Md. Sirajul Islam",   "severity": "MEDIUM", "time": "3:48 PM"},
        ]

        if st.session_state.sos_triggered:
            st.error("🆘 **DRIVER SOS ALERT — ACTIVE!** A driver has triggered an emergency SOS. Patrol team dispatched!")

        for alert in sos_alerts:
            sev_color = "#e74c3c" if alert["severity"] == "HIGH" else "#f39c12"
            st.markdown(f"""
            <div class="diu-card" style="border-left:4px solid {sev_color}">
                <h4>🚨 {alert['severity']} ALERT — Bus {alert['bus']} ({alert['route']} Route)</h4>
                <p>Issue: <b>{alert['issue']}</b> | Driver: <b>{alert['driver']}</b> | Reported: <b>{alert['time']}</b><br>
                Status: <span style="color:{sev_color}">⚠️ Rescue Team En Route</span></p>
            </div>
            """, unsafe_allow_html=True)

        if not sos_alerts and not st.session_state.sos_triggered:
            st.success("✅ No active emergencies. All buses operating normally.")

# ══════════════════════════════════════════════
#  PANEL 3 — DRIVER
# ══════════════════════════════════════════════

def render_driver_panel():
    st.markdown('<div class="page-title">🚍 Driver Operations Panel</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Smart scanner, passenger counter, AI routing & emergency controls.</div>', unsafe_allow_html=True)

    # Driver selector (simulated login)
    selected_bus = st.selectbox(
        "Select Your Bus",
        options=[b["bus_id"] for b in buses_db],
        format_func=lambda x: next(f"{b['bus_id']} — {b['route']} Route ({b['driver']})" for b in buses_db if b["bus_id"] == x),
    )
    bus_info = next(b for b in buses_db if b["bus_id"] == selected_bus)

    st.markdown("---")

    tab_scan, tab_counter, tab_routing, tab_sos = st.tabs([
        "📷 Access Scanner", "👥 Passenger Count", "🗺️ AI Routing", "🆘 Emergency SOS"
    ])

    with tab_scan:
        st.markdown("#### 📷 Smart Student Access Scanner")
        st.markdown('<div class="page-sub">Scan or type Student ID to verify boarding eligibility.</div>', unsafe_allow_html=True)

        scan_id = st.text_input(
            "🔍 Scan / Enter Student ID",
            placeholder="Type Student ID (e.g. STU001)…",
            key="driver_scan",
        )
        col_scan, col_clear = st.columns([1, 1])
        with col_scan:
            scan_btn = st.button("✅ Verify Access", use_container_width=True)
        with col_clear:
            clear_btn = st.button("🔄 Clear", use_container_width=True)

        if clear_btn:
            st.session_state.scan_result = None

        if scan_btn:
            scan_id_up = scan_id.strip().upper()
            if scan_id_up in students_db:
                stu = students_db[scan_id_up]
                st.session_state.scan_result = {
                    "id": scan_id_up,
                    "status": stu["fee_status"],
                    "name": stu["name"],
                    "route": stu["route"],
                    "dept": stu["dept"],
                }
            else:
                st.session_state.scan_result = {"id": scan_id_up, "status": "NOT_FOUND"}

        if st.session_state.scan_result:
            res = st.session_state.scan_result
            if res["status"] == "Paid":
                st.markdown(f"""
                <div class="status-granted">
                    ✅ ACCESS GRANTED
                </div>
                <div class="diu-card" style="margin-top:14px;">
                    <h4>👤 {res['name']} — {res['id']}</h4>
                    <p>Department: <b>{res['dept']}</b> | Route: <b>{res['route']}</b> | Fee: <b style="color:#39b54a">PAID ✅</b></p>
                </div>
                """, unsafe_allow_html=True)
            elif res["status"] == "Unpaid":
                st.markdown(f"""
                <div class="status-denied">
                    🚫 ACCESS DENIED
                </div>
                <div class="diu-card" style="margin-top:14px;border-left:4px solid #e74c3c">
                    <h4>👤 {res['name']} — {res['id']}</h4>
                    <p>Department: <b>{res['dept']}</b> | Route: <b>{res['route']}</b> | Fee: <b style="color:#e74c3c">UNPAID ❌</b><br>
                    Instruct student to contact the Finance Office before boarding.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="status-denied">⚠️ ID NOT FOUND</div>
                """, unsafe_allow_html=True)
                st.warning("Student ID not in the system. Please check the ID card and rescan.")

    with tab_counter:
        st.markdown("#### 👥 Mid-Route Passenger Counter")

        free_seats  = bus_info["capacity"] - bus_info["occupancy"]
        pre_bookings = st.session_state.mid_bookings

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Capacity",    bus_info["capacity"])
        c2.metric("Currently Occupied",bus_info["occupancy"])
        c3.metric("Available Seats",   free_seats,            delta=f"-{pre_bookings} pre-booked")

        st.markdown(f"""
        <div class="diu-card">
            <h4>📋 Mid-Route Pre-Bookings</h4>
            <p><b>{pre_bookings} students</b> have virtually requested a seat via the app for <b>mid-route pickup</b>.
            Effective available seats for walk-ins: <b>{max(0, free_seats - pre_bookings)}</b>.</p>
        </div>
        """, unsafe_allow_html=True)

        # Load bar
        occ_pct = bus_info["occupancy"] / bus_info["capacity"]
        bar_color = "🔴" if occ_pct >= 0.9 else ("🟡" if occ_pct >= 0.65 else "🟢")
        st.markdown(f"**Occupancy Load:** {bar_color} {int(occ_pct*100)}%")
        st.progress(occ_pct)

        # Simulated passenger log
        st.markdown("##### 📋 Recent Boarding Log")
        log_data = pd.DataFrame({
            "Time":       [f"{h}:{m:02d} PM" for h, m in [(3,12),(3,24),(3,31),(3,44),(3,52)]],
            "Student ID": ["STU001","STU004","STU006","STU010","STU002"],
            "Name":       ["Rahim Uddin","Sultana Begum","Fatema Khanam","Priya Chakraborty","Nadia Islam"],
            "Status":     ["✅ Boarded","✅ Boarded","✅ Boarded","✅ Boarded","✅ Boarded"],
        })
        st.dataframe(log_data, use_container_width=True, hide_index=True)

    with tab_routing:
        st.markdown("#### 🗺️ AI Smart Routing Engine")
        st.markdown('<div class="page-sub">Shortest traffic-free path computed using real-time road data.</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="diu-card" style="border-left:4px solid #39b54a">
            <h4>🧭 Optimal Route — {bus_info['route']} via DIU Campus</h4>
            <p>AI Engine recommends: <b>Ashulia → Bypass Road → Savar → Nabinagar → {bus_info['route']}</b><br>
            Estimated journey time: <b>{format_eta() + 10} minutes</b> | Traffic: <b>Moderate</b> | Distance: <b>24.6 km</b></p>
        </div>
        """, unsafe_allow_html=True)

        # Route map (current bus position)
        route_map = pd.DataFrame([
            {"lat": jitter(bus_info["lat"]), "lon": jitter(bus_info["lon"])},
            {"lat": 23.7985, "lon": 90.3630},  # DIU Campus (Dhanmondi/Ashulia approx)
        ])
        st.map(route_map, zoom=11, use_container_width=True)

        st.markdown("""
        <div class="diu-card">
            <h4>🤖 AI Routing Note</h4>
            <p>Algorithm: <b>Dijkstra's shortest path</b> + <b>live traffic weight scores</b> from Google Maps API.
            Route is recalculated every <b>2 minutes</b>. Alternate route via Mirpur 12 available if main road load exceeds 80%.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab_sos:
        st.markdown("#### 🆘 One-Tap Emergency SOS")

        st.markdown("""
        <div class="diu-card" style="border-left:4px solid #e74c3c; text-align:center;">
            <h4 style="color:#e74c3c; font-size:1.1rem">⚠️ USE ONLY IN GENUINE EMERGENCIES</h4>
            <p>Pressing SOS will immediately alert the Admin control room, nearest patrol team, and campus security. Your GPS location will be shared automatically.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_sos, col_sp = st.columns([1, 2])
        with col_sos:
            sos_btn = st.button("🆘  EMERGENCY SOS", use_container_width=True, type="primary")

        if sos_btn:
            st.session_state.sos_triggered = True
            st.error("""
            🚨 **SOS ALERT SENT SUCCESSFULLY!**

            ✅ Admin Control Room — **NOTIFIED**
            ✅ Nearest Patrol Bus (DIU-05) — **REROUTING TO YOU**
            ✅ Campus Security — **ALERTED**
            ✅ Your GPS Location — **SHARED**

            **Estimated rescue arrival: 8–12 minutes.**
            Stay calm. Keep your hazard lights on.
            """)

        if st.session_state.sos_triggered:
            st.markdown(f"""
            <div class="diu-card" style="border-left:4px solid #e74c3c">
                <h4 style="color:#e74c3c">🚨 Active SOS — Bus {bus_info['bus_id']} ({bus_info['route']})</h4>
                <p>Driver: <b>{bus_info['driver']}</b> | Triggered at: <b>{datetime.now().strftime('%I:%M %p')}</b><br>
                Rescue Status: <b style="color:#f39c12">En Route — ETA 8 min</b></p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("##### 🩺 Report Non-Emergency Issue")
        issue_type = st.selectbox("Issue Type", ["Select…","Flat Tyre","Engine Problem","Passenger Medical Emergency","Road Blockage","Fuel Empty","Mechanical Failure"])
        issue_note = st.text_input("Brief Description", placeholder="e.g. Engine light on since Ashulia...")
        if st.button("📤 Report Issue to Admin"):
            if issue_type != "Select…":
                st.success(f"✅ Issue **'{issue_type}'** reported to Admin. Ticket #T-{random.randint(1000,9999)} created. Expect callback in 5 minutes.")
            else:
                st.warning("Please select an issue type first.")

# ══════════════════════════════════════════════
#  MAIN APP ENTRY POINT
# ══════════════════════════════════════════════

def main():
    init_session_state()
    inject_css()
    panel = render_sidebar()

    if panel == "🎓 Student Panel":
        render_student_panel()
    elif panel == "🏢 Admin Panel":
        render_admin_panel()
    elif panel == "🚍 Driver Panel":
        render_driver_panel()


if __name__ == "__main__":
    main()
