import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

base_url = os.getenv('URL')
# print(base_url)
# base_url = "https://lira.epac.to/DOCS-TECH/Forensics/Malware/"

save_dir = "downloaded_pdfs"
os.makedirs(save_dir, exist_ok=True)

response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")
pdf_links = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.pdf')]

for pdf_link in pdf_links:
    file_url = base_url + pdf_link
    file_path = os.path.join(save_dir, pdf_link)
    
    with requests.get(file_url, stream=True) as r:
        total_size = int(r.headers.get('content-length', 0))
        with open(file_path, 'wb') as f, tqdm(
                desc=f"Downloading {pdf_link}",
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
                bar.update(len(chunk))
    
    if os.path.exists(file_path):
        print(f"Downloaded: {pdf_link} successfully!")
    else:
        print(f"Failed to download: {pdf_link}")

print("All files downloaded.")
