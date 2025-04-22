from django.db import models

class FSUser(models.Model):
    user_id = models.CharField(max_length=255)
    # keys = models.OneToOneField(FiatShamirKeys, on_delete=models.CASCADE)

class FSDevicePK(models.Model):
    # set key's max_length from a constant for the specific znp implementation
    n = models.BinaryField(max_length=2024)
    v = models.BinaryField(max_length=2024)
    user = models.ForeignKey(FSUser, on_delete=models.CASCADE)

class FSOtherPK(models.Model):
    # set key's max_length from a constant for the specific znp implementation
    n = models.BinaryField(max_length=2024)
    v = models.BinaryField(max_length=2024)
    user = models.ForeignKey(FSUser, on_delete=models.CASCADE)
    device = models.ForeignKey(FSDevicePK, on_delete=models.CASCADE)
