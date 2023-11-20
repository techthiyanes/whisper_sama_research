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

fp = Fetch_wiki()
df  = pd.read_csv('medicines.csv')
df['name'] = df['drug_page'].apply(lambda x: x.split('wiki/')[-1])
df['content'] = df['name'].apply(lambda x: fp.fetch(x))
df
