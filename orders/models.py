from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, DateTimeField, CharField, SlugField, FloatField, TextField, ForeignKey, SET_NULL, \
    UUIDField, CASCADE, ImageField
from django.utils.text import slugify


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugBaseModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True)

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self._get_unique_slug()
        if force_update is True:
            self.name = slugify(self.name)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Category(BaseModel, SlugBaseModel):

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'


class Shop(BaseModel, SlugBaseModel):
    description = TextField()
    author = ForeignKey(User, SET_NULL, null=True, blank=True)


class Product(BaseModel):
    id = UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    price = FloatField()
    description = TextField()
    shop = ForeignKey(Shop, CASCADE)
    category = ForeignKey(Category, CASCADE)

    class Meta:
        ordering = ['created_at']
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Product'


class ProductImage(BaseModel):
    image = ImageField(upload_to='images/')
    product = ForeignKey(Product, CASCADE, 'product_image')

    class Meta:
        db_table = "images"
