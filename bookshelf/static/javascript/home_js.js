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
                newComment.innerHTML = `
                    <div class="d-flex justify-content-between w-100">
                        <div>
                            <strong>${data.username}</strong>: ${data.text}
                        </div>
                        <div class="d-flex align-items-center flex-column flex-md-row">
                            <div class="btn-group mb-2 mb-md-0">
                                <a href="/edit_comment/${data.id}/" class="btn btn-sm btn-light">Edit</a>
                                <a href="/delete_comment/${data.id}/" class="btn btn-sm btn-light">Delete</a>
                            </div>
                            <small class="text-muted ml-2">${data.created_at}</small>
                        </div>
                    </div>
                `;
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
                    body: new URLSearchParams({ rating: ratingValue }),
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

                    // Highlight selected stars
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
