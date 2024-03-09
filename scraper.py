import pandas as pd
import numpy as np
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

def get_reviews_url(title_ids):
    urls = [f'https://www.imdb.com/title/{title_id}/reviews/' for title_id in title_ids]
    return urls

def scrape_reviews(driver):
    review_title = []
    review_date = []
    review_content = []
    user_rating = []
    titles = []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    reviews_divs = soup.find_all('div', class_='lister-item-content')

    for div in reviews_divs:
        title = div.find('a', class_='title')
        if title:
            titles.append(title.text)
            review_title.append(title.text)
        else:
            titles.append('N/A')
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

    return titles, review_date, review_content, user_rating

def scrape_titles(title_ids):
    all_review_titles = []
    all_review_dates = []
    all_review_contents = []
    all_user_ratings = []

    for title_id in title_ids:
        url = f'https://www.imdb.com/title/{title_id}/reviews/'
        driver.get(url)

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

        print(f'Loaded {counter} times for Title ID: {title_id}')
        titles, review_dates, review_contents, user_ratings = scrape_reviews(driver)

        all_review_titles.extend(titles)
        all_review_dates.extend(review_dates)
        all_review_contents.extend(review_contents)
        all_user_ratings.extend(user_ratings)

    return all_review_titles, all_review_dates, all_review_contents, all_user_ratings

def main():
    title_ids = input("Enter IMDb title IDs separated by commas: ").split(',')
    title_ids = [title_id.strip() for title_id in title_ids]

    review_titles, review_dates, review_contents, user_ratings = scrape_titles(title_ids)

    driver.quit()

    df = pd.DataFrame({
        'Review Title': review_titles,
        'Review Date': review_dates,
        'Review Content': review_contents,
        'User Rating': user_ratings
    })

    output_file_name = input("Enter the output file name (without extension): ") + ".csv"
    df.to_csv(output_file_name, index=False)
    print(f'Data saved to {output_file_name}')

if __name__ == "__main__":
    main()
