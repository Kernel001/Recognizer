from django.db import models

# Create your models here.
class Source(models.Model):
    ip_adress = models.CharField(max_length=15)
    video_feed_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{} ({})".format(self.name, self.ip_adress)

class Target(models.Model):
    target_name = models.CharField(max_length=150)
    target_photo = models.BinaryField()
    target_recognizer_photo = models.BinaryField()
    targer_reco_vector = models.BinaryField()
    target_photo_info=models.CharField(max_length=150)
    def __str__(self):
        return self.target_name

class Encounter(models.Model):
    enc_time = models.DateTimeField() # use timezone.now()!!!
    enc_source = models.ForeignKey(Source, on_delete=models.DO_NOTHING)
    enc_target = models.ForeignKey(Target, on_delete=models.DO_NOTHING)
