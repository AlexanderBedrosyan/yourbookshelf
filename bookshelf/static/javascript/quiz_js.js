function submitAnswer(answer, book_id) {
    const bookId = book_id;
    const userAnswer = answer;
    console.log(bookId)

    const resultMessage = document.getElementById('resultMessage');
    console.log(answer)
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
            if (data.correct) {
                resultMessage.innerHTML = `<p class="text-success">Correct! 🎉 Your score: ${data.new_score}</p>`;
            } else {
                resultMessage.innerHTML = `<p class="text-danger">Wrong answer. Try again! 😞</p>`;
            }

            fetchNextQuestion()
        })
        .catch(error => {
            console.error('Error:', error);
            resultMessage.innerHTML = '<p class="text-danger">Something went wrong!</p>';
        });
}

function fetchNextQuestion() {
    fetch(`/quiz/next_question/`)
        .then(response => response.json())
        .then(data => {
            document.querySelector('.card-text').innerText = data.question;

            const answersContainer = document.querySelector('.d-flex');
            answersContainer.innerHTML = '';

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
