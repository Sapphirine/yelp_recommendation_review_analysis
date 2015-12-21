from django.db import models

# Create your models here.

class Business(models.Model):
	business_id = models.TextField()
	name = models.TextField()
	address = models.TextField()
	starts = models.FloatField()
	review_count = models.FloatField()
	categories = models.TextField()


class Review(models.Model):
	review_id = models.TextField()
	business_id = models.TextField()
	topic_id = models.TextField()
	score = models.FloatField()


class LDADict(models.Model):
	topic_id = models.TextField()
	word = models.TextField()
	score = models.FloatField()


class Categories(models.Model):
	business_id = models.TextField()
	categories = models.TextField()


