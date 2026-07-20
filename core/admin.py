from django.contrib import admin
from django import forms
from django.db import models
from .models import Categoria, Subcategoria, Producto, ProductoImagen, Proyecto, ProyectoImagen, Testimonio, FAQ, Servicio, ServicioImagen, MensajeContacto


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


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    fields = ['imagen', 'imagen_ruta', 'numero', 'orden', 'activa']
    readonly_fields = ['numero']
    ordering = ['orden']
    verbose_name = "Imagen del Producto"
    verbose_name_plural = "Imágenes (se guardan en static/img/productos/{categoria}/{producto}/)"
    can_delete = True
    show_change_link = True


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
            'fields': ('descripcion_corta', 'descripcion')
        }),
        ('Detalles del Producto', {
            'fields': ('materiales', 'capacidad', 'dimensiones', 'regulacion', 'componentes', 'aplicaciones', 'beneficios', 'especificaciones'),
            'classes': ('collapse',)
        }),
        ('Características Extra', {
            'fields': ('caracteristicas',)
        }),
        ('Medios', {
            'fields': ('imagen',)
        }),
        ('Precio y Estado', {
            'fields': ('precio', 'disponible', 'destacado', 'orden')
        }),
    )
    inlines = [ProductoImagenInline]


class ProyectoImagenInline(admin.TabularInline):
    model = ProyectoImagen
    extra = 1
    fields = ['imagen', 'imagen_ruta', 'numero', 'orden', 'activa']
    readonly_fields = ['numero']
    ordering = ['orden']
    verbose_name = "Imagen del Proyecto"
    verbose_name_plural = "Imágenes (se guardan en static/img/proyectos/{orden}/)"
    can_delete = True
    show_change_link = True


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'cliente', 'ubicacion', 'periodo_ejecucion', 'tipo_trabajo', 'destacado', 'activo', 'orden']
    list_filter = ['destacado', 'activo']
    list_editable = ['destacado', 'activo', 'orden']
    search_fields = ['titulo', 'cliente', 'descripcion']
    fieldsets = (
        (None, {
            'fields': ('titulo', 'cliente', 'ubicacion', 'periodo_ejecucion', 'tipo_trabajo')
        }),
        ('Descripción', {
            'fields': ('descripcion',)
        }),
        ('Estado', {
            'fields': ('destacado', 'activo', 'orden')
        }),
    )
    inlines = [ProyectoImagenInline]


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


class ServicioImagenInline(admin.TabularInline):
    model = ServicioImagen
    extra = 1
    fields = ['imagen', 'imagen_ruta', 'numero', 'orden', 'activa']
    readonly_fields = ['numero']
    ordering = ['orden']
    verbose_name = "Imagen del Servicio"
    verbose_name_plural = "Imágenes (se guardan en static/img/servicios/{orden}/)"
    can_delete = True
    show_change_link = True


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'orden', 'activo']
    list_filter = ['activo']
    list_editable = ['orden', 'activo']
    search_fields = ['titulo', 'descripcion']
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 3})},
    }
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
    inlines = [ServicioImagenInline]
