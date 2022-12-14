from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Post(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,blank=True,related_name="likes")
    dislikes = models.ManyToManyField(User,blank=True,related_name="dislikes")
    
    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey('Post',on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,verbose_name='user',related_name='profile')
    name = models.CharField(max_length=30,blank=True,null=True)
    bio = models.TextField(max_length=500,blank=True,null=True)
    birth_date = models.DateField(null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to='uploads/ProfileImages',default='uploads/ProfileImages/default.png',blank=True)
    followers = models.ManyToManyField(User,blank=True,related_name="followers")


@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
