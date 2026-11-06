import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# TASK 5 : WEB DATA EXTRACTION & ANALYSIS
# --------------------------------------------------

print("\n========== WEB DATA EXTRACTION ==========")

url = "https://books.toscrape.com/"

# --------------------------------------------------
# SEND REQUEST
# --------------------------------------------------

response = requests.get(url)

print("\nWEBSITE STATUS CODE")
print(response.status_code)

# Check if website loaded successfully

if response.status_code != 200:

    print("Unable to access website.")
    exit()

# --------------------------------------------------
# CREATE BEAUTIFULSOUP OBJECT
# --------------------------------------------------

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

# --------------------------------------------------
# EXTRACT BOOK DATA
# --------------------------------------------------

books = []

for book in soup.select("article.product_pod"):

    title = book.h3.a["title"]

    price = book.select_one(
        ".price_color"
    ).text.strip()

    rating = book.select_one(
        "p.star-rating"
    )["class"][1]

    books.append({
        "Title": title,
        "Price": price,
        "Rating": rating
    })

# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

data = pd.DataFrame(books)

print("\nFIRST FIVE SCRAPED RECORDS")
print(data.head())

print("\nNUMBER OF BOOKS SCRAPED")
print(len(data))

# --------------------------------------------------
# CLEAN PRICE
# --------------------------------------------------
# CLEAN PRICE

data["Price"] = (
    data["Price"]
    .astype(str)
    .str.replace("Â", "", regex=False)
    .str.replace("£", "", regex=False)
    .str.strip()
)

data["Price"] = pd.to_numeric(
    data["Price"],
    errors="coerce"
)
print("\nCLEANED PRICE VALUES")
print(data["Price"].head())

print("\nMISSING PRICE VALUES")
print(data["Price"].isna().sum())
# --------------------------------------------------
# CONVERT RATINGS TO NUMBERS
# --------------------------------------------------

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

data["Rating"] = data["Rating"].map(
    rating_map
)

# --------------------------------------------------
# BASIC ANALYSIS
# --------------------------------------------------

print("\n========== SCRAPED DATA ANALYSIS ==========")

print("\nAVERAGE BOOK PRICE")

print(
    round(data["Price"].mean(), 2)
)

print("\nMOST EXPENSIVE BOOK")

print(
    data.loc[
        data["Price"].idxmax(),
        ["Title", "Price"]
    ]
)

print("\nCHEAPEST BOOK")

print(
    data.loc[
        data["Price"].idxmin(),
        ["Title", "Price"]
    ]
)

print("\nRATING DISTRIBUTION")

print(
    data["Rating"].value_counts()
    .sort_index()
)

# --------------------------------------------------
# SAVE DATA
# --------------------------------------------------

data.to_csv(
    "scraped_books.csv",
    index=False
)

print("\nSCRAPED DATA SAVED")
print("scraped_books.csv")

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

rating_counts = (
    data["Rating"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(8, 5))

rating_counts.plot(kind="bar")

plt.title("Book Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Books")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    "visualizations/book_rating_distribution.png"
)

plt.show()

print("\nTASK 5 COMPLETED SUCCESSFULLY")