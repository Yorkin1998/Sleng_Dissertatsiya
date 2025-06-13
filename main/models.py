from django.db import models

# Create your models here.
class SlangModel(models.Model):
    
    slang = models.CharField(max_length=100)
    definition = models.CharField(max_length=300)

    def __str__(self):
        return self.slang