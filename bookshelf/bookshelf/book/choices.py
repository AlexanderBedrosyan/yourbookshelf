from django.db import models


class GenreChoices(models.TextChoices):
    CLASSICS = 'Classics', 'Classics'
    CRIME = 'Crime', 'Crime'
    THRILLER = 'Thriller', 'Thriller'
    SPORTS = 'Sports', 'Sports'
    BIOGRAPHY = 'Biography', 'Biography'
    FICTION = 'Fiction', 'Fiction'
    SCIENCE = 'Science', 'Science'
    FANTASY = 'Fantasy', 'Fantasy'
    HORROR = 'Horror', 'Horror'
    BUSINESS = 'Business', 'Business'
    PSYCHOLOGY = 'Psychology', 'Psychology'
    NONFICTION = 'Nonfiction', 'Nonfiction'
    OTHERS = 'Others', 'Others'


class BookStatusChoices(models.TextChoices):
    WANT_TO_READ = 'Want to Read', 'Want to Read'
    CURRENTLY_READING = 'Currently Reading', 'Currently Reading'
    READ = 'Read', 'Read'
    NONE = 'None', 'None'