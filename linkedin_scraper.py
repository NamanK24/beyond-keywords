import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def scrape_linkedin_jobs(job_title):
    url = "https://www.linkedin.com/jobs/"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)

    search_box = driver.find_element(By.XPATH, "//input[@name='keywords']")
    search_box.clear()
    search_box.send_keys(job_title)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    job_listings = []
    job_elements = driver.find_elements(
        By.XPATH, "//li[contains(@class, 'job-result-card')]"
    )
    for job_element in job_elements:
        title = job_element.find_element(
            By.XPATH, ".//span[@class='screen-reader-text']"
        ).text.strip()
        company = job_element.find_element(
            By.XPATH, ".//h4[@class='base-search-card__subtitle']"
        ).text.strip()
        location = job_element.find_element(
            By.XPATH, ".//span[@class='job-result-card__location']"
        ).text.strip()
        job_listings.append({"Title": title, "Company": company, "Location": location})

    driver.quit()
    return job_listings
