from django.db import models

# Create your models here.
class SourceList(models.Model):
    ip_adress = models.CharField(max_length=15)
    video_feed_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{} ({})".format(self.name, self.ip_adress)

class Targets(models.Model):
    target_name = models.CharField(max_length=150)
    target_photo = models.BinaryField()

    def __str__(self):
        return self.target_name

class Encounters(models.Model):
    enc_time = models.DateTimeField() # use timezone.now()!!!
    enc_source = models.ForeignKey(SourceList, on_delete=models.DO_NOTHING)
    enc_target = models.ForeignKey(Targets, on_delete=models.DO_NOTHING)
