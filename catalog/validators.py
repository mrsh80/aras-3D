from pathlib import Path

from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError


MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

ALLOWED_IMAGE_FORMATS = {
    "JPEG",
    "PNG",
    "WEBP",
}


def validate_product_image(image):
    """
    اعتبارسنجی حجم، فرمت و محتوای واقعی تصویر محصول.
    """

    if not image:
        return

    # بررسی حداکثر حجم فایل
    if image.size > MAX_IMAGE_SIZE:
        raise ValidationError(
            "حجم تصویر نباید بیشتر از ۵ مگابایت باشد."
        )

    # بررسی پسوند فایل
    extension = Path(image.name).suffix.lower()

    if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise ValidationError(
            "فرمت تصویر باید JPG، JPEG، PNG یا WEBP باشد."
        )

    # بررسی محتوای واقعی تصویر
    try:
        image.seek(0)

        with Image.open(image) as img:
            if img.format not in ALLOWED_IMAGE_FORMATS:
                raise ValidationError(
                    "محتوای فایل با فرمت تصویر مجاز مطابقت ندارد."
                )

            img.verify()

        # بررسی امکان بازخوانی کامل تصویر
        image.seek(0)

        with Image.open(image) as img:
            img.load()

    except ValidationError:
        raise

    except (UnidentifiedImageError, OSError, ValueError):
        raise ValidationError(
            "فایل انتخاب‌شده یک تصویر معتبر نیست یا آسیب دیده است."
        )

    finally:
        image.seek(0)
