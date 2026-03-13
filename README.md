# 🩺 Digital Pharmacy Checkout & Claims Analysis

## 📌 Executive Summary
**The Business Problem:** A digital health e-commerce platform was experiencing a high rate of cart abandonment at checkout. 
**The Objective:** Determine if patient drop-off is driven by front-end user experience issues or back-end insurance claim rejections (simulated EDI 837/835 workflows).

This end-to-end data engineering and analytics project bridges digital retail behavior with back-office healthcare operations. I architected a relational database, engineered a synthetic data pipeline, and built a live interactive web dashboard to uncover the root cause of the sales funnel leak.

## 🏗️ Architecture & Tech Stack
* **Data Generation:** Python (`Faker`, `Pandas`) used to synthesize 10,000 relational records mapping web session data to patient insurance claims.
* **Database / Data Engineering:** Local PostgreSQL instance. Built an automated ETL pipeline using `SQLAlchemy` and `psycopg2` to load the data securely.
* **Analytics & Visualization:** `Streamlit` and `Plotly` used to query the PostgreSQL database live and deploy an interactive dashboard.

## 📊 Key Insights & Business Recommendation
![Streamllit_dashboard.png]

**The Discovery:**
Using SQL `INNER JOIN` operations and aggregation, the data revealed that standard claim denials (e.g., "Out of Network") caused a moderate 85% drop-off, but **"Prior Authorization Required" denials caused a massive 95% cart abandonment rate.**

**💡 Strategic Recommendation:**
Rather than forcing a hard checkout failure when an EDI transaction returns a "Prior Auth Required" code, the engineering team should implement a **"Save Cart & Verify"** UI feature. This holds the patient's cart and triggers an automated SMS flow once their physician clears the authorization with the clearinghouse.

## 🚀 How to Run Locally
1. Clone this repository.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt