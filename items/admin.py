from django.contrib import admin

from .models import Category, Item, PurchaseReceipt, PurchasedItem, Pedido, PedidoItem


class PurchasedItemInline(admin.TabularInline):
	model = PurchasedItem
	extra = 0
	fields = ('item', 'size', 'quantity')
	readonly_fields = ('item', 'size', 'quantity')
	can_delete = False
	show_change_link = False

class PedidoItemInline(admin.TabularInline):
	model = PedidoItem
	extra = 0
	fields = ('item', 'cantidad')
	readonly_fields = ('item', 'cantidad')
	can_delete = False
	show_change_link = False

class PurchaseReceiptAdmin(admin.ModelAdmin):
	inlines = [PurchasedItemInline]
	list_display = ('buyer', 'total', 'date')

class PedidoAdmin(admin.ModelAdmin):
	inlines = [PedidoItemInline]
	list_display = ('id', 'nombre_cliente', 'estado', 'empresa_encargada', 'fecha_creacion')
	list_filter = ('estado', 'empresa_encargada', 'fecha_creacion')
	search_fields = ('nombre_cliente', 'direccion_envio')
	readonly_fields = ('fecha_creacion',)

admin.site.register(Category)
class ItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'price', 'stock', 'is_sold', 'is_on_sale')
	list_editable = ('stock',)

admin.site.register(Item, ItemAdmin)
admin.site.register(PurchaseReceipt, PurchaseReceiptAdmin)
admin.site.register(Pedido, PedidoAdmin)
