function generateSentences(isMultipleJudgement=false) {

    const generateSentences = '/generate_sentences/';

    // Fetch generated sentences
    if (isMultipleJudgement === true) {
        console.log('Bulky Judgement initiated');
        fetch(generateSentences + '?batch=true').then(response => {
            if (!response.ok) {
                throw new Error('Error in generateSentences request');
            }
            if (response.status === 200) {
                return response.json();
            } else {
                throw new Error('Unexpected response status: ' + response.status);
            }
        })
        .then(data =>{
            console.log('Django Response:', data);
            document.getElementById('sentences').innerHTML = `${JSON.stringify(data['sentences'])}`;
            // Fetch a result of entailment judgement
            judgeEntailment(data);
        })
        .catch((error) => {
            console.error('Fetch Error:', error);
        });
    } else {
        console.log('Single Judgement initiated');
        fetch(generateSentences).then(response => {
            if (!response.ok) {
                throw new Error('Error in generateSentences request');
            }
            if (response.status === 200) {
                return response.json();
            } else {
                throw new Error('Unexpected response status: ' + response.status);
            }
        })
        .then(data =>{
            console.log('Django Response:', data);
            document.getElementById('sentences').innerHTML = `${JSON.stringify(data['sentences'])}`;
            // Fetch a result of entailment judgement
            judgeEntailment(data);
        })
        .catch((error) => {
            console.error('Fetch Error:', error);
        });
    }
}
