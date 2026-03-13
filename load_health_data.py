import pandas as pd
from sqlalchemy import create_engine

# 1. Professional Database Credentials
# Update the password to the one you set for the health_admin user in pgAdmin
USER = 'health_admin'
PASSWORD = 'vineeth123'
HOST = 'localhost'
PORT = '5432'  # Default port for PostgreSQL
DATABASE = 'health_ecommerce_db'

print("Initializing PostgreSQL connection...")

# 2. Create the SQLAlchemy Engine
# Notice the connection string now specifically calls postgresql and psycopg2
connection_string = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(connection_string)

# 3. Read the generated CSVs
print("Reading CSV files...")
df_web = pd.read_csv('../web_sessions.csv')
df_claims = pd.read_csv('../claims_transactions.csv')

# Mentor Tip: Force Pandas to format the timestamp perfectly for PostgreSQL
print("Formatting data types...")
df_web['session_timestamp'] = pd.to_datetime(df_web['session_timestamp'])

print("Loading data into PostgreSQL. This might take a few seconds...")

# 4. Push the data to Postgres (The simplified, modern Pandas approach)
try:
    # Pass the connection_string DIRECTLY to pandas.
    # Pandas will safely create and close the engine under the hood.
    df_web.to_sql(name='web_sessions', con=connection_string, if_exists='append', index=False)
    print("Success: Loaded 10,000 rows into 'web_sessions'.")

    df_claims.to_sql(name='claims_transactions', con=connection_string, if_exists='append', index=False)
    print("Success: Loaded 10,000 rows into 'claims_transactions'.")

    print("\nETL Pipeline Complete! Data is ready for analysis.")

except Exception as e:
    print(f"\nAn error occurred: {e}")