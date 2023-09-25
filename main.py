from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException


import random
import string
import requests
import time

def gen_password(length, special_chars=False, digits=False, upper_case=False, lower_case=False):
    """
    Generate a random password with the specified length and optional inclusion of special characters, digits, uppercase letters, and lowercase letters.
    @param length - the length of the password
    @param special_chars - whether to include special characters in the password (default: False)
    @param digits - whether to include digits in the password (default: False)
    @param upper_case - whether to include uppercase letters in the password (default: False)
    @param lower_case - whether to include lowercase letters in the password (default: False)
    @return The generated password
    """
    password = ''
    for _ in range(length):
        password += random.choice(string.ascii_lowercase)
    if special_chars:
        password += random.choice(string.punctuation)
    if digits:
        password += random.choice(string.digits)
    if upper_case:
        password += random.choice(string.ascii_uppercase)
    return password

def clear_input(input):
    """
    Clear the input field by selecting all text and deleting it.
    @param input - the input field to be cleared
    """
    input.send_keys(Keys.COMMAND, 'a')
    input.send_keys(Keys.BACK_SPACE)

def get_mailbox():
    """
    Retrieve the mailbox associated with the current user.
    @return The mailbox object.
    """
    api_key = 'd04d8e4e-b501-4bce-8e5e-bf4e4da95b42'
    namespace = 'j4bjm'
    url = f'https://api.testmail.app/api/json?apikey={api_key}&namespace={namespace}&pretty=true'
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        email = response.json()['emails']
        return email
    else:
        print('Error getting email')

def num_emails():
    """
    Retrieve the number of emails in the mailbox associated with the current user.
    """
    api_key = 'd04d8e4e-b501-4bce-8e5e-bf4e4da95b42'
    namespace = 'j4bjm'
    url = f'https://api.testmail.app/api/json?apikey={api_key}&namespace={namespace}&pretty=true'
    response = requests.get(url)
    if response.status_code == 200:
        num = response.json()['count']
        return num
    else:
        print('Error getting mailbox')

def gen_email(name):
    """
    Generate a random email address.
    @return A randomly generated email address.
    """
    namespace = 'j4bjm'
    tag = name.replace(' ', '')
    email = f'{namespace}.{tag}@inbox.testmail.app'
    return email

def log_creds(email, password):
    """
    This function logs the credentials provided by the user.
    @param creds - the credentials provided by the user
    @return None
    """
    with open('creds.txt', 'a') as f:
        f.write(f'{email}:{password}\n')

def parseEmail(text):
    """
    Parse an email and extract relevant information such as the sender, recipient, subject, and body.
    @return A dictionary containing the parsed email information
    """
    index = text.find('app:')
    code = text[0:6]
    return code

if __name__ == "__main__":
    options = Options()
    # options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    driver.get("https://www.instagram.com/accounts/emailsignup/")
       
    inputs = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'input')))
    buttons = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'button')))
    # Generate random credentials
    fake = Faker()
    name = fake.name() #full name
    email = gen_email(name)
    password = gen_password(10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    inputs[0].send_keys(email)
    inputs[1].send_keys(name) 
    inputs[3].send_keys(password) 
    log_creds(email, password)
    # try different usernames until one works
    while(1):
        try: 
            inputs[2].send_keys('_' + fake.user_name()) #username
            buttons[1].click() #submit
            errors = wait.until(EC.visibility_of_all_elements_located((By.ID, 'ssfErrorAlert')))
            clear_input(inputs[2]) #clear username
        except StaleElementReferenceException:
            continue
        except TimeoutException:
            break
    try:
        # birthday
        time.sleep(1)
        element = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'select')))
        month = Select(element[0])
        day = Select(element[1])
        year = Select(element[2])
        month.select_by_value(str(random.randint(1, 12)))
        day.select_by_value(str(random.randint(1, 30)))
        year.select_by_value(str(random.randint(1919, 2005)))
        time.sleep(1)
        buttons = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
        buttons[1].click()
        # 2FA
        time.sleep(5)
        oldnum = num_emails()
        while(1):
            if oldnum != num_emails():
                break
        emails = get_mailbox()
        input = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input')))
        con_code = parseEmail(emails[0]['subject'])
        input.send_keys(con_code)
        buttons = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))
        buttons[0].click()
        time.sleep(25)
        driver.quit()
    except TimeoutException:
        print('Timeout')
        exit(-1)

    driver.quit()

   