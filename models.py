from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MyUser(User):
    
    imagepath=models.CharField(max_length=500,primary_key=True)

    class Meta:
        db_table='auth_user2'    


