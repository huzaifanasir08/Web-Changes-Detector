from django.db import models
from manage_web.models import Web  # Import the Web model
import datetime
class Check(models.Model):
    web_name = models.ForeignKey(Web, on_delete=models.CASCADE) # Add a foreign key to the Web model
    original_hash = models.JSONField() # Add a JSONField to store the original hash of each web page
    status = models.CharField(max_length=255) # Status of the web page, whether it online or offline
    result = models.CharField(max_length=255)  # Result of the check, whether the web page is modified or not
    last_check = models.CharField(max_length=255)  # Last check time of the web page
    content = models.TextField() # Content of the whole web. This field is used to store the content of the web page

    def __str__(self):
        return f"{self.web_name.web_name} is now {self.status} and last check = {self.result}"
