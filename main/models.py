from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime

class Profile(models.Model): #class based view
    user = models.OneToOneField(User, on_delete=models.CASCADE) # OneToOneField is one to one relationship i.e the user can only have one profile
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self, *args, **kwargs): #*args and **kwargs required to create profile for superuse
        super().save(*args, **kwargs) #override normal save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300: # for resizing profile pictures so that they dont take up unneccessary space in the system
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # ForeignKey is one to many relationship i.e one user can have many posts
    date = models.DateTimeField(default=datetime.now)
    image = models.ImageField(upload_to="user_posts", blank=True, null=True)
    caption = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name="post_likes")
    like_count = models.BigIntegerField(default="0")

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    raw_date = models.DateTimeField(default=datetime.now)
    def date(self):
        return self.raw_date.strftime("%d/%m/%y")
    caption = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name="comment_likes")
    like_count = models.BigIntegerField(default="0")
