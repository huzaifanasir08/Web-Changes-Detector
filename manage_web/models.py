from django.db import models

class Web(models.Model):
    web_name = models.CharField(max_length=255)
    web_url = models.CharField(max_length=255)

    def __str__(self):
        return self.web_name
