import getpass
import constants as c
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def __prompt_email_password():
    """
    Prompt the user for their LinkedIn email and password.
    :return: A tuple containing the email and password.
    """
    u = input("Email: ")
    p = getpass.getpass(prompt="Password: ")
    return u, p

def page_has_loaded(driver):
    """
    Check if the webpage has fully loaded.
    :param driver: The Selenium WebDriver instance.
    :return: True if the page is fully loaded, False otherwise.
    """
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'

def login(driver, email=None, password=None, cookie=None, timeout=10):
    """
    Log into LinkedIn using email and password or a cookie.
    :param driver: The Selenium WebDriver instance.
    :param email: The email address for LinkedIn login.
    :param password: The password for LinkedIn login.
    :param cookie: The cookie for LinkedIn login (if available).
    :param timeout: The maximum time to wait for page elements to load.
    """
    if cookie is not None:
        return _login_with_cookie(driver, cookie)

    if not email or not password:
        email, password = __prompt_email_password()

    # Navigate to the LinkedIn login page
    driver.get("https://www.linkedin.com/login")

    # Wait for the username field to be present
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    # Enter the email address
    email_elem = driver.find_element(By.ID, "username")
    email_elem.send_keys(email)

    # Enter the password and submit the form
    password_elem = driver.find_element(By.ID, "password")
    password_elem.send_keys(password)
    password_elem.submit()

    # Handle the post-login check for "remember me" prompt
    if driver.current_url == 'https://www.linkedin.com/checkpoint/lg/login-submit':
        remember = driver.find_element(By.ID, c.REMEMBER_PROMPT)
        if remember:
            remember.submit()

    # Wait for an element that indicates a successful login
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, c.VERIFY_LOGIN_ID)))

def _login_with_cookie(driver, cookie):
    """
    Log into LinkedIn using a pre-defined cookie.
    :param driver: The Selenium WebDriver instance.
    :param cookie: The cookie for LinkedIn login.
    """
    driver.get("https://www.linkedin.com/login")
    driver.add_cookie({
        "name": "li_at",
        "value": cookie
    })
