import pandas as pd
import numpy as np
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Initialize Chrome WebDriver
driver = webdriver.Chrome()
def get_reviews_url(title_id):
    return f'https://www.imdb.com/title/{title_id}/reviews/'

title_id = input('Enter the IMDb title ID: ')
while not title_id:
    title_id = input('Enter the IMDb title ID: ')

url = get_reviews_url(title_id)
response = requests.get(url)

if response.status_code == 404:
    print("This IMDb title ID does not exist. Please try again.")
    exit()

else:
    # Page loaded successfully
    print("Page loaded successfully. Proceed with the rest of your code.")
    title_soup = BeautifulSoup(response.text, 'html.parser')
    title = title_soup.find('a', attrs={'itemprop': 'url'}).text
    driver.get(url)

def scrape_reviews():
    review_title = []
    review_date = []
    review_content = []
    user_rating = []
    title = None

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    reviews_divs = soup.find_all('div', class_='lister-item-content')

    for div in reviews_divs:
        title = div.find('a', class_='title')
        if title:
            review_title.append(title.text)
        else:
            review_title.append('N/A')

        date = div.find('span', class_='review-date')
        if date:
            date_str = date.text
            date_obj = datetime.strptime(date_str, "%d %B %Y")
            review_date.append(date_obj)
        else:
            review_date.append('N/A')

        # Check for both classes for review content
        review = div.find('div', class_='text show-more__control')
        if not review:
            review = div.find('div', class_='text show-more__control clickable')

        if review:
            review_content.append(review.text.strip())
        else:
            review_content.append('N/A')

        rating = div.find('span', class_='rating-other-user-rating')
        if rating:
            user_rating_span = rating.find('span')
            if user_rating_span:
                score_text = user_rating_span.text.strip()
                if score_text.isdigit():
                    user_rating.append(int(score_text))
                else:
                    user_rating.append(np.nan)
            else:
                user_rating.append(np.nan)  
        else:
            user_rating.append(np.nan)

    return review_title, review_date, review_content, user_rating

counter = 0
while True:
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ipl-load-more__button'))
        )
        button.click()
        counter += 1
    except:
        break

print(f'Loaded {counter} times')
review_title, review_date, review_content, user_rating = scrape_reviews()
driver.quit()


df = pd.DataFrame({
    'Review Title': review_title,
    'Review Date': review_date,
    'Review Content': review_content,
    'User Rating': user_rating
})

df.to_csv(f'{title}-reviews.csv', index=False)
