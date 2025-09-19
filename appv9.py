import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="CRISIL AML Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Custom CSS for Professional Look -----------------
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79, #2d5aa0);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #1f4e79;
        margin-bottom: 1rem;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .metric-number {
        font-size: 3rem;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 1.1rem;
        color: #666;
        margin: 0;
    }
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .executive-summary {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
        padding: 2rem;
        border-left: 5px solid #28a745;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #f1f3f4, #e8eaed);
        border-radius: 20px;
        padding: 15px 30px;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1f4e79, #2d5aa0);
        color: white !important;
        box-shadow: 0 4px 15px rgba(31,78,121,0.3);
    }
    .alert-box {
        background: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background: #d1edff;
        border: 2px solid #0066cc;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa, #e9ecef);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Data Generation Functions -----------------
def calculate_next_review_date(last_review_date, risk_category):
    """Calculate next review date based on risk category"""
    if risk_category == "High":
        return last_review_date + timedelta(days=365)
    elif risk_category == "Medium":
        return last_review_date + timedelta(days=1095)
    else:
        return last_review_date + timedelta(days=1825)

def generate_enhanced_mock_data(month, year):
    """Generate comprehensive mock data"""
    np.random.seed(year + month)
    random.seed(year + month)
    
    client_count = 27
    countries = ["India", "Mauritius", "Singapore", "UAE", "UK", "Panama", "Qatar", "China", "USA", "Switzerland"]
    industries = ["Defence", "Material", "Co-operative", "Banking", "Trading", "Real Estate", "Financial Services", "IT Services"]
    
    # Create structured data based on report
    client_data = []
    
    # High Risk: 11 clients (5 Defence + 6 Material)
    for i in range(11):
        subcat = "Defence" if i < 5 else "Material"
        is_new = i < 5  # 5 new high risk clients
        client_data.append({
            "Risk_Category": "High",
            "Subcategory": subcat,
            "Is_New": is_new
        })
    
    # Medium Risk: 11 clients (3 Co-operative + 8 Material)  
    for i in range(11):
        subcat = "Co-operative" if i < 3 else "Material"
        is_new = i < 1  # 1 new medium risk
        client_data.append({
            "Risk_Category": "Medium",
            "Subcategory": subcat,
            "Is_New": is_new
        })
    
    # Low Risk: 5 clients
    for i in range(5):
        client_data.append({
            "Risk_Category": "Low",
            "Subcategory": "Low Risk",
            "Is_New": False
        })
    
    # Generate DataFrame
    base_date = datetime(year, month, 1)
    data_rows = []
    
    for i, client_info in enumerate(client_data):
        if client_info["Is_New"]:
            days_back = random.randint(1, 30)
        else:
            if client_info["Risk_Category"] == "High":
                days_back = random.randint(30, 365)
            elif client_info["Risk_Category"] == "Medium":
                days_back = random.randint(180, 1095)
            else:
                days_back = random.randint(365, 1825)
        
        review_date = base_date - timedelta(days=days_back)
        
        # Status assignment
        if month == 5 and year == 2025 and i < 3:
            status = random.choice(["NCC", "Suspended", "Withdrawn"])
        else:
            status = "Active"
        
        data_rows.append({
            "Client_ID": f"C{str(i+1).zfill(3)}",
            "Client_Name": f"Client_{i+1}",
            "Country": np.random.choice(countries),
            "Industry": client_info["Subcategory"],
            "Risk_Category": client_info["Risk_Category"],
            "Subcategory": client_info["Subcategory"],
            "Last_Reviewed": review_date,
            "Status": status,
            "Is_New_Client": client_info["Is_New"],
            "GST_PAN_Verified": random.choice([True, False]) if client_info["Is_New"] else True,
            "Sanctions_Checked": True,
            "Dow_Jones_Alert": False,
            "Month": month,
            "Year": year,
            "Business_Vertical": random.choice(["Ratings", "Research", "Advisory", "Risk Solutions"]),
            "AUM_Million_USD": random.randint(10, 500),
            "Last_Transaction_Date": review_date + timedelta(days=random.randint(1, 30))
        })
    
    df = pd.DataFrame(data_rows)
    df["Next_Review"] = df.apply(
        lambda row: calculate_next_review_date(row["Last_Reviewed"], row["Risk_Category"]), 
        axis=1
    )
    
    current_date = datetime.now()
    df["Days_Until_Review"] = (df["Next_Review"] - current_date).dt.days
    
    return df

# ----------------- Load Data -----------------
@st.cache_data
def load_all_data():
    data_may_2025 = generate_enhanced_mock_data(5, 2025)
    data_apr_2025 = generate_enhanced_mock_data(4, 2025) 
    data_may_2024 = generate_enhanced_mock_data(5, 2024)
    return pd.concat([data_may_2025, data_apr_2025, data_may_2024])

all_data = load_all_data()

# ----------------- Header -----------------
st.markdown("""
<div class="main-header">
    <h1>🏢 CRISIL - AML Risk Management Dashboard</h1>
    <h3>Executive Anti-Money Laundering Risk Assessment & Monitoring</h3>
</div>
""", unsafe_allow_html=True)

# ----------------- Sidebar -----------------
with st.sidebar:
    st.markdown("### 📊 Dashboard Controls")
    
    selected_year = st.selectbox("📅 Select Year", options=sorted(all_data["Year"].unique(), reverse=True))
    selected_month = st.selectbox("📅 Select Month", options=sorted(all_data["Month"].unique(), reverse=True))
    
    st.markdown("---")
    st.markdown("### 🔍 Advanced Filters")
    
    selected_countries = st.multiselect(
        "🌍 Countries", 
        options=sorted(all_data["Country"].unique()), 
        default=sorted(all_data["Country"].unique())
    )
    
    selected_industries = st.multiselect(
        "🏭 Industries", 
        options=sorted(all_data["Industry"].unique()), 
        default=sorted(all_data["Industry"].unique())
    )
    
    show_only_active = st.checkbox("Show Active Clients Only", value=True)
    
    # Quick Stats in Sidebar
    current_data = all_data[(all_data["Year"] == selected_year) & (all_data["Month"] == selected_month)]
    if show_only_active:
        current_data = current_data[current_data["Status"] == "Active"]
    
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    st.metric("Total Clients", len(current_data))
    st.metric("New This Month", len(current_data[current_data["Is_New_Client"] == True]))
    st.metric("High Risk", len(current_data[current_data["Risk_Category"] == "High"]))

# Filter data
filtered_data = all_data[
    (all_data["Year"] == selected_year) &
    (all_data["Month"] == selected_month) &
    (all_data["Country"].isin(selected_countries)) &
    (all_data["Industry"].isin(selected_industries))
]

if show_only_active:
    filtered_data = filtered_data[filtered_data["Status"] == "Active"]

# ----------------- Main Dashboard Tabs -----------------
tab1, tab2 = st.tabs(["📊 Executive Summary", "📋 Detailed Analytics"])

# ====================== TAB 1: EXECUTIVE SUMMARY ======================
with tab1:
    
    # ----------------- Key Performance Indicators -----------------
    st.markdown("### 🎯 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_clients = len(filtered_data)
    new_clients = len(filtered_data[filtered_data["Is_New_Client"] == True])
    high_risk = len(filtered_data[filtered_data["Risk_Category"] == "High"])
    pending_reviews = len(filtered_data[filtered_data["Days_Until_Review"] <= 30])
    ncc_clients = len(all_data[(all_data["Status"].isin(["NCC", "Suspended", "Withdrawn"])) & 
                              (all_data["Year"] == selected_year) & 
                              (all_data["Month"] == selected_month)])
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number" style="color: #1f4e79;">📊<br>{total_clients}</div>
            <div class="metric-label">Total Active Clients</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number" style="color: #28a745;">➕<br>{new_clients}</div>
            <div class="metric-label">New Clients</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number" style="color: #dc3545;">🔴<br>{high_risk}</div>
            <div class="metric-label">High Risk Clients</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number" style="color: #ffc107;">⏰<br>{pending_reviews}</div>
            <div class="metric-label">Reviews Due (30d)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number" style="color: #6c757d;">⚠️<br>{ncc_clients}</div>
            <div class="metric-label">NCC/Inactive</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ----------------- Executive Charts Grid -----------------
    st.markdown("### 📊 Executive Risk Analysis")
    
    # Row 1: Risk Distribution and Portfolio Overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Risk Distribution Donut Chart
        risk_counts = filtered_data["Risk_Category"].value_counts()
        fig_risk = go.Figure(data=[go.Pie(
            labels=risk_counts.index, 
            values=risk_counts.values,
            hole=0.4,
            marker_colors=['#dc3545', '#ffc107', '#28a745']
        )])
        fig_risk.update_layout(
            title="Risk Category Distribution",
            font_size=12,
            height=300,
            showlegend=True,
            annotations=[dict(text=f'{total_clients}<br>Total', x=0.5, y=0.5, font_size=16, showarrow=False)]
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        # New vs Existing Clients
        new_vs_existing = filtered_data.groupby(['Risk_Category', 'Is_New_Client']).size().reset_index(name='Count')
        new_vs_existing['Client_Type'] = new_vs_existing['Is_New_Client'].map({True: 'New', False: 'Existing'})
        
        fig_new_existing = px.bar(
            new_vs_existing,
            x='Risk_Category',
            y='Count',
            color='Client_Type',
            title="New vs Existing Clients by Risk",
            color_discrete_map={'New': '#17a2b8', 'Existing': '#6c757d'},
            height=300
        )
        st.plotly_chart(fig_new_existing, use_container_width=True)
    
    with col3:
        # Geographic Distribution
        country_counts = filtered_data["Country"].value_counts().head(8)
        fig_geo = px.bar(
            x=country_counts.values,
            y=country_counts.index,
            orientation='h',
            title="Top Countries by Client Count",
            color=country_counts.values,
            color_continuous_scale='viridis',
            height=300
        )
        fig_geo.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_geo, use_container_width=True)
    
    # Row 2: Business Intelligence Charts
    col4, col5, col6 = st.columns(3)
    
    with col4:
        # Industry Risk Heatmap
        industry_risk = filtered_data.groupby(['Industry', 'Risk_Category']).size().unstack(fill_value=0)
        fig_heatmap = px.imshow(
            industry_risk.values,
            x=industry_risk.columns,
            y=industry_risk.index,
            title="Risk Heatmap by Industry",
            color_continuous_scale='RdYlGn_r',
            height=300
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col5:
        # Review Timeline - Next 6 Months
        current_date = datetime.now()
        six_months = current_date + timedelta(days=180)
        
        upcoming_data = filtered_data[
            (filtered_data["Next_Review"] >= current_date) & 
            (filtered_data["Next_Review"] <= six_months)
        ].copy()
        
        if not upcoming_data.empty:
            upcoming_data["Review_Month"] = upcoming_data["Next_Review"].dt.to_period("M")
            reviews_timeline = upcoming_data.groupby(["Review_Month", "Risk_Category"]).size().reset_index(name="Count")
            reviews_timeline["Review_Month"] = reviews_timeline["Review_Month"].astype(str)
            
            fig_timeline = px.area(
                reviews_timeline,
                x="Review_Month",
                y="Count", 
                color="Risk_Category",
                title="Upcoming Reviews (6 Months)",
                color_discrete_map={'High': '#dc3545', 'Medium': '#ffc107', 'Low': '#28a745'},
                height=300
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("No upcoming reviews in next 6 months")
    
    with col6:
        # Business Vertical Distribution
        vertical_counts = filtered_data["Business_Vertical"].value_counts()
        fig_vertical = px.pie(
            values=vertical_counts.values,
            names=vertical_counts.index,
            title="Distribution by Business Vertical",
            height=300
        )
        st.plotly_chart(fig_vertical, use_container_width=True)
    
    # ----------------- Management Summary Report -----------------
    st.markdown("### 📋 Executive Management Summary")
    
    col_summary, col_table = st.columns([2, 1])
    
    with col_summary:
        st.markdown("""
        <div class="executive-summary">
            <h4>🎯 Key Management Highlights</h4>
        </div>
        """, unsafe_allow_html=True)
        
        current_data = all_data[(all_data["Year"] == selected_year) & (all_data["Month"] == selected_month)]
        new_clients_total = len(current_data[current_data["Is_New_Client"] == True])
        new_medium = len(current_data[(current_data["Is_New_Client"] == True) & (current_data["Risk_Category"] == "Medium")])
        new_low = len(current_data[(current_data["Is_New_Client"] == True) & (current_data["Risk_Category"] == "Low")])
        unverified_gst = len(current_data[current_data["GST_PAN_Verified"] == False])
        
        st.markdown(f"""
        <div class="success-box">
            <h5>✅ Compliance Status</h5>
            <ul>
                <li><strong>No sanctions matches</strong> found in UNSC, OFAC, UAPA, S&P HRI lists</li>
                <li><strong>No Dow Jones alerts</strong> for non-Indian clients</li>
                <li><strong>All active clients</strong> have completed sanctions screening</li>
                <li><strong>{len(current_data)} total clients</strong> under active monitoring</li>
            </ul>
        </div>
        
        <div class="alert-box">
            <h5>⚠️ Action Items</h5>
            <ul>
                <li><strong>{unverified_gst} clients</strong> pending GST/PAN verification</li>
                <li><strong>{len(current_data[(current_data["Risk_Category"] == "High") & (current_data["Days_Until_Review"] <= 30)])} high-risk clients</strong> due for periodic review</li>
                <li><strong>{ncc_clients} clients</strong> reported as NCC/suspended/withdrawn</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        **📊 Monthly Statistics:**
        - **{new_clients_total} new clients** onboarded ({new_medium} medium risk, {new_low} low risk)
        - **{len(current_data[current_data["Subcategory"] == "Co-operative"])} co-operative clients** (all medium risk)
        - **2 clients migrated** from high to low risk due to resolved adverse information
        - **{len(current_data[current_data["Risk_Category"] == "High"])} high-risk clients** active with {len(current_data[(current_data["Risk_Category"] == "High") & (current_data["Days_Until_Review"] > 30)])} reviewed
        """)
    
    with col_table:
        # Risk Summary Table
        st.markdown("#### 📊 Risk Distribution Table")
        
        summary_data = []
        for risk in ["High", "Medium", "Low"]:
            risk_clients = current_data[current_data["Risk_Category"] == risk]
            for subcat in risk_clients["Subcategory"].unique():
                subcat_clients = risk_clients[risk_clients["Subcategory"] == subcat]
                new_count = len(subcat_clients[subcat_clients["Is_New_Client"] == True])
                existing_count = len(subcat_clients[subcat_clients["Is_New_Client"] == False])
                summary_data.append({
                    "Risk Category": risk,
                    "Subcategory": subcat,
                    "New": new_count,
                    "Existing": existing_count,
                    "Total": new_count + existing_count
                })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        # Total row
        total_new = summary_df["New"].sum()
        total_existing = summary_df["Existing"].sum()
        total_all = summary_df["Total"].sum()
        
        st.markdown(f"""
        **Totals:** {total_new} New | {total_existing} Existing | **{total_all} Total**
        """)

# ====================== TAB 2: DETAILED ANALYTICS ======================
with tab2:
    st.markdown("### 📋 Detailed Client Analytics & Management")
    
    # Sub-tabs for detailed analytics
    subtab1, subtab2, subtab3 = st.tabs(["🔍 Client Search & Details", "📅 Review Management", "📊 Advanced Analytics"])
    
    with subtab1:
        # Client Search and Detailed Information
        st.markdown("#### 🔍 Client Search & Information")
        
        col_search, col_filter = st.columns([2, 1])
        
        with col_search:
            search_client = st.text_input("🔍 Search Client", placeholder="Enter client name or ID...")
        
        with col_filter:
            risk_filter = st.selectbox("Filter by Risk", ["All", "High", "Medium", "Low"])
        
        # Apply search and filters
        if search_client:
            search_results = filtered_data[
                (filtered_data["Client_Name"].str.contains(search_client, case=False, na=False)) |
                (filtered_data["Client_ID"].str.contains(search_client, case=False, na=False))
            ]
        else:
            search_results = filtered_data
        
        if risk_filter != "All":
            search_results = search_results[search_results["Risk_Category"] == risk_filter]
        
        # Detailed Client Table
        if not search_results.empty:
            st.markdown("#### 📊 Client Details")
            
            display_columns = [
                "Client_ID", "Client_Name", "Risk_Category", "Industry", "Country", 
                "Status", "Business_Vertical", "Last_Reviewed", "Next_Review", "Days_Until_Review"
            ]
            
            styled_df = search_results[display_columns].copy()
            styled_df["Last_Reviewed"] = styled_df["Last_Reviewed"].dt.strftime('%Y-%m-%d')
            styled_df["Next_Review"] = styled_df["Next_Review"].dt.strftime('%Y-%m-%d')
            
            st.dataframe(
                styled_df,
                use_container_width=True,
                column_config={
                    "Days_Until_Review": st.column_config.NumberColumn(
                        "Days Until Review",
                        help="Days until next review (negative = overdue)",
                        format="%d days"
                    ),
                    "Risk_Category": st.column_config.SelectboxColumn(
                        "Risk Category",
                        options=["Low", "Medium", "High"]
                    )
                },
                hide_index=True
            )
            
            # Export button
            csv = styled_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Client Data as CSV",
                data=csv,
                file_name=f'crisil_aml_clients_{selected_year}_{selected_month}.csv',
                mime='text/csv'
            )
        else:
            st.warning("No clients found matching the search criteria.")
    
    with subtab2:
        # Review Management Details
        st.markdown("#### 📅 Review Management Dashboard")
        
        # Review Status Summary
        col1, col2, col3, col4 = st.columns(4)
        
        overdue = len(filtered_data[filtered_data["Days_Until_Review"] < 0])
        due_soon = len(filtered_data[(filtered_data["Days_Until_Review"] >= 0) & (filtered_data["Days_Until_Review"] <= 30)])
        due_later = len(filtered_data[(filtered_data["Days_Until_Review"] > 30) & (filtered_data["Days_Until_Review"] <= 90)])
        scheduled = len(filtered_data[filtered_data["Days_Until_Review"] > 90])
        
        with col1:
            st.metric("🔴 Overdue Reviews", overdue)
        with col2:
            st.metric("🟡 Due in 30 Days", due_soon)
        with col3:
            st.metric("🟠 Due in 90 Days", due_later)
        with col4:
            st.metric("🟢 Future Scheduled", scheduled)
        
        # Priority Review List
        st.markdown("#### ⚠️ Priority Reviews (Next 10)")
        
        current_date = datetime.now()
        priority_reviews = filtered_data[filtered_data["Next_Review"] >= current_date].nsmallest(10, "Next_Review")
        
        if not priority_reviews.empty:
            for idx, row in priority_reviews.iterrows():
                days_left = (row["Next_Review"] - current_date).days
                
                if days_left <= 0:
                    urgency_color = "#dc3545"
                    urgency_text = "🔴 OVERDUE"
                elif days_left <= 30:
                    urgency_color = "#ffc107"
                    urgency_text = "🟡 URGENT"
                elif days_left <= 90:
                    urgency_color = "#fd7e14"
                    urgency_text = "🟠 SOON"
                else:
                    urgency_color = "#28a745"
                    urgency_text = "🟢 SCHEDULED"
                
                st.markdown(f"""
                <div style="border-left: 5px solid {urgency_color}; padding: 15px; margin: 10px 0; 
                            background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0; color: #1f4e79;">{row['Client_Name']} ({row['Client_ID']})</h4>
                            <p style="margin: 5px 0; color: {urgency_color}; font-weight: bold;">
                                {row['Risk_Category']} Risk | {row['Industry']} | {row['Country']}
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <p style="margin: 0; font-weight: bold;">Next Review: {row['Next_Review'].strftime('%Y-%m-%d')}</p>
                            <p style="margin: 0; color: {urgency_color}; font-weight: bold;">({days_left} days) {urgency_text}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with subtab3:
        # Advanced Analytics
        st.markdown("#### 📊 Advanced Risk Analytics")
        
        # Advanced Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk Trend Analysis (if multiple periods available)
            if len(all_data["Month"].unique()) > 1:
                trend_data = all_data.groupby(["Year", "Month", "Risk_Category"]).size().reset_index(name="Count")
                trend_data["Period"] = trend_data["Year"].astype(str) + "-" + trend_data["Month"].astype(str).str.zfill(2)
                
                fig_trend = px.line(
                    trend_data,
                    x="Period",
                    y="Count",
                    color="Risk_Category",
                    title="Risk Category Trends Over Time",
                    color_discrete_map={'High': '#dc3545', 'Medium': '#ffc107', 'Low': '#28a745'}
                )
                st.plotly_chart(fig_trend, use_container_width=True)
        
        with col2:
            # Portfolio Composition by AUM
            aum_risk = filtered_data.groupby("Risk_Category")["AUM_Million_USD"].sum().reset_index()
            
            fig_aum = px.bar(
                aum_risk,
                x="Risk_Category",
                y="AUM_Million_USD",
                title="Assets Under Management by Risk Category",
                color="Risk_Category",
                color_discrete_map={'High': '#dc3545', 'Medium': '#ffc107', 'Low': '#28a745'}
            )
            fig_aum.update_layout(yaxis_title="AUM (Million USD)")
            st.plotly_chart(fig_aum, use_container_width=True)
        
        # Risk Correlation Matrix
        st.markdown("#### 🔗 Risk Correlation Analysis")
        
        # Create correlation data
        corr_data = filtered_data.copy()
        corr_data['Risk_Score'] = corr_data['Risk_Category'].map({'Low': 1, 'Medium': 2, 'High': 3})
        corr_data['Days_Overdue'] = corr_data['Days_Until_Review'].apply(lambda x: max(0, -x))
        corr_data['Is_High_AUM'] = (corr_data['AUM_Million_USD'] > corr_data['AUM_Million_USD'].median()).astype(int)
        
        # Correlation matrix for numerical columns
        numeric_cols = ['Risk_Score', 'Days_Overdue', 'AUM_Million_USD', 'Is_High_AUM']
        correlation_matrix = corr_data[numeric_cols].corr()
        
        fig_corr = px.imshow(
            correlation_matrix,
            title="Risk Factors Correlation Matrix",
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Summary Statistics Table
        st.markdown("#### 📈 Portfolio Summary Statistics")
        
        summary_stats = []
        for risk in ['High', 'Medium', 'Low']:
            risk_data = filtered_data[filtered_data['Risk_Category'] == risk]
            if len(risk_data) > 0:
                summary_stats.append({
                    'Risk Category': risk,
                    'Client Count': len(risk_data),
                    'Avg AUM (M USD)': f"{risk_data['AUM_Million_USD'].mean():.1f}",
                    'Total AUM (M USD)': f"{risk_data['AUM_Million_USD'].sum():.1f}",
                    'Countries': len(risk_data['Country'].unique()),
                    'Industries': len(risk_data['Industry'].unique()),
                    'Avg Days to Review': f"{risk_data['Days_Until_Review'].mean():.0f}"
                })
        
        stats_df = pd.DataFrame(summary_stats)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)

# ----------------- Footer -----------------
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 20px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 10px; margin-top: 2rem;">
    <p><strong>🏢 CRISIL AML Risk Management Dashboard</strong></p>
    <p>📊 Risk Management & Compliance Division | Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")} IST</p>
    <p><small>Confidential - For Internal Use Only</small></p>
</div>
""", unsafe_allow_html=True)