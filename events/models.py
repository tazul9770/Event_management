from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    participants = models.ManyToManyField("Participant", related_name="events")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="events")

    def __str__(self):
        return f"{self.name} - {self.date}"
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    
