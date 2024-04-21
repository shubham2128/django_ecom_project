from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=50)
    feedback_text = models.TextField()
    star_rating = models.IntegerField(default=0)  # Assuming a rating out of 5

    def __str__(self):
        return f"Feedback from {self.customer_name} on {self.product_name}"