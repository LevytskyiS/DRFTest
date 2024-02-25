from rest_framework import serializers
from django.forms.models import model_to_dict


from .models import (
    Product,
    AttributeName,
    AttributeValue,
    Attribute,
    Product,
    ProductAttributes,
    Image,
    ProductImage,
    Catalog,
)


class AttributeNameSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    nazev = serializers.CharField(source="name")
    zobrazit = serializers.BooleanField(source="display", required=False)
    kod = serializers.CharField(source="code", required=False)

    class Meta:
        model = AttributeName
        fields = ["id", "nazev", "zobrazit", "kod"]

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = AttributeName.objects.get(id=instance_id)
            if model_to_dict(instance) == validated_data:
                return instance
            instance.name = validated_data.get("name", instance.name)
            instance.display = validated_data.get("display", instance.display)
            instance.code = validated_data.get("code", instance.code)
            instance.save()
            return instance
        except AttributeName.DoesNotExist as e:
            return AttributeName.objects.create(**validated_data)


class AttributeValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    hodnota = serializers.CharField(source="value")

    class Meta:
        model = AttributeValue
        fields = ["id", "hodnota"]

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = AttributeValue.objects.get(id=instance_id)
            if model_to_dict(instance) == validated_data:
                return instance
            instance.value = validated_data.get("value", instance.value)
            instance.save()
            return instance
        except AttributeValue.DoesNotExist as e:
            return AttributeValue.objects.create(**validated_data)


class AttributeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    nazev_atributu_id = serializers.PrimaryKeyRelatedField(
        queryset=AttributeName.objects.all(), source="attribute_name"
    )
    hodnota_atributu_id = serializers.PrimaryKeyRelatedField(
        queryset=AttributeValue.objects.all(), source="attribute_value"
    )

    class Meta:
        model = Attribute
        fields = ["id", "nazev_atributu_id", "hodnota_atributu_id"]

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = Attribute.objects.get(id=instance_id)
            if model_to_dict(instance) == validated_data:
                return instance

            instance.attribute_name = validated_data.get(
                "attribute_name", instance.attribute_name
            )
            instance.attribute_value = validated_data.get(
                "attribute_value", instance.attribute_value
            )
            instance.save()
            return instance
        except Attribute.DoesNotExist as e:
            return Attribute.objects.create(**validated_data)


class ProductSeralizer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    nazev = serializers.CharField(source="name", required=False)
    cena = serializers.DecimalField(
        source="price", max_digits=8, decimal_places=2, min_value=0, required=False
    )
    description = serializers.CharField(required=False)
    mena = serializers.CharField(source="currency")

    class Meta:
        model = Product
        fields = [
            "id",
            "nazev",
            "description",
            "cena",
            "mena",
            "published_on",
            "is_published",
        ]

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = Product.objects.get(id=instance_id)
            if model_to_dict(instance) == validated_data:
                return instance
            instance.name = validated_data.get("name", instance.name)
            instance.description = validated_data.get(
                "description", instance.description
            )
            instance.price = validated_data.get("price", instance.price)
            instance.currency = validated_data.get("currency", instance.currency)
            instance.published_on = validated_data.get(
                "published_on", instance.published_on
            )
            instance.is_published = validated_data.get(
                "is_published", instance.is_published
            )

            instance.save()
            return instance
        except Product.DoesNotExist as e:
            return Product.objects.create(**validated_data)


class ProductAttributesSeralizer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    attribute = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ProductAttributes
        fields = ["id", "attribute", "product"]

    def create(self, validated_data):
        instance_id = validated_data.get("id")
        try:
            instance = ProductAttributes.objects.get(id=instance_id)

            if model_to_dict(instance) == validated_data:
                return instance

            instance.attribute = validated_data.get("attribute", instance.attribute)
            instance.product = validated_data.get("product", instance.product)

            instance.save()
            return instance
        except ProductAttributes.DoesNotExist as e:
            return ProductAttributes.objects.create(**validated_data)


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    nazev = serializers.CharField(source="name", required=False)
    obrazek = serializers.URLField(source="image")

    class Meta:
        model = Image
        fields = ["id", "nazev", "obrazek"]

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = Image.objects.get(id=instance_id)
            if model_to_dict(instance) == validated_data:
                return instance
            instance.name = validated_data.get("name", instance.name)
            instance.image = validated_data.get("image", instance.image)
            instance.save()
            return instance
        except Image.DoesNotExist as e:
            return Image.objects.create(**validated_data)


class ProductImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    nazev = serializers.CharField(source="name", required=False)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
    )
    obrazek_id = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(),
        source="image",
    )

    class Meta:
        model = ProductImage
        fields = ["id", "nazev", "product", "obrazek_id"]

    def create(self, validated_data):
        instance_id = validated_data.get("id")
        try:
            instance = ProductImage.objects.get(id=instance_id)
            if model_to_dict(instance) == validated_data:
                return instance
            instance.name = validated_data.pop("name", instance.name)
            instance.product = validated_data.get("product", instance.product)
            instance.image = validated_data.get("image", instance.image)
            instance.save()
            return instance
        except ProductImage.DoesNotExist as e:
            return ProductImage.objects.create(**validated_data)


class CatalogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    nazev = serializers.CharField(source="name", required=False)
    obrazek_id = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(), source="image", required=False
    )
    products_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="products", many=True, required=False
    )

    attributes_ids = serializers.PrimaryKeyRelatedField(
        queryset=Attribute.objects.all(), source="attributes", many=True, required=False
    )

    class Meta:
        model = Catalog
        fields = ["id", "nazev", "obrazek_id", "products_ids", "attributes_ids"]

    def create(self, validated_data):
        instance_id = validated_data.get("id")

        try:
            instance = Catalog.objects.get(id=instance_id)
        except Catalog.DoesNotExist as e:
            instance = Catalog.objects.create(id=instance_id)

        if model_to_dict(instance) == validated_data:
            return instance

        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.products.set(validated_data.get("products", instance.products.all()))
        instance.attributes.set(
            validated_data.get("attributes", instance.attributes.all())
        )
        instance.save()
        return instance
