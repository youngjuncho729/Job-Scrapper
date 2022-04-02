from django.db import models
class JobList(models.Model):
    word = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now=True)
    list = models.TextField()

    def __str__(self):
        return self.word + "-" + self.location + "-" + str(self.date)
