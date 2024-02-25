import json

from django.test import TestCase
from django.forms.models import model_to_dict
from rest_framework.test import APIClient
from rest_framework import status

from .models import (
    AttributeName,
    AttributeValue,
    Attribute,
    Product,
    ProductImage,
    Image,
    ProductAttributes,
    Catalog,
)


class APIViewTest(TestCase):

    def setUp(self):
        self.attribute_name = AttributeName.objects.create(
            id=1, name="Color", display=True, code="05"
        )
        self.attribute_value = AttributeValue.objects.create(id=1, value="red")
        self.attribute = Attribute.objects.create(
            id=1,
            attribute_name=self.attribute_name,
            attribute_value=self.attribute_value,
        )
        self.product = Product.objects.create(
            id=1,
            name="Phone",
            description="Cool",
            price=1111.99,
            currency="EUR",
            published_on="2022-12-12",
            is_published=False,
        )
        self.product_attributes = ProductAttributes.objects.create(
            id=1, attribute=self.attribute, product=self.product
        )
        self.image = Image.objects.create(
            id=1,
            name="phone-img",
            image="https://ss7.vzw.com/is/image/VerizonWireless/apple-iphone-15-128gb-pink-mtlw3ll-a-a?wid=930&hei=930&fmt=webp",
        )
        self.product_image = ProductImage.objects.create(
            id=1, name="new-phone", product=self.product, image=self.image
        )
        self.catalog = Catalog.objects.create(
            id=1, name="Catalogue 2024", image=self.image
        )
        self.catalog.products.set(Product.objects.filter(name="Phone"))
        self.catalog.attributes.set(Attribute.objects.all())

        self.client = APIClient()
        self.url = "/import/"

    def _perform_post(self, data):
        response = self.client.post(
            self.url, data=json.dumps(data), content_type="application/json"
        )
        return response.json()["received"], response.status_code

    def test_valid_post(self):
        valid_data = [
            {
                "AttributeName": {
                    "id": 2,
                    "nazev": "Resistance",
                    "zobrazit": True,
                    "kod": "QWE1",
                }
            }
        ]
        data, status_code = self._perform_post(valid_data)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(data["created_or_updated"], valid_data)
        self.assertEqual(len(data["created_or_updated"]), 1)
        self.assertEqual(data["invalid_data"], [])
        self.assertEqual(data["unknown_models"], [])
        self.assertEqual(len(AttributeName.objects.all()), 2)

    def test_invalid_post(self):
        invalid_data = [
            {
                "AttributeName": {
                    "id": 1,
                    "nazev": "Color",
                    "zobrazit": True,
                    "kod": False,
                }
            }
        ]
        data, status_code = self._perform_post(invalid_data)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(data["created_or_updated"], [])
        self.assertNotEqual(data["invalid_data"], invalid_data)
        self.assertNotEqual(len(data["invalid_data"]), invalid_data)
        self.assertEqual(data["unknown_models"], [])

    def test_unknown_model(self):
        unknown_model = [
            {
                "Stock": {
                    "id": 1,
                    "nazev": "Color",
                    "zobrazit": True,
                    "kod": "QWE1",
                }
            }
        ]
        data, status_code = self._perform_post(unknown_model)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(data["created_or_updated"], [])
        self.assertEqual(data["invalid_data"], [])
        self.assertEqual(data["unknown_models"], unknown_model)
        self.assertEqual(len(data["unknown_models"]), 1)

    def test_valid_attributename_update(self):
        valid_data = [
            {
                "AttributeName": {
                    "id": 1,
                    "nazev": "Stock",
                    "zobrazit": False,
                    "kod": "00",
                }
            }
        ]
        data, status_code = self._perform_post(valid_data)
        updated_obj = AttributeName.objects.get(id=1)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(updated_obj.name, "Stock")
        self.assertEqual(updated_obj.display, False)
        self.assertEqual(updated_obj.code, "00")

    def test_valid_attributevalue_update(self):
        valid_data = [{"AttributeValue": {"id": 1, "hodnota": "blue"}}]
        data, status_code = self._perform_post(valid_data)
        updated_obj = AttributeValue.objects.get(id=1)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(updated_obj.value, "blue")
        self.assertEqual(updated_obj.id, 1)

    def test_valid_attribute_update(self):
        attribute_name_1 = AttributeName.objects.create(
            id=3, name="Cola", display=True, code="33"
        )
        attribute_value_1 = AttributeValue.objects.create(id=3, value="green")
        valid_data = [
            {
                "Attribute": {
                    "id": 1,
                    "nazev_atributu_id": attribute_name_1.id,
                    "hodnota_atributu_id": attribute_value_1.id,
                }
            }
        ]
        data, status_code = self._perform_post(valid_data)
        updated_obj = Attribute.objects.get(id=1)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(updated_obj.attribute_name, attribute_name_1)
        self.assertEqual(updated_obj.attribute_value, attribute_value_1)

    def test_valid_product_update(self):
        valid_data = [{"Product": {"id": 1, "nazev": "X", "mena": "CZK"}}]
        data, status_code = self._perform_post(valid_data)
        updated_obj = Product.objects.get(id=1)

        self.assertNotEqual(updated_obj.name, self.product.name)
        self.assertNotEqual(updated_obj.currency, self.product.currency)
        self.assertNotEqual(updated_obj.name, self.product.name)

    def test_valid_product_attribute_update(self):
        product = Product.objects.create(
            id=2,
            name="Cooler",
            description="powerful",
            price=100,
            currency="CZK",
            published_on="2022-12-12",
            is_published=True,
        )
        valid_data = [{"ProductAttributes": {"id": 1, "attribute": 1, "product": 2}}]
        data, status_code = self._perform_post(valid_data)
        updated_obj = ProductAttributes.objects.get(id=1)

        self.assertEqual(updated_obj.id, 1)
        self.assertEqual(updated_obj.product, product)

    def test_valid_image_update(self):
        name = "cat"
        image = "https://www.animalfriends.co.uk/siteassets/media/images/article-images/cat-articles/51_afi_article1_the-secret-language-of-cats.png"

        valid_data = [
            {
                "Image": {
                    "id": 1,
                    "nazev": name,
                    "obrazek": image,
                }
            }
        ]
        data, status_code = self._perform_post(valid_data)
        updated_obj = Image.objects.get(id=1)

        self.assertEqual(updated_obj.name, name)
        self.assertEqual(updated_obj.image, image)

    def test_valid_product_image_update(self):
        image = Image.objects.create(
            id=4,
            name="test",
            image="https://www.instagram.com/p/C3kliNKr4qx/?img_index=1",
        )
        product = Product.objects.create(
            id=3,
            name="Bag",
            description="nice",
            price=100,
            currency="CZK",
            published_on="2022-12-12",
            is_published=True,
        )
        valid_data = [
            {
                "ProductImage": {
                    "id": 1,
                    "nazev": "nature",
                    "obrazek_id": image.id,
                    "product": product.id,
                }
            }
        ]
        data, status_code = self._perform_post(valid_data)
        updated_obj = ProductImage.objects.get(id=1)

        self.assertEqual(updated_obj.name, "nature")
        self.assertEqual(updated_obj.image, image)
        self.assertEqual(updated_obj.product, product)

    def test_valid_catalog_update(self):
        name = "Cat catalogue"
        image = Image.objects.create(
            id=5,
            name="test",
            image="https://www.instagram.com/p/C3kliNKr4qx/?img_index=1",
        )
        product = Product.objects.create(
            id=3,
            name="Bag",
            description="nice",
            price=100,
            currency="CZK",
            published_on="2022-12-12",
            is_published=True,
        )
        valid_data = [
            {
                "Catalog": {
                    "id": 1,
                    "nazev": name,
                    "obrazek_id": image.id,
                    "products_ids": [product.id],
                    "attributes_ids": [],
                }
            }
        ]
        data, status_code = self._perform_post(valid_data)
        updated_obj = Catalog.objects.get(id=1)

        self.assertEqual(updated_obj.name, name)
        self.assertEqual(updated_obj.image, image)
        self.assertEqual(len(updated_obj.products.all()), 1)
        self.assertEqual(updated_obj.products.get(id=3), product)
        self.assertEqual(len(updated_obj.attributes.all()), 0)

    def test_model_list_get(self):
        url = "/detail/image/"
        response = self.client.get(url)
        data = response.json()
        image = data[0]

        self.assertEqual(len(data), 1)

    def test_model_detail_get(self):
        url = "/detail/catalog/1/"
        response = self.client.get(url)
        catalogue = response.json()

        self.assertEqual(len(catalogue["products_ids"]), 1)
        self.assertEqual(catalogue["nazev"], "Catalogue 2024")
