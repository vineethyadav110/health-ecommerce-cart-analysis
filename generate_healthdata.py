import pandas as pd
import random
import uuid
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)  # Ensures our "random" data is reproducible

num_records = 10000

# Reference lists for our simulated healthcare e-commerce environment
insurance_providers = ['Aetna', 'BlueCross', 'UnitedHealthcare', 'Cigna', 'Humana', 'Kaiser Permanente']
rejection_reasons = ['Prior Auth Required', 'Out of Network', 'Coverage Inactive', 'Deductible Not Met']

web_sessions_data = []
claims_transactions_data = []

print("Generating synthetic health e-commerce data...")

for _ in range(num_records):
    # 1. Generate Shared Keys (The Bridge)
    session_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    # 2. Generate Front-End E-Commerce Data
    session_timestamp = fake.date_time_between(start_date='-6m', end_date='now')
    cart_value = round(random.uniform(15.00, 500.00), 2)

    # 3. Generate Back-End Healthcare Claims Data
    claim_id = str(uuid.uuid4())
    provider = random.choice(insurance_providers)

    # Simulate a 75% claim approval rate
    is_approved = random.random() < 0.75

    if is_approved:
        claim_status = 'Approved'
        copay_amount = round(random.uniform(0.00, 50.00), 2)
        rejection_reason = None

        # Business Logic: If approved, 90% chance the user completes checkout
        checkout_status = 'Completed' if random.random() < 0.90 else 'Abandoned'

    else:
        claim_status = 'Denied'
        copay_amount = None
        rejection_reason = random.choice(rejection_reasons)

        # Business Logic: If denied, 85% chance they abandon the cart (Too expensive out of pocket)
        # We will make 'Prior Auth Required' have a 95% abandonment rate to create a strong data story
        if rejection_reason == 'Prior Auth Required':
            checkout_status = 'Abandoned' if random.random() < 0.95 else 'Completed'
        else:
            checkout_status = 'Abandoned' if random.random() < 0.85 else 'Completed'

    # Append to our data lists
    web_sessions_data.append([session_id, user_id, session_timestamp, cart_value, checkout_status])
    claims_transactions_data.append(
        [claim_id, session_id, user_id, provider, claim_status, copay_amount, rejection_reason])

# 4. Convert to Pandas DataFrames
df_web = pd.DataFrame(web_sessions_data,
                      columns=['session_id', 'user_id', 'session_timestamp', 'cart_value', 'checkout_status'])
df_claims = pd.DataFrame(claims_transactions_data,
                         columns=['claim_id', 'session_id', 'user_id', 'insurance_provider', 'claim_status',
                                  'copay_amount', 'rejection_reason'])

# 5. Export to CSV files
df_web.to_csv('web_sessions.csv', index=False)
df_claims.to_csv('claims_transactions.csv', index=False)

print("Success! Generated 'web_sessions.csv' and 'claims_transactions.csv'.")