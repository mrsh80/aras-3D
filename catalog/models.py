from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from .validators import validate_product_image
from django.core.exceptions import ValidationError
from .validators import validate_product_image

def product_image_upload_path(instance, filename):
    """
    تعیین مسیر ذخیره‌سازی تصویر محصول.
    تصاویر هر محصول در پوشه‌ای جداگانه ذخیره می‌شوند.
    """
    return f"products/{instance.product.slug}/{filename}"


class Category(models.Model):
    """
    دسته‌بندی محصولات Aras 3D.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="نام دسته‌بندی",
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        allow_unicode=True,
        verbose_name="شناسه آدرس",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات دسته‌بندی",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین ویرایش",
    )

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        super().save(*args, **kwargs)


class Product(models.Model):
    """
    محصول قابل نمایش در ویترین Aras 3D.
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="دسته‌بندی",
    )

    name = models.CharField(
        max_length=200,
        verbose_name="نام محصول",
    )

    slug = models.SlugField(
        max_length=220,
        unique=True,
        allow_unicode=True,
        verbose_name="شناسه آدرس",
    )

    short_description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="توضیحات کوتاه",
    )

    description = models.TextField(
        verbose_name="توضیحات کامل",
    )

    material = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="جنس مواد مصرفی",
    )

    dimensions = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="ابعاد محصول",
    )

    color = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="رنگ محصول",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="نمایش در سایت",
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name="محصول منتخب",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین ویرایش",
    )

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "catalog:product_detail",
            kwargs={"slug": self.slug},
        )


class ProductImage(models.Model):
    """
    تصاویر هر محصول.
    هر محصول می‌تواند چند تصویر داشته باشد.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="محصول",
    )

    image = models.ImageField(
    upload_to=product_image_upload_path,
    validators=[validate_product_image],
    verbose_name="تصویر",
    )

    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="توضیح تصویر برای دسترس‌پذیری",
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ بارگذاری",
    )
    def clean(self):
        super().clean()

        if self.image and not getattr(self.image, "_committed", False):
            validate_product_image(self.image)
    def save(self, *args, **kwargs):
        if self.image and not getattr(self.image, "_committed", False):
            validate_product_image(self.image)

        super().save(*args, **kwargs)    
        
        
    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصولات"
        ordering = ["order", "id"]
    def save(self, *args, **kwargs):
        if self.image:
            self.image.open()
            try:
                validate_product_image(self.image)
            finally:
                self.image.close()

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"تصویر {self.product.name} - {self.pk}"
    
class ContactMessage(models.Model):
    """
    پیام‌های ارسال‌شده از فرم تماس با ما.
    """

    SUBJECT_CHOICES = [
        ("product", "پرسش درباره محصولات"),
        ("order", "ثبت سفارش و استعلام"),
        ("cooperation", "همکاری"),
        ("other", "سایر موارد"),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="نام و نام خانوادگی",
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="شماره تماس",
    )

    email = models.EmailField(
        blank=True,
        verbose_name="ایمیل",
    )

    subject = models.CharField(
        max_length=20,
        choices=SUBJECT_CHOICES,
        default="other",
        verbose_name="موضوع پیام",
    )

    message = models.TextField(
        max_length=3000,
        verbose_name="متن پیام",
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name="بررسی شده",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ارسال",
    )

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"