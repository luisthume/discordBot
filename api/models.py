from django.db import models

# Create your models here.
class Base(models.Model):
    dt_creation = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class DiscordUser(Base):
    code = models.CharField(max_length=18, unique=True)
    name = models.CharField(max_length=30)
    
    def save(self,*args,**kwargs):
        created = not self.pk
        super().save(*args,**kwargs)
        if created:
            Hour.objects.create(discorduser=self)

class Hour(Base):
    discorduser = models.ForeignKey(DiscordUser, on_delete=models.CASCADE)
    minutes = models.IntegerField(default=0, blank=True)