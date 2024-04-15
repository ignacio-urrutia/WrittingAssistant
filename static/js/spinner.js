document.getElementById('chat-form').onsubmit = async function(e) {
    e.preventDefault();
    let formData = new FormData(this);
    document.getElementById('loading').style.display = 'block'; // Show the spinner

    let response = await fetch("/invoke_agent", {
        method: "POST",
        body: formData
    }).then(response => {
        document.getElementById('loading').style.display = 'none'; // Hide the spinner once data is received
        return response.json();
    }).catch(error => {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none'; // Ensure to hide spinner on error as well
    });

    let result = await response;
    document.getElementById('response').textContent = result.response;
    document.querySelector('textarea[name="user_input"]').value = '';  // Clear input field after sending
};
