from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
<<<<<<< HEAD:news/models.py
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)  # added
=======
    pub_date = models.DateTimeField()
>>>>>>> 004ab6783df51e7660ea2dd5a0182e380bcfb5d7:newsapp/models.py

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title