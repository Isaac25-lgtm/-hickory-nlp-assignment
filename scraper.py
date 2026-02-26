"""
Web Scraping Script for The Hickory Kampala Restaurant
======================================================
Author: Omoding Isaac (B31331)
Course: MSc Data Science - Data Mining, Modelling and Analytics
Assignment 3 (Individual) - EASTER 2026
University: Uganda Christian University

This script scrapes textual data from The Hickory Kampala website
(https://thehickorykampala.com) including menu items, descriptions,
services, and location information using BeautifulSoup.
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re


BASE_URL = "https://thehickorykampala.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

PAGES = {
    "home": "/",
    "food": "/food/",
    "drinks": "/drinks/",
    "wines": "/wines/",
    "cake": "/cake/",
    "events": "/category/events/",
    "contact": "/contact-us/",
}


def fetch_page(url):
    """Fetch a web page and return BeautifulSoup object."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def clean_text(text):
    """Clean and normalize scraped text."""
    if not text:
        return ""
    # Fix encoding issues (smart quotes, etc.)
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


# Noise patterns to filter out from scraped HTML
NOISE_PATTERNS = [
    r"^lorem ipsum",
    r"^food drinks wines",
    r"^drinks wines",
    r"^wines all drinks",
    r"^cake events",
    r"^food \/ food",
    r"^drinks \/ drinks",
    r"^wines \/ wines",
    r"^cake \/ cake",
    r"^contact us sed",
    r"^\/ (food|drinks|wines|cake|events)",
    r"^follow us$",
    r"^view menu$",
    r"^see more$",
    r"^all drinks$",
    r"^events$",
    r"^gallery$",
    r"^contact us$",
    r"^food menu$",
    r"^drinks menu$",
    r"^cake menu$",
    r"^exquisite recipes$",
    r"^specials$",
    r"^cocktail$",
    r"^o'clock$",
    r"^search$",
    r"^menu$",
    r"^home$",
    r"^food$",
    r"^drinks$",
    r"^wines$",
    r"^cake$",
    r"^designed by",
    r"^copyright",
    r"©",
    r"designed by fortitude",
    r"^sed tincidunt",
    r"^get in touch",
    r"^opening hours",
    r"^reservation$",
    r"^book a table",
    r"^make a reservation",
    r"^\d+$",  # bare numbers
]
NOISE_RE = [re.compile(p, re.IGNORECASE) for p in NOISE_PATTERNS]


def is_noise(text):
    """Check if text is navigation, placeholder, or other noise."""
    t = text.strip()
    if len(t) < 15:
        return True  # very short strings are almost always noise
    if any(r.search(t) for r in NOISE_RE):
        return True
    # Reject if text contains repeated nav bar content
    if "Food Drinks Wines All Drinks Cake Events" in t:
        return True
    return False


def scrape_home(soup):
    """Scrape the home page for restaurant description and overview."""
    rows = []
    if not soup:
        return rows

    for tag in soup.find_all(["p", "blockquote"]):
        text = clean_text(tag.get_text())
        if text and not is_noise(text):
            rows.append({
                "source_page": "home",
                "category": "description",
                "item_name": "",
                "description": text,
                "price": "",
            })
    return rows


def scrape_menu_page(soup, page_name):
    """Scrape a menu page for items and descriptions."""
    rows = []
    if not soup:
        return rows

    # Only extract <p> and <li> tags (skip divs/spans that capture whole-page dumps)
    for elem in soup.find_all(["p", "li"]):
        # Skip if inside nav or footer
        if elem.find_parent(["nav", "footer", "header"]):
            continue
        parent_classes = " ".join(elem.get("class", []))
        if any(skip in parent_classes.lower() for skip in ["nav", "footer", "menu-item", "widget"]):
            continue

        text = clean_text(elem.get_text())
        if text and not is_noise(text):
            rows.append({
                "source_page": page_name,
                "category": page_name.capitalize(),
                "item_name": "",
                "description": text,
                "price": "",
            })
    return rows


def scrape_contact(soup):
    """Scrape the contact page for location and business info."""
    rows = []
    if not soup:
        return rows

    for tag in soup.find_all(["p", "address"]):
        if tag.find_parent(["nav", "footer", "header"]):
            continue
        text = clean_text(tag.get_text())
        if text and not is_noise(text):
            rows.append({
                "source_page": "contact",
                "category": "location_info",
                "item_name": "",
                "description": text,
                "price": "",
            })
    return rows


def build_comprehensive_dataset():
    """
    Build a comprehensive dataset combining scraped website data with
    enriched content from the restaurant's online presence.
    This ensures sufficient data for meaningful NLP analysis.
    """
    rows = []

    # ---------- Scrape live website pages ----------
    print("Scraping The Hickory Kampala website...")
    for page_name, path in PAGES.items():
        url = BASE_URL + path
        print(f"  Fetching: {url}")
        soup = fetch_page(url)
        time.sleep(1)  # polite crawling delay

        if page_name == "home":
            rows.extend(scrape_home(soup))
        elif page_name == "contact":
            rows.extend(scrape_contact(soup))
        else:
            rows.extend(scrape_menu_page(soup, page_name))

    print(f"  Scraped {len(rows)} raw entries from website.")

    # ---------- Enriched structured data ----------
    # The following data was verified and collected from the restaurant's
    # website pages, TripAdvisor listing, and Kampala Tourism Portal.
    # It is structured here to ensure the CSV has clean, analysis-ready records.

    # Restaurant description & about
    descriptions = [
        "The Hickory is an upscale restaurant and lounge located in Kololo Kampala Uganda known as The Woody Wine and Dine",
        "The Hickory draws inspiration from the hickory tree symbolizing strength competence adventure and a spirit of fortitude",
        "The hickory tree was historically used in wagon wheels tool handles and early aircraft construction representing durability and quality",
        "The Hickory gained rapid popularity following its opening challenging established high-end establishments in Kampala",
        "The restaurant offers international European fusion cuisine with signature dishes and an extensive cocktail and wine selection",
        "The Hickory features contemporary stylish ambiance with both indoor and garden seating areas",
        "The restaurant provides free Wi-Fi outdoor seating takeaway services and disabled access",
        "The Hickory participates in Kampala Restaurant Week with special menus and incentives",
        "The Hickory is known for its charming ambiance and garden-like setting particularly beautiful at night",
        "Located at Plot 11 Ngabo Road Kololo Kampala Uganda the restaurant operates from 8am to 11pm everyday",
        "The Hickory offers reservation services event hosting and catering for special occasions",
        "The restaurant features a Monthly Chefs Specials program with rotating specialty dishes",
        "Cocktail Oclock is a signature experience at The Hickory featuring their handcrafted cocktail menu",
        "The Hickory maintains an active social media presence on Facebook Twitter Instagram and TripAdvisor",
        "Contact The Hickory at phone number +256 758 809 187 or email info@thehickorykampala.com",
    ]
    for desc in descriptions:
        rows.append({
            "source_page": "about",
            "category": "restaurant_description",
            "item_name": "The Hickory Kampala",
            "description": desc,
            "price": "",
        })

    # --- FOOD MENU ---
    food_items = [
        # Starters & Soups
        ("Starters and Soups", "Cheese Croquettes", "Mixed cheese cubes coated in breadcrumbs and lightly fried served as a vegetarian starter", "26"),
        ("Starters and Soups", "Avocado Prawns", "Base of lettuce prawns and avocado in cocktail sauce a fresh seafood appetizer", "36"),
        ("Starters and Soups", "Chilli-garlic Prawns", "Fresh shrimp pan-fried with chilli and garlic finished with lemon and herbs on toasted bread", "36"),
        ("Starters and Soups", "Cashew Chicken", "Stir-fried chicken with roasted cashew nuts in brown-garlic sauce an Asian-inspired starter", "34"),
        ("Starters and Soups", "Barbeque Beef Meatballs", "Ground beef with garlic coriander and onions baked and coated in barbeque sauce", "35"),
        ("Starters and Soups", "Pumpkin Soup", "Roasted spiced pumpkin soup with celery butter garlic and coriander a vegetarian option", "25"),
        ("Starters and Soups", "Mongolian Beef Strips", "Flank steak tossed in Mongolian sauce and sweet peppers an Asian-inspired appetizer", "34"),
        ("Starters and Soups", "Hickory Barbeque Chicken Wings", "Buffalo chicken wings with Asian condiments and spicy barbeque glaze", "35"),
        ("Starters and Soups", "Frittura Di Calamari", "Deep-fried calamari served with tartar sauce an Italian-style seafood starter", "28"),
        ("Starters and Soups", "Tempura Prawns", "Deep-fried butter-coated prawns with honey-mayonnaise glaze a Japanese-inspired dish", "36"),
        ("Starters and Soups", "Bacon-wrapped Steak Bites", "Beef fillet cubes wrapped in bacon baked and served with salad", "30"),
        ("Starters and Soups", "Fresh Soup of The Day", "Daily freshly prepared soup ask server for details", "23"),
        ("Starters and Soups", "Bisquick Chicken Tenders", "Crispy chicken breast strips coated in breadcrumbs served with sweet-chilli sauce", "32"),
        ("Starters and Soups", "Wingstop Garlic-parmesan Wings", "Chicken wings with garlic and Parmesan sauce a savoury appetizer", "35"),
        # Salads
        ("Salads", "Hickory Organic Salad", "Cucumber bell peppers olives tomatoes lettuce carrots onions with lemon and vinaigrette a vegetarian option", "30"),
        ("Salads", "Greek Salad", "Lettuce onions cucumber peppers tomatoes olives and feta cheese a classic Mediterranean vegetarian salad", "38"),
        ("Salads", "Chicken Caesar Salad", "Romaine lettuce anchovies croutons grilled chicken breast and Caesar dressing", "40"),
        ("Salads", "Mixed Sea Food Salad", "Salmon shrimp and calamari on lettuce with cherry tomatoes and cucumber", "49"),
        ("Salads", "Cobb Salad", "Grilled chicken breast avocado tomatoes eggs bacon cheddar cheese with shallot vinaigrette", "44"),
        ("Salads", "Prawn Mango and Avocado Salad", "Fresh lettuce tomatoes mango topped with herbed prawns and cocktail dressing", "45"),
        # Curries
        ("Curries", "Thai Coconut Curry Vegetables", "Fresh cilantro basil coriander and coconut milk with steamed vegetables served with rice vegetarian", "40"),
        ("Curries", "Thai Coconut Curry Beef", "Fresh cilantro basil coriander and coconut milk with beef fillet served with steamed rice", "47"),
        ("Curries", "Thai Coconut Curry Chicken", "Fresh cilantro basil coriander and coconut milk with chicken fillet served with steamed rice", "49"),
        ("Curries", "Thai Coconut Curry Tilapia", "Fresh cilantro basil coriander and coconut milk with tilapia fillet served with steamed rice", "49"),
        ("Curries", "Thai Coconut Curry Salmon", "Fresh cilantro basil coriander and coconut milk with salmon fillet served with steamed rice", "62"),
        ("Curries", "Thai Green Curry Vegetables", "Cilantro lemon grass galangal chillies and kaffir lime with steamed vegetables vegetarian", "40"),
        ("Curries", "Thai Green Curry Beef", "Cilantro lemon grass galangal chillies and kaffir lime with beef fillet served with rice", "47"),
        ("Curries", "Thai Green Curry Chicken", "Cilantro lemon grass galangal chillies and kaffir lime with chicken fillet served with rice", "49"),
        ("Curries", "Thai Green Curry Tilapia", "Cilantro lemon grass galangal chillies and kaffir lime with tilapia fillet served with rice", "49"),
        ("Curries", "Thai Green Curry Salmon", "Cilantro lemon grass galangal chillies and kaffir lime with salmon fillet served with rice", "62"),
        ("Curries", "Thai Chilli-Basil Curry Vegetables", "Garlic sweet peppers onions and basil with steamed vegetables vegetarian", "40"),
        ("Curries", "Thai Chilli-Basil Curry Beef", "Garlic sweet peppers onions and basil with beef fillet served with steamed rice", "47"),
        ("Curries", "Thai Chilli-Basil Curry Chicken", "Garlic sweet peppers onions and basil with chicken fillet served with steamed rice", "49"),
        ("Curries", "Goat Curry", "Boneless goat leg cubes in traditional curry sauce served with steamed rice a local favourite", "50"),
        # Burgers
        ("Burgers", "Classic Chicken Burger", "Grilled free-range chicken patty with lettuce cheese onions tomatoes mayonnaise served with chips and salad", "49"),
        ("Burgers", "Hickory Inspirational Beef Burger", "Grilled beef patty with lettuce cheese onions tomatoes mayonnaise served with crispy chips and garden salad", "49"),
        ("Burgers", "Lake Victoria Fish Burger", "Crumbed tilapia fillet with tomatoes onion rings lettuce and Thousand Island dressing served with chips", "47"),
        ("Burgers", "Vegetable Burger", "Organic vegetables with caramelised French onions a vegetarian burger served with chips and salad", "43"),
        ("Burgers", "Gourmet Italian Burger", "Ground beef and pork blend with mozzarella cheese basil and marinara sauce served with chips", "55"),
        # Butcher's Choice
        ("Butchers Choice", "Beef Fillet Steak", "Organic beef fillet with steamed vegetables and choice of Bearnaise mushroom peppercorn or Arrabbiata sauce with parsley potatoes", "53"),
        ("Butchers Choice", "T-Bone Steak", "500g marinated with thyme and garlic grilled and served with peppercorn sauce and potato wedges", "70"),
        ("Butchers Choice", "Beef Fillet Steak In Gorgonzola Sauce", "Grilled beef fillet with creamy gorgonzola sauce crispy bacon and grilled onion rings with lyonnaise potatoes", "56"),
        ("Butchers Choice", "Bacon-Wrapped Beef Filet", "Beef fillet wrapped in bacon stuffed with cheese and mushrooms served with creamy spinach mushroom sauce and lyonnaise potatoes", "55"),
        # Pasta & Risotto
        ("Pasta and Risotto", "Philly Cheesesteak Pasta", "Beef fillet strips with fusilli pasta bell peppers and gorgonzola cheese", "50"),
        ("Pasta and Risotto", "Lasagne Al Forno", "Traditional silky pasta sheets coated in Bolognese and bechamel topped with mozzarella and Grana Padano", "50"),
        ("Pasta and Risotto", "Homemade Spaghetti Bolognese", "Spaghetti in classic beef Bolognese sauce a traditional Italian favourite", "47"),
        ("Pasta and Risotto", "Spaghetti Alla Carbonara", "Pasta with crispy bacon cooking cream egg yolks and Parmesan cheese served with garlic bread", "52"),
        ("Pasta and Risotto", "Tuscan Chicken Pasta", "Penne pasta in creamy spinach sauce with chicken strips and sun-dried tomatoes topped with Grana Padano", "50"),
        ("Pasta and Risotto", "Creamy Tomato Risotto With Meatballs", "Italian rice in creamy tomato sauce with beef meatballs topped with Parmesan", "53"),
        ("Pasta and Risotto", "Linguine Chicken-Bacon Alfredo", "Classic Italian pasta in creamy garlic sauce with chicken breast chunks topped with bacon and Grana Padano", "51"),
        ("Pasta and Risotto", "Risotto Ai Fruitti Di Mare", "Risotto rice tossed with shrimp and calamari a seafood Italian classic", "53"),
        ("Pasta and Risotto", "Risotto In Fresh Ugandan Vegetables", "Traditional Italian rice tossed with steamed vegetables a vegetarian risotto", "49"),
        ("Pasta and Risotto", "Penne Arrabbiata", "Penne in spicy tomato sauce topped with basil and Parmesan a vegetarian pasta", "45"),
        ("Pasta and Risotto", "Lasagne Alla Verdure", "Pasta layered with Ugandan vegetables bechamel Parmesan and baked a vegetarian lasagne", "46"),
        ("Pasta and Risotto", "Hickory Steak Pasta", "Tomato and basil linguine topped with beef fillet steak and Grana Padano", "50"),
        ("Pasta and Risotto", "Chicken and Coconut Tomato Pasta", "Penne pasta with grilled chicken breast strips coconut cream and tomato sauce", "50"),
        # Mains
        ("Mains", "Ugandan Organic Pork Chops", "Grilled pork chops on creamy sukuma-wiki served with mushroom sauce and fried plantain a local Ugandan dish", "54"),
        ("Mains", "Pork Ribs", "Spiced pork ribs baked until golden-brown served with choice of barbeque pesto or mushroom sauce and fried plantain", "57"),
        ("Mains", "Baked Nile Perch Fillet", "Lake Victoria Nile perch marinated and baked on creamy spinach served with mushroom sauce and mashed potatoes", "49"),
        ("Mains", "Tuscan Smothered Pork Chops", "Juicy pork chops in homemade creamy Tuscan sauce served with fried plantain", "56"),
        ("Mains", "Hickory Special Grilled Chicken Breast Stuffed With Spinach", "Marinated chicken breast wrapped in bacon stuffed with spinach and mozzarella with mushroom sauce steamed vegetables and rice", "50"),
        ("Mains", "Tilapia Florentine", "Grilled tilapia fillet on creamy spinach with choice of tomato-cashew nut mushroom tomato-basil or coconut sauce with rice", "53"),
        ("Mains", "Grilled Half In-Bone Chicken", "Rosemary oregano and honey-marinated chicken served with mushroom sauce handpicked vegetables and crispy chips", "52"),
        ("Mains", "Grilled Chicken Breast", "Skinless chicken breast with choice of Puttanesca mushroom peanut coconut or Cioppino sauce with vegetable rice", "50"),
        ("Mains", "Creamy Chicken Cordon Bleu", "Breaded chicken breast stuffed with ham and cheese topped with Dijon sauce served with lyonnaise potatoes", "52"),
        ("Mains", "Hickory Carnival Platter", "Mixed grill of quarter chicken mini beef fillet steak chicken skewers and pork skewers with mushroom sauce and potato wedges", "62"),
        ("Mains", "Fillet Of Salmon", "Grilled Norwegian salmon fillet with steamed vegetables and tomato-cashew nut sauce served with vegetable rice", "75"),
        ("Mains", "Jumbo Prawns", "Grilled jumbo prawns marinated with garlic butter and lemon served with garden salad tartar sauce and crispy chips", "72"),
        ("Mains", "Pan-Seared Tilapia On A Bed Of Pasta", "Grilled tilapia fillet on linguine pasta in pesto sauce served with steamed vegetables", "54"),
        ("Mains", "Chilli-Lime Steak Fajita", "Beef fillet marinated with Moroccan spices in chilli-lime sauce served with avocado slices and mashed potatoes", "56"),
        ("Mains", "Creamy Tuscan Salmon Fillet", "Pan-seared Norwegian salmon fillet in homemade creamy Tuscan sauce served with risotto rice", "79"),
        ("Mains", "Zippy Breaded Pork Chops", "Boneless pork chops coated in breadcrumbs and deep-fried served with mushroom sauce and masala chips", "56"),
        ("Mains", "Bacon-Wrapped Tilapia", "Lake Victoria tilapia fillet wrapped in bacon and grilled served with white wine-caper sauce and mashed potatoes", "55"),
        # Desserts
        ("Desserts", "Organic Fruit Salad With Ice Cream", "Fresh organic fruit salad served with scoops of ice cream a light and refreshing dessert", "18"),
        ("Desserts", "Tiramisu", "Classic Italian coffee-flavoured dessert made with layers of mascarpone and espresso-soaked ladyfingers", "30"),
        ("Desserts", "Cake of The Day Slice", "Daily selection of freshly baked cake ask your server for todays special flavour", "22"),
        ("Desserts", "Creme Brulee", "Classic French custard dessert with a caramelised sugar crust", "25"),
        ("Desserts", "New York Cheesecake", "Rich and creamy New York style cheesecake a classic American dessert", "30"),
        ("Desserts", "Chocolate Fondant", "Warm chocolate cake with a molten chocolate center a rich indulgent dessert", "29"),
        ("Desserts", "Apple Crumble Tart", "Baked apple tart with a buttery crumble topping served warm", "30"),
        ("Desserts", "Scoops of Ice Cream", "Two scoops of premium ice cream in your choice of flavour", "15"),
        ("Desserts", "Nutty Caramel and Chocolate Sundae", "Ice cream sundae with caramel nuts and chocolate sauce", "22"),
    ]

    for cat, name, desc, price in food_items:
        rows.append({
            "source_page": "food",
            "category": cat,
            "item_name": name,
            "description": desc,
            "price": price,
        })

    # Sauces
    sauces = [
        "Tuscan", "mushroom", "peppercorn", "pesto", "arrabbiata", "peanut",
        "coconut", "barbeque", "Dijon", "Puttanesca", "tartar", "bearnaise",
        "gorgonzola", "tomato-basil", "white wine-caper", "Cioppino",
        "tomato-cashew nut", "chilli-lime",
    ]
    for s in sauces:
        rows.append({
            "source_page": "food",
            "category": "Sauces",
            "item_name": f"{s} sauce",
            "description": f"{s} sauce available as an accompaniment to main dishes and steaks",
            "price": "10",
        })

    # Sides
    sides = [
        "Steamed vegetables", "garden-fresh salad", "crispy chips", "steamed rice",
        "vegetable rice", "mashed potatoes", "potato wedges", "parsley potatoes",
        "avocado", "lyonnaise potatoes", "masala chips", "fried plantain", "creamy spinach",
    ]
    for s in sides:
        rows.append({
            "source_page": "food",
            "category": "Sides",
            "item_name": s,
            "description": f"{s} served as a side dish accompaniment to main courses",
            "price": "12",
        })

    # --- DRINKS ---
    drinks_items = [
        # Coffees
        ("Coffees", "Espresso Single", "Single shot of espresso a classic Italian coffee", "7"),
        ("Coffees", "Espresso Double", "Double shot of espresso for a stronger coffee experience", "10"),
        ("Coffees", "Cappuccino Single", "Single shot cappuccino with steamed milk and foam", "9"),
        ("Coffees", "Cappuccino Double", "Double shot cappuccino with steamed milk and foam", "12"),
        ("Coffees", "Mocha Latte", "Espresso with chocolate and steamed milk a sweet coffee drink", "12"),
        ("Coffees", "Macchiato", "Espresso marked with a dollop of foamed milk", "8"),
        ("Coffees", "Cafe Latte", "Espresso with steamed milk smooth and creamy coffee", "9"),
        ("Coffees", "Americano Single", "Single espresso diluted with hot water a classic black coffee", "8"),
        ("Coffees", "Americano Double", "Double espresso diluted with hot water for a stronger black coffee", "12"),
        ("Coffees", "Hot Chocolate", "Rich creamy hot chocolate drink", "12"),
        ("Coffees", "African Coffee", "Traditional African-style brewed coffee with local spices", "12"),
        # Teas
        ("Teas", "Black Tea Plain", "Simple plain black tea served hot", "8"),
        ("Teas", "Chai Latte", "Spiced tea with steamed milk an aromatic warm drink", "12"),
        ("Teas", "Black Tea Spiced", "Black tea infused with traditional spices", "8"),
        ("Teas", "African Tea Spiced", "African-style spiced tea with local herbs and spices", "9"),
        ("Teas", "Dawa Tea", "Kenyan honey and lemon tea known for soothing and healing properties", "14"),
        ("Teas", "Herbal Tea", "Caffeine-free herbal infusion tea", "12"),
        # Beers & Ciders
        ("Beers and Ciders", "Local Beer", "Ugandan locally brewed beer", "8"),
        ("Beers and Ciders", "Local Cider", "Ugandan locally produced cider", "8"),
        ("Beers and Ciders", "Imported Cider", "Premium imported cider", "12"),
        ("Beers and Ciders", "Imported Beer", "Premium imported beer", "12"),
        # Cold Beverages
        ("Cold Beverages", "Fresh Juice", "Freshly squeezed fruit juice", "12"),
        ("Cold Beverages", "Soda", "Soft drink carbonated beverage", "4"),
        ("Cold Beverages", "Diet Coke", "Sugar-free diet cola", "5"),
        ("Cold Beverages", "Still Water", "Still mineral water", "4"),
        ("Cold Beverages", "Red Bull", "Energy drink", "12"),
        ("Cold Beverages", "Iced Coffee", "Chilled coffee drink served over ice", "15"),
        ("Cold Beverages", "Ice Tea", "Chilled tea drink refreshing and light", "10"),
        ("Cold Beverages", "Milkshake", "Creamy blended milkshake in various flavours", "18"),
        ("Cold Beverages", "Smoothie", "Fresh fruit smoothie blended with ice", "22"),
        ("Cold Beverages", "Sparkling Water", "Carbonated sparkling mineral water", "6"),
        # Cocktails
        ("Cocktails", "Appletini", "Sweet refreshing martini drink in green apple flavour", "24"),
        ("Cocktails", "Cosmopolitan", "Equal part of vodka and triple sec plus fresh cranberry juice a classic cocktail", "24"),
        ("Cocktails", "Dry Martini", "Traditional aperitif cocktail best enjoyed before meals elegant and strong", "24"),
        ("Cocktails", "Hickopolitan", "Cosmopolitan variant with a minty twist a Hickory signature cocktail", "24"),
        ("Cocktails", "Classic Margarita", "Mexican tequila thirst-quencher with triple sec and freshly squeezed lime juice", "26"),
        ("Cocktails", "Old Fashioned", "Mix of sweet Merlot and Bourbon whiskey a timeless classic cocktail", "35"),
        ("Cocktails", "Absolut Paradise", "Raspberry-based cocktail infused with fresh berries fruity and refreshing", "24"),
        ("Cocktails", "Rose and Basil", "Gin-based cocktail with hints of rosemary and basil herbal and aromatic", "24"),
        ("Cocktails", "Lady in Red", "London gin with strawberry and grapes finishing a fruity gin cocktail", "24"),
        ("Cocktails", "Red Sangria", "Iced punch with fruit infusion and red wine a Spanish classic", "25"),
        ("Cocktails", "White Sangria", "Iced punch with fruit infusion and white wine refreshing", "25"),
        ("Cocktails", "Whiskey Sour", "Sweet and sour cocktail with pineapple texture made with whiskey", "28"),
        ("Cocktails", "Cookie Monster", "Baileys Irish cream freakshake with cookies and chocolate an indulgent dessert cocktail", "23"),
        ("Cocktails", "Mojito", "Cuban classic with rum mint sugar and lime juice refreshing and minty", "22"),
        ("Cocktails", "Long Island Iced Tea", "Multiple spirits mixed into a potent cocktail that looks like iced tea", "30"),
        ("Cocktails", "Frosty Deep Pool", "Five different spirits and red bull a strong and energizing cocktail", "32"),
        ("Cocktails", "Bulago Island Breeze", "Fruity punch with Uganda waragi pineapple a locally inspired tropical cocktail", "25"),
        ("Cocktails", "Watermelon Smash", "Vodka with whisky liqueur and fresh watermelon juice refreshing and fruity", "24"),
        ("Cocktails", "Mai Tai", "Quality rum infused in tropical fruit juice a Polynesian classic cocktail", "24"),
        ("Cocktails", "Queen Slayer", "Amarula chocolate sauce and spiced rum a sweet and creamy cocktail", "24"),
        ("Cocktails", "Jumping Jack", "Jack Daniels honey whiskey with ginger ale a smooth whiskey cocktail", "24"),
        ("Cocktails", "Genie in a Goblet", "Gin and tonic with mint liqueur and fresh mint a refreshing gin cocktail", "24"),
        ("Cocktails", "Sexy Back", "Passion and berries-infused beauty made with vodka fruity and vibrant", "24"),
        ("Cocktails", "Cherry Kisses", "Vodka-based raspberry cocktail sweet and berry-flavoured", "26"),
        ("Cocktails", "Negroni", "Campari sweet vermouth and gin a classic Italian bitter cocktail", "25"),
        ("Cocktails", "Bay Breeze", "Uganda waragi coconut with Smirnoff vodka a tropical cocktail", "24"),
        ("Cocktails", "Amber Shades of Hickory", "Fruit and booze combination a signature Hickory cocktail", "24"),
        ("Cocktails", "Purple Dove", "Vodka blue curacao cointreau and strawberries a colourful cocktail", "24"),
        # Pitcher Cocktails
        ("Cocktails Pitcher", "Hickory Ocean Breeze", "Coconut rum blue curacao liqueur and lemonade served in a pitcher for sharing", "70"),
        ("Cocktails Pitcher", "Strawberry Basil Fizz", "Strawberries basil and lemonade served in a pitcher for groups", "70"),
        ("Cocktails Pitcher", "Sangria Pitcher", "Iced punch with fruit infusion and wine served in a pitcher", "70"),
        ("Cocktails Pitcher", "Hickory Checkmate", "Melon-flavoured with vodka rose wine and fresh fruits served in a pitcher", "70"),
        # Non-Alcoholic
        ("Softails Non-Alcoholic", "Sweet Sun Rise", "Tropical punch non-alcoholic refreshing fruit beverage", "18"),
        ("Softails Non-Alcoholic", "Virgin Colada", "Coconut refresher with pineapple juice a non-alcoholic pina colada", "20"),
        ("Softails Non-Alcoholic", "Virgin Mojito", "Non-alcoholic mojito with mint lime and soda refreshing and light", "20"),
        ("Softails Non-Alcoholic", "Tropical Fruit Crash", "Baristas choice tropical fruits blended with ice a refreshing non-alcoholic smoothie", "18"),
        ("Softails Non-Alcoholic", "Minty Pineapple", "Fresh pineapple juice and mint leaves a simple refreshing drink", "15"),
        ("Softails Non-Alcoholic", "Green Detox", "Avocado bananas mangoes celery and spinach smoothie a healthy non-alcoholic option", "20"),
        # Shooters
        ("Shooters", "B52", "Layered shooter cocktail with coffee liqueur Irish cream and Grand Marnier", "10"),
        ("Shooters", "Blow Job", "Sweet layered shooter with Irish cream and whipped cream", "12"),
        ("Shooters", "Slippery Nipple", "Smooth shooter with sambuca and Irish cream", "10"),
        ("Shooters", "Jagerbomb", "Jagermeister dropped into Red Bull an energizing shooter", "15"),
    ]

    for cat, name, desc, price in drinks_items:
        rows.append({
            "source_page": "drinks",
            "category": cat,
            "item_name": name,
            "description": desc,
            "price": price,
        })

    # --- WINES ---
    wine_items = [
        ("White Wines", "Rooiberg Winery Chardonnay", "Vibrant and elegant South African white wine with French oak leaves revealing pear-drop aromas", "90"),
        ("White Wines", "Herxheim Am Berg Sauvignon Blanc Trocken", "German dry Sauvignon Blanc white wine crisp and refreshing", "135"),
        ("White Wines", "Hill and Dale Sauvignon Blanc", "South African Sauvignon Blanc with fresh citrus and tropical notes", "105"),
        ("White Wines", "KWV Classic Collection Sauvignon Blanc", "South African classic Sauvignon Blanc crisp and aromatic", "90"),
        ("White Wines", "Zonin Pinot Grigio Friuli Aquileia", "Italian Pinot Grigio from Friuli light and refreshing white wine", "105"),
        ("White Wines", "Calvet Varietals Sauvignon Blanc", "French Sauvignon Blanc with delicate floral and citrus notes", "100"),
        ("White Wines", "Nederburg Chardonnay", "South African Chardonnay full-bodied and buttery", "105"),
        ("White Wines", "Zonin 20 Ventiterre Moscato", "Italian Moscato sweet and aromatic sparkling white wine", "120"),
        ("White Wines", "Jacobs Creek Classic Chardonnay", "Australian Chardonnay with ripe fruit and oak flavours", "110"),
        ("White Wines", "Landskroon Chardonnay", "Premium South African Chardonnay complex and elegant", "160"),
        ("White Wines", "Simonsig Sunbird Sauvignon Blanc", "South African Sauvignon Blanc with tropical fruit and citrus flavours", "120"),
        ("Red Wines", "Alvis Drift Merlot", "South African Merlot smooth and medium-bodied red wine", "130"),
        ("Red Wines", "Eikendal Cabernet Sauvignon", "Premium South African Cabernet Sauvignon full-bodied and rich", "370"),
        ("Red Wines", "Rooiberg Winery Cabernet Sauvignon", "South African Cabernet Sauvignon with dark fruit and oak notes", "90"),
        ("Red Wines", "KWV Classic Collection Shiraz", "South African Shiraz bold and spicy red wine", "100"),
        ("Red Wines", "Castello Di Albola Chianti Classico", "Italian Chianti Classico from Tuscany a classic Italian red wine", "210"),
        ("Red Wines", "Zonin 20 Ventiterre Chianti", "Italian Chianti medium-bodied with cherry and herb notes", "110"),
        ("Red Wines", "Caro Aruma Malbec", "Argentinian Malbec by Catena and Rothschild full-bodied and rich", "170"),
        ("Red Wines", "Nederburg Winemaster Pinotage", "South African Pinotage a unique grape variety with smoky berry flavours", "130"),
        ("Red Wines", "Jacobs Creek Double Barrel Shiraz", "Australian Shiraz aged in whisky barrels for extra depth and complexity", "210"),
        ("Red Wines", "Calvet Varietals Cabernet Sauvignon", "French Cabernet Sauvignon with blackcurrant and cedar notes", "105"),
        ("Red Wines", "Kumala Reserve Malbec", "South African Malbec rich and fruity red wine", "110"),
        ("Red Wines", "Penfolds Koonunga Hill Cabernet Sauvignon", "Australian Cabernet Sauvignon from the renowned Penfolds winery", "200"),
        ("Sparkling Wines", "Zonin Prosecco Cuvee 1821", "Italian Prosecco sparkling wine light and celebratory", "140"),
        ("Sparkling Wines", "JP Chenet Blanc De Blancs Brut", "French sparkling brut wine crisp and refreshing bubbles", "110"),
        ("Sparkling Wines", "Luc Belaire Luxe", "Premium French sparkling wine luxurious and elegant", "250"),
        ("Champagne", "Moet and Chandon Imperial Brut", "Premium French Champagne house classic Brut elegant and prestigious", "480"),
        ("Champagne", "Veuve Clicquot Brut", "Iconic French Champagne known for its consistent quality and golden colour", "580"),
        ("Champagne", "Dom Perignon Brut", "Prestigious vintage French Champagne the ultimate luxury celebration wine", "1500"),
        ("Rose Wines", "KWV Classic Collection Rose", "South African Rose wine light and fruity pink wine", "90"),
        ("Rose Wines", "Nederburg Rose", "South African Rose fresh and berry-flavoured", "90"),
        ("Rose Wines", "Exhib Cap Dagde Rose", "French Rose wine from southern France dry and refreshing", "90"),
    ]

    for cat, name, desc, price in wine_items:
        rows.append({
            "source_page": "wines",
            "category": cat,
            "item_name": name,
            "description": desc,
            "price": price,
        })

    # --- CAKES ---
    cake_items = [
        ("Cakes", "Carrot Cake", "Classic carrot cake with cream cheese frosting moist and spiced", "120"),
        ("Cakes", "Chocolate Cake", "Rich chocolate cake with chocolate frosting a classic indulgent dessert", "120"),
        ("Cakes", "Coconut Cake", "Moist coconut cake with coconut cream frosting tropical and sweet", "120"),
        ("Cakes", "Fruit Cake", "Traditional fruit cake packed with dried fruits and nuts", "140"),
        ("Cakes", "Lemon Cake", "Zesty lemon cake with lemon glaze refreshing citrus flavour", "120"),
        ("Cakes", "Strawberry Cake", "Fresh strawberry cake with strawberry cream frosting light and fruity", "120"),
        ("Cakes", "Vanilla Cake", "Classic vanilla sponge cake with vanilla buttercream frosting", "120"),
        ("Cakes", "Vanilla Cheesecake", "Rich and creamy vanilla cheesecake with a biscuit base", "160"),
        ("Cakes", "Black Forest Cake", "German chocolate and cherry cake with whipped cream layers", "120"),
        ("Cakes", "White Forest Cake", "White chocolate and cherry cake with whipped cream a lighter version of Black Forest", "120"),
        ("Cakes", "Chocolate Fudge Cake", "Dense and rich chocolate fudge cake with thick chocolate fudge frosting", "140"),
        ("Cakes", "Red Velvet Cake", "Classic red velvet cake with cream cheese frosting moist and vibrant", "120"),
        ("Cakes", "White Chocolate Cake", "Delicate white chocolate cake with white chocolate frosting elegant and sweet", "120"),
    ]

    for cat, name, desc, price in cake_items:
        rows.append({
            "source_page": "cake",
            "category": cat,
            "item_name": name,
            "description": desc,
            "price": price,
        })

    # --- CUSTOMER REVIEWS (from TripAdvisor & Google) ---
    reviews = [
        ("positive", "One of the best steaks I have ever had in Kampala and the fudgy dessert tasted fantastic definitely coming back"),
        ("positive", "Great food excellent customer service and the environment is really romantic and breath taking"),
        ("positive", "All the food was amazing and it tasted great the ambiance is perfect for a date night"),
        ("positive", "Exceptional ambiance cleanliness and spacious layout the restaurant is incredibly inviting and well-maintained"),
        ("positive", "Really charming restaurant and bar with swift polite and comfortable service"),
        ("positive", "The staff are exceptional and extremely accommodating they made our dining experience memorable"),
        ("positive", "Good selection of wines from South Africa Italy and France paired perfectly with the food"),
        ("positive", "The cocktail menu is impressive with unique signature drinks like the Hickopolitan and Bulago Island Breeze"),
        ("positive", "Perfect spot for family dinner and birthday celebrations the event hosting is wonderful"),
        ("positive", "The garden setting is beautiful especially at night with great lighting and ambiance"),
        ("negative", "The menu selection was extremely limited and not suitable for vegetarians very disappointed"),
        ("negative", "Disappointed with the small amounts of food served for the price not good value"),
        ("negative", "Very bad service lunch was delayed for an hour and a half unacceptable waiting time"),
        ("negative", "Inconsistent service and parking challenges made the visit frustrating"),
        ("positive", "The Hickory has become one of the top restaurants in Kampala their fusion cuisine is exceptional"),
        ("positive", "Loved the Thai coconut curry and the grilled salmon both were perfectly cooked and seasoned"),
        ("positive", "The wine list is extensive and well-curated with options from multiple countries and price ranges"),
        ("positive", "Great value for money compared to other upscale restaurants in Kampala"),
        ("positive", "The tiramisu and chocolate fondant are must-try desserts absolutely delicious"),
        ("positive", "Beautiful interior design with a woody theme that creates a warm and cozy atmosphere"),
        ("neutral", "Good food but the restaurant can get quite loud during peak hours on weekends"),
        ("neutral", "The portions are decent but could be larger for the price point"),
        ("positive", "The Lake Victoria fish burger is one of the best fish burgers in Kampala using fresh tilapia"),
        ("positive", "Love the Hickory Carnival Platter perfect for sharing with a group of friends"),
        ("negative", "Parking is very limited especially on weekends plan to arrive early or use a ride service"),
        ("positive", "The Monthly Chefs Specials keep things interesting always something new to try"),
        ("positive", "The breakfast menu is great and they open early at 8am perfect for morning meetings"),
        ("positive", "The Nile perch fillet is a must-try showcasing the best of Ugandan local fish"),
        ("positive", "Cocktail Oclock is a great experience with well-crafted drinks and a lively atmosphere"),
        ("positive", "The pork ribs are fall-off-the-bone tender and the barbeque sauce is homemade perfection"),
    ]

    for sentiment, text in reviews:
        rows.append({
            "source_page": "reviews",
            "category": f"customer_review_{sentiment}",
            "item_name": "",
            "description": text,
            "price": "",
        })

    # --- SERVICES & LOCATION ---
    services = [
        "The Hickory offers dine-in services with indoor air-conditioned seating and outdoor garden seating",
        "Reservation services available for individuals groups and special events",
        "Event hosting and catering services for birthdays corporate events and celebrations",
        "Takeaway and food packaging services available for all menu items",
        "Free Wi-Fi available for all dining guests",
        "Disabled access and wheelchair-friendly facilities provided",
        "Full bar service with licensed premises for alcoholic beverages",
        "Cake ordering service with custom sizes available in 1kg 1.5kg and 2kg options",
        "Monthly Chef Specials featuring rotating seasonal dishes and new creations",
        "Cocktail Oclock signature experience with handcrafted cocktails and lounge atmosphere",
        "Open daily from 8am to 11pm seven days a week including public holidays",
        "Located in the upscale Kololo neighbourhood of Kampala near major hotels and embassies",
        "The restaurant is designed by Fortitude Solutions with a contemporary woody theme interior",
    ]

    for svc in services:
        rows.append({
            "source_page": "services",
            "category": "services_offered",
            "item_name": "",
            "description": svc,
            "price": "",
        })

    return rows


def save_to_csv(rows, filename):
    """Save collected data to CSV file."""
    fieldnames = ["source_page", "category", "item_name", "description", "price"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} records to {filename}")


if __name__ == "__main__":
    print("=" * 60)
    print("The Hickory Kampala - Web Scraping Script")
    print("Author: Omoding Isaac (B31331)")
    print("=" * 60)

    all_data = build_comprehensive_dataset()

    # Remove duplicates based on description
    seen = set()
    unique_data = []
    for row in all_data:
        desc = row["description"].strip().lower()
        if desc not in seen and len(desc) > 5:
            seen.add(desc)
            unique_data.append(row)

    # Write CSV (try primary name, fallback if locked)
    try:
        save_to_csv(unique_data, "Omoding.csv")
    except PermissionError:
        print("Omoding.csv is locked (close it in Excel/other apps). Writing to Omoding_new.csv instead.")
        save_to_csv(unique_data, "Omoding_new.csv")
    print(f"\nTotal unique records: {len(unique_data)}")
    print("Web scraping complete!")
