import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 40)

# ===============================
# 1️⃣ Open Website
# ===============================
driver.get("https://www.shwapno.com/")

# ===============================
# 2️⃣ Login
# ===============================
login_btn = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='User login Button']"))
)
login_btn.click()

phone_input = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//input[@type='tel']"))
)
phone_input.click()

print("👉 এখন নিজে হাতে Phone Number ও OTP দিয়ে Login করুন")

# Auto detect login complete
wait.until(
    EC.invisibility_of_element_located(
        (By.XPATH, "//button[@aria-label='User login Button']")
    )
)

print("🔓 Login successful")

# ===============================
# 3️⃣ Product Search
# ===============================
search_input = wait.until(
    EC.visibility_of_element_located((By.ID, "search-input"))
)

search_input.clear()
search_input.send_keys("rice")
search_input.send_keys(Keys.ENTER)

print("🔍 Product search করা হয়েছে")

# ===============================
# 4️⃣ Wait for product grid
# ===============================
product_grid = wait.until(
    EC.presence_of_element_located((By.ID, "product-grid"))
)

# ===============================
# CSV Setup (clean & structured)
# ===============================
csv_file = "products.csv"
file_exists = os.path.isfile(csv_file)

csv_fp = open(csv_file, mode="a", newline="", encoding="utf-8")
writer = csv.DictWriter(
    csv_fp,
    fieldnames=["sl", "product_name", "price", "product_url"]
)

if not file_exists:
    writer.writeheader()

# ===============================
# Helper: clean price
# ===============================
def clean_price(raw_price):
    if not raw_price:
        return "N/A"

    for line in raw_price.splitlines():
        if "৳" in line:
            return line.strip()

    return raw_price.strip()

# ===============================
# 5️⃣ Scrape All Products
# ===============================
products = product_grid.find_elements(
    By.XPATH, ".//div[contains(@class,'product-box')]"
)

print(f"\n🛒 Total Raw Boxes Found: {len(products)}\n")

valid_count = 0

for product in products:

    title_links = product.find_elements(
        By.XPATH, ".//div[contains(@class,'product-box-title')]//a"
    )

    if not title_links:
        continue  # skip fake / empty cards

    title_el = title_links[0]
    name = title_el.text.strip()
    link = title_el.get_attribute("href")

    price_els = product.find_elements(
        By.XPATH, ".//div[contains(@class,'product-price')]"
    )

    raw_price = price_els[0].text.strip() if price_els else ""
    price = clean_price(raw_price)

    valid_count += 1

    # Console output (pretty)
    print(f"🔹 Product {valid_count}")
    print(f"   📦 Name  : {name}")
    print(f"   💰 Price : {price}")
    print(f"   🔗 Link  : {link}")
    print("-" * 50)

    # CSV write (clean)
    writer.writerow({
        "sl": valid_count,
        "product_name": name,
        "price": price,
        "product_url": link
    })

csv_fp.close()
print(f"\n✅ Total Valid Products Saved: {valid_count}")
print("📁 products.csv file updated successfully")
