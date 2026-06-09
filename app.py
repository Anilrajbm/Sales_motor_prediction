import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Set up page configurations
st.set_page_config(
    layout="wide",
    page_title="DYUTHI MOTORS - Sales Analytics Dashboard",
    page_icon="🏍️",
    initial_sidebar_state="expanded"
)

# Custom premium styling using CSS
st.markdown("""
<style>
    /* Main container adjustments */
    .reportview-container {
        background: #f8f9fa;
    }
    
    /* Card design with smooth gradients */
    .metric-card {
        padding: 24px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease;
        margin-bottom: 15px;
    }
    .metric-card:hover {
        transform: translateY(-4px);
    }
    .card-sales {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    .card-revenue {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .card-profit {
        background: linear-gradient(135deg, #ff9900 0%, #ff5500 100%);
    }
    .card-top {
        background: linear-gradient(135deg, #8a2be2 0%, #4b0082 100%);
    }
    
    .card-title {
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 10px;
        opacity: 0.85;
    }
    .card-value {
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .card-subtitle {
        font-size: 11px;
        opacity: 0.75;
    }
    
    /* Header layout */
    .dashboard-header {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 25px;
        border-left: 5px solid #2a5298;
    }
    
    /* Segment titles */
    .section-title {
        font-weight: 700;
        color: #2c3e50;
        margin-top: 20px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Load data helper
@st.cache_data
def load_data():
    df = pd.read_csv('processed_sales_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Initialize data
df_raw = load_data()

# ----------------- SIDEBAR FILTER SECTION -----------------
st.sidebar.image("https://img.icons8.com/color/96/vespa.png", width=70)
st.sidebar.title("Dyuthi Motors Filters")
st.sidebar.write("Refine sales analysis parameters below:")

# Get filter options
seasons_list = sorted(list(df_raw['Season'].unique()))
categories_list = sorted(list(df_raw['Category'].unique()))
vehicles_list = sorted(list(df_raw['Vehicle'].unique()))

# Session state to handle filter resets
if 'selected_seasons' not in st.session_state:
    st.session_state.selected_seasons = seasons_list
if 'selected_categories' not in st.session_state:
    st.session_state.selected_categories = categories_list
if 'selected_vehicles' not in st.session_state:
    st.session_state.selected_vehicles = vehicles_list

def reset_filters():
    st.session_state.selected_seasons = seasons_list
    st.session_state.selected_categories = categories_list
    st.session_state.selected_vehicles = vehicles_list

# Sidebar controls
selected_seasons = st.sidebar.multiselect(
    "Select Season", 
    seasons_list, 
    key='selected_seasons'
)
selected_categories = st.sidebar.multiselect(
    "Select Vehicle Category", 
    categories_list, 
    key='selected_categories'
)
selected_vehicles = st.sidebar.multiselect(
    "Select Vehicle Model", 
    vehicles_list, 
    key='selected_vehicles'
)

if st.sidebar.button("Reset All Filters", type="secondary"):
    reset_filters()
    st.rerun()

# Apply filters to dataset
df_filtered = df_raw.copy()

if selected_seasons:
    df_filtered = df_filtered[df_filtered['Season'].isin(selected_seasons)]
if selected_categories:
    df_filtered = df_filtered[df_filtered['Category'].isin(selected_categories)]
if selected_vehicles:
    df_filtered = df_filtered[df_filtered['Vehicle'].isin(selected_vehicles)]

# Check if filtered data is empty
if df_filtered.empty:
    st.error("No records found for the selected filters. Please expand your filter criteria in the sidebar.")
    st.stop()

# ----------------- APP LAYOUT & TITLE -----------------
st.markdown("""
<div class="dashboard-header">
    <h1 style="margin: 0; font-size: 32px; color: #1e3c72; font-family: 'Outfit', sans-serif;">JAYA MOTORS SALES ANALYTICS</h1>
    <p style="margin: 5px 0 0 0; color: #7f8c8d; font-size: 14px;">Data Mining & Predictive Business Intelligence Dashboard for Two-Wheeler Sales</p>
</div>
""", unsafe_allow_html=True)

# ----------------- INSIGHT CALCULATIONS -----------------
# Core aggregates
total_sales = int(df_filtered['Units_Sold'].sum())
total_rev = int(df_filtered['Revenue'].sum())
total_profit = int(df_filtered['Profit'].sum())

# Best/Lowest Selling Vehicle
vehicle_sales_group = df_filtered.groupby('Vehicle').agg(
    Units=('Units_Sold', 'sum'),
    Rev=('Revenue', 'sum')
)
best_selling_vehicle = vehicle_sales_group['Units'].idxmax()
best_selling_units = int(vehicle_sales_group['Units'].max())

lowest_selling_vehicle = vehicle_sales_group['Units'].idxmin()
lowest_selling_units = int(vehicle_sales_group['Units'].min())

highest_rev_vehicle = vehicle_sales_group['Rev'].idxmax()
highest_rev_val = int(vehicle_sales_group['Rev'].max())

# Best Month calculation
monthly_summary = df_filtered.groupby(['Date', 'Month'])['Units_Sold'].sum().reset_index()
best_month_idx = monthly_summary['Units_Sold'].idxmax()
best_month_name = monthly_summary.loc[best_month_idx, 'Month']
best_month_units = int(monthly_summary.loc[best_month_idx, 'Units_Sold'])

# Average Monthly Sales
avg_monthly_sales = float(monthly_summary['Units_Sold'].mean())

# Estimated Net Margin
net_margin = (total_profit / total_rev * 100) if total_rev > 0 else 0.0


# ----------------- KPI CARDS DISPLAY -----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card card-sales">
        <div class="card-title">Total Units Sold</div>
        <div class="card-value">{total_sales:,} Units</div>
        <div class="card-subtitle">Avg: {avg_monthly_sales:.1f} units/month</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card card-revenue">
        <div class="card-title">Total Revenue</div>
        <div class="card-value">₹{total_rev:,}</div>
        <div class="card-subtitle">Gross showroom invoice sales</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card card-profit">
        <div class="card-title">Estimated Profit</div>
        <div class="card-value">₹{total_profit:,}</div>
        <div class="card-subtitle">Based on category dealer margins</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card card-top">
        <div class="card-title">Best Seller Model</div>
        <div class="card-value" style="font-size: 20px; padding: 5px 0;">{best_selling_vehicle}</div>
        <div class="card-subtitle">{best_selling_units} units sold total</div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- TABS SETUP -----------------
tabs = st.tabs([
    "📊 Executive Summary", 
    "📈 Sales & Revenue Trends", 
    "🏍️ Vehicle Analysis", 
    "🔮 3-Month Sales Forecast", 
    "💡 Business Strategy"
])

# ================= TAB 1: EXECUTIVE SUMMARY =================
with tabs[0]:
    st.markdown("<h3 class='section-title'>Key Sales Performance Metrics</h3>", unsafe_allow_html=True)
    
    col_metric1, col_metric2 = st.columns(2)
    
    with col_metric1:
        st.markdown(f"""
        **Top Selling Vehicle:** `{best_selling_vehicle}` with **{best_selling_units}** units sold.  
        **Highest Revenue Contributor:** `{highest_rev_vehicle}` generating **₹{highest_rev_val:,}** in gross sales.  
        **Best Performance Month:** `{best_month_name}` recording a peak sales of **{best_month_units}** units.
        """)
        
    with col_metric2:
        st.markdown(f"""
        **Lowest Selling Vehicle:** `{lowest_selling_vehicle}` with only **{lowest_selling_units}** unit(s) sold.  
        **Estimated Net Margin:** **{net_margin:.2f}%** average margin across all categories.  
        **Overall Portfolio Size:** **{len(df_filtered['Vehicle'].unique())}** unique vehicle models active.
        """)

    # Grid of basic figures
    st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
    st.markdown("#### Category-Wise Breakdown")
    category_summary = df_filtered.groupby('Category').agg(
        Units_Sold=('Units_Sold', 'sum'),
        Revenue=('Revenue', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()
    
    # Format currency columns for rendering
    formatted_cat_summary = category_summary.copy()
    formatted_cat_summary['Revenue'] = formatted_cat_summary['Revenue'].apply(lambda x: f"₹{x:,}")
    formatted_cat_summary['Profit'] = formatted_cat_summary['Profit'].apply(lambda x: f"₹{x:,}")
    st.dataframe(formatted_cat_summary, use_container_width=True, hide_index=True)

# ================= TAB 2: SALES & REVENUE TRENDS =================
with tabs[1]:
    st.markdown("<h3 class='section-title'>Chronological Sales and Revenue Trends</h3>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns(2)
    
    # Monthly sales volume trend line chart
    with col_t1:
        # Group by Date and Month Name
        trend_df = df_filtered.groupby('Date')['Units_Sold'].sum().reset_index().sort_values('Date')
        trend_df['Month_Label'] = trend_df['Date'].dt.strftime('%b %Y')
        
        fig_sales_trend = px.line(
            trend_df,
            x='Month_Label',
            y='Units_Sold',
            markers=True,
            title='Monthly Sales Trend (Units Sold)',
            labels={'Units_Sold': 'Units Sold', 'Month_Label': 'Month'},
            line_shape='linear',
            color_discrete_sequence=['#2a5298']
        )
        fig_sales_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#eaeaea'),
            yaxis=dict(showgrid=True, gridcolor='#eaeaea'),
        )
        st.plotly_chart(fig_sales_trend, use_container_width=True)

    # Monthly revenue trend line chart
    with col_t2:
        rev_trend_df = df_filtered.groupby('Date')['Revenue'].sum().reset_index().sort_values('Date')
        rev_trend_df['Month_Label'] = rev_trend_df['Date'].dt.strftime('%b %Y')
        
        fig_rev_trend = px.line(
            rev_trend_df,
            x='Month_Label',
            y='Revenue',
            markers=True,
            title='Monthly Revenue Trend (INR)',
            labels={'Revenue': 'Revenue (₹)', 'Month_Label': 'Month'},
            line_shape='linear',
            color_discrete_sequence=['#11998e']
        )
        fig_rev_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#eaeaea'),
            yaxis=dict(showgrid=True, gridcolor='#eaeaea'),
        )
        st.plotly_chart(fig_rev_trend, use_container_width=True)

    # Revenue Contribution by Vehicle / Category
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    col_pie1, col_pie2 = st.columns(2)
    
    with col_pie1:
        # Pie chart for Revenue Contribution by Category
        cat_rev_df = df_filtered.groupby('Category')['Revenue'].sum().reset_index()
        fig_cat_pie = px.pie(
            cat_rev_df,
            values='Revenue',
            names='Category',
            title='Revenue Contribution by Vehicle Category',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_cat_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_cat_pie, use_container_width=True)
        
    with col_pie2:
        # Pie chart for Revenue Contribution by Vehicle Model
        veh_rev_df = df_filtered.groupby('Vehicle')['Revenue'].sum().reset_index()
        fig_veh_pie = px.pie(
            veh_rev_df,
            values='Revenue',
            names='Vehicle',
            title='Revenue Contribution by Vehicle Model',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_veh_pie.update_traces(textinfo='percent')
        st.plotly_chart(fig_veh_pie, use_container_width=True)

# ================= TAB 3: VEHICLE ANALYSIS =================
with tabs[2]:
    st.markdown("<h3 class='section-title'>Detailed Vehicle-wise Performance</h3>", unsafe_allow_html=True)
    
    # Horizontal bar chart: Sales Count by Vehicle
    fig_vehicle_sales = px.bar(
        vehicle_sales_group.reset_index().sort_values(by='Units', ascending=True),
        x='Units',
        y='Vehicle',
        orientation='h',
        title='Total Sales Volume by Vehicle Model',
        labels={'Units': 'Units Sold', 'Vehicle': 'Vehicle Model'},
        color='Units',
        color_continuous_scale='Blues'
    )
    fig_vehicle_sales.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_vehicle_sales, use_container_width=True)
    
    # Revenue contribution by Vehicle Bar Chart
    fig_vehicle_rev = px.bar(
        vehicle_sales_group.reset_index().sort_values(by='Rev', ascending=True),
        x='Rev',
        y='Vehicle',
        orientation='h',
        title='Total Revenue Generated by Vehicle Model (INR)',
        labels={'Rev': 'Revenue (₹)', 'Vehicle': 'Vehicle Model'},
        color='Rev',
        color_continuous_scale='Viridis'
    )
    fig_vehicle_rev.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_vehicle_rev, use_container_width=True)

    # Demand Distribution (Low, Medium, High)
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("#### Month-wise Vehicle Demand Level Heatmap")
    
    # Create pivot table for demand levels
    demand_pivot = df_filtered.pivot_table(
        index='Vehicle', 
        columns='Month', 
        values='Units_Sold', 
        aggfunc='sum'
    ).fillna(0)
    
    # Reorder columns chronologically based on available months in df_filtered
    ordered_months = [m for m in ['April 2025', 'May 2025', 'June 2025', 'July 2025', 'August 2025', 'September 2025', 'October 2025', 'November 2025', 'December 2025', 'January 2026', 'February 2026', 'March 2026', 'April 2026'] if m in demand_pivot.columns]
    demand_pivot = demand_pivot[ordered_months]
    
    # Render interactive heatmap
    fig_heatmap = px.imshow(
        demand_pivot,
        labels=dict(x="Month", y="Vehicle Model", color="Units Sold"),
        x=ordered_months,
        y=demand_pivot.index,
        color_continuous_scale='YlOrRd',
        title='Monthly Units Sold Heatmap'
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# ================= TAB 4: FORECASTING SECTION (LINEAR REGRESSION) =================
with tabs[3]:
    st.markdown("<h3 class='section-title'>Predictive Modeling: 3-Month Future Sales Forecast</h3>", unsafe_allow_html=True)
    st.write("Using a **Simple Linear Regression** model, we project overall sales volumes for the next 3 months based on historical data.")
    
    # Prepare historical aggregated sales data chronologically
    hist_monthly = df_raw.groupby('Date')['Units_Sold'].sum().reset_index().sort_values('Date').reset_index(drop=True)
    hist_monthly['Month_Label'] = hist_monthly['Date'].dt.strftime('%b %Y')
    hist_monthly['Month_Index'] = np.arange(1, len(hist_monthly) + 1)
    
    # Setup Regression
    X = hist_monthly[['Month_Index']].values
    y = hist_monthly['Units_Sold'].values
    
    # Fit Linear Regression Model
    lr_model = LinearRegression()
    lr_model.fit(X, y)
    
    # Predict next 3 months (Months 14, 15, 16)
    last_index = hist_monthly['Month_Index'].iloc[-1]
    next_months_indices = np.array([last_index + 1, last_index + 2, last_index + 3]).reshape(-1, 1)
    predicted_sales = lr_model.predict(next_months_indices)
    predicted_sales = np.clip(predicted_sales, 0, None)  # Ensure non-negative predictions
    
    # Generate labels for future months
    last_date = hist_monthly['Date'].iloc[-1]
    future_dates = [last_date + pd.DateOffset(months=i) for i in range(1, 4)]
    future_labels = [d.strftime('%b %Y') for d in future_dates]
    
    # Build a combined dataframe for charting
    chart_data = pd.DataFrame({
        'Month': hist_monthly['Month_Label'].tolist() + future_labels,
        'Sales': hist_monthly['Units_Sold'].tolist() + [None]*3,
        'Forecast': [None]*len(hist_monthly) + list(predicted_sales.round(1)),
        'Type': ['Historical']*len(hist_monthly) + ['Forecasted']*3
    })
    
    # Add a transition point to make the line continuous in the plot
    chart_data.loc[len(hist_monthly) - 1, 'Forecast'] = hist_monthly['Units_Sold'].iloc[-1]
    
    # Plotly Forecast Chart
    fig_forecast = go.Figure()
    
    # Historical trace
    fig_forecast.add_trace(go.Scatter(
        x=chart_data['Month'],
        y=chart_data['Sales'],
        mode='lines+markers',
        name='Historical Sales',
        line=dict(color='#2a5298', width=3),
        marker=dict(size=8)
    ))
    
    # Forecast trace
    fig_forecast.add_trace(go.Scatter(
        x=chart_data['Month'],
        y=chart_data['Forecast'],
        mode='lines+markers',
        name='Forecasted Sales',
        line=dict(color='#ff5500', width=3, dash='dash'),
        marker=dict(size=8, symbol='diamond')
    ))
    
    fig_forecast.update_layout(
        title='Dyuthi Motors Sales Volume Forecast (Next 3 Months)',
        xaxis_title='Month',
        yaxis_title='Total Units Sold',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#eaeaea'),
        yaxis=dict(showgrid=True, gridcolor='#eaeaea'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Forecast details card
    col_fc1, col_fc2, col_fc3 = st.columns(3)
    
    with col_fc1:
        st.metric(label=f"Projected Sales ({future_labels[0]})", value=f"{int(round(predicted_sales[0]))} units")
    with col_fc2:
        st.metric(label=f"Projected Sales ({future_labels[1]})", value=f"{int(round(predicted_sales[1]))} units")
    with col_fc3:
        st.metric(label=f"Projected Sales ({future_labels[2]})", value=f"{int(round(predicted_sales[2]))} units")

    trend_direction = "upward" if lr_model.coef_[0] > 0 else "downward"
    coef_abs = abs(lr_model.coef_[0])
    st.markdown(f"""
    > **Linear Regression Model Details:**  
    > Equation: $Sales = \\beta_0 + \\beta_1 \\times Month\\_Index$  
    > - **Base Baseline Intercept ($\\beta_0$):** **{lr_model.intercept_:.2f}** units  
    > - **Growth Coefficient / Slope ($\\beta_1$):** **{lr_model.coef_[0]:.2f}** units/month  
    > 
    > **Interpretation:** The positive/negative growth coefficient represents the average monthly growth trend. In this case, sales are trending **{trend_direction}** by **{coef_abs:.2f} units per month**.
    """)

# ================= TAB 5: BUSINESS STRATEGY & RECOMMENDATIONS =================
with tabs[4]:
    st.markdown("<h3 class='section-title'>Data-Driven Business Recommendations</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    Based on the historical patterns extracted from the sales records of **Jaya Motors**, we present the following business strategies suitable for presentation at your college event:
    
    1. **Double Down on the Commuter Segment (Splendor+ Focus)**
       - **Observation:** `Splendor+` is the undisputed crown jewel of the dealership, contributing **163 units** (nearly 46% of all sales volume) and generating the highest revenue of **₹14.67 Lakhs**.
       - **Action:** Ensure high inventory levels of `Splendor+` and its XTEC variants at all times, especially before peak seasons, to prevent stockouts and capitalize on its high customer trust.
       
    2. **Leverage the October Festive Peak**
       - **Observation:** Sales peaked heavily in **October 2025 (45 units)** due to the festive season (Dussehra/Diwali in India), representing a major volume surge.
       - **Action:** Design special pre-festive promotional offers, finance schemes, and zero-down-payment plans starting in late September. Pre-book stocks from OEMs at least 30-45 days in advance.
       
    3. **Address Underperforming Models (Xoom & Vida EV)**
       - **Observation:** `Xoom` recorded the lowest sales volume of **1 unit**, and the electric `Vida VX2 Plus` sold only **3 units** over the year.
       - **Action:** 
         - Re-evaluate the marketing approach for the EV segment (`Vida`). Since EV has the highest dealer margin (**12%**), even a modest increase in EV sales will significantly boost profitability.
         - Offer test-ride events at local colleges or residential hubs to build consumer confidence in EV technology.
       
    4. **Seasonal Resource Allocation**
       - **Observation:** Monsoon season (July-September) saw average/flat demand, while Festive Autumn (October-November) saw the highest growth.
       - **Action:** Align marketing expenditures and dealership sales staff training schedules. Conduct staff training and vehicle maintenance camps during lower-demand monsoon months, and schedule maximum advertising and outdoor roadshows for the festive and winter seasons.
       
    5. **Optimize Dealer Profit Mix**
       - **Observation:** Different vehicle classes have different dealer margins (EV: 12%, Commuter: 8%). 
       - **Action:** Incentivize sales representatives with slightly higher commissions on premium bikes (X Pulse 200, Xtreme 125R) and EV scooters (Vida VX2 Plus) because they bring in higher absolute profits per unit sold.
    """)

# Footer credits
st.markdown("<hr style='margin: 40px 0 10px 0;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 12px;'>Jaya Motors Sales Analytics Dashboard • Created for College Event Demonstration • Powered by Streamlit & Scikit-Learn</p>", unsafe_allow_html=True)
