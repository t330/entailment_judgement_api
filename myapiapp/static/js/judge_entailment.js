function judgeEntailment(data) {
    // Get CSRF token
    const csrftoken = getCSRFToken();
    console.log('CSRF Token:', csrftoken);

    // Fetch a result of entailment judgement
    const judge = '/judge/';
    fetch(judge, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error in judge request');
        }
        if (response.status === 200) {
            return response.json();
        } else {
            throw new Error('Unexpected response status: ' + response.status);
        }
    })
    .then(data => {
        console.log('Django Response:', data);
        document.getElementById('results').innerHTML = `${JSON.stringify(data['results'])}`;
    })
    .catch((error) => {
        console.error('Fetch Error:', error);
    });
}
