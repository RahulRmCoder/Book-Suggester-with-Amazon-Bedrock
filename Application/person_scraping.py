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
    """
    Scrapes LinkedIn profile data from a given LinkedIn URL.
    
    Args:
    linkedin_url (str): The URL of the LinkedIn profile to scrape.
    
    Returns:
    str: A JSON string containing the scraped profile data or an error message.
    """
    # Initialize WebDriver with Service object
    service = Service("C:/Users/ACER/Downloads/chromedriver.exe")

    # Set up Chrome options to run in headless mode (without a GUI)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")

    # Create the driver with the specified options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # LinkedIn login credentials (to be provided)
    email = ""
    password = ""

    # Log in to LinkedIn
    actions.login(driver, email, password)  # Perform login using provided credentials
    time.sleep(2)  # Adjust sleep time if necessary

    # Dictionary to store scraped profile data
    profile_data = {}

    try:
        # Navigate to the LinkedIn profile URL
        driver.get(linkedin_url)

        # Wait for the profile page to load
        time.sleep(2)  # Adjust sleep time if necessary

        # Scrape profile information

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
            profile_data['about'] = about.replace('\n', '\\n')  # Ensure newline characters are escaped properly
        except NoSuchElementException:
            profile_data['about'] = 'About section not available'
            print("About section not found")

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
                print("Experience not found")
        except TimeoutException:
            profile_data['experience'] = ["Experience section did not load in time"]
            print("Experience section did not load in time")

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
                print("Education not found")
        except TimeoutException:
            profile_data['education'] = ["Education section did not load in time"]
            print("Education section did not load in time")

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
                print("Projects not found")
        except TimeoutException:
            profile_data['projects'] = ["Projects section did not load in time"]
            print("Projects section did not load in time")

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
                print("Skills not found")
        except TimeoutException:
            profile_data['skills'] = ["Skills section did not load in time"]
            print("Skills section did not load in time")

        # Concatenate fields into a single string
        question = (f"Name: {profile_data.get('name', '')}, Headline: {profile_data.get('headline', '')}, "
                    f"Location: {profile_data.get('location', '')}, Connections: {profile_data.get('connections', '')}, "
                    f"About: {profile_data.get('about', '')}, Experience: {', '.join(profile_data.get('experience', []))}, "
                    f"Education: {', '.join(profile_data.get('education', []))}, "
                    f"Projects: {', '.join(profile_data.get('projects', []))}, "
                    f"Skills: {', '.join(profile_data.get('skills', []))}")

        # Construct output dictionary
        output = {
            "question": question
        }

    except Exception as e:
        # Handle exceptions during scraping
        print(f"Error occurred during scraping: {str(e)}")
        output = {'error': 'Scraping failed'}

    finally:
        # Close the WebDriver
        driver.quit()

    # Convert output dictionary to JSON string
    output_json = json.dumps(output, indent=4, ensure_ascii=False)
    return output_json

if __name__ == "__main__":
    # Check if a LinkedIn URL was provided as a command line argument
    if len(sys.argv) > 1:
        linkedin_url = sys.argv[1]
        # Perform scraping and print the result
        scraped_data = scrape_linkedin_data(linkedin_url)
        print(scraped_data)
    else:
        # Print error message if no URL was provided
        print("No LinkedIn URL provided.")
