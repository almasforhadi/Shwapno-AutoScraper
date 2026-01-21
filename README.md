# Shwapno AutoScraper

A Selenium-based automation and scraping tool for Shwapno.com.  
This script logs into the website, searches for a product, scrapes product details (name, price, link), and saves the results into a structured CSV file.

---

## 🚀 Features

- Automated login detection (OTP-based)
- Product search automation
- Scrapes all valid products from search results
- Handles missing data and placeholder cards
- Saves results to `products.csv`

---

## 🛠️ Tools & Libraries

- Python
- Selenium
- webdriver-manager
- Chrome WebDriver
- CSV module

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd <repo-folder>
```


If you don't have a requirements.txt, install manually:
```bash
pip install selenium webdriver-manager
```

## Usage

Run the script:

python shwapno_scraper.py


Login manually using phone number + OTP.

The script will automatically search for the product and save results to products.csv.

## Output

The scraped product data will be saved in:

products.csv


Example format:

sl	product_name	price	product_url
1	Rice Brand A	৳150	https://...
2	Rice Brand B	৳120	https://...

## ⚠️ Notes

You must login manually using OTP.

The script uses explicit waits to handle dynamic page loading.

📌 License

This project is for learning and personal use.


---
