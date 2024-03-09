## IMDb Review Scraper

This Python script scrapes reviews from IMDb for a given list of IMDb title IDs. 

### Requirements

This script requires the following Python libraries:

* pandas
* numpy
* beautifulsoup4
* selenium
* webdriver_manager (to install the appropriate chromedriver for your system)

You can install these libraries using the following command:

```bash
pip install -r requirements.txt
```

### Usage

1. Clone this repository.
2. Install the required libraries (see above).
3. Place your IMDb title IDs in a comma-separated list.
4. Run the script using the following command:

```bash
python scraper.py
```

**Note:** You will be prompted to enter the following:

* IMDb title IDs (comma-separated)
* Output file name (without extension)

The script will scrape reviews for each IMDb title ID and save the results to a CSV file.

### Files

* `scraper.py`: This file contains all the scraping logic for IMDb reviews.
* `requirements.txt`: This file lists the required Python libraries.

### How it Works

1. The script takes a list of IMDb title IDs as input.
2. For each title ID, it constructs the URL for the reviews page.
3. It uses Selenium to open the reviews page in a headless Chrome browser.
4. It uses BeautifulSoup to parse the HTML content of the reviews page.
5. It iterates through each review and extracts the title, date, content, and user rating (if available).
6. It stores the extracted data in a Pandas DataFrame.
7. It saves the DataFrame to a CSV file.

### Disclaimer

This script is for educational purposes only. Scraping data from websites without permission can be a violation of their terms of service. Please use this script responsibly and ethically.
