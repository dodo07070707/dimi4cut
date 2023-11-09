from django.db import models


class Data(models.Model):
    image = models.ImageField(upload_to='media/')
    user_id = models.IntegerField()
    pw = models.CharField(max_length=6)

    def __str__(self) -> str:
        return str(self.user_id)
