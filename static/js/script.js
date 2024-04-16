var easyMDE;
document.addEventListener('DOMContentLoaded', function () {
    easyMDE = new EasyMDE({ element: document.getElementById('article-content') });
});

function submitMDEContent(event) {
    event.preventDefault(); // Prevent the form from causing a page reload
    let markdownContent = easyMDE.value();

    // get session_id from the url
    // Example URL: http://127.0.0.1:5000/session/ntN1lAjeSXo9zXU9WGUn
    let url = new URL(window.location.href);
    let session_id = url.pathname.split('/').pop();
    fetch("/update_article/" + session_id, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ article: markdownContent })
    }).then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert("Article updated successfully!");
    }).catch((error) => {
        console.error('Error:', error);
        alert("An error occurred while updating the article.");
    });
}

document.getElementById('chat-form').onsubmit = async function(e) {
    e.preventDefault();
    let formData = new FormData(this);
    let session_id = window.location.pathname.split('/').pop();
    formData.append('session_id', session_id);

    document.getElementById('response').innerHTML = '';
    document.querySelector('textarea[name="user_input"]').value = '';  // Clear input field after sending
    document.getElementById('loading').style.display = 'block'; // Show the spinner

    let response = await fetch("/invoke_agent", {
        method: "POST",
        body: formData
    });
    response = await response.json();  // Get the JSON response
    document.getElementById('loading').style.display = 'none'; // Hide the spinner

    // Create a new div for the response and append it to the response container
    let responseDiv = document.createElement('div');
    responseDiv.className = 'response-message';
    responseDiv.textContent = response.response;  // Assuming 'response' is the key where the server sends its text

    let converter = new showdown.Converter();
    let html = converter.makeHtml(response.response);
    responseDiv.innerHTML = html;
    document.getElementById('response').appendChild(responseDiv);

    easyMDE.value(response.content);  // Update the article content with the response content
    document.getElementById('response').scrollTop = document.getElementById('response').scrollHeight; // Scroll to the bottom of the response container
};