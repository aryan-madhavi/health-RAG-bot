from bs4 import BeautifulSoup
import requests
import string

base_url = "https://www.1mg.com/all-diseases?label="

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
}

all_hrefs = []

# Loop through all letters A–Z
for letter in string.ascii_lowercase:
    url = base_url + letter
    print(f"Scraping: {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get all <a> tags for disease cards
    anchors = soup.find_all("a", class_="style__product-name___HASYw")

    for a in anchors:
        if a.has_attr("href"):
            # Convert relative to absolute URL
            href = "https://www.1mg.com" + a["href"] + "#"
            all_hrefs.append(href)

# Save all hrefs in a single file
with open("all_disease_links.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_hrefs))

print(f"✅ Done! Collected {len(all_hrefs)} links.")
