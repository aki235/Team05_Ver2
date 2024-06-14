from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=100)
    subject_number = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subjects_teach = models.ManyToManyField(Subject, related_name='teachers')
    subjects_learn = models.ManyToManyField(Subject, related_name='learners')

    def __str__(self):
        return self.username
    
class AvailableSlot(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='available_slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.teacher.username} available from {self.start_time} to {self.end_time}"

class Schedule(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sessions_as_teacher')
    learner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sessions_as_student')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='scheduled_sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.teacher.username} teaches {self.learner.username} at {self.start_time}"