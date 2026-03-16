from django.db import models
from categories.models import Category
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
import uuid
from django.utils import timezone


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):

    CURRENCY_CHOICES = [
        ("GEL", "GEL"),
        ("USD", "USD"),
        ("EUR", "EUR"),
    ]

    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        null=True,  # optional
        blank=True
    )

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default="GEL"
    )

    tags = models.ManyToManyField(
        "ProductTag",
        related_name="products",
        blank=True
    )

    def __str__(self):
        return self.name

    def average_rating(self):
        return self.reviews.aggregate(avg=Avg("rating"))["avg"] or 0


class Review(BaseModel):
    product = models.ForeignKey(
        Product,
        related_name="reviews",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    content = models.TextField()

    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    def __str__(self):
        return f"{self.product.name} review"


class FavoriteProduct(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.user} -> {self.product}"


class ProductTag(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Cart(BaseModel):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user}'s cart"


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class ProductImage(BaseModel):
    image = models.ImageField(upload_to="products/")

    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Image for {self.product.name}"
