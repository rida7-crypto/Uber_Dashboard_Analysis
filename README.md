# Uber NCR Ride Analytics Dashboard

An interactive, AI-accelerated data engineering and analytics application built to analyze high-volume rideshare transactional data. This dashboard processes over 150,000 simulated ride bookings in the National Capital Region (NCR), India, to uncover critical insights regarding demand patterns, cancellation hot spots, and revenue loss.

## Project Overview & Features

* **Executive KPI Tracking:** Displays high-level business metrics including Total Bookings (150K), Ride Completion Rate (62%), Total Revenue (₹47.2M), and Average Ride Distance (24.64 km) with real-time sidebar filtering by vehicle type.
* **Booking Status Distribution:** Visualizes the breakdown of successfully completed rides versus various cancellation types (by driver, customer, or no driver found).
* **Revenue Analysis:** Compares overall booking value contributions across different vehicle categories (Auto, Bike, Go Mini, Go Sedan, Premier Sedan, Uber XL, eBike).
* **Peak Hourly Demand Spikes:** Tracks time-of-day performance to pinpoint exactly when and where fleet optimization is required.
* **Revenue Leakage Analysis:** Pinpoints financial losses in INR stemming directly from driver and customer cancellations.
* **Geospatial Cancellation Hotspots:** Highlights the top 10 pickup locations (such as Pragati Maidan, Saket, and Vinobapuri) experiencing the highest failure rates.
* **Granular Deep Dives:** Breaks down specific categorical reasons behind cancellations for both drivers and customers.

## Tech Stack & Tools

* **Language:** Python 100%
* **Framework:** Streamlit (for UI layout and interactive state management)
* **Data Processing:** Pandas
* **Data Visualization:** Plotly (Express and Graph Objects)
* **Development Acceleration:** Leveraged AI pair-programming tools for rapid prototyping, complex dashboard callback logic optimization, and UI refinement.

## Dataset Credit

The foundational rideshare transactional data used to build and populate this dashboard was sourced from **Kaggle**.

## Getting Started

### Prerequisites
Make sure you have Python installed on your machine along with the required libraries:
```bash
pip install streamlit pandas plotly
```

Running the Application
Clone this repository to your local machine.

Navigate to the project directory.

Run the following command in your terminal:
```bash
streamlit run Dashboard.py
```
