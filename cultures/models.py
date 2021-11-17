from django.db import models
from farmer.models import Farmer

class Culture(models.Model):
    name = models.CharField(max_length=50, unique=True)
    basal_inf = models.FloatField()
    basal_sup = models.FloatField()
    thermal_constant = models.FloatField()
    
    def __str__(self):
        return self.name
    
class UserCultures(models.Model):
    acummulated_degrees = models.FloatField(default=0.0, blank=True)
    culture = models.ForeignKey(Culture, models.CASCADE, related_name="culture", blank=True, null=True)
    farmer = models.ForeignKey(Farmer, related_name="cultures", on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return str(self.acummulated_degrees)