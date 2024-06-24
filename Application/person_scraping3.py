import time
import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from linkedin_scraper import actions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_linkedin_data(linkedin_url):
    # Initialize WebDriver with Service object
    service = Service("C:/Users/ACER/Downloads/chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    # LinkedIn login
    email = "juug22btech47863@gmail.com"
    password = "RRM@25@12345"
    actions.login(driver, email, password)  # Login to LinkedIn
    time.sleep(50)

    try:
        # Navigate to the LinkedIn profile URL
        driver.get(linkedin_url)

        # Wait for the profile to load
        time.sleep(10)

        # Scrape profile information
        profile_data = {}

        # Scrape name
        try:
            name_element = driver.find_element(By.XPATH, "//*[@class='mt2 relative']")
            name = name_element.find_element(By.TAG_NAME, "h1").text.strip()
            profile_data['name'] = name
        except NoSuchElementException:
            profile_data['name'] = 'Name not available'
            print("Name not found")

        # Scrape headline
        try:
            headline_element = driver.find_element(By.CLASS_NAME, "text-body-medium.break-words")
            headline = headline_element.text.strip()
            profile_data['headline'] = headline
        except NoSuchElementException:
            profile_data['headline'] = 'Headline not available'
            print("Headline not found")

        # Scrape location
        try:
            location_element = driver.find_element(By.CLASS_NAME, "text-body-small.inline.t-black--light.break-words")
            location = location_element.text.strip()
            profile_data['location'] = location
        except NoSuchElementException:
            profile_data['location'] = 'Location not available'
            print("Location not found")

        # Scrape number of connections
        try:
            connections_element = driver.find_element(By.CLASS_NAME, "t-bold")
            connections = connections_element.text.strip()
            profile_data['connections'] = connections
        except NoSuchElementException:
            profile_data['connections'] = 'Connections not available'
            print("Connections not found")

        # Scrape about section
        try:
            about_element = driver.find_element(By.ID, "about").find_element(By.XPATH, "..").find_element(By.CLASS_NAME, "display-flex")
            about = about_element.text.strip()
            profile_data['about'] = about
        except NoSuchElementException:
            profile_data['about'] = 'About section not available'
            print("About section not found")

        # Navigate to the skills section
        skills_url = linkedin_url + "details/skills/"
        driver.get(skills_url)

        # Wait until skills elements are visible
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "pvs-list__paged-list-item")))
            # Scrape skills section
            try:
                skills_elements = driver.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item")
                skills = [element.text.strip() for element in skills_elements]
                profile_data['skills'] = skills
            except NoSuchElementException:
                profile_data['skills'] = ["Skills not available"]
                print("Skills not found")
        except TimeoutException:
            profile_data['skills'] = ["Skills not available"]
            print("Skills section did not load in time")

        # Construct output string
        output_data = f"Name: {profile_data['name']}, Headline: {profile_data['headline']}, Location: {profile_data['location']}, Connections: {profile_data['connections']}, About: {profile_data['about']}, Skills: {', '.join(profile_data['skills'])}"

    except Exception as e:
        print(f"Error occurred during scraping: {str(e)}")
        output_data = 'Scraping failed'

    finally:
        # Close the WebDriver
        driver.quit()

    json_data = json.dumps(output_data)
    print(json_data)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        linkedin_url = sys.argv[1]
        scraped_data = scrape_linkedin_data(linkedin_url)
        print(scraped_data)
    else:
        print("No LinkedIn URL provided.")
