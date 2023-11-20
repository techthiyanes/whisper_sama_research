# Assumptions
# You have Python. You've installed the requests library. You have docker on your machine.

# Usage
# Launch the ICD-11 docker container
# docker run -p 80:80  --env "acceptLicense=true" --env "saveAnalytics=true" --env "includeIp=false" whoicd/icd11_sw_1904_mms_en


import requests
import pandas as pd
from tqdm import tqdm 

uri = 'http://localhost/icd/release/11/2019-04/mms'
base_uri = 'http://localhost/icd/release/11/2019-04/mms/{}'
headers = {
    'Accept': 'application/json', 
    'Accept-Language': 'en',
    'API-Version': 'v2'
}

# Create an empty DataFrame
df = pd.DataFrame(columns=['code', 'source', 'title', 'definition'])

def retrieve_code(uri):
    global df
    req = requests.get(uri, headers=headers, verify=False)
    output = req.json()     

    if 'classKind' in output and output['classKind'] == 'category':
        code = output.get('code', '')
        source = output.get('source', '')
        title = output.get('title', {}).get('@value', '')
        definition = output.get('definition', {}).get('@value', '')

        # Append to DataFrame
        df = df.append({'code': code, 'source': source, 'title': title, 'definition': definition}, ignore_index=True)
    
    if 'child' in output:
        children = output['child']
        item_uris = [base_uri.format(item.split("/mms/")[-1]) for item in children]
        for next_uri in item_uris:
            retrieve_code(next_uri)

# Start the recursive data retrieval
retrieve_code(uri)

# Save DataFrame to CSV
df.to_csv('icd_data.csv', index=False)
