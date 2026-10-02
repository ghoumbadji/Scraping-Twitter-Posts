from urllib.parse import urljoin
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_x_posts(username, nbr):
    posts = []
    count = 0
    base_url = f"https://lightbrd.com/{username}"
    url = base_url

    # Initialize undetected_chromedriver with specific version
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=152)
    
    try:
        while count < nbr:
            driver.get(url)
            
            # Wait dynamically for the timeline items to load (max 10 seconds)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "timeline-item"))
                )
            except Exception:
                print("Timeout waiting for page to load or no tweets found.")
                break

            soup = BeautifulSoup(driver.page_source, "html.parser")
            divs = soup.find_all("div", class_="timeline-item")

            if not divs:
                print("Unable to load tweets.")
                break

            for div in divs:
                if count == nbr:
                    break

                # Retrieving tweet link
                a_tag = div.find("a", class_="tweet-link")
                if not a_tag:
                    continue
                
                # Safely joining URLs using urljoin
                link = urljoin("https://lightbrd.com", a_tag.get("href"))
                    
                # Avoiding retweets
                if username in link:
                    # Retrieving date
                    span_tag = div.find("span", class_="tweet-date")
                    a_date_tag = span_tag.find("a") if span_tag else None
                    publication_date = a_date_tag["title"] if a_date_tag else "unknown"
                        
                    # Retrieving tweet content
                    content_div = div.find("div", class_="tweet-content media-body")
                    content = content_div.get_text(strip=True) if content_div else ""

                    # Adding tweet to list
                    posts.append({
                        "link": link,
                        "publication_date": publication_date,
                        "content": content
                    })
                    count += 1

            # Handling page transitions safely
            show_more = soup.find("div", class_="show-more", string=lambda text: text and "Load more" in text)
            next_link_tag = show_more.find("a") if show_more else None
            
            if next_link_tag:
                url = urljoin(base_url, next_link_tag["href"])
            else:
                break
                
    finally:
        # Ensuring browser is always closed even if an error occurs during execution
        driver.quit()
        
    return posts

posts = scrape_x_posts("ylecun", 10)
print(posts)