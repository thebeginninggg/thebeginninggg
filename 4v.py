import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker

# Configuration
CHROMEDRIVER_PATH = 'C:\\chromedriver\\chromedriver-win64\\chromedriver.exe'  # Update this path
WAIT_TIME = 15  # Increased wait time to handle slower page loads

# Initialize Faker
faker = Faker()

def setup_driver():
    chrome_options = Options()
    # Comment out headless mode for debugging
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    # Optional: Add user-agent to mimic a real browser
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def close_overlays(driver):
    try:
        # Wait for the overlay to be present
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'zbc-content'))
        )
        # Click the close button on the overlay
        close_button = driver.find_element(By.CLASS_NAME, 'zbc-close-icon')
        close_button.click()
        print("Overlay closed.")
    except (NoSuchElementException, TimeoutException):
        print("No overlay found.")

def create_zoho_account(driver, first_name, last_name, email, password):
    try:
        driver.get('https://www.zoho.com/signup.html')  # Zoho sign-up URL

        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )

        # Close any overlays or pop-ups
        close_overlays(driver)

        # Fill out the registration form
        driver.find_element(By.NAME, 'email').send_keys(email)
        driver.find_element(By.NAME, 'password').send_keys(password)

        # Agree to the terms of service
        tos_checkbox = driver.find_element(By.NAME, 'tos')
        if not tos_checkbox.is_selected():
            tos_checkbox.click()

        submit_button = driver.find_element(By.ID, 'signupbtn')
        submit_button.click()

        print("Zoho account registration attempted.")

        # Additional code to handle post-submission steps...

    except Exception as e:
        print(f"Error during Zoho registration: {e}")
        driver.save_screenshot('zoho_error_screenshot.png')
        with open('page_source_zoho.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)
        print("Screenshot and HTML source saved for debugging.")


def generate_fake_data():
    first_name = faker.first_name()
    last_name = faker.last_name()
    # Generate a username without special characters
    username = faker.user_name() + str(faker.random_int(1000, 9999))
    password = faker.password(length=12)
    return first_name, last_name, username, password

def create_zoho_account(driver, first_name, last_name, email, password):
    try:
        driver.get('https://www.zoho.com/signup.html')  # Zoho sign-up URL

        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )

        # Fill out the registration form
        driver.find_element(By.NAME, 'email').send_keys(email)
        driver.find_element(By.NAME, 'password').send_keys(password)

        # Find the 'Terms of Service' checkbox element
        tos_checkbox = driver.find_element(By.NAME, 'tos')

        # Scroll to the checkbox before clicking
        driver.execute_script("arguments[0].scrollIntoView();", tos_checkbox)
        time.sleep(1)  # Wait for any scrolling animations

        # Click the checkbox if it's not already selected
        if not tos_checkbox.is_selected(): tos_checkbox.click()

        # Use JavaScript to click the checkbox
        driver.execute_script("arguments[0].click();", tos_checkbox)

        # Wait until the checkbox is clickable
        tos_checkbox = WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.NAME, 'tos'))
        )

        # Switch to iframe if necessary
        iframe = driver.find_element(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(iframe)

        # Perform actions inside iframe
        # ...

        # Switch back to the default content
        driver.switch_to.default_content()

        # Agree to the terms of service
        tos_checkbox = driver.find_element(By.NAME, 'tos')
        if not tos_checkbox.is_selected():
            tos_checkbox.click()

        submit_button = driver.find_element(By.ID, 'signupbtn')
        submit_button.click()

        print("Zoho account registration attempted.")

        # Wait for potential captcha
        time.sleep(5)

        # Check for success message or captcha
        if "verify your sign-up" in driver.page_source.lower():
            print("Account created successfully or further verification needed.")
        else:
            print("Registration may have failed or requires manual verification.")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error during Zoho registration: {e}")
        with open('page_source_zoho.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)
        print("HTML source saved to 'page_source_zoho.html' for debugging.")

def handle_yahoo_registration(driver, first_name, last_name, username, password):
    try:
        driver.get('https://login.yahoo.com/account/create')  # Yahoo Mail sign-up URL

        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, 'usernamereg-firstName'))
        )

        # Fill out the registration form
        driver.find_element(By.ID, 'usernamereg-firstName').send_keys(first_name)
        driver.find_element(By.ID, 'usernamereg-lastName').send_keys(last_name)
        driver.find_element(By.ID, 'usernamereg-yid').send_keys(username)
        driver.find_element(By.ID, 'usernamereg-password').send_keys(password)

        # Select country code (assuming US for this example)
        country_code_dropdown = driver.find_element(By.NAME, 'shortCountryCode')
        country_code_dropdown.send_keys('United States (+1)')

        # Enter a valid phone number
        phone_number = input("Enter your phone number for verification (e.g., 5551234567): ")
        driver.find_element(By.ID, 'usernamereg-phone').send_keys(phone_number)

        # Birthdate
        driver.find_element(By.ID, 'usernamereg-month').send_keys('January')
        driver.find_element(By.ID, 'usernamereg-day').send_keys('1')
        driver.find_element(By.ID, 'usernamereg-year').send_keys('1990')

        submit_button = driver.find_element(By.ID, 'reg-submit-button')
        submit_button.click()

        print("Yahoo account registration attempted.")

        # Wait for the SMS verification page to load
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, 'verificationCode'))
        )

        # Prompt user to enter the verification code
        verification_code = input("Enter the verification code sent to your phone: ")
        driver.find_element(By.NAME, 'verificationCode').send_keys(verification_code)
        driver.find_element(By.ID, 'verify-code-button').click()

        print("Yahoo account registration completed.")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error during Yahoo registration: {e}")
        with open('page_source_yahoo.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)
        print("HTML source saved to 'page_source_yahoo.html' for debugging.")

def main():
    driver = setup_driver()
    try:
        first_name, last_name, username, password = generate_fake_data()
        email = f"{username}@gmail.com"  # Use a realistic email format
        print(f"Generated credentials:\nFirst Name: {first_name}\nLast Name: {last_name}\nUsername: {username}\nPassword: {password}\nEmail: {email}")

        # Create Zoho account
        create_zoho_account(driver, first_name, last_name, email, password)

        # Create Yahoo account
        handle_yahoo_registration(driver, first_name, last_name, username, password)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
