import os
import requests
from bs4 import BeautifulSoup

# Create the diseases directory if it doesn't exist
output_dir = "diseases"
os.makedirs(output_dir, exist_ok=True)

# User-Agent header for the requests
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
    )
}

# Open the file containing the disease URLs
with open("all_disease_links.txt", "r") as file:
    # Iterate over each line in the file
    for line in file:
        url = line.strip()
        if url:
            # Extract the disease name (e.g., acidity-42 from www.1mg.com/diseases/acidity-42#)
            disease_name = url.split("/diseases/")[-1].split("#")[0]
            
            # Fetch the URL's content
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Check if the request was successful
                soup = BeautifulSoup(response.text, "html.parser")

                # Step 1: Extract references BEFORE removing them
                references = []
                references_section = soup.find(id="references")
                if references_section:
                    for li in references_section.find_all("li"):
                        parts = []
                        for child in li.children:
                            if child.name == "a" and child.has_attr("href"):
                                link_text = child.get_text(strip=True)
                                link_url = child['href']
                                parts.append(f"{link_text} ({link_url})")
                            elif child.string and not child.name:
                                parts.append(child.string.strip())
                        ref_text = " ".join(parts).strip()
                        if ref_text:
                            references.append(ref_text)

                # Step 2: Remove References and FAQ sections from DOM
                for unwanted_id in ["references", "faqs"]:
                    unwanted = soup.find(id=unwanted_id)
                    if unwanted:
                        unwanted.decompose()

                # Step 3: Extract main content divs (excluding removed References & FAQ)
                items = soup.find_all("div", class_="col-6 marginTop-16")

                sections = []
                for item in items:
                    text = []
                    for elem in item.descendants:
                        if elem.name in ["h1", "h2", "h3"]:
                            text.append("\n" + elem.get_text(strip=True).upper() + "\n")
                        elif elem.name in ["p", "br"]:
                            text.append("\n")
                        elif elem.string and not elem.name:
                            text.append(elem.strip())
                    cleaned = "".join(text).strip()
                    if cleaned:
                        sections.append(cleaned)

                # Step 4: Write everything to output file
                filepath = os.path.join(output_dir, f"{disease_name}.txt")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(url + "\n\n")
                    f.write("\n\n".join(sections))
                    if references:
                        f.write("\n\n--- REFERENCES ---\n\n")
                        for ref in references:
                            f.write(f"- {ref}\n")

                print(f"✅ Done! Saved to {filepath}")

            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL {url}: {e}")

print("Processing complete!")
