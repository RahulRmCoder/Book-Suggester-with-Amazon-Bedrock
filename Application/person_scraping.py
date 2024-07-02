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
import os

def scrape_linkedin_data(linkedin_url):
    # Initialize WebDriver with Service object
    service = Service("C:/Users/ACER/Downloads/chromedriver.exe")

    # Set up Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")

    # Create the driver with the options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # LinkedIn login credentials
    email = "rrmgoat@gmail.com"
    password = "RRM@25@12345"
    cookies_file = 'cookies.json'

    if os.path.exists(cookies_file):
        # Load cookies if they exist
        driver.get("https://www.linkedin.com")
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
            for cookie in cookies:
                # Remove 'sameSite' attribute to avoid assertion error
                if 'sameSite' in cookie:
                    del cookie['sameSite']
                driver.add_cookie(cookie)
        driver.get(linkedin_url)
    else:
        # Perform login and save cookies
        actions.login(driver, email, password)  # Login to LinkedIn
        time.sleep(2)  # Adjust sleep time as necessary

        # Save cookies to a file
        cookies = driver.get_cookies()
        with open(cookies_file, 'w') as f:
            json.dump(cookies, f)

        driver.get(linkedin_url)

    profile_data = {}

    try:
        # Wait for the profile to load
        time.sleep(2)  # Adjust sleep time as necessary

        # Scrape profile information

        # Scrape name
        try:
            name_element = driver.find_element(By.XPATH, "//*[@class='mt2 relative']")
            name = name_element.find_element(By.TAG_NAME, "h1").text.strip()
            profile_data['name'] = name
        except NoSuchElementException:
            profile_data['name'] = 'Name not available'
            # print("Name not found")  # Commented out

        # Scrape headline
        try:
            headline_element = driver.find_element(By.CLASS_NAME, "text-body-medium.break-words")
            headline = headline_element.text.strip()
            profile_data['headline'] = headline
        except NoSuchElementException:
            profile_data['headline'] = 'Headline not available'
            # print("Headline not found")  # Commented out

        # Scrape location
        try:
            location_element = driver.find_element(By.CLASS_NAME, "text-body-small.inline.t-black--light.break-words")
            location = location_element.text.strip()
            profile_data['location'] = location
        except NoSuchElementException:
            profile_data['location'] = 'Location not available'
            # print("Location not found")  # Commented out

        # Scrape number of connections
        try:
            connections_element = driver.find_element(By.CLASS_NAME, "t-bold")
            connections = connections_element.text.strip()
            profile_data['connections'] = connections
        except NoSuchElementException:
            profile_data['connections'] = 'Connections not available'
            # print("Connections not found")  # Commented out

        # Scrape about section
        try:
            about_element = driver.find_element(By.ID, "about").find_element(By.XPATH, "..").find_element(By.CLASS_NAME, "display-flex")
            about = about_element.text.strip()
            profile_data['about'] = about.replace('\n', '\\n')  # Ensure newline characters are escaped properly
        except NoSuchElementException:
            profile_data['about'] = 'About section not available'
            # print("About section not found")  # Commented out

        # Scrape experience section
        try:
            experience_url = linkedin_url + "details/experience/"
            driver.get(experience_url)
            
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, "pvs-list__paged-list-item")))
            try:
                experience_elements = driver.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item")
                experiences = [element.text.strip().replace('\n', '\\n') for element in experience_elements if element.text.strip()]
                profile_data['experience'] = experiences
            except NoSuchElementException:
                profile_data['experience'] = ["Experience not available"]
                # print("Experience not found")  # Commented out
        except TimeoutException:
            profile_data['experience'] = ["Experience section did not load in time"]
            # print("Experience section did not load in time")  # Commented out

        # Scrape education section
        try:
            education_url = linkedin_url + "details/education/"
            driver.get(education_url)
            
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, "pvs-list__paged-list-item")))
            try:
                education_elements = driver.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item")
                educations = [element.text.strip().replace('\n', '\\n') for element in education_elements if element.text.strip()]
                profile_data['education'] = educations
            except NoSuchElementException:
                profile_data['education'] = ["Education not available"]
                # print("Education not found")  # Commented out
        except TimeoutException:
            profile_data['education'] = ["Education section did not load in time"]
            # print("Education section did not load in time")  # Commented out

        # Scrape projects section
        try:
            projects_url = linkedin_url + "details/projects/"
            driver.get(projects_url)
            
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, "pvs-list__paged-list-item")))
            try:
                projects_elements = driver.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item")
                projects = [element.text.strip().replace('\n', '\\n') for element in projects_elements if element.text.strip()]
                profile_data['projects'] = projects
            except NoSuchElementException:
                profile_data['projects'] = ["Projects not available"]
                # print("Projects not found")  # Commented out
        except TimeoutException:
            profile_data['projects'] = ["Projects section did not load in time"]
            # print("Projects section did not load in time")  # Commented out

        # Navigate to the skills section
        skills_url = linkedin_url + "details/skills/"
        driver.get(skills_url)

        # Wait until skills elements are visible
        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, "pvs-list__paged-list-item")))
            # Scrape skills section
            try:
                skills_elements = driver.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item")
                skills = [element.text.strip() for element in skills_elements if element.text.strip()]
                profile_data['skills'] = skills
            except NoSuchElementException:
                profile_data['skills'] = ["Skills not available"]
                # print("Skills not found")  # Commented out
        except TimeoutException:
            profile_data['skills'] = ["Skills not available"]
            # print("Skills section did not load in time")  # Commented out

        # Concatenate fields into a single string
        if profile_data['about'] == "About section not available":
            if profile_data['skills'] == "Skills not available":
                question = (f"Name: {profile_data.get('name', '')}, Headline: {profile_data.get('headline', '')}, "
                            f"Location: {profile_data.get('location', '')}, Connections: {profile_data.get('connections', '')}, "
                            f"Experience: {', '.join(profile_data.get('experience', []))}, Education: {', '.join(profile_data.get('education', []))}, "
                            f"Projects: {', '.join(profile_data.get('projects', []))}")
            else:
                question = (f"Name: {profile_data.get('name', '')}, Headline: {profile_data.get('headline', '')}, "
                            f"Location: {profile_data.get('location', '')}, Connections: {profile_data.get('connections', '')}, "
                            f"Experience: {', '.join(profile_data.get('experience', []))}, Education: {', '.join(profile_data.get('education', []))}, "
                            f"Projects: {', '.join(profile_data.get('projects', []))}, Skills: {', '.join(profile_data.get('skills', []))}")
        elif profile_data['skills'] == "Skills not available":
            if profile_data['about'] == "About section not available":
                question = (f"Name: {profile_data.get('name', '')}, Headline: {profile_data.get('headline', '')}, "
                            f"Location: {profile_data.get('location', '')}, Connections: {profile_data.get('connections', '')}, "
                            f"Experience: {', '.join(profile_data.get('experience', []))}, Education: {', '.join(profile_data.get('education', []))}, "
                            f"Projects: {', '.join(profile_data.get('projects', []))}")
            else:
                question = (f"Name: {profile_data.get('name', '')}, Headline: {profile_data.get('headline', '')}, "
                            f"Location: {profile_data.get('location', '')}, Connections: {profile_data.get('connections', '')}, "
                            f"About: {profile_data.get('about', '')}, Experience: {', '.join(profile_data.get('experience', []))}, "
                            f"Education: {', '.join(profile_data.get('education', []))}, Projects: {', '.join(profile_data.get('projects', []))}")
        else:
            question = (f"Name: {profile_data.get('name', '')}, Headline: {profile_data.get('headline', '')}, "
                        f"Location: {profile_data.get('location', '')}, Connections: {profile_data.get('connections', '')}, "
                        f"About: {profile_data.get('about', '')}, Experience: {', '.join(profile_data.get('experience', []))}, "
                        f"Education: {', '.join(profile_data.get('education', []))}, Projects: {', '.join(profile_data.get('projects', []))}, "
                        f"Skills: {', '.join(profile_data.get('skills', []))}")

        # Construct output dictionary
        output = {
            "question": question
        }

    except Exception as e:
        # print(f"Error occurred during scraping: {str(e)}")  # Commented out
        output = {'error': 'Scraping failed'}

    finally:
        # Close the WebDriver
        driver.quit()

    output_json = json.dumps(output, indent=4, ensure_ascii=False)
    return output_json

if __name__ == "__main__":
    if len(sys.argv) > 1:
        linkedin_url = sys.argv[1]
        scraped_data = scrape_linkedin_data(linkedin_url)
        print(scraped_data)
    else:
        print("No LinkedIn URL provided.")
