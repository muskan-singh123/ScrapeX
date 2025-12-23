import pandas as pd
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import db
from db import insert_products

def scrape_flipkart(query, price):

    products = []

    for i in range(1, 3):
        url = f"https://www.flipkart.com/search?q={query}+under+{price}+rupees&page={i}"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=20000)
            page.wait_for_load_state("networkidle")

            web = requests.get(url)
            soup = BeautifulSoup(web.text, "lxml")

            box = soup.find("div", class_="QSCKDh dLgFEE")
            if not box:
                continue

            browser.close()

        names = box.find_all("div", class_="RG5Slk")
        prices = box.find_all("div", class_="hZ3P6w DeU9vF")
        descs = box.find_all("ul", class_="HwRTzP")
        reviews = box.find_all("div", class_="MKiFS6")
        link = box.find_all("a",class_="k7wcnx") 
        count = max(len(names), len(prices), len(descs), len(reviews), len(link))

        for idx in range(count):
            products.append({
                "Product_name": names[idx].text if idx < len(names) else None,
                "Prices": prices[idx].text if idx < len(prices) else None,
                "Description": descs[idx].text if idx < len(descs) else None,
                "Reviews": reviews[idx].text if idx < len(reviews) else None,
                "Links": link[idx]["href"] if idx < len(link) else None

            })

    df = pd.DataFrame(products)
    if products:
        try:
            # ensure DB and table exist
            try:
                db.init_db()
            except Exception as init_err:
                print(f"DB init warning: {init_err}")

            inserted = insert_products(products)
            print(f"Inserted {inserted} rows into MySQL")
        except Exception as e:
            print("DB insert failed:", e)
    else:
        print("No products found.")

    print(df)
    return df.to_dict(orient="records")

if __name__ == "__main__":
    scrape_flipkart(price=10000)
