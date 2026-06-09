# 🏍️ Dyuthi Motors - Sales Analytics & Predictive Dashboard

An interactive Data Mining and Business Intelligence dashboard built with Python, Streamlit, and Scikit-Learn to analyze, visualize, and forecast sales trends for **Dyuthi Motors** (a multi-brand two-wheeler dealership).

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [Project Structure](#-project-structure)
4. [Dataset & Data Schema](#-dataset--data-schema)
5. [Installation & Setup](#-installation--setup)
6. [How to Run](#-how-to-run)
7. [Key Business Insights](#-key-business-insights)
8. [Predictive Modeling](#-predictive-modeling)

---

## 🌟 Project Overview
This project processes raw, unstructured monthly sales sheets into a structured data warehouse, extracts key dealership performance metrics, builds machine learning forecasting models, and serves them via a modern, interactive web dashboard. 

The application is designed to help dealership managers optimize vehicle stock levels, prepare for seasonal surges (such as the Diwali/Dussehra festive season), and target high-margin vehicle segments.

---

## 🚀 Key Features
* **ETL Pipeline**: Cleans, merges, and reshapes raw Excel spreadsheets into a normalized database.
* **Interactive Dashboard**: Premium UI built with Streamlit featuring responsive metrics cards, data tables, and dynamic filters.
* **Rich Visualizations**: Real-time sales volume lines, revenue shares, model popularity charts, and monthly heatmaps powered by Plotly.
* **Predictive Analytics**: A 3-Month sales volume forecast generated using a Linear Regression model.
* **Business Recommendations**: Actionable strategies to maximize profitability across commuter, premium, and EV categories.

---

## 📁 Project Structure
```text
Data_mining/
│
├── Dyuthi MOTORS SALE.xlsx        # Raw input Excel sales records
├── processed_sales_data.csv       # Cleaned, melted, and structured dataset (ETL output)
├── requirements.txt               # Python package dependencies
│
├── data_processing.py             # Data extraction, cleaning, and transformation script
├── app.py                         # Streamlit dashboard application
├── PROJECT_REPORT.md              # Detailed academic/professional report
└── README.md                      # Project documentation (this file)
```

---

## 📊 Dataset & Data Schema
The dataset consists of **152 sales records** covering **12 vehicle models** over **13 consecutive months** (April 2025 to April 2026).

| Column | Type | Description |
| :--- | :--- | :--- |
| **Date** | Date | First day of each month (e.g., `2025-04-01`). |
| **Vehicle** | String | Standardized vehicle model name (e.g., Splendor+, Vida VX2 Plus). |
| **Units_Sold** | Integer | Quantity of vehicles sold. |
| **Revenue** | Integer | Total revenue calculated as: `Units_Sold × Invoice Price`. |
| **Profit** | Integer | Dealer profit calculated based on category margins. |
| **Category** | String | Vehicle type (Commuter, Sports/Premium, Scooter, EV Scooter). |
| **Season** | String | Seasonal group (Summer, Monsoon, Festive/Autumn, Winter, Spring). |

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.8 or higher installed on your system.

### Steps
1. **Clone or download the project** and open your terminal in the directory:
   ```bash
   cd OneDrive/Desktop/Data_mining
   ```

2. **Install the required libraries**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃 How to Run

### Step 1: Run the ETL Pipeline (Data Processing)
Run this command to clean the raw Excel file and generate the processed CSV:
```bash
python data_processing.py
```

### Step 2: Launch the Analytics Dashboard
Launch the Streamlit web dashboard in your browser:
```bash
streamlit run app.py
```

---

## 💡 Key Business Insights
* **Total Sales Volume**: **352 units** sold over the 13-month period.
* **Total Gross Revenue**: **₹3.24 Crores** (₹3,24,49,000).
* **Estimated Net Profit**: **₹26.60 Lakhs** (₹26,60,150).
* **Top Seller**: **Splendor+** represents **46.3%** of all sales (163 units sold).
* **Peak Sales Season**: **October 2025** recorded a peak of **45 units** sold due to autumn festive demand.

---

## 🔮 Predictive Modeling
A **Simple Linear Regression** model predicts overall sales trends based on historical timelines:
* **Growth Rate**: An average sales growth of **+0.85 units per month**.
* **3-Month Forecast**:
  * **May 2026**: ~33 units
  * **June 2026**: ~34 units
  * **July 2026**: ~35 units
