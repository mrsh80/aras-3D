from django.contrib import admin
from django import forms
from .models import Category, Product, ProductImage, ContactMessage
from .validators import validate_product_image


class ProductImageAdminForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = "__all__"

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if image:
            validate_product_image(image)

        return image

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    form = ProductImageAdminForm
    extra = 1

    fields = (
        "image",
        "alt_text",
        "order",
    )

    ordering = (
        "order",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "is_active",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "category",
        "is_active",
        "is_featured",
        "created_at",
    )

    search_fields = (
        "name",
        "short_description",
        "description",
        "material",
        "dimensions",
        "color",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "category",
    )

    inlines = (
        ProductImageInline,
    )

    fieldsets = (
        (
            "اطلاعات اصلی",
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "short_description",
                    "description",
                ),
            },
        ),
        (
            "مشخصات فنی",
            {
                "fields": (
                    "material",
                    "dimensions",
                    "color",
                ),
            },
        ),
        (
            "وضعیت نمایش",
            {
                "fields": (
                    "is_active",
                    "is_featured",
                ),
            },
        ),
        (
            "اطلاعات سیستمی",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    ordering = (
        "-created_at",
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "order",
        "alt_text",
        "created_at",
    )
    form = ProductImageAdminForm
    list_filter = (
        "created_at",
    )

    search_fields = (
        "product__name",
        "alt_text",
    )

    autocomplete_fields = (
        "product",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "product",
        "order",
    )
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "subject",
        "is_read",
        "created_at",
    )

    list_filter = (
        "subject",
        "is_read",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "message",
    )

    list_editable = ("is_read",)

    readonly_fields = ("created_at",)

    ordering = ("-created_at",)

    list_per_page = 25

    fieldsets = (
        (
            "اطلاعات فرستنده",
            {
                "fields": (
                    "name",
                    "phone",
                    "email",
                ),
            },
        ),
        (
            "متن پیام",
            {
                "fields": (
                    "subject",
                    "message",
                ),
            },
        ),
        (
            "وضعیت پیام",
            {
                "fields": (
                    "is_read",
                    "created_at",
                ),
            },
        ),
    )