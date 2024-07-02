document.getElementById('scrapeForm').addEventListener('submit', function(event) {
    const linkedinUrl = document.getElementById('linkedin_url').value.trim();

    const linkedinRegex = /^https:\/\/[a-z]{2,3}\.linkedin\.com\/.*$/;

    if (!linkedinRegex.test(linkedinUrl)) {
        event.preventDefault();
        document.getElementById('message').textContent = 'Invalid LinkedIn URL format.';
    } else {
        document.getElementById('message').textContent = ''; // Clear error message if URL is valid
        document.getElementById('loader').style.display = 'block';
        document.getElementById('scrapeForm').style.display = 'none'; // Hide the form
    }
});

function goBack() {
    document.getElementById('result').style.display = 'none';
    document.getElementById('scrapeForm').style.display = 'block';
}
