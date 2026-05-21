import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Uber NCR Analytics Dashboard", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Replace with your actual file path
    df = pd.read_csv('ncr_ride_bookings.csv')

    # Cleaning IDs and Datetime
    df['Booking ID'] = df['Booking ID'].str.strip('"')
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
    df['Hour'] = df['DateTime'].dt.hour
    df['Month'] = df['DateTime'].dt.month_name()
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Dashboard")
vehicle_filter = st.sidebar.multiselect(
    "Select Vehicle Type:",
    options=df["Vehicle Type"].unique(),
    default=df["Vehicle Type"].unique()
)

df_selection = df[df["Vehicle Type"].isin(vehicle_filter)]

# --- MAIN DASHBOARD ---
st.title("Uber NCR Ride Analytics")
st.markdown("Interactive overview of booking patterns, revenue, and cancellations.")

# --- TOP KPI METRICS ---
total_bookings = len(df_selection)
completed_rides = len(df_selection[df_selection["Booking Status"] == "Completed"])
completion_rate = (completed_rides / total_bookings) * 100
total_rev = df_selection[df_selection["Booking Status"] == "Completed"]["Booking Value"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Bookings", f"{total_bookings:,}")
col2.metric("Completion Rate", f"{completion_rate:.1f}%")
col3.metric("Total Revenue", f"₹{total_rev:,.0f}")
col4.metric("Avg Ride Distance", f"{df_selection['Ride Distance'].mean():.2f} km")

st.divider()

# --- SECTION 1: STATUS AND REVENUE ---
left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Booking Status Distribution")
    status_df = df_selection["Booking Status"].value_counts().reset_index()
    fig_status = px.pie(status_df, values='count', names='Booking Status',
                        hole=0.4, color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig_status, use_container_width=True)

with right_column:
    st.subheader("Revenue by Vehicle Type")
    rev_by_vehicle = df_selection[df_selection["Booking Status"] == "Completed"].groupby("Vehicle Type")[
        "Booking Value"].sum().reset_index()
    fig_rev = px.bar(rev_by_vehicle, x="Vehicle Type", y="Booking Value",
                     text_auto='.2s', color="Vehicle Type", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_rev, use_container_width=True)

# --- SECTION 2: PEAK HOURS PER VEHICLE ---
st.subheader("Peak Booking Hours per Vehicle")
hourly_veh = df_selection.groupby(['Hour', 'Vehicle Type']).size().reset_index(name="Count")
fig_hour_veh = px.line(hourly_veh, x="Hour", y="Count", color="Vehicle Type", markers=True,
                       line_shape="spline", title="Hourly Demand Spikes by Category")
st.plotly_chart(fig_hour_veh, use_container_width=True)

# --- SECTION 3: REVENUE LEAKAGE ---
st.header("Revenue Leakage Analysis")
avg_val = df_selection[df_selection["Booking Status"] == "Completed"]["Booking Value"].mean()
leakage = df_selection[df_selection["Booking Status"] != "Completed"].groupby("Vehicle Type").size().reset_index(name="Lost Rides")
leakage["Estimated Loss"] = leakage["Lost Rides"] * avg_val

fig_leak = px.bar(leakage, x="Vehicle Type", y="Estimated Loss",
                  title="Estimated Revenue Lost to Cancellations (INR)",
                  text_auto='.2s', color_discrete_sequence=['#E05252'])
st.plotly_chart(fig_leak, use_container_width=True)

# --- SECTION 4: LOCATION ANALYSIS ---
st.header("Cancellation Hotspots")
loc_fail = df_selection[df_selection["Booking Status"] != "Completed"].groupby("Pickup Location").size().reset_index(name="Failures")
loc_fail = loc_fail.sort_values(by="Failures", ascending=False).head(10)
fig_loc = px.bar(loc_fail, x="Failures", y="Pickup Location", orientation='h',
                 title="Top 10 Locations with Highest Cancellation Volume", color="Failures", color_continuous_scale="Reds")
st.plotly_chart(fig_loc, use_container_width=True)

# --- SECTION 5: CANCELLATION REASONS ---
st.divider()
st.subheader("Deep Dive: Cancellation Reasons")
cancel_col1, cancel_col2 = st.columns(2)

with cancel_col1:
    cust_cancel = df_selection['Reason for cancelling by Customer'].value_counts().reset_index()
    fig_cust = px.bar(cust_cancel, x='count', y='Reason for cancelling by Customer', orientation='h',
                      title="Customer Reasons", color_discrete_sequence=['#E05252'])
    st.plotly_chart(fig_cust, use_container_width=True)

with cancel_col2:
    driver_cancel = df_selection['Driver Cancellation Reason'].value_counts().reset_index()
    fig_driv = px.bar(driver_cancel, x='count', y='Driver Cancellation Reason', orientation='h',
                      title="Driver Reasons", color_discrete_sequence=['#F5A623'])
    st.plotly_chart(fig_driv, use_container_width=True)