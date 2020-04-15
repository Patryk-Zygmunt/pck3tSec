from django.db import models

# Create your models here.


class BlackListItem(models.Model):
    id = models.IntegerField(primary_key=True)
    host = models.CharField(max_length=15)

