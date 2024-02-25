from django.apps import apps
from django.db import IntegrityError
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.response import Response

from .serializers import (
    AttributeNameSerializer,
    AttributeValueSerializer,
    AttributeSerializer,
    ProductSeralizer,
    ProductAttributesSeralizer,
    ImageSerializer,
    ProductImageSerializer,
    CatalogSerializer,
)
from .models import (
    AttributeName,
    AttributeValue,
    Attribute,
    Product,
    ProductAttributes,
    Image,
    ProductImage,
    Catalog,
)


model_serializers_mapping = {
    "AttributeName": AttributeNameSerializer,
    "AttributeValue": AttributeValueSerializer,
    "Attribute": AttributeSerializer,
    "Product": ProductSeralizer,
    "ProductAttributes": ProductAttributesSeralizer,
    "Image": ImageSerializer,
    "ProductImage": ProductImageSerializer,
    "Catalog": CatalogSerializer,
}
models = {
    "AttributeName": AttributeName,
    "AttributeValue": AttributeValue,
    "Attribute": Attribute,
    "Product": Product,
    "ProductAttributes": ProductAttributes,
    "Image": Image,
    "ProductImage": ProductImage,
    "Catalog": Catalog,
}
APP_NAME = "eshop"


def get_app_models():
    """Get all models' names in the given application."""
    return apps.get_app_config(APP_NAME).get_models()


def get_app_model(model_name: str):
    return next(filter(lambda model: model.__name__ == model_name, get_app_models()))


def serialize_data(data: dict, serializer_class: ModelSerializer):
    serializer = serializer_class(data=data)
    if serializer.is_valid():
        try:
            serializer.save()
            return True
        except IntegrityError as e:
            return False
    return False


def filter_models(model_name: str):
    """Find and retrieve models by name."""
    app_models = apps.get_app_config(APP_NAME).get_models()

    for model in app_models:
        if model.__name__.lower() == model_name.lower():
            return model.objects.all()

    return Response(
        {"error": f"No model with name '{model_name}' was found"},
        status=status.HTTP_404_NOT_FOUND,
    )


def get_deserialized_object(obj: object) -> ReturnDict:
    for key, value in models.items():
        if isinstance(obj, value):
            return model_serializers_mapping[key](obj).data


def get_serializer_model(key: str) -> ModelSerializer:
    """Find a proper serializer class based on the data provided to it."""
    return model_serializers_mapping.get(key, None)
