# admin.py

from django.contrib import admin
from .models import Post, Category, Tag



# registertions
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
