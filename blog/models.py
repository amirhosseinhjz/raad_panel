from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-priority', '-pub_date']
        verbose_name_plural = "پست ها"
        verbose_name = "پست"


class BlogPostImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='blog_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name_plural = "عکس ها"
        verbose_name = "عکس"
