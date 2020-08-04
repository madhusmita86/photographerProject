from django.db import models

# Model class for all photographs fields
class Photos(models.Model):
    img = models.ImageField(upload_to='pics')
    img_category = models.CharField(max_length=100)
    img_desc = models.TextField(default='')
    img_special = models.BooleanField(default=False)


class UserDetails(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=25)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=200)
    user_message = models.CharField(max_length=200)

# Model class for the users images with user details
class UserImages(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    user_img = models.ImageField(upload_to='user_pics')






