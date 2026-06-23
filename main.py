import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime
import time


# --- PAGE SETUP ---
st.set_page_config(
    page_title="stcourse | Premium Analytics Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (Sleek Glassmorphism & UI Polish) ---
st.markdown("""
<style>
    /* Card design */
    .premium-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: transform 0.2s ease-in-out, border-color 0.2s ease-in-out;
    }
    .premium-card:hover {
        transform: translateY(-2px);
        border-color: #6366f1;
    }
    
    /* Custom font styling */
    .title-gradient {
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        margin-bottom: 0.2rem;
    }
    
    /* Info text */
    .sub-title {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=300&q=80", use_container_width=True)
    st.markdown("### 🛠️ Dashboard Controls")
    
    # Date Range Selector
    today = datetime.date.today()
    start_date = st.date_input("Start Date", today - datetime.timedelta(days=30))
    end_date = st.date_input("End Date", today)
    
    # Data Density Selector
    data_points = st.slider("Data Points Density", min_value=10, max_value=500, value=100, step=10)
    
    # Category Filter
    categories = st.multiselect("Filter by Categories", ["SaaS Products", "Cloud Services", "AI Compute"], default=["SaaS Products", "Cloud Services", "AI Compute"])
    
    st.divider()
    st.markdown("🌐 **Workspace Mode**: `stcourse` v0.1.0")

# --- HEADER SECTION ---
st.markdown('<div class="title-gradient">⚡ Streamlit Premium Analytics Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">A modern, responsive, and data-rich workspace built with uv & streamlit.</div>', unsafe_allow_html=True)

# --- TOP METRICS ROW ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Revenue", value="$128,450", delta="+12.4% (vs Last Month)", delta_color="normal")
with col2:
    st.metric(label="Active Users", value="14,295", delta="+8.3%", delta_color="normal")
with col3:
    st.metric(label="API Conversion Rate", value="94.2%", delta="-1.5%", delta_color="inverse")
with col4:
    st.metric(label="System Load (AI Compute)", value="24.8 ms", delta="-4.2 ms", delta_color="normal")

st.markdown("---")

# --- MAIN DASHBOARD TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Performance & Trends", "📈 Advanced Simulation", "💬 Interactive Chatbot UI"])

# Tab 1: Performance & Trends
with tab1:
    st.markdown("### 📊 Performance & Revenue Trends")
    
    # Generate mock time-series data
    date_range = pd.date_range(start=start_date, periods=data_points, freq='D')
    np.random.seed(42)
    
    trend_data = pd.DataFrame({
        'Date': date_range,
        'SaaS Products': np.cumsum(np.random.normal(150, 40, size=data_points)),
        'Cloud Services': np.cumsum(np.random.normal(100, 30, size=data_points)),
        'AI Compute': np.cumsum(np.random.normal(250, 70, size=data_points))
    })
    
    # Melt the dataframe for Altair plotting
    melted_data = trend_data.melt('Date', var_name='Category', value_name='Cumulative Revenue ($)')
    
    # Filter by category
    filtered_data = melted_data[melted_data['Category'].isin(categories)]
    
    # Create Altair Line Chart with tooltips and interactive zoom
    chart = alt.Chart(filtered_data).mark_line(strokeWidth=3, interpolate='monotone').encode(
        x='Date:T',
        y='Cumulative Revenue ($):Q',
        color=alt.Color('Category:N', scale=alt.Scale(scheme='tableau10')),
        tooltip=['Date:T', 'Category:N', 'Cumulative Revenue ($):Q']
    ).properties(
        height=400
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Interactive Table Expandable
    with st.expander("📋 View Raw Tabular Data"):
        st.dataframe(trend_data.set_index('Date'), use_container_width=True)

# Tab 2: Advanced Simulation
with tab2:
    st.markdown("### 📈 Project Growth Simulation")
    
    sim_col1, sim_col2 = st.columns([1, 2])
    
    with sim_col1:
        st.write("#### Simulation Parameters")
        growth_rate = st.slider("Monthly Growth Rate (%)", min_value=0.0, max_value=50.0, value=15.0, step=0.5)
        periods = st.number_input("Projection Horizon (Months)", min_value=1, max_value=60, value=12)
        initial_val = st.number_input("Initial Investment ($)", min_value=1000, max_value=1000000, value=10000)
        
    with sim_col2:
        st.write("#### Projection Chart")
        
        # Calculate simulation
        months = np.arange(periods + 1)
        values = initial_val * ((1 + growth_rate / 100) ** months)
        
        sim_df = pd.DataFrame({
            'Month': months,
            'Projected Value ($)': values
        })
        
        # Area chart for growth
        sim_chart = alt.Chart(sim_df).mark_area(
            color=alt.Gradient(
                gradient='linear',
                stops=[alt.GradientStop(color='#818cf8', offset=0),
                       alt.GradientStop(color='#c084fc', offset=1)],
                x1=1, y1=1, x2=1, y2=0
            ),
            opacity=0.3
        ).encode(
            x='Month:Q',
            y='Projected Value ($):Q'
        ) + alt.Chart(sim_df).mark_line(color='#818cf8', strokeWidth=2).encode(
            x='Month:Q',
            y='Projected Value ($):Q'
        )
        
        st.altair_chart(sim_chart, use_container_width=True)
        
        final_value = values[-1]
        st.success(f"🎯 **Projected Value at Month {periods}:** ${final_value:,.2f} ({((final_value - initial_val)/initial_val)*100:.1f}% Total Increase)")

# Tab 3: Interactive Chatbot UI
with tab3:
    st.markdown("### 💬 Interactive Assistant Preview")
    
    # Store chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I am your AI assistant in `stcourse`. How can I help you analyze the project data today?"}
        ]
        
    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # Handle user input
    if prompt := st.chat_input("Ask a question about the simulation or trends..."):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Simple interactive mock responses
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                time.sleep(0.5)
                if "revenue" in prompt.lower() or "trend" in prompt.lower():
                    response = "Based on our latest cumulative revenue charts, SaaS Products have shown the most stable and consistent growth over time."
                elif "growth" in prompt.lower() or "rate" in prompt.lower():
                    response = f"Your simulator is currently configured with a monthly growth rate of {growth_rate}%. At this rate, the initial investment will double roughly every {72 / (growth_rate or 0.1):.1f} months."
                else:
                    response = f"Thank you for your question: '{prompt}'. I am equipped to analyze the stcourse dataset in real-time."
                st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- FOOTER ---
st.markdown('<div class="footer">stcourse Workspace • Built with ❤️ using Streamlit & uv</div>', unsafe_allow_html=True)
