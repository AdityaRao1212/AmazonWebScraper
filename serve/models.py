from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Scraped(models.Model):
    brands = models.CharField(max_length=255)
    categories = models.CharField(max_length=255)
    names = models.CharField(max_length=1000)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    total_rating = models.IntegerField(default=0)
    cost_price = models.IntegerField(default=0)
    selling_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    discount_per = models.IntegerField(default=0)
    links = models.URLField(null=True)
    
    class Meta:
        db_table = 'Scraped Data'
    
    def __str__(self):
        return self.names