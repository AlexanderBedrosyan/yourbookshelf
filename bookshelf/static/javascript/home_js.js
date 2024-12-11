document.addEventListener('DOMContentLoaded', () => {
    const commentForms = document.querySelectorAll('form[id^="comment-"]');

    commentForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const url = form.action;
            const formData = new FormData(form);
            const commentList = form.closest('.card').querySelector('.list-group');

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                if (!response.ok) {
                    throw new Error('Failed to submit the comment.');
                }

                const data = await response.json();

                const newComment = document.createElement('li');
                newComment.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');

                const contentDiv = document.createElement('div');
                contentDiv.classList.add('d-flex', 'justify-content-between', 'w-100');

                const textDiv = document.createElement('div');
                textDiv.innerHTML = `<strong>${data.username}</strong>: ${data.text}`;

                const buttonGroupDiv = document.createElement('div');
                buttonGroupDiv.classList.add('d-flex', 'align-items-center', 'flex-column', 'flex-md-row');

                const btnGroup = document.createElement('div');
                btnGroup.classList.add('btn-group', 'mb-2', 'mb-md-0');

                const editLink = document.createElement('a');
                editLink.href = `/${data.id}/edit_comment/`;
                editLink.classList.add('btn', 'btn-sm', 'btn-light');
                editLink.textContent = 'Edit';

                const deleteLink = document.createElement('a');
                deleteLink.href = `/${data.id}/delete_comment/`;
                deleteLink.classList.add('btn', 'btn-sm', 'btn-light');
                deleteLink.textContent = 'Delete';

                const createdAt = document.createElement('small');
                createdAt.classList.add('text-muted', 'ml-2');
                createdAt.textContent = data.created_at;

                btnGroup.append(editLink, deleteLink, createdAt);
                buttonGroupDiv.append(btnGroup);

                contentDiv.append(textDiv, buttonGroupDiv);
                newComment.appendChild(contentDiv);
                commentList.append(newComment);
                form.reset();
            } catch (error) {
                console.error('Error:', error);
                alert('There was an error submitting your comment. Please try again.');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const ratingElements = document.querySelectorAll('.rating');

    ratingElements.forEach(rating => {
        const bookId = rating.getAttribute('data-book-id');
        const stars = rating.querySelectorAll('.rating-star');

        stars.forEach(star => {
            star.addEventListener('click', () => {
                const ratingValue = star.getAttribute('data-value');
                const url = `/rate_book/${bookId}/`;
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                fetch(url, {
                    method: 'POST',
                    body: new URLSearchParams({rating: ratingValue}),
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Failed to submit rating');
                        }
                        return response.json();
                    })
                    .then(data => {
                        const averageRatingElement = document.getElementById(`average-rating-${bookId}`);
                        if (averageRatingElement) {
                            averageRatingElement.textContent = data.new_average_rating;
                        }

                        stars.forEach(s => {
                            s.classList.toggle('text-warning', s.getAttribute('data-value') <= ratingValue);
                            s.classList.toggle('text-muted', s.getAttribute('data-value') > ratingValue);
                        });
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('An error occurred while submitting your rating.');
                    });
            });
        });
    });
});
