# Amazon Order Details Extractor

This project uses Selenium to log in to your Amazon account, navigate to the orders page, save the page source as an XML file, and then uses OpenAI to fetch order details from the XML file.

## Prerequisites

1. **Python**: Make sure you have Python installed (version 3.6 or higher).
2. **Install Required Libraries**:
   ```sh
   pip install openai selenium beautifulsoup4
   ```
3. **ChromeDriver**: 
    Ensure you have ChromeDriver installed and it's in your system's PATH. You can download by running the following command.
    ```sh
    sudo apt-get update
    sudo apt-get install chromium-chromedrive
    ```

4. **OpenAI API Key**: 
    You need an OpenAI API key. You can set it as an environment variable or directly in the script.

## Configuration

1. **Create `config/credentials.json` File**:
    <ul>
    <li>Create a folder named config in the same directory as your script.</li>
    <li>Inside the config folder, create a file named credentials.json.</li>
    <li>Add your Amazon username and password to the credentials.json file with the following structure:</li>
    ```{    
    "username": "your_amazon_username",
    "password": "your_amazon_password"
    }
    ```
    <ul>
## Explaination

1. **Login Process**: The script logs into Amazon using credentials from config/credentials.json.
2. **Navigate to Orders Page**: It navigates to the orders page and saves the page source as an XML file.
3. **Extract Text from XML**: The extract_text_from_xml function reads the XML file and extracts its text content using BeautifulSoup.
4. **Fetch Order Details using OpenAI**: The fetch_order_details_from_openai function sends a prompt to text-davinci with the XML text and requests a summary of order details.
5. **Main Function**: The main function coordinates reading the XML file and fetching order details, then prints the extracted details.

## Notes:
    
<ul>
    <li>Ensure the chromedriver path is correct for your system.</li>
    <li>Update the config/credentials.json with your Amazon username and password.</li>
    <li>Make sure you have set your OpenAI API key correctly.</li>
</ul>

Run the script, and it will log in to Amazon, navigate to the orders page, save the page source in orders_page.xml, and then extract and print the order details using OpenAI.
