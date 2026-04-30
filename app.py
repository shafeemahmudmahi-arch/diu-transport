"""
DIU Smart Transport Management System - Pro Dispatch UI
Dark Theme Logistics Dashboard based on user reference.
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import hashlib
from datetime import datetime, timedelta
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="DIU Transport Dispatch",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PRO DISPATCH CUSTOM CSS ====================
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * { font-family: 'Inter', sans-serif; }
        
        /* Deep Dark Backgrounds */
        .stApp, [data-testid="stSidebar"] {
            background-color: #121212;
            color: #e0e0e0;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            border-right: 1px solid #2d2d2d;
        }
        
        /* Dark Glass Cards */
        .glass-card, .dashboard-card { 
            background: #1e1e1e; 
            border-radius: 12px; 
            border: 1px solid #2d2d2d; 
            padding: 1.5rem; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); 
            margin-bottom: 1rem;
        }
        
        /* Typography */
        h1, h2, h3, h4 { color: #ffffff; font-weight: 600; }
        .main-title { color: #ffffff; font-size: 1.5rem; font-weight: 700; margin-bottom: 0px; }
        .subtitle { color: #888888; font-size: 0.9rem; margin-bottom: 20px; }
        
        /* Status Badges */
        .badge-delivered { background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(16, 185, 129, 0.3); }
        .badge-transit { background: rgba(245, 158, 11, 0.15); color: #f59e0b; padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(245, 158, 11, 0.3); }
        .badge-delayed { background: rgba(59, 130, 246, 0.15); color: #3b82f6; padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(59, 130, 246, 0.3); }
        .badge-cancelled { background: rgba(239, 68, 68, 0.15); color: #ef4444; padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(239, 68, 68, 0.3); }
        
        /* Route Line */
        .route-line { border-left: 2px dashed #444; padding-left: 15px; margin-left: 5px; margin-top: 10px; margin-bottom: 10px; }
        
        /* Buttons */
        .stButton > button { background: #2d2d2d; color: white; border: 1px solid #444; border-radius: 8px; transition: 0.3s; }
        .stButton > button:hover { background: #3d3d3d; border-color: #666; color: white;}
        
        /* Primary Button */
        .primary-btn > button { background: #ffffff; color: #000000; font-weight: bold; }
        .primary-btn > button:hover { background: #e0e0e0; color: #000000; }

        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==================== DATA GENERATORS ====================

@st.cache_data
def generate_routes():
    return ["Dhanmondi", "Narayanganj", "Uttara", "Savar", "Mirpur-14", "Mirpur-12", "Gabtoli"]

@st.cache_data
def generate_buses():
    routes = generate_routes()
    buses = []
    base_coords = {
        "Dhanmondi": (23.7461, 90.3742), "Narayanganj": (23.6238, 90.5000), "Uttara": (23.8759, 90.3795),
        "Savar": (23.8583, 90.2667), "Mirpur-14": (23.8103, 90.3667), "Mirpur-12": (23.8256, 90.3689), "Gabtoli": (23.7783, 90.3494)
    }
    drivers = ["Karim T.", "Jabbar M.", "Rashed K.", "Habib R.", "Mizan I.", "Shafiq A."]
    statuses = ["In Transit", "In Transit", "In Transit", "Delivered", "Delayed", "Loading", "Cancelled"]
    
    for route in routes:
        for i in range(random.randint(5, 8)):
            status = random.choice(statuses)
            buses.append({
                "Bus_ID": f"#{random.randint(4000, 9999)}", 
                "Route": route, 
                "Driver": random.choice(drivers),
                "Latitude": base_coords[route][0] + random.uniform(-0.03, 0.03),
                "Longitude": base_coords[route][1] + random.uniform(-0.03, 0.03),
                "Status": status,
                "Students_Count": random.randint(15, 40) if status != "Cancelled" else 0,
                "Weight": f"{random.randint(150, 450)}kg" # Mock data to match screenshot
            })
    return pd.DataFrame(buses)

@st.cache_data
def generate_chart_data():
    dates = pd.date_range(start='2025-02-01', end='2025-11-30', freq='W')
    volumes = [random.randint(2000, 5000) for _ in range(len(dates))]
    return pd.DataFrame({'Date': dates, 'Volume': volumes})

# ==================== SESSION & AUTH ====================

def init_session():
    if 'logged_in' not in st.session_state: st.session_state.logged_in = False
    if 'buses_db' not in st.session_state: st.session_state.buses_db = generate_buses()
    if 'chart_data' not in st.session_state: st.session_state.chart_data = generate_chart_data()

def auth_user(user_id, password):
    if user_id == "admin" and password == "admin":
        return True
    return False

# ==================== LOGIN SCREEN ====================

def login_screen():
    st.markdown('<br><br>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="dashboard-card" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown('<h2>DIU Dispatch System</h2>', unsafe_allow_html=True)
        st.caption("Admin Login Required. ID: admin | Pass: admin")
        
        user_id = st.text_input("User ID", placeholder="admin")
        password = st.text_input("Password", type="password", placeholder="•••••")
        
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("Log In", use_container_width=True):
            if auth_user(user_id, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials.")
        st.markdown('</div></div>', unsafe_allow_html=True)

# ==================== MAIN DASHBOARD (PRO UI) ====================

def dispatch_dashboard():
    buses = st.session_state.buses_db
    
    # 1. SIDEBAR
    with st.sidebar:
        st.markdown('''
            <div style="display: flex; align-items: center; margin-bottom: 30px;">
                <div style="background: #333; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                    <b>MT</b>
                </div>
                <div>
                    <div style="font-weight: bold; color: white;">Max Turner</div>
                    <div style="font-size: 0.8rem; color: #888;">Admin</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        menu = st.radio("Navigation", ["Dashboard", "Orders", "Vehicles", "Documents", "Finance", "Analytics", "Settings", "Log out"], label_visibility="collapsed")
        
        if menu == "Log out":
            st.session_state.clear()
            st.rerun()
            
        st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
        st.markdown('''
            <div style="background: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333;">
                <h4 style="margin-top:0;">Dispatch App</h4>
                <p style="font-size: 0.8rem; color: #888;">Manage deliveries and driver fleet anywhere.</p>
                <button style="width: 100%; padding: 8px; border-radius: 5px; border: none; background: white; color: black; font-weight: bold;">Download app</button>
            </div>
        ''', unsafe_allow_html=True)

    # 2. TOP HEADER
    st.markdown('<div class="subtitle">Dashboard / <b>Shipment map</b> <span style="float:right;">Today 10 Nov ☀️</span></div>', unsafe_allow_html=True)

    # 3. LARGE MAP SECTION
    st.markdown('<div class="dashboard-card" style="padding: 0; position: relative; overflow: hidden; border-radius: 12px; height: 400px;">', unsafe_allow_html=True)
    
    # Map Markers Logic
    def get_color(status):
        if status == "Delivered": return [16, 185, 129, 200] # Green
        elif status == "In Transit": return [245, 158, 11, 200] # Yellow/Orange
        elif status == "Delayed": return [59, 130, 246, 200] # Blue
        elif status == "Cancelled": return [239, 68, 68, 200] # Red
        else: return [156, 163, 175, 200] # Gray (Loading)

    buses['Color'] = buses['Status'].apply(get_color)
    
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=buses,
        get_position='[Longitude, Latitude]',
        get_fill_color='Color',
        get_radius=200,
        pickable=True
    )
    
    view_state = pdk.ViewState(latitude=23.81, longitude=90.40, zoom=11.5, pitch=0)
    
    st.pydeck_chart(pdk.Deck(
        layers=[layer], 
        initial_view_state=view_state, 
        tooltip={"html": "<b style='color:#fff;'>{Bus_ID}</b> <span style='color:#aaa;'>{Status}</span>", "style": {"backgroundColor": "#1e1e1e", "color": "white", "border": "1px solid #333"}},
        map_style="mapbox://styles/mapbox/dark-v10" # Dark Mapbox style
    ))
    
    # Overlay Map Stats (Simulating absolute positioning with columns)
    st.markdown(f'''
        <div style="position: absolute; bottom: 20px; left: 20px; background: rgba(18, 18, 18, 0.8); padding: 15px; border-radius: 8px; border: 1px solid #333; font-size: 0.9rem;">
            <div style="margin-bottom: 5px;">Delivered Today: <b style="color:white;">{len(buses[buses['Status'] == 'Delivered']) * 21}</b></div>
            <div style="margin-bottom: 5px;">In Transit Today: <b style="color:white;">{len(buses[buses['Status'] == 'In Transit']) * 14}</b></div>
            <div>On-Time Rate Today (%): <b style="color:white;">87%</b></div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. BOTTOM SECTIONS
    col1, col2, col3 = st.columns([1.2, 0.8, 1])
    
    # Bottom Left: Volume Chart
    with col1:
        st.markdown('<div class="dashboard-card" style="height: 380px;">', unsafe_allow_html=True)
        st.markdown('<div style="display:flex; justify-content:space-between; margin-bottom: 10px;"><b>Shipments Volume & Transit Time</b> <select style="background:#333; color:white; border:none; border-radius:4px;"><option>Month</option></select></div>', unsafe_allow_html=True)
        
        # Area chart simulating the green gradient
        fig = px.area(st.session_state.chart_data, x="Date", y="Volume")
        fig.update_traces(line_color='#10b981', fillcolor='rgba(16, 185, 129, 0.2)')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False, color="#888"), yaxis=dict(showgrid=False, visible=False),
            height=280
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Middle: Status & Vehicles
    with col2:
        # Top half: Status Overview
        st.markdown('<div class="dashboard-card" style="height: 180px;">', unsafe_allow_html=True)
        st.markdown('<b>Status Overview</b>', unsafe_allow_html=True)
        
        # Simulating the stacked bar progress
        st.markdown('''
            <div style="display: flex; height: 20px; border-radius: 10px; overflow: hidden; margin-top: 15px; margin-bottom: 15px;">
                <div style="background: #10b981; width: 45%;"></div>
                <div style="background: #f59e0b; width: 30%;"></div>
                <div style="background: #3b82f6; width: 15%;"></div>
                <div style="background: #155e75; width: 5%;"></div>
                <div style="background: #ef4444; width: 5%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #888; display: grid; grid-template-columns: 1fr 1fr; gap: 5px;">
                <div><span style="color:#10b981;">■</span> Delivered</div>
                <div><span style="color:#f59e0b;">■</span> In Transit</div>
                <div><span style="color:#155e75;">■</span> Loading</div>
                <div><span style="color:#3b82f6;">■</span> Delayed</div>
                <div><span style="color:#ef4444;">■</span> Cancelled</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Bottom half: Vehicles in Transit
        st.markdown('<div class="dashboard-card" style="height: 180px; display:flex; flex-direction:column; justify-content:center;">', unsafe_allow_html=True)
        st.markdown('<b>Vehicles in Transit</b>', unsafe_allow_html=True)
        st.markdown(f'''
            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 20px;">
                <div>
                    <div style="color: #10b981; font-weight: bold;">+5</div>
                    <div style="font-size: 3rem; font-weight: bold; line-height: 1;">{len(buses[buses['Status'] == 'In Transit'])}</div>
                </div>
                <div style="font-size: 4rem;">🚛</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Right: Orders List
    with col3:
        st.markdown('<div class="dashboard-card" style="height: 380px; overflow-y: auto;">', unsafe_allow_html=True)
        st.markdown('<div style="display:flex; justify-content:space-between; margin-bottom: 20px;"><div><b>Orders</b><br><span style="font-size:0.8rem; color:#888;">Total: 6489</span></div> </div>', unsafe_allow_html=True)
        
        # Simulating the Order List items
        active_orders = buses[buses['Status'].isin(['In Transit', 'Delayed'])].head(3)
        for _, order in active_orders.iterrows():
            badge_class = "badge-transit" if order['Status'] == "In Transit" else "badge-delayed"
            st.markdown(f'''
                <div style="margin-bottom: 25px;">
                    <span style="color: white; font-weight: bold; margin-right: 10px;">{order['Bus_ID']}</span> 
                    <span class="{badge_class}">{order['Status']}</span>
                    
                    <div style="display: flex; margin-top: 15px; font-size: 0.85rem;">
                        <div style="flex: 2;">
                            <div style="color: #888; margin-bottom: 5px;">Shipment Route</div>
                            <div style="color: white;">DIU Main Campus, Savar<br>To: {order['Route']} Route Area</div>
                        </div>
                        <div style="flex: 1; text-align: right;">
                            <div style="color: #888; margin-bottom: 5px;">Est. delivery</div>
                            <div style="color: white;">{ (datetime.now() + timedelta(hours=random.randint(1,4))).strftime('%d %b, %Y') }</div>
                            <div style="color: #888; margin-top: 5px; margin-bottom: 2px;">Total weight</div>
                            <div style="color: white;">{order['Weight']}</div>
                        </div>
                    </div>
                </div>
                <hr style="border-color: #333; margin: 15px 0;">
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== MAIN RUNNER ====================
def main():
    init_session()
    inject_custom_css()
    if not st.session_state.logged_in:
        login_screen()
    else:
        dispatch_dashboard()

if __name__ == "__main__":
    main()
