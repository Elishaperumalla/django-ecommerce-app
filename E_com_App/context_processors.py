from .models import Category


def navbar_categories(request):
    return {
        "nav_categories": Category.objects.all().order_by("name"),
    }

