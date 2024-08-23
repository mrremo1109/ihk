from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Job_Seeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    address = models.TextField(max_length=80, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    company = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.company 

class Job_Post(models.Model):
    user = models.ForeignKey("Recruiter", on_delete=models.CASCADE)
    post = models.CharField(max_length=50)
    salary = models.IntegerField()
    description = models.TextField()
    posted_on = models.DateField()
    upto = models.DateField()

    def __str__(self):
        return self.post

class AppliedPost(models.Model):
    applied_by = models.ForeignKey("Job_Seeker", on_delete=models.CASCADE)
    job = models.ForeignKey("Job_Post", on_delete=models.CASCADE)
    applied_on = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('reviewing', 'Reviewing'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected')
    ], default='reviewing')

    def __str__(self):
        return f'{self.applied_by.user.first_name} {self.applied_by.user.last_name} - {self.job.post}'
    
class Feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    feedback = models.TextField()

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver} at {self.timestamp}'