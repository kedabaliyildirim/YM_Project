import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

base_url = 'https://eksisozluk1923.com/avengers-infinity-war--4733018?p={}'

# Create a Service object with the path to ChromeDriver
chrome_service = Service()

# Use Selenium to load dynamic content
driver = webdriver.Chrome(service=chrome_service)

all_comments = []

# Iterate through pages
for page_number in range(1, 3):  # Assuming you want to scrape the first 2 pages, you can adjust this limit
    url = base_url.format(page_number)
    driver.get(url)

    # Wait for a few seconds to allow dynamic content to load (adjust as needed)
    time.sleep(5)

    # Scroll down to load more content if available (you may need to adjust the loop limit)
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # Get the page source after dynamic content is loaded
    html_content = driver.page_source

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all comment divs
    comment_divs = soup.find_all('div', {'class': 'content'})

    if comment_divs:
        for comment_div in comment_divs:
            comment_text = comment_div.get_text(strip=True)
            all_comments.append(comment_text)

# Close the Selenium WebDriver
driver.quit()

# Print all comments
for i, comment_text in enumerate(all_comments, start=1):
    print(f"Comment {i}: {comment_text}")
