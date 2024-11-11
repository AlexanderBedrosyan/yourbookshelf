from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookshelf.common.urls')),
    path('book/', include('bookshelf.book.urls')),
    path('author/', include('bookshelf.author.urls')),
    path('accounts/', include('bookshelf.accounts.urls')),
]
