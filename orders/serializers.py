from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from orders.models import Category, Shop, Product, ProductImage


class CategoryModelSerializer(ModelSerializer):
    def validate(self, data):
        if Category.objects.filter(name=data['name']).exists():
            raise ValidationError("This category name is already taken")
        return data

    class Meta:
        model = Category
        exclude = ('slug',)


class ShopModelSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ProductModelSerializer(ModelSerializer):
    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['category'] = CategoryModelSerializer(instance.category).data
        return represent


class Meta:
    model = Product
    fields = '__all__'


class ProductImageModelSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
