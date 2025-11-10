from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, ProductForm
from django import forms

@user_passes_test(lambda u: u.is_staff)
def edit_products(request):
    products = Product.objects.all()
    return render(request, 'edit_products.html', {'products': products})


@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

@login_required
def update_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contraseña actualizada exitosamente, inicia sesión nuevamente 🐾")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'update_password.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        current_profile = Profile.objects.get(user__id=request.user.id)
        info_form = UserInfoForm(request.POST or None, request.FILES or None, instance=current_profile)

        if request.method == "POST":
            if 'update_user' in request.POST:
                if user_form.is_valid():
                    user_form.save()
                    messages.success(request, "Perfil actualizado correctamente.")
                    return redirect('update_user')
            
            elif 'update_info' in request.POST:
                if info_form.is_valid():
                    info_form.save()
                    messages.success(request, "Información adicional actualizada.")
                    return redirect('update_user')

        return render(request, 'update_user.html', {
            'user_form': user_form,
            'form': info_form,
            'profile': current_profile,
        })

    else:
        messages.error(request, "Debes iniciar sesión para ver tu perfil.")
        return redirect('login')


def category(request, category_name):
    category_name = category_name.replace('-', ' ')
    try:
        print(">>> category_name recibido:", category_name)
        category = Category.objects.get(name=category_name)
        print(">>> categoría encontrada:", category)
        products = Product.objects.filter(category=category)
        print(">>> productos encontrados:", products)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Exception as e:
        print(">>> ERROR EN CATEGORY VIEW:", e)
        messages.error(request, "La categoría solicitada no existe.")
        return redirect('home')

def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    
    if form.is_valid():
        form.save()
        messages.success(request, "Producto actualizado correctamente.")
        return redirect('edit_products')
    return render(request, 'edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('edit_products')  # o donde tengas la lista de productos


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("Has iniciado sesión exitosamente."))
            return redirect('home')
        else:
            messages.error(request,("Nombre de usuario o contraseña incorrectos."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,("Has cerrado sesión exitosamente."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("Registro exitoso. Has iniciado sesión."))
            return redirect('home')
        else:
            messages.error(request,("Error en el registro. Por favor corrige los errores."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
    
def profile(request):
    return render(request, 'profile.html', {})
