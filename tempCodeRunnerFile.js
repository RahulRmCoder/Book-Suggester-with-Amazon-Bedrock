import express from 'express';
import bodyParser from 'body-parser';
import { exec } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import axios from 'axios';

const app = express();
const port = 3000;

// Get the directory name of the current module file
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.render('index');
});

app.post('/scrape', (req, res) => {
    const linkedinUrl = req.body.linkedin_url;

    // Updated LinkedIn URL regex to allow for different valid formats
    const linkedinRegex = /^https:\/\/[a-z]{2,3}\.linkedin\.com\/.*$/;
    if (!linkedinRegex.test(linkedinUrl)) {
        return res.send('Invalid LinkedIn URL format.');
    }

    // Run the Python script with the URL to scrape data
    exec(`python Application/person_scraping.py "${linkedinUrl}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.send('Error occurred while running the script.');
        }

        console.log('Python script output:', stdout);

        // Attempt to parse the scraped JSON data
        let scrapedData;
        try {
            scrapedData = JSON.parse(stdout.trim());
        } catch (err) {
            console.error('Error parsing scraped data:', err);
            return res.send('Error parsing scraped data.');
        }

        // Validate the scraped data
        if (!isValidJSON(scrapedData)) {
            return res.send('Invalid JSON data');
        }

        // Define API endpoint URL
        const apiUrl = 'https://llm.notionpress.in/api/v1/prediction/dd343f26-5094-4e41-846f-a7c43cd47cb6';

        // Send scraped data to the API
        axios.post(apiUrl, scrapedData, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            // Handle API response
            console.log('API Response:', response.data);
            const bookSuggestions = response.data.text; // Assuming "text" field contains the suggestions

            // Render response on the webpage (with HTML structure)
            res.send(`
                <h2>Scraped Data</h2>
                <pre>${bookSuggestions}</pre>
            `);
        })
        .catch(err => {
            console.error('Error sending data to API:', err);
            res.send('Error sending data to API.');
        });
    });
});

// Helper function to validate JSON data
function isValidJSON(data) {
    try {
        JSON.stringify(data);
    } catch (err) {
        return false;
    }
    return true;
}

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});