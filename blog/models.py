from django.db import models
from django.conf import settings



# Category Ability
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# tag Ability
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Post Model
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="blog_images/", null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name="posts")
    tags = models.ManyToManyField(Tag, related_name="posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[("draft", "Draft"), ("published", "Published")],
        default="draft",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
