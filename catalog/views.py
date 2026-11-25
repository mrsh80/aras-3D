from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .forms import ContactMessageForm
from .models import Category, Product


def home(request):
    """
    صفحه اصلی سایت Aras 3D.
    """

    featured_products = (
        Product.objects
        .filter(is_active=True, is_featured=True)
        .select_related("category")
        .prefetch_related("images")[:6]
    )

    categories = (
        Category.objects
        .filter(
            is_active=True,
            products__is_active=True,
        )
        .distinct()
    )

    context = {
        "featured_products": featured_products,
        "categories": categories,
    }

    return render(request, "catalog/home.html", context)


def product_list(request):
    """
    فهرست محصولات همراه با جست‌وجو، فیلتر دسته‌بندی و صفحه‌بندی.
    """

    products = Product.objects.filter(
        is_active=True,
        category__is_active=True,
    ).select_related("category").prefetch_related("images")

    # جست‌وجوی محصول
    query = request.GET.get("q", "").strip()

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(short_description__icontains=query)
            | Q(description__icontains=query)
            | Q(material__icontains=query)
        )

    # فیلتر بر اساس دسته‌بندی
    category_slug = request.GET.get("category", "").strip()

    if category_slug:
        products = products.filter(
            category__slug=category_slug,
        )

    # صفحه‌بندی: هر صفحه حداکثر ۹ محصول
    paginator = Paginator(products, 9)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(
        is_active=True,
        products__is_active=True,
    ).distinct()

    context = {
        "products": page_obj.object_list,
        "page_obj": page_obj,
        "categories": categories,
        "query": query,
        "selected_category": category_slug,
    }

    return render(request, "catalog/product_list.html", context)


def product_detail(request, slug):
    """
    جزئیات یک محصول فعال.
    """

    product = get_object_or_404(
        Product.objects
        .filter(
            is_active=True,
            category__is_active=True,
        )
        .select_related("category")
        .prefetch_related("images"),
        slug=slug,
    )

    context = {
        "product": product,
    }

    return render(request, "catalog/product_detail.html", context)


def about(request):
    """
    صفحه درباره ما.
    """

    return render(request, "catalog/about.html")


def contact(request):
    """
    نمایش و پردازش فرم تماس با ما.
    """

    success = False

    if request.method == "POST":
        form = ContactMessageForm(request.POST)

        # بررسی فیلد مخفی ضد هرزنامه
        if request.POST.get("website", "").strip():
            form.add_error(
                None,
                "ارسال پیام امکان‌پذیر نیست.",
            )
        elif form.is_valid():
            form.save()
            success = True
            form = ContactMessageForm()

    else:
        form = ContactMessageForm()

    context = {
        "form": form,
        "success": success,
    }

    return render(
        request,
        "catalog/contact.html",
        context,
    )