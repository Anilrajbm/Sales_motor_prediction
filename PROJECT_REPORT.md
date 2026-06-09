# Jaya Motors Sales Analytics - Data Mining Project Report

This report outlines the methodology, dataset structure, analytical insights, predictive modeling, and business recommendations for the **Jaya Motors Sales Analytics** project. It serves as a comprehensive and standard project report for academic and professional presentation.

---

## 1. Introduction & Project Overview

Jaya Motors is a multi-brand two-wheeler dealership. To optimize inventory, increase profits, and forecast future demand, we designed and implemented a data mining and business intelligence pipeline. The primary objective is to clean unstructured, monthly sales data, extract key performance metrics across categories and individual models, and build a machine learning model to predict sales trends for subsequent months.

### Project Directory Structure
```text
Data_mining/
│
├── JAYA MOTORS SALE.xlsx        # Raw input Excel sales records
├── processed_sales_data.csv     # Cleaned, melted, and processed dataset (output of ETL)
├── requirements.txt             # Project software dependencies
│
├── data_processing.py           # ETL script (Python, Pandas)
├── app.py                       # Streamlit web application dashboard
└── PROJECT_REPORT.md            # Project report (this file)
```

---

## 2. Dataset Structure & Data Dictionary

The pipeline processes monthly sales volumes for 12 vehicle models over 13 consecutive months (April 2025 to April 2026). The processed dataset `processed_sales_data.csv` contains the following schema:
152 records with 10 attributes Date,Month,Vehicle,Units_Sold,Price,Revenue,Profit,Category,Demand,Season

| Column | Type | Origin | Description |
| :--- | :--- | :--- | :--- |
| **Date** | Date | Derived | Chronological index representing the first day of each month (e.g., `2025-04-01`). |
| **Month** | String | Cleaned | Formatted Month and Year (e.g., `April 2025`). |
| **Vehicle** | String | Cleaned | Standardized vehicle model name. |
| **Units_Sold** | Integer | Raw | Number of units sold. Missing records are imputed as `0`. |
| **Price** | Integer | Mapped | Showroom invoice price in INR. |
| **Revenue** | Integer | Calculated | Total gross sales calculated as: `Units_Sold × Price`. |
| **Profit** | Integer | Calculated | Dealer profit calculated as: `Revenue × Dealer Margin`. |
| **Category** | String | Mapped | Vehicle classification: *Commuter Motorcycle*, *Sports/Premium Motorcycle*, *Scooter*, *EV Scooter*. |
| **Demand** | String | Calculated | Volume classification: `Low` (0-2 units), `Medium` (3-7 units), `High` (8+ units). |
| **Season** | String | Derived | Seasonal grouping: *Summer* (Apr-Jun), *Monsoon* (Jul-Sep), *Festive/Autumn* (Oct-Nov), *Winter* (Dec-Feb), *Spring* (Mar). |

---

## 3. Data Preprocessing & ETL Pipeline

The preprocessing logic in `data_processing.py` executes the following operations:
1. **Extraction**: Reads raw rows from `JAYA MOTORS SALE.xlsx`. It drops administrative headers, blank rows, and total summary records to ensure data integrity.
2. **Melting**: Converts the wide-format Excel layout (where months are individual columns) into a tidy, tabular long-format layout utilizing `pandas.melt`.
3. **Data Cleaning**: Corrects typographical errors in raw text (such as mapping `NAVEMBER` to `November`) and removes leading/trailing whitespaces.
4. **Calculations**: Mapped showroom prices (ranging from ₹70,000 for HF100 to ₹1,80,000 for X Pulse 200) and category-based dealer profit margins:
   - *EV Scooter*: 12% margin
   - *Sports/Premium Motorcycle*: 10% margin
   - *Scooter*: 9% margin
   - *Commuter Motorcycle*: 8% margin
5. **Categorization**: Groups individual vehicle models and flags demand levels per row based on units sold.
6. **Export**: Saves the resulting structure to `processed_sales_data.csv`.

---

## 4. Key Performance Insights (Data Analysis)

The following tables and figures represent the exact mined parameters from the historical sales records:

### 4.1 Overall Performance Metrics
* **Total Sales Volume**: **352 units**
* **Total Gross Revenue**: **₹3,24,49,000** (₹3.24 Crores)
* **Total Estimated Profit**: **₹26,60,150** (₹26.60 Lakhs)
* **Best-Selling Vehicle**: **Splendor+** with **163 units** sold (46.3% of total volume).
* **Lowest-Selling Vehicle**: **Xoom** with **1 unit** sold.
* **Highest-Revenue Vehicle**: **Splendor+** contributing **₹1,46,70,000** (₹1.46 Crores) to gross revenue.
* **Peak Sales Month**: **October 2025** with **45 units** sold (Festive Autumn).
* **Lowest Sales Month**: **July 2025** with **12 units** sold (Heavy Monsoon).

### 4.2 Category-Wise Performance Summary
| Category | Units Sold | Revenue (INR) | Estimated Profit (INR) | Volume Share |
| :--- | :---: | :---: | :---: | :---: |
| **Commuter Motorcycle** | 319 | ₹2,85,96,000 | ₹22,87,680 | 90.62% |
| **Scooter** | 18 | ₹17,63,000 | ₹1,58,670 | 5.11% |
| **Sports/Premium Motorcycle** | 13 | ₹18,50,000 | ₹1,85,000 | 3.69% |
| **EV Scooter** | 2 | ₹2,40,000 | ₹28,800 | 0.57% |
| **Total / Average** | **352** | **₹3,24,49,000** | **₹26,60,150** | **100.00%** |

### 4.3 Detailed Vehicle Model Performance Summary
| Vehicle Model | Units Sold | Price (INR) | Revenue (INR) | Profit (INR) | Margin | Segment |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Splendor+** | 163 | ₹90,000 | ₹1,46,70,000 | ₹11,73,600 | 8% | Commuter Motorcycle |
| **Passion+** | 55 | ₹95,000 | ₹52,25,000 | ₹4,18,000 | 8% | Commuter Motorcycle |
| **Splendor+ XTEC** | 52 | ₹98,000 | ₹50,96,000 | ₹4,07,680 | 8% | Commuter Motorcycle |
| **HF100** | 44 | ₹70,000 | ₹30,80,000 | ₹2,46,400 | 8% | Commuter Motorcycle |
| **Destini 125** | 10 | ₹1,05,000 | ₹10,50,000 | ₹94,500 | 9% | Scooter |
| **Xtreme 125R** | 7 | ₹1,10,000 | ₹7,70,000 | ₹77,000 | 10% | Sports/Premium Motorcycle |
| **X Pulse 200** | 6 | ₹1,80,000 | ₹10,80,000 | ₹1,08,000 | 10% | Sports/Premium Motorcycle |
| **Super Splendor XTEC** | 5 | ₹1,05,000 | ₹5,25,000 | ₹42,000 | 8% | Commuter Motorcycle |
| **Pleasure XTEC** | 4 | ₹92,000 | ₹3,68,000 | ₹33,120 | 9% | Scooter |
| **Pleasure+** | 3 | ₹85,000 | ₹2,55,000 | ₹22,950 | 9% | Scooter |
| **Vida VX2 Plus** | 2 | ₹1,20,000 | ₹2,40,000 | ₹28,800 | 12% | EV Scooter |
| **Xoom** | 1 | ₹90,000 | ₹90,000 | ₹8,100 | 9% | Scooter |

### 4.4 Monthly Sales Trend
| Date Index | Month | Units Sold | Revenue (INR) | Estimated Profit (INR) | Season |
| :---: | :--- | :---: | :---: | :---: | :--- |
| 1 | April 2025 | 20 | ₹18,91,000 | ₹1,55,930 | Summer |
| 2 | May 2025 | 21 | ₹20,52,000 | ₹1,71,010 | Summer |
| 3 | June 2025 | 18 | ₹15,41,000 | ₹1,23,280 | Summer |
| 4 | July 2025 | 12 | ₹11,45,000 | ₹99,300 | Monsoon |
| 5 | August 2025 | 29 | ₹26,55,000 | ₹2,20,440 | Monsoon |
| 6 | September 2025 | 42 | ₹39,13,000 | ₹3,17,490 | Monsoon |
| 7 | October 2025 | 45 | ₹41,91,000 | ₹3,40,830 | Festive/Autumn |
| 8 | November 2025 | 23 | ₹20,81,000 | ₹1,73,480 | Festive/Autumn |
| 9 | December 2025 | 21 | ₹19,34,000 | ₹1,61,570 | Winter |
| 10 | January 2026 | 36 | ₹33,29,000 | ₹2,73,090 | Winter |
| 11 | February 2026 | 29 | ₹26,41,000 | ₹2,12,200 | Winter |
| 12 | March 2026 | 37 | ₹34,17,000 | ₹2,78,810 | Spring |
| 13 | April 2026 | 19 | ₹16,59,000 | ₹1,32,720 | Summer |

---

## 5. Predictive Machine Learning Model

We trained a **Simple Linear Regression** model to predict the dealership's future sales volume.

### Model Setup:
* **Independent Variable ($X$)**: Month Index (1 = April 2025, 13 = April 2026).
* **Dependent Variable ($y$)**: Aggregated Monthly Units Sold.
* **Equation**: $y = \beta_0 + \beta_1 X$

### Regression Parameters (Fitted on 13 Months of Data):
* **Baseline Intercept ($\beta_0$)**: **21.12 units**
* **Growth Rate / Slope ($\beta_1$)**: **+0.85 units/month**
* **Trend Interpretation**: The dealership shows a steady upward sales trajectory, increasing by an average of **0.85 units per month**.

### 3-Month Demand Forecast:
1. **May 2026 (Month 14)**: Projected **33.04 units** (Rounded to **33 units**)
2. **June 2026 (Month 15)**: Projected **33.89 units** (Rounded to **34 units**)
3. **July 2026 (Month 16)**: Projected **34.74 units** (Rounded to **35 units**)

---

## 6. Business Strategy & Recommendations

1. **Secure Commuter Inventory**: The commuter motorcycle segment generates **90.62% of sales volume** and **86% of profits**. Stabilizing inventory for high-demand models like `Splendor+` and `Passion+` is critical to preventing stockouts.
2. **Festive Scaling**: October sales are **125% higher** than the yearly monthly average (~20 units/month). Preparing promotional campaigns and bank loan tie-ups by mid-September will capture peak consumer purchase intent.
3. **Expand EV Marketing**: Although EV scooters (`Vida VX2 Plus`) have the highest profit margin per unit (**12%**), they account for only **0.57% of total sales volume**. Focused marketing campaigns, test rides, and exchange offers can significantly enhance dealership profitability.
4. **Targeted Seasonal Sales**: The low-performing monsoon season (e.g., July) should focus on secondary revenue streams (servicing and parts sales) and customer relationship programs to prepare for the autumn upswing.
