from django.db import models
from users.models import User
# Create your models here.

class Post(models.Model):
    userId=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    
    
 
