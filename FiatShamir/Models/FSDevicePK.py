# from django.db import models
# from Models.FSUser import FSUser

# class FSDevicePK(models.Model):
#     # set key's max_length from a constant for the specific znp implementation
#     n = models.BinaryField(max_length=2024)
#     v = models.BinaryField(max_length=2024)
#     user = models.ForeignKey(FSUser, on_delete=models.CASCADE)

#     class Meta:
#         app_label = 'FiatShamir'