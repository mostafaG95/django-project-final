from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Fund(models.Model):
    title = models.CharField(db_column='title', max_length=100, blank=False)
    description = models.TextField(db_column='description', max_length=1000, blank=False)
    author = models.CharField(db_column='author', max_length=100, blank=False)
    year = models.IntegerField(db_column='year',blank=False, default=2000)
    image = models.ImageField(blank= True,upload_to='')
    user = models.ForeignKey(User, default=None,null=True, on_delete=models.CASCADE)