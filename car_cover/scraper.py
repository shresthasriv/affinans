import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_olx_car_covers(url, num_pages=3):
    driver = setup_driver()
    all_listings = []
    current_page = 1
    
    try:
        # Load initial page
        print(f"Loading initial page: {url}")
        driver.get(url)
        
        while current_page <= num_pages:
            print(f"Processing page {current_page}")

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li._1DNjI"))
                )
                print("Found listings on page")
            except TimeoutException:
                print(f"Could not find listings on page {current_page}")
                break
            time.sleep(3)

            listings = driver.find_elements(By.CSS_SELECTOR, "li._1DNjI")
            
            if not listings:
                print(f"No listings found on page {current_page}")
                break
            
            print(f"Found {len(listings)} listings on page {current_page}")

            for listing in listings:
                try:
                    title = extract_with_selectors(listing, ["span._2poNJ", "span[data-aut-id='itemTitle']"])

                    price = extract_with_selectors(listing, ["span._2Ks63", "span[data-aut-id='itemPrice']"])

                    location = extract_with_selectors(listing, ["span._2VQu4", "span[data-aut-id='item-location']"])

                    date = extract_with_selectors(listing, ["span._2jcGx span", "span._2jcGx"])

                    link = ""
                    try:
                        link_el = listing.find_element(By.CSS_SELECTOR, "a._2cbZ2")
                        link = link_el.get_attribute("href")
                    except NoSuchElementException:
                        pass

                    image_url = ""
                    try:
                        img_el = listing.find_element(By.CSS_SELECTOR, "img._3vnjf")
                        image_url = img_el.get_attribute("src")
                    except NoSuchElementException:
                        pass

                    listing_data = {
                        "title": title if title else "N/A",
                        "price": price if price else "N/A",
                        "location": location if location else "N/A",
                        "date": date if date else "N/A",
                        "link": link if link else "N/A",
                        "image_url": image_url if image_url else "N/A"
                    }
                    
                    all_listings.append(listing_data)
                except Exception as e:
                    print(f"Error extracting data from listing: {e}")
                    continue
            
            if current_page >= num_pages:
                print(f"Reached maximum number of pages ({num_pages})")
                break

            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-aut-id='btnLoadMore']"))
                )
                
                print("Found Load More button")

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                driver.execute_script("arguments[0].click();", load_more_button)
                print("Clicked Load More button using JavaScript")

                time.sleep(5)
                
                current_page += 1
                
            except Exception as e:
                print(f"Error with Load More button: {e}")
                break
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    
    return all_listings

def save_to_csv(listings, filename="olx_car_covers.csv"):
    if not listings:
        print("No listings to save")
        return
    
    fieldnames = listings[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(listings)
    
    print(f"Saved {len(listings)} listings to {filename}")

def save_to_txt(listings, filename="olx_car_covers.txt"):
    if not listings:
        print("No listings to save")
        return
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"OLX Car Cover Search Results - Total: {len(listings)}\n")
        f.write("="*80 + "\n\n")
        
        for i, item in enumerate(listings, 1):
            f.write(f"Listing #{i}\n")
            f.write(f"Title: {item['title']}\n")
            f.write(f"Price: {item['price']}\n")
            f.write(f"Location: {item['location']}\n")
            f.write(f"Date: {item['date']}\n")
            f.write(f"Link: {item['link']}\n")
            if item['image_url']:
                f.write(f"Image: {item['image_url']}\n")
            f.write("\n" + "-"*50 + "\n\n")
    
    print(f"Saved {len(listings)} listings to {filename}")

def save_to_json(listings, filename="olx_car_covers.json"):
    if not listings:
        print("No listings to save")
        return
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(listings, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(listings)} listings to {filename}")

def extract_with_selectors(element, selectors):
    for selector in selectors:
        try:
            sub_element = element.find_element(By.CSS_SELECTOR, selector)
            if sub_element:
                return sub_element.text.strip()
        except NoSuchElementException:
            continue
    return ""

def main():
    search_url = "https://www.olx.in/items/q-car-cover"
    num_pages = 3  
    
    print(f"Starting to scrape car cover listings from OLX...")
    listings = scrape_olx_car_covers(search_url, num_pages)
    
    if listings:
        print(f"Successfully scraped {len(listings)} car cover listings")
        save_to_csv(listings)
        save_to_txt(listings)
        save_to_json(listings)
    else:
        print("No listings were found")

if __name__ == "__main__":
    main()