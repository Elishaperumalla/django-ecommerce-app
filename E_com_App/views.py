from django.contrib.auth import authenticate, get_user_model, login, logout 
from django.contrib.auth.decorators import login_required  
from django.shortcuts import get_object_or_404, redirect, render  
from django.db.models import Q

from .models import Cart, CartItem, Product, Wishlist


def home(request):
    q = (request.GET.get('q') or '').strip()
    category_id = (request.GET.get('category') or '').strip()
    products = Product.objects.all()

    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(description__icontains=q) | Q(category__name__icontains=q)
        )
    if category_id:
        products = products.filter(category_id=category_id)

    products = products[:20]

    context = {'items': products, 'q': q, 'category': category_id}

    if request.GET.get('partial') == '1':
        return render(request, 'E_com_App/register/_home_results.html', context)

    return render(request, 'E_com_App/register/home.html', context)


def product_list(request):
    q = (request.GET.get('q') or '').strip()
    category_id = (request.GET.get('category') or '').strip()
    products = Product.objects.all()
    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(description__icontains=q) | Q(category__name__icontains=q)
        )
    if category_id:
        products = products.filter(category_id=category_id)

    if request.GET.get('partial') == '1':
        return render(
            request,
            'E_com_App/register/_products_results.html',
            {'items': products, 'q': q, 'category': category_id},
        )

    return render(
        request,
        'E_com_App/register/products.html',
        {'items': products, 'q': q, 'category': category_id},
    )


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'E_com_App/register/product.html', {'product': product})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        email = request.POST.get('email').strip()
        full_name = request.POST.get('full_name').strip() or username

        if not username or not password:
            return render(
                request,
                'E_com_App/register/register.html',
                {'error': 'Username and password are required.'},
            )

        user_model = get_user_model()
        if user_model.objects.filter(username=username).exists():
            return render(
                request,
                'E_com_App/register/register.html',
                {'error': 'This username is already taken.'},
            )
        if email and user_model.objects.filter(email=email).exists():
            return render(
                request,
                'E_com_App/register/register.html',
                {'error': 'This email is already registered.'},
            )

        user_model.objects.create_user(
            username=username,
            password=password,
            email=email,
            full_name=full_name,
        )
        return redirect('login')

    return render(request, 'E_com_App/register/register.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username', '').strip(),
            password=request.POST.get('password', '').strip(),
        )
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'E_com_App/register/login.html', {'error': 'Invalid username or password'})

    return render(request, 'E_com_App/register/login.html')


@login_required
def profile_view(request):
    return render(request, 'E_com_App/register/profile.html')


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')

@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()

    return redirect('cart')
@login_required
def remove_from_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = Cart.objects.get(user=request.user)

    CartItem.objects.filter(cart=cart, product=product).delete()
    return redirect('cart')

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'E_com_App/register/cart.html', {'items': items,'total':total})

@login_required
def update_quantity(request, id, action):
    cart = Cart.objects.get(user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=id)

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease':
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            return redirect('cart')

    item.save()
    return redirect('cart')

@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'E_com_App/register/wishlist.html', {'items': items})


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'E_com_App/register/checkout.html', {
        'items': items,
        'total': total
    })