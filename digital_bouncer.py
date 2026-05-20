import pandas as pd
import random

sources = ['UK_Legacy_Server', 'EU_Legacy_Server']
destinations = ['UK_Sovereign_Cloud', 'EU_Sovereign_Cloud', 'Global_Analytics_Lake']
data_types = ['PII_Customer_Data', 'Anonymous_Network_Telemetry']

mock_data = []
for i in range(1, 101):
    mock_data.append({
        'flow_id': f'FLOW-{i:03d}',
        'source_node': random.choice(sources),
        'destination_node': random.choice(destinations),
        'data_type': random.choice(data_types)
    })

df = pd.DataFrame(mock_data)


def check_sovereignty(row):
    source = row['source_node']
    dest = row['destination_node']
    data = row['data_type']
    
    if data == 'Anonymous_Network_Telemetry':
        return "Safe"
        
    if data == 'PII_Customer_Data':
        if source == 'UK_Legacy_Server' and dest != 'UK_Sovereign_Cloud':
            return "VIOLATION: UK Data leaving UK"
            
        elif source == 'EU_Legacy_Server' and dest != 'EU_Sovereign_Cloud':
            return "VIOLATION: EU Data leaving EU"
            
        else:
            return "Safe"

df['sovereignty_status'] = df.apply(check_sovereignty, axis=1)

print("--- VODAFONE ODA CLOUD MIGRATION AUDIT ---")
print(df['sovereignty_status'].value_counts())
print("\nHere are the first 5 intercepted routes:")
print(df.head())

df.to_csv('vodafone_migration_audit.csv', index=False)
print("\n File saved successfully as 'vodafone_migration_audit.csv'")