
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('bookshelf.book.urls')),
    path('author/', include('bookshelf.author.urls')),
]
