from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'image', 'is_sale', 'sale_price']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del producto (opcional)',
                'rows': 3,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'is_sale': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'sale_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio en oferta (si aplica)',
            }),
        }

        labels = {
            'name': 'Nombre',
            'price': 'Precio',
            'category': 'Categoría',
            'description': 'Descripción',
            'image': 'Imagen del producto',
            'is_sale': '¿Está en oferta?',
            'sale_price': 'Precio en oferta',
        }

class UserInfoForm(forms.ModelForm):
    profile_picture = forms.ImageField(label='', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    phone = forms.CharField(label='', max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}))
    address1 = forms.CharField(label='', max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección 1'}))
    address2 = forms.CharField(label='', max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección 2'}))
    city = forms.CharField(label='', max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}))
    state = forms.CharField(label='', max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}))
    zip_code = forms.CharField(label='', max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal'}))
    country = forms.CharField(label='', max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}))

    class Meta:
        model = Profile
        fields = ('profile_picture', 'phone', 'address1', 'address2', 'city', 'state', 'zip_code', 'country')

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].help_text = '<span class="form-text text-muted">Sube una foto de perfil.</span>'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.label = ''


class ChangePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='', max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva Contraseña'}))
    new_password2 = forms.CharField(label='', max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Nueva Contraseña'}))

    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')
        
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Nueva Contraseña'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '<ul class="form-text text-muted"><li>Tu contraseña no puede ser muy similar al resto de tu información personal.</li><li>Tu contraseña debe contener al menos 8 caracteres.</li><li>Tu contraseña no puede ser completamente numérica.</li><li>Tu contraseña no puede ser común.</li></ul>'
        
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirmar Nueva Contraseña'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted">Ingresa la misma contraseña para verificación.</span>'

class UpdateUserForm(UserChangeForm):
    password=None
    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    last_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}))
    email = forms.EmailField(label='', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted">150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.</span>'


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    last_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}))
    email = forms.EmailField(label='', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted">150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.</span>'
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted"><li>Tu contraseña no puede ser muy similar al resto de tu información personal.</li><li>Tu contraseña debe contener al menos 8 caracteres.</li><li>Tu contraseña no puede ser completamente numérica.</li><li>Tu contraseña no puede ser común.</li></ul>'
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar Contraseña'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted">Ingresa la misma contraseña para verificación.</span>'