# LinkedIn Profile Scraper Web Application

This project is a web application built with Node.js and Express to scrape LinkedIn profile data using Selenium in Python. It includes functionality to validate LinkedIn URLs, scrape data from profiles, and send the scraped data to an external API.

## Project Structure

<pre>my_web_scraper_app/
├── application/
│ └── person_scraping.py
│ └── actions.py
│ └── constants.py
├── public/
│ ├── validate.js
│ └── styles.css
├── views/
│ └── index.ejs
├── app.js
└── package.json</pre>


### Detailed Description

- **`app.js`**: This file contains the main application logic using Express. It sets up routes, serves static files, and handles POST requests to initiate scraping of LinkedIn profiles.

- **`views/index.ejs`**: This file defines the HTML structure for the web interface. It includes a form to input a LinkedIn URL, display messages, and show the scraped data.

- **`public/validate.js`**: This JavaScript file contains client-side validation for the LinkedIn URL entered in the form. It checks if the URL matches a specific regex pattern before submitting the form for scraping.

- **`application/person_scraping.py`**: Python script using Selenium to scrape LinkedIn profile data. It logs into LinkedIn, navigates to the provided profile URL, and extracts information such as name, headline, location, connections, about section, and skills.

- **`public/styles.css`**: CSS file defining the styling for the web interface, including layout, form elements, buttons, and animations.

## Usage

1. **Clone the Repository**:
```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
```
2. **Install Dependencies**:
```bash
    npm init
```
```bash
    npm i express body-parser child_process axios
```
3. **Install WebDriver**:
   - **Chrome WebDriver**: Ensure Chrome WebDriver is installed and configured properly. You can download it from [Chrome WebDriver](https://googlechromelabs.github.io/chrome-for-testing/).
   - Extract the WebDriver executable to a directory and update the path in `application/person_scraping.py` where `Service("path_to_chromedriver")` is set.

4. **Run the Application**:
```bash
    node app.js
```

5. **Access the Application**:
Open a web browser and go to http://localhost:3000 to use the LinkedIn Profile Scraper. Enter a valid LinkedIn profile URL and click "Scrape" to initiate the scraping process.

## Dependencies

**Node.js**: JavaScript runtime environment
**Express**: Web framework for Node.js
**Selenium WebDriver**: Browser automation tool for Python. Requires installation of Chrome WebDriver.
**axios**: Promise-based HTTP client for Node.js
**body-parser**: Middleware to handle form data in Express applications

## Notes

Ensure you have Python installed along with Chrome WebDriver configured correctly for Selenium to work.
The application uses headless Chrome for web scraping to run invisibly in the background.

## License
This project is licensed under the MIT License.
