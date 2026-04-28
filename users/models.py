from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import base64
from django.conf import settings
from .basic_algorithms.chiphers import encrypt, decrypt
# Create your models here.


# User's profiles
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

#Rubrics
class Rubric(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name


#Messages    
class Messages(models.Model):
    name = models.TextField(default="Noname",verbose_name="Имя")

#users
    sender=models.CharField(max_length=150,blank=True,verbose_name="Отправитель")
    getter=models.CharField(max_length=150,blank=True,verbose_name="Получатель")

#content
    message=models.TextField(verbose_name="Сообщение",null=True ,blank=True)
    image=models.ImageField(verbose_name="картинка",upload_to="images/", null=True,blank=True)
    file=models.FileField(verbose_name="файл", upload_to="files/",null=True ,blank=True)
    video=models.FileField(verbose_name="видео", upload_to="videos/", null=True, blank=True)
    published=models.DateTimeField(default=timezone.now,blank=True)

    def __str__(self):
        return self.name
    
     

    #code encrypter
    def save(self, *args, **kwargs):
        # Encrypt text before storing; avoid double‑encrypting by
        # checking for the "enc:" prefix. Leave None/empty as-is.
        if self.message:
            if not str(self.message).startswith("enc:"):
                self.message = "enc:" + encrypt(self.message)
        super().save(*args, **kwargs)

    def get_decrypted(self):
        """Return decrypted plaintext for the stored message.

        Stored messages are prefixed with "enc:". If decryption fails
        an empty string is returned.
        """
        if not self.message:
            return ""
        text = str(self.message)
        if text.startswith("enc:"):
            try:
                return decrypt(text[len("enc:"):])
            except Exception:
                return ""
        return text  # already plain text


# Simple room model for HTTP-polling WebRTC signaling
import uuid


class VideoRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    initiator = models.CharField(max_length=150, blank=True)
    callee = models.CharField(max_length=150, blank=True)
    offer = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class IceCandidate(models.Model):
    room = models.ForeignKey(VideoRoom, on_delete=models.CASCADE, related_name='candidates')
    sender = models.CharField(max_length=20)  # 'initiator' or 'callee'
    candidate = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room.id} {self.sender}"
    

class AcceptedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address
