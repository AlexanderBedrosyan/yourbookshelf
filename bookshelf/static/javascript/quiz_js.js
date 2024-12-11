function submitAnswer(answer, book_id) {
    const bookId = book_id;
    const userAnswer = answer;

    const resultMessage = document.getElementById('resultMessage');
    const csrfToken = document.querySelector('[name=csrf-token]').content;

    // Send the answer to the backend
    fetch('/quiz/submit_answer/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            'user_answer': userAnswer,
            'book_id': book_id
        })
    })
        .then(response => response.json())
        .then(data => {
            resultMessage.textContent = ''
            if (data.correct) {
                const message = document.createElement('p');
                message.classList.add('text-success');
                message.textContent = `Correct! 🎉 Your score: ${data.new_score}`;
                resultMessage.appendChild(message);
            } else {
                const message = document.createElement('p');
                message.classList.add('text-danger');
                message.textContent = 'Wrong answer. Try again! 😞';
                resultMessage.appendChild(message);
            }

            fetchNextQuestion()
        })
        .catch(error => {
            resultMessage.textContent = ''
            console.error('Error:', error);
            const errorMessage = document.createElement('p');
            errorMessage.classList.add('text-danger');
            errorMessage.textContent = 'Something went wrong!';
            resultMessage.appendChild(errorMessage);
        });
}

function fetchNextQuestion() {
    fetch(`/quiz/next_question/`)
        .then(response => response.json())
        .then(data => {
            document.querySelector('.card-text').innerText = data.question;

            const answersContainer = document.querySelector('.d-flex');
            answersContainer.replaceChildren();

            data.answers.forEach(answer => {
                const button = document.createElement('button');
                button.className = 'btn btn-outline-secondary btn-lg';
                button.textContent = answer;
                button.onclick = () => submitAnswer(answer, data.book_id);
                answersContainer.appendChild(button);
                button.style.marginBottom = '1.2em';
            });
        })
        .catch(error => console.error('Error:', error));
}
