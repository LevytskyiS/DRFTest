from django.db import models
from django.core.validators import MinValueValidator


class AttributeName(models.Model):
    name = models.CharField(max_length=256, unique=True)
    display = models.BooleanField(default=False)
    code = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.value


class Attribute(models.Model):
    attribute_name = models.ForeignKey(
        AttributeName, related_name="attribute", on_delete=models.CASCADE
    )
    attribute_value = models.ForeignKey(
        AttributeValue, related_name="attribute", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.attribute_name} - {self.attribute_value}"


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(
                MinValueValidator(0, "The price must be equal or greater than 0.")
            )
        ],
    )
    currency = models.CharField(max_length=3, default="CZK")
    published_on = models.DateTimeField(null=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductAttributes(models.Model):
    attribute = models.ForeignKey(
        Attribute,
        related_name="product_attribute",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product, related_name="product_attribute", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Product Attribute of {self.product}"


class Image(models.Model):
    name = models.CharField(max_length=256)
    image = models.URLField(unique=True)

    def __str__(self):
        if self.name:
            return self.name
        return self.image


class ProductImage(models.Model):
    name = models.CharField(max_length=256)
    product = models.ForeignKey(
        Product, related_name="product_image", on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        Image, related_name="product_image", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Product Image of {self.product}"


class Catalog(models.Model):
    name = models.CharField(max_length=256, unique=True)
    image = models.ForeignKey(
        Image, related_name="catalogue", on_delete=models.CASCADE, null=True
    )
    products = models.ManyToManyField(
        Product,
        related_name="catalogue",
    )
    attributes = models.ManyToManyField(
        Attribute,
        related_name="catalogue",
    )

    def __str__(self):
        return self.name
