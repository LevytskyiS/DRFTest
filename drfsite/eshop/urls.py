from django.urls import path

from . import views

app_name = "eshop"

urlpatterns = [
    path("import/", views.ImportAPIView.as_view()),
    path(
        "detail/<str:model_name>/", views.ModelListAPIView.as_view(), name="object_list"
    ),
    path(
        "detail/<str:model_name>/<int:pk>/",
        views.ModelDetailAPIView.as_view(),
        name="object_detail",
    ),
]
