
import re

from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    """
    فرم تماس با ما برای سایت Aras 3D.
    """

    # فیلد ضد هرزنامه (Honeypot)
    website = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
            }
        ),
    )

    class Meta:
        model = ContactMessage

        fields = [
            "name",
            "phone",
            "email",
            "subject",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام و نام خانوادگی",
                    "autocomplete": "name",
                    "maxlength": 100,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "مثلاً 09123456789",
                    "autocomplete": "tel",
                    "maxlength": 20,
                    "inputmode": "tel",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "example@email.com",
                    "autocomplete": "email",
                }
            ),
            "subject": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "پیام خود را بنویسید...",
                    "rows": 6,
                    "maxlength": 3000,
                }
            ),
        }

        labels = {
            "name": "نام و نام خانوادگی",
            "phone": "شماره تماس",
            "email": "ایمیل (اختیاری)",
            "subject": "موضوع پیام",
            "message": "متن پیام",
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 2:
            raise forms.ValidationError(
                "نام باید حداقل ۲ کاراکتر داشته باشد."
            )

        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        # حذف جداکننده‌های رایج
        phone = re.sub(r"[\s\-()]+", "", phone)

        # تبدیل ارقام فارسی و عربی به ارقام انگلیسی
        digit_translation = str.maketrans(
            "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
            "01234567890123456789",
        )
        phone = phone.translate(digit_translation)

        # تبدیل پیش‌شماره‌های بین‌المللی ایران به قالب داخلی
        if phone.startswith("+98"):
            phone = "0" + phone[3:]
        elif phone.startswith("0098"):
            phone = "0" + phone[4:]

        # موبایل ایران: 09 به همراه 9 رقم
        mobile_pattern = r"09\d{9}"

        # تلفن ثابت ایران: کد شهر با صفر و شماره 8 رقمی
        landline_pattern = r"0\d{9,10}"

        if not (
            re.fullmatch(mobile_pattern, phone)
            or re.fullmatch(landline_pattern, phone)
        ):
            raise forms.ValidationError(
                "شماره تماس معتبر ایران وارد کنید؛ "
                "مثلاً 09123456789 یا 02112345678."
            )

        return phone

    def clean_message(self):
        message = self.cleaned_data["message"].strip()

        if len(message) < 10:
            raise forms.ValidationError(
                "متن پیام باید حداقل ۱۰ کاراکتر داشته باشد."
            )

        return message