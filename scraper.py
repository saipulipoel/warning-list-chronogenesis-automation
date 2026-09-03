"""
scraper.py
Scrapes a target site and saves the results as JSON for GitHub Pages to display.

Install dependencies first:
    pip install requests beautifulsoup4
"""

import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

TARGET_URL = "https://chronogenesis.net/club_profile?circle_id=614073943"  # swap this for the real site you want


def scrape():
    response = requests.get(TARGET_URL, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # --- Adjust these selectors for the actual site you're scraping ---
    title = soup.find("title")
    title_text = title.get_text(strip=True) if title else "No title found"

    # Example: grabbing all headline-like elements
    # Change '.headline' to match the real site's CSS class/tag
    headlines = []
    for el in soup.select("h1, h2"):
        text = el.get_text(strip=True)
        if text:
            headlines.append(text)

    data = {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "source": TARGET_URL,
        "page_title": title_text,
        "headlines": headlines[:20],  # limit to first 20
    }

    return data


def main():
    data = scrape()

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Scraped {len(data['headlines'])} headlines. Saved to data.json")


if __name__ == "__main__":
    main()
