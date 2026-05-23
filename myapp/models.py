from django.db import models
import datetime,math,random
from django.utils import timezone

# Create your models here.

class InstaUser(models.Model):
    GENDER_CHOICES = (
        ('male','Male'),
        ('female','Female'),
    )
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(blank=True, null=True,default=1234)

    def __str__(self):
        return self.username

    
class InstaPost(models.Model):
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    tagged_users = models.ManyToManyField(InstaUser, related_name= "tagged_posts",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

 
    def __str__(self):
        return self.caption

    def whenpublished(self):

        now = timezone.now()
        diff = now-self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + " seconds ago"
            
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600 :
            minutes = math.floor(diff.seconds/60)
             
            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"
            
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400 :
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"
            
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"
            
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago" 
            else:
                return str(months) + " months ago"
            
        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"
            
            else:
                return str(years) + " years ago"
class instrareels(models.Model):

    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    video = models.FileField(upload_to='instrareels/')
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.caption
    
    def whenpublished(self):
        now = timezone.now()
        diff = now-self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + " seconds ago"
            
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600 :
            minutes = math.floor(diff.seconds/60)
             
            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"
            
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400 :
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"
            
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"
            
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago" 
            else:
                return str(months) + " months ago"
            
        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"
            
            else:
                return str(years) + " years ago"
class FollowUsers(models.Model):
    Following = models.ForeignKey(InstaUser, on_delete=models.CASCADE,related_name="Following")
    Following_person = models.ForeignKey(InstaUser, on_delete=models.CASCADE,related_name="Following_person")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Following.name} - Following {self.Following_person.name}"

class notification(models.Model):
    notification_type = (
        ('follow','follow'),
        ('like','like'),
        ('comment','comment'),
    )

    sender = models.ForeignKey(InstaUser, on_delete=models.CASCADE,related_name="sender_notification")
    reciver = models.ForeignKey(InstaUser, on_delete=models.CASCADE,related_name="reciver_notification")
    post_fk = models.ForeignKey(InstaPost, on_delete=models.CASCADE,null=True,blank=True)
    reel_fk = models.ForeignKey(instrareels, on_delete=models.CASCADE,null=True,blank=True)
    message = models.CharField(max_length=40)
    notification_type = models.CharField(max_length=20,choices=notification_type)
    read_status = models.CharField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} {self.message} {self.reciver.username}"

    def whenpublished(self):
        now = timezone.now()
        diff = now-self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + " seconds ago"
            
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600 :
            minutes = math.floor(diff.seconds/60)
             
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"
            
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400 :
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"
            
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"
            
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago" 
            else:
                return str(months) + " months ago"
            
        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"



class like_unlike(models.Model):
    user_fk = models.ForeignKey(InstaUser, on_delete=models.CASCADE,related_name="liked_by")
    post_fk = models.ForeignKey(InstaPost, on_delete=models.CASCADE,related_name="like_post",null=True, blank=True)
    reel_fk = models.ForeignKey("instrareels", on_delete=models.CASCADE, related_name="like_reel",null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user_fk','post_fk','reel_fk']

    def __str__(self):
        if self.post_fk:
            return f"{self.user_fk.username} liked post: {self.post_fk.caption}"
        elif self.reel_fk:
            return f"{self.user_fk.username} liked reel: {self.reel_fk.caption}"

class comments(models.Model):
    user_fk = models.ForeignKey(InstaUser, on_delete=models.CASCADE,related_name="commented_by")
    post_fk = models.ForeignKey(InstaPost, on_delete=models.CASCADE,related_name="commented_post",null=True, blank=True)
    reel_fk = models.ForeignKey("instrareels", on_delete=models.CASCADE, related_name="commented_reel",null=True, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.post_fk:
            return f"{self.user_fk.username} commented post: {self.post_fk.caption}"
        elif self.reel_fk:
            return f"{self.user_fk.username} commented reel: {self.reel_fk.caption}"

class chatroom(models.Model):
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE,related_name="sender")
    user2 = models.ForeignKey(InstaUser, on_delete=models.CASCADE,related_name="receiver")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} -> {self.user2.name}"
    
class message(models.Model):
    ROLE_CHOICES = (
        ('sender', 'sender'),
        ('receiver', 'receiver'),
    )

    chat_room = models.ForeignKey(chatroom, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES) 
    content = models.TextField()
    image = models.FileField(upload_to='chat/images/', null=True, blank=True)
    video = models.FileField(upload_to='chat/videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - {self.chat_room.sender.name}"
    
    def whenpublished(self):
        now = timezone.now()
        diff = now-self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + " seconds ago"
            
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600 :
            minutes = math.floor(diff.seconds/60)
             
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"
            
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400 :
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"
            
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"
            
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago" 
            else:
                return str(months) + " months ago"
            
        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"

