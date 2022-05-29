from django.db import models


class user_info(models.Model):
    user_name = models.CharField(("user_name"), max_length=300)
    fav_genre = models.CharField(("fav_genre"), max_length=300)
    fav_actor = models.CharField(("fav_actor"), max_length=300)
    fav_actress = models.CharField(("fav_actress"), max_length=300)


# Create your models here.
