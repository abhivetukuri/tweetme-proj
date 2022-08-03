from statistics import mode
from django.db import models
import random
from django.conf import settings

user = settings.AUTH_USER_MODEL

# Create your models here.
class Tweet(models.Model):
    #id = auto created (hidden)
    #Maps to SQL Data
    users = models.ForeignKey(user, on_delete=models.CASCADE) #many unsers can have many tweets
    content = models.TextField(blank=True,null=True)
    image = models.FileField(upload_to='images/', blank=True,null=True)

    #def __str__(self):
        #return self.content

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,100)
        }
