import requests
from bs4 import BeautifulSoup
import csv
import wikipediaapi

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/WHO_Model_List_of_Essential_Medicines"

# Fetch the content from the URL
response = requests.get(url)
html_content = response.content

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all relevant elements (update the selector as per your HTML structure)
medicine_elements = soup.find_all('a', href=True)

# Extract medicine names and links
medicines = []
for element in medicine_elements:
    if 'title' in element.attrs and element['href'].startswith('/wiki/'):
        drug_name = element.text.strip()
        drug_link = 'https://en.wikipedia.org' + element['href']
        medicines.append([drug_name, drug_link])

# Save to CSV
with open('medicines.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['drug_name', 'drug_page'])  # Writing header
    for medicine in medicines:
        writer.writerow(medicine)

class Fetch_wiki:
    def __init__(self):
        self.wiki_wiki = wikipediaapi.Wikipedia(
            user_agent='MyProjectName (merlin@example.com)',
                language='en',
                extract_format=wikipediaapi.ExtractFormat.WIKI
        )

    def fetch(self, page_name):
        p_wiki = self.wiki_wiki.page(page_name)
        return p_wiki.summary


import pandas as pd
df_1 = pd.read_csv('medicines_data.csv')

def common_preprocessing(df):
    df = df.dropna(subset=['content'])
    df = df.drop_duplicates(subset=['content'])
    df = df.drop_duplicates(subset=['name'])
    df['len'] = df['content'].apply(lambda x: len(x.split()))
    df = df.sort_values('len', ascending = True)
    return df


# Define the function to limit words
def limit_to_approx_60_words(sentence, limit_=60, backtrack_limit=10):
    words = sentence.split()
    if len(words) <= limit_:
        return sentence

    # Initial cut-off at the word limit
    limited_text = " ".join(words[:limit_])

    # Search for the last punctuation within the backtrack_limit
    for i in range(limit_ - 1, limit_ - backtrack_limit, -1):
        if words[i][-1] in ".?!;,":  # Add any other punctuation marks if needed
            return " ".join(words[: i + 1])

    # If no punctuation is found within the backtrack_limit, return the limited_text
    return limited_text


df_1 = common_preprocessing(df_1)
df_1 = df_1[df_1['len']>=40]
df_1['content'] = df_1['content'].apply(lambda x: limit_to_approx_60_words(x))
df_1 = common_preprocessing(df_1)
df_1.to_csv('medicine_updated.csv', index=False)
