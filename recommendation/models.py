from django.db import models

class Recommendation(models.Model):
    user_id = models.CharField(max_length=100)
    recommended_product_id = models.CharField(max_length=100)
    predicted_rating = models.FloatField()

    def __str__(self):
        return f"User: {self.user_id}, Product: {self.recommended_product_id}, Rating: {self.predicted_rating}"
