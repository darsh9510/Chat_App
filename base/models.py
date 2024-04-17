from django.db import models
from django.contrib.auth.models import AbstractUser,User



class topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class modarator(models.Model):
    modarator_user = models.OneToOneField(User, on_delete=models.CASCADE)
    modarator_id = models.IntegerField(null= False)


class Rooms(models.Model):
    name = models.CharField(max_length=100)
    type = models.IntegerField(null=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rtopic = models.ForeignKey(topic, on_delete=models.SET_NULL, null=True)
    participent = models.ManyToManyField(User, related_name='participent',null = True)
    modarator = models.ManyToManyField(modarator, related_name='modarator', null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Anonumous(models.Model):
    anonumous_user = models.ForeignKey(User, on_delete=models.CASCADE)
    anonumous_name = models.CharField(max_length=100)
    anonumous_room = models.ForeignKey(Rooms, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.anonumous_name
    class Meta:
        ordering = ['anonumous_name']

class Massage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    a_name = models.ForeignKey(Anonumous, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    room = models.ForeignKey(Rooms, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ['created_at']
