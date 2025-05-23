from django.db import models
from django.template.defaultfilters import title

from django.urls import reverse


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)

    slug = models.SlugField(max_length=250, db_index=True, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])

    def __str__(self):
        return self.name;


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="product", on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default="un-branded")
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title;

    def get_absolute_url(self):
        return reverse("product_info", args=[self.slug])



