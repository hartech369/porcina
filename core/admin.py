from django.contrib import admin
from .models import Categoria, Subcategoria, Producto, Proyecto, Testimonio, FAQ, Servicio, MensajeContacto


class SubcategoriaInline(admin.TabularInline):
    model = Subcategoria
    extra = 1
    fields = ['nombre', 'slug', 'orden', 'activa']


class ProductoInline(admin.TabularInline):
    model = Producto
    extra = 1
    fields = ['nombre', 'slug', 'descripcion_corta', 'imagen', 'destacado', 'orden']
    show_change_link = True


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'orden', 'activa']
    list_editable = ['orden', 'activa']
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [SubcategoriaInline, ProductoInline]
    fieldsets = (
        (None, {
            'fields': ('nombre', 'slug', 'descripcion', 'descripcion_corta')
        }),
        ('Imagen y Orden', {
            'fields': ('imagen', 'icono', 'orden', 'activa')
        }),
    )


@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'orden', 'activa']
    list_filter = ['categoria', 'activa']
    list_editable = ['orden', 'activa']
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [ProductoInline]
    search_fields = ['nombre', 'descripcion']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'subcategoria', 'destacado', 'disponible', 'orden']
    list_filter = ['categoria', 'subcategoria', 'destacado', 'disponible']
    list_editable = ['destacado', 'disponible', 'orden']
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ['nombre', 'descripcion_corta', 'descripcion']
    fieldsets = (
        (None, {
            'fields': ('nombre', 'slug', 'categoria', 'subcategoria')
        }),
        ('Descripción', {
            'fields': ('descripcion_corta', 'descripcion', 'caracteristicas')
        }),
        ('Medios', {
            'fields': ('imagen',)
        }),
        ('Precio y Estado', {
            'fields': ('precio', 'disponible', 'destacado', 'orden')
        }),
    )


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'cliente', 'ubicacion', 'destacado', 'activo', 'fecha']
    list_filter = ['destacado', 'activo']
    list_editable = ['destacado', 'activo']
    search_fields = ['titulo', 'cliente', 'descripcion']


@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'empresa', 'rating', 'activo', 'orden']
    list_filter = ['activo', 'rating']
    list_editable = ['activo', 'orden']
    search_fields = ['nombre', 'empresa', 'texto']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'categoria', 'orden', 'activa']
    list_filter = ['activa', 'categoria']
    list_editable = ['orden', 'activa']
    search_fields = ['pregunta', 'respuesta']


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'asunto', 'servicio_interes', 'leido', 'respondido', 'creado']
    list_filter = ['leido', 'respondido', 'servicio_interes', 'creado']
    list_editable = ['leido', 'respondido']
    search_fields = ['nombre', 'email', 'asunto', 'mensaje']
    readonly_fields = ['creado']


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'orden', 'activo']
    list_filter = ['activo']
    list_editable = ['orden', 'activo']
    prepopulated_fields = {'slug': ('titulo',)}
    search_fields = ['titulo', 'descripcion']
    fieldsets = (
        (None, {
            'fields': ('titulo', 'slug', 'descripcion')
        }),
        ('Contenido', {
            'fields': ('beneficios',)
        }),
        ('Medios', {
            'fields': ('imagen', 'icono')
        }),
        ('Estado', {
            'fields': ('orden', 'activo')
        }),
    )
