from django.db import models

# Create your models here.

class Code(models.Model):
    user=models.OneToOneField('auth.User',on_delete=models.CASCADE,related_name='user')
    code=models.IntegerField(max_length=6)
    deadline=models.DateTimeField()

    def __str__(self):
        return self.user.username