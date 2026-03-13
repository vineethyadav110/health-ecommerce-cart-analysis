import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# 1. Page Configuration (Sets up the web page title and layout width)
st.set_page_config(page_title="Health E-Commerce Analytics", layout="wide")

st.title("🩺 Digital Pharmacy Checkout & Claims Analysis")
st.markdown("""
**Business Problem:** Patients are abandoning their digital shopping carts at a high rate. 
This dashboard queries our live PostgreSQL database to determine if backend EDI 837/835 insurance claim rejections are driving the drop-off.
""")


# 2. Secure Database Connection & Caching
@st.cache_data
def load_data():
    # Using the exact credentials from your PostgreSQL setup
    USER = 'health_admin'
    PASSWORD = 'secure_password_123'
    HOST = 'localhost'
    PORT = '5432'
    DATABASE = 'health_ecommerce_db'

    connection_string = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    engine = create_engine(connection_string)

    # The exact SQL insight query we tested in pgAdmin
    query = """
    SELECT 
        COALESCE(c.rejection_reason, 'Claim Approved') AS insurance_outcome,
        COUNT(w.session_id) AS total_checkout_attempts,
        SUM(CASE WHEN w.checkout_status = 'Abandoned' THEN 1 ELSE 0 END) AS total_abandoned,
        ROUND(
            (SUM(CASE WHEN w.checkout_status = 'Abandoned' THEN 1 ELSE 0 END)::DECIMAL / COUNT(w.session_id)) * 100, 
        2) AS abandonment_rate_percentage
    FROM 
        web_sessions w
    INNER JOIN 
        claims_transactions c ON w.session_id = c.session_id
    GROUP BY 
        COALESCE(c.rejection_reason, 'Claim Approved')
    ORDER BY 
        abandonment_rate_percentage DESC;
    """

    # Pandas executes the query and returns a DataFrame
    df = pd.read_sql(query, engine)
    return df


# Load the data into the app
df_insights = load_data()

# 3. Build the Visualization using Plotly
st.subheader("Cart Abandonment Rate by Insurance Outcome")

# Create an interactive bar chart
fig = px.bar(
    df_insights,
    x='insurance_outcome',
    y='abandonment_rate_percentage',
    text='abandonment_rate_percentage',
    color='abandonment_rate_percentage',
    color_continuous_scale='Reds',  # Visually highlights the highest drop-off in dark red
    labels={
        'insurance_outcome': 'Insurance Outcome (EDI Status)',
        'abandonment_rate_percentage': 'Abandonment Rate (%)'
    }
)

# Format the chart to look clean and professional
fig.update_traces(textposition='outside', texttemplate='%{text}%')
fig.update_layout(yaxis_range=[0, 100])  # Locks the Y-axis to 100%

# Render the chart on the webpage
st.plotly_chart(fig, use_container_width=True)

# 4. Display the Raw SQL Data Table
st.subheader("Underlying Database Extract")
st.dataframe(df_insights, use_container_width=True)

# 5. Business Recommendation (The Analyst's Conclusion)
st.info("""
**💡 Analyst Recommendation:** The data clearly shows that 'Prior Auth Required' denials cause the most significant cart abandonment. 
I recommend the engineering team implement a "Save Cart & Verify" UI feature that holds the patient's cart 
and triggers an automated SMS once their doctor clears the authorization, rather than forcing a hard checkout failure.
""")