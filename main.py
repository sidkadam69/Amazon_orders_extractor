import json
import openai
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure your API key is set as an environment variable

# Load credentials from the JSON file
with open('config/credentials.json', 'r') as file:
    credentials = json.load(file)

username = credentials['username']
password = credentials['password']

# Set up the webdriver
driver = webdriver.Chrome("/usr/bin/chromedriver")
driver.get("https://www.amazon.in/")

# Log in to Amazon
try:
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-link-accountList"]/span'))
    )
    sign_in_button.click()
    
    username_textbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ap_email"))
    )
    username_textbox.send_keys(username)
    
    continue_button = driver.find_element(By.ID, "continue")
    continue_button.click()
    
    password_textbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ap_password"))
    )
    password_textbox.send_keys(password)
    
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "signInSubmit"))
    )
    driver.execute_script("arguments[0].click();", sign_in_button)
    
except Exception as e:
    print(f"Error during login: {e}")
    driver.quit()

# Navigate to orders page
try:
    orders_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="nav-orders"]'))
    )
    orders_link.click()
    
    # Wait for the orders to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "order")]'))
    )
    
    # Save the page source as XML
    with open('orders_page.xml', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    print("Orders page has been saved as orders_page.xml")
    
except Exception as e:
    print(f"Error navigating to orders page: {e}")
    driver.quit()

# Close the browser
driver.quit()

# Function to extract text from XML
def extract_text_from_xml(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text()

# Function to fetch order details using GPT-4
def fetch_order_details_from_gpt4(xml_text):
    prompt = f"Extract and summarize the order details from the following XML content:\n\n{xml_text}\n\nThe details should include order date, order total, and item names."

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

# Main function to integrate both processes
def main():
    xml_file = 'orders_page.xml'
    xml_text = extract_text_from_xml(xml_file)
    
    order_details = fetch_order_details_from_gpt4(xml_text)
    print("Order Details Extracted from XML:")
    print(order_details)

if __name__ == "__main__":
    main()
