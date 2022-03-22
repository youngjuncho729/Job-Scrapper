from statistics import mode
from django.db import models

# Create your models here.
class jobList(models.Model):
    word = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True)
    date = models.DateField(auto_now_add=True)
    list = models.TextField()

    def __str__(self):
        return self.word + "-" + self.location + "-" + str(self.date)
