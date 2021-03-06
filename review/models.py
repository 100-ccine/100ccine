from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User



class Review(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    pub_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def summary(self):
        return self.content[:100]

class Comment(models.Model):
    board = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    writer = models.CharField(max_length=30, verbose_name="작성자",null=True)
    text = models.CharField(max_length=100, null=True)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
