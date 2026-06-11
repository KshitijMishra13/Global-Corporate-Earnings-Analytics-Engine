# Global-Corporate-Earnings-Analytics-Engine
Engineered an end-to-end analytical pipeline to clean, transform, and process unstructured financial records for 10,859 global companies, normalizing unformatted text strings into uniform, floating-point numeric data structures.
Scrapped Link: https://companiesmarketcap.com/most-profitable-companies/

#PowerBI Dashboard
Dashboard: https://app.powerbi.com/links/X1m4EQIdOg?ctid=969d451d-17aa-4133-9e0d-e9122e7fc438&pbi_source=linkShare
<img width="1401" height="858" alt="Screenshot 2026-06-11 at 16 11 02" src="https://github.com/user-attachments/assets/31ce4f51-6f64-4b4c-a445-993573c1b411" />

#Tech Stack
ETL Engine: Python 3.11 (Pandas, NumPy)
Data Warehousing: MySQL (Staging layer)
Business Intelligence: Power BI Online (Star Schema modeling, DAX)

#Pipeline Highlights
Vectorized ETL: Memory-efficient text parsing into standardized numerical data types.
Outlier Engine: Isolated extreme financial anomalies using Interquartile Range (IQR) bounds.
Feature Engineering: Programmatically segmented companies into dynamic tier brackets.

#Star Schema Architecture
fact_earnings: Ranks, normalized earnings, stock prices, and anomaly flags.
dim_company: Company names, ticker symbols, and corporate tiers.
dim_geography: Country-level distribution tracking.

#Power BI Dashboard
Executive KPIs: Live visibility into total global wealth and corporate headcount.
Interactive Slicers: Instant cross-filtering by Corporate Tiers and Earnings Anomalies.
Performance Matrix: Detailed grid tracking companies by revenue and dynamic Revenue Share %.
