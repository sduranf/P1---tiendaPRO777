from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Empresa

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('correo', 'nombre', 'tipo_usuario', 'is_active', 'is_staff')
    list_filter = ('tipo_usuario', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('correo', 'nombre')
    ordering = ('correo',)
    
    fieldsets = (
        (None, {'fields': ('correo', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'tipo_usuario')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'nombre', 'tipo_usuario', 'password1', 'password2'),
        }),
    )

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'direccion')
    search_fields = ('usuario__nombre', 'usuario__correo', 'direccion')
    list_filter = ('usuario__tipo_usuario',)
