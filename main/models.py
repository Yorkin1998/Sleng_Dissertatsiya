from django.db import models

# Create your models here.
class SlangModel(models.Model):
    
    slang = models.CharField(max_length=100)
    definition = models.CharField(max_length=300)

    def __str__(self):
        return self.slang

class SlangSentence(models.Model):

    slang = models.TextField(null=True, blank=True)
    slang_word = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.slang