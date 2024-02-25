from django.db import IntegrityError
from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status


from .utils import (
    filter_models,
    get_deserialized_object,
    get_serializer_model,
    get_app_models,
)

app_models = [model.__name__ for model in get_app_models()]


class ImportAPIView(APIView):
    """Accept POST request with JSON content."""

    parser_classes = [JSONParser]

    def post(self, request, format="json") -> Response:
        saved_models, invalid_data, unknown_models = [], [], []
        json_data = request.data

        if not json_data:
            return Response({"result": "No data provided"}, status=200)

        # Iterate over dictionaries in JSON file
        for data in json_data:
            data_keys = data.keys()

            # Iterate over keys in the dictionary
            for key in data_keys:
                if key not in app_models:
                    unknown_models.append(data)
                    continue

                serializer_model = get_serializer_model(key)
                serializer = serializer_model(data=data[key])

                if not serializer.is_valid():
                    object_data = data[key]
                    object_data["error"] = serializer.errors
                    invalid_data.append(data)
                    continue

                try:
                    serializer.save()
                except IntegrityError as e:
                    object_data = data[key]
                    object_data["error"] = str(e)
                    invalid_data.append(data)
                    continue

                data[key] = serializer.data
                saved_models.append(data)

        return Response(
            {
                "received": {
                    "created_or_updated": saved_models,
                    "invalid_data": invalid_data,
                    "unknown_models": unknown_models,
                }
            },
            status=status.HTTP_200_OK,
        )


class ModelListAPIView(APIView):
    """Accept GET request and return objects by model name."""

    def get(self, request: HttpRequest, model_name: str) -> Response:
        result: QuerySet | Response = filter_models(model_name)

        if isinstance(result, Response):
            return result

        if not result:
            return Response(
                {"result": f"No objects of the '{model_name}' model found"}, status=404
            )

        data = [get_deserialized_object(obj) for obj in result]
        return Response(data, status=status.HTTP_200_OK)


class ModelDetailAPIView(APIView):
    """Accept GET request and return product details by it's model name and id."""

    def get(
        self, request: HttpRequest, model_name: str, pk: int, format="json"
    ) -> Response:
        result: QuerySet | Response = filter_models(model_name)

        if isinstance(result, Response):
            return result

        object_class = result.first().__class__
        model = get_object_or_404(object_class, id=pk)

        serialized_model: ReturnDict = get_deserialized_object(model)
        return Response(serialized_model)
