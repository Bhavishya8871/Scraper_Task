import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class AjaxEcommerceScraper:
    def __init__(self):
        print("Initializing scraper...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.base_url = "https://webscraper.io/test-sites/e-commerce/ajax"
        self.results = []
        
    def scrape_category(self, category_url, category_name, max_products=50):
        """Scrape a specific category."""
        print(f"\nScraping category: {category_name} ({category_url})")
        self.driver.get(category_url)
        time.sleep(3)  # Wait for page to load
        
        # Check if there are subcategories
        subcategories = []
        try:
            subcategory_elements = self.driver.find_elements(By.CSS_SELECTOR, ".sidebar-sub-category a")
            for sub in subcategory_elements:
                name = sub.text.strip()
                url = sub.get_attribute("href")
                if name and url:
                    subcategories.append((name, url))
            print(f"Found {len(subcategories)} subcategories")
        except Exception as e:
            print(f"Error finding subcategories: {e}")
        
        if subcategories:
            # Process each subcategory
            for sub_name, sub_url in subcategories:
                print(f"Processing subcategory: {sub_name}")
                self.driver.get(sub_url)
                time.sleep(3)
                self.extract_products(f"{category_name} > {sub_name}", max_products)
        else:
            # Process the category page directly
            self.extract_products(category_name, max_products)
    
    def extract_products(self, category_path, max_products=50):
        """Extract products from the current page with pagination handling."""
        products_extracted = 0
        page = 1
        
        while products_extracted < max_products:
            print(f"Extracting products from page {page}")
            
            # Wait for products to be visible
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".thumbnail"))
                )
            except TimeoutException:
                print("No products found or timeout")
                break
                
            # Get all products on the current page
            products = self.driver.find_elements(By.CSS_SELECTOR, ".thumbnail")
            if not products:
                print("No products found on this page")
                break
                
            print(f"Found {len(products)} products on page {page}")
            
            # Process each product
            for product in products:
                if products_extracted >= max_products:
                    break
                    
                try:
                    # Extract product data
                    name = product.find_element(By.CSS_SELECTOR, ".title").text.strip()
                    price = product.find_element(By.CSS_SELECTOR, ".price").text.strip()
                    url = product.find_element(By.CSS_SELECTOR, ".title").get_attribute("href")
                    
                    # Handle ratings and reviews
                    rating = 0
                    reviews = 0
                    try:
                        rating_element = product.find_element(By.CSS_SELECTOR, ".ratings")
                        stars = rating_element.find_elements(By.CSS_SELECTOR, ".glyphicon-star")
                        rating = len(stars)
                        
                        review_text = rating_element.find_element(By.CSS_SELECTOR, "p").text.strip()
                        reviews = int(''.join(filter(str.isdigit, review_text)))
                    except NoSuchElementException:
                        # Some products might not have ratings
                        pass
                    
                    self.results.append({
                        'category': category_path,
                        'name': name,
                        'price': price,
                        'rating': rating,
                        'reviews': reviews,
                        'url': url
                    })
                    products_extracted += 1
                    print(f"Extracted: {name}, Price: {price}, Rating: {rating}, Reviews: {reviews}")
                    
                except Exception as e:
                    print(f"Error extracting product: {e}")
            
            # Check if there's a next page and if we need more products
            if products_extracted < max_products:
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, ".pagination .next")
                    if "disabled" in next_button.get_attribute("class"):
                        print("No more pages")
                        break
                        
                    print("Clicking next page")
                    next_button.click()
                    page += 1
                    time.sleep(3)  # Wait for AJAX to load
                except Exception as e:
                    print(f"Error navigating to next page: {e}")
                    break
            else:
                break
                
        print(f"Extracted {products_extracted} products from {category_path}")
    
    def run(self):
        """Main function to run the scraper."""
        print("Starting scraping process...")
        
        # Define the categories to scrape
        categories = [
            ("Computers", f"{self.base_url}/computers"),
            ("Phones", f"{self.base_url}/phones")
        ]
        
        # Scrape each category
        for name, url in categories:
            self.scrape_category(url, name)
            
        print(f"Scraping complete! Total products extracted: {len(self.results)}")
        
    def save_results(self, filename="product_data.json"):
        """Save results to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=4)
        print(f"Saved {len(self.results)} products to {filename}")
    
    def close(self):
        """Close the WebDriver."""
        self.driver.quit()
        print("WebDriver closed")

if __name__ == "__main__":
    scraper = AjaxEcommerceScraper()
    try:
        scraper.run()
        scraper.save_results()
    finally:
        scraper.close()
