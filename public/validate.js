// Add an event listener to the form with the ID 'scrapeForm' that listens for the 'submit' event
document.getElementById('scrapeForm').addEventListener('submit', function(event) {
    // Retrieve the LinkedIn URL entered in the form and remove any leading or trailing whitespace
    const linkedinUrl = document.getElementById('linkedin_url').value.trim();
    
    // Define a regular expression to match valid LinkedIn profile URLs
    const linkedinRegex = /^https:\/\/[a-z]{2,3}\.linkedin\.com\/.*$/;

    // Check if the entered LinkedIn URL matches the defined regular expression
    if (!linkedinRegex.test(linkedinUrl)) {
        // If the URL is invalid, prevent the form from being submitted
        event.preventDefault();
        // Display an error message indicating that the LinkedIn URL format is invalid
        document.getElementById('message').textContent = 'Invalid LinkedIn URL format.';
    } else {
        // If the URL is valid, clear any existing error messages
        document.getElementById('message').textContent = ''; 

        // Show the loading animation by changing its display style to 'block'
        document.getElementById('loader').style.display = 'block';
        // Hide the form by changing its display style to 'none'
        document.getElementById('scrapeForm').style.display = 'none'; 

        // Submit the form to the server
        this.submit();
    }
});
