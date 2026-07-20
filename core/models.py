from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField(blank=True)
    descripcion_corta = models.CharField(max_length=255, blank=True)
    icono = models.CharField(max_length=50, blank=True, help_text="Icono SVG o clase CSS")
    imagen = models.CharField(max_length=500, blank=True, null=True, help_text="Ruta relativa de la imagen en static/")
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class Subcategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    nombre = models.CharField(max_length=150)
    slug = models.SlugField(blank=True)
    descripcion = models.TextField(blank=True)
    imagen = models.CharField(max_length=500, blank=True, null=True, help_text="Ruta relativa de la imagen en static/")
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Subcategoría'
        verbose_name_plural = 'Subcategorías'

    def __str__(self):
        return f"{self.categoria.nombre} → {self.nombre}"


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descripcion_corta = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    materiales = models.TextField(blank=True)
    capacidad = models.TextField(blank=True)
    dimensiones = models.TextField(blank=True)
    regulacion = models.TextField(blank=True)
    componentes = models.TextField(blank=True)
    aplicaciones = models.TextField(blank=True)
    beneficios = models.TextField(blank=True)
    especificaciones = models.TextField(blank=True)
    caracteristicas = models.JSONField(default=list, blank=True)
    imagen = models.CharField(max_length=500, blank=True, null=True, help_text="Ruta relativa de la imagen principal, ej: img/productos/alimentacion/comederos/1.png")
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['orden', '-destacado', 'nombre']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre


class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(blank=True, null=True, help_text="La imagen se guardará automáticamente en static/img/productos/")
    imagen_ruta = models.CharField(max_length=500, blank=True, null=True, help_text="Ruta de imagen en static/ (alternativo a subir archivo)")
    numero = models.CharField(max_length=10, blank=True, help_text="Número automático: 1.1, 1.2, 1.3...")
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']
        verbose_name = 'Imagen de Producto'
        verbose_name_plural = 'Imágenes de Productos'

    def __str__(self):
        return f"{self.numero} - {self.producto.nombre}"

    def save(self, *args, **kwargs):
        import os
        import shutil
        from django.conf import settings

        if not self.orden:
            last_order = ProductoImagen.objects.filter(producto=self.producto).aggregate(models.Max('orden'))['orden__max'] or 0
            self.orden = last_order + 1

        if self.producto.subcategoria:
            productos_en_sub = list(Producto.objects.filter(
                subcategoria=self.producto.subcategoria
            ).order_by('orden', 'nombre').values_list('id', flat=True))
            producto_posicion = productos_en_sub.index(self.producto.id) + 1 if self.producto.id in productos_en_sub else 1
        else:
            producto_posicion = self.producto.orden or 1

        self.numero = f"{producto_posicion}.{self.orden}"

        # If uploading a new file
        if self.imagen and hasattr(self.imagen, 'file'):
            # Let Django save the file first (to media/)
            super().save(*args, **kwargs)

            # Source path from media/
            source_path = os.path.join(settings.MEDIA_ROOT, self.imagen.name)

            if os.path.exists(source_path):
                # Build destination path: static/img/productos/{categoria}/{subcategoria}/{producto}/
                cat_slug = self.producto.categoria.slug
                sub_slug = self.producto.subcategoria.slug if self.producto.subcategoria else 'general'
                prod_slug = self.producto.slug
                static_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'productos', cat_slug, sub_slug, prod_slug)
                os.makedirs(static_dir, exist_ok=True)

                ext = os.path.splitext(self.imagen.name)[1].lower() or '.png'
                new_filename = f"{self.numero}{ext}"
                dest_path = os.path.join(static_dir, new_filename)

                shutil.copy2(source_path, dest_path)
                os.remove(source_path)

                # Save ruta and clear imagen
                self.imagen_ruta = f"img/productos/{cat_slug}/{sub_slug}/{prod_slug}/{new_filename}"
                self.imagen = None
                super().save(update_fields=['imagen_ruta', 'imagen'])

            return

        super().save(*args, **kwargs)

    def get_imagen_url(self):
        if self.imagen_ruta:
            from django.templatetags.static import static
            return static(self.imagen_ruta)
        elif self.imagen:
            return self.imagen.url
        return None


class Proyecto(models.Model):
    titulo = models.CharField(max_length=200)
    cliente = models.CharField(max_length=200, blank=True)
    ubicacion = models.CharField(max_length=200, blank=True)
    periodo_ejecucion = models.CharField(max_length=100, blank=True, help_text="Ej: 2025, 2024-2026, Desde 2022")
    tipo_trabajo = models.CharField(max_length=300, blank=True)
    descripcion = models.TextField()
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', '-destacado']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        return self.titulo


class ProyectoImagen(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(blank=True, null=True, help_text="La imagen se guardará automáticamente en static/img/proyectos/")
    imagen_ruta = models.CharField(max_length=500, blank=True, null=True, help_text="Ruta de imagen en static/ (alternativo a subir archivo)")
    numero = models.CharField(max_length=10, blank=True, help_text="Número automático: 1.1, 1.2, 1.3...")
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']
        verbose_name = 'Imagen de Proyecto'
        verbose_name_plural = 'Imágenes de Proyectos'

    def __str__(self):
        return f"{self.numero} - {self.proyecto.titulo}"

    def save(self, *args, **kwargs):
        import os
        import shutil
        from django.conf import settings

        if not self.orden:
            last_order = ProyectoImagen.objects.filter(proyecto=self.proyecto).aggregate(models.Max('orden'))['orden__max'] or 0
            self.orden = last_order + 1

        self.numero = f"{self.proyecto.orden}.{self.orden}"

        if self.imagen and hasattr(self.imagen, 'file'):
            super().save(*args, **kwargs)

            source_path = os.path.join(settings.MEDIA_ROOT, self.imagen.name)

            if os.path.exists(source_path):
                static_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'proyectos', str(self.proyecto.orden))
                os.makedirs(static_dir, exist_ok=True)

                ext = os.path.splitext(self.imagen.name)[1].lower() or '.png'
                new_filename = f"{self.numero}{ext}"
                dest_path = os.path.join(static_dir, new_filename)

                shutil.copy2(source_path, dest_path)
                os.remove(source_path)

                self.imagen_ruta = f"img/proyectos/{self.proyecto.orden}/{new_filename}"
                self.imagen = None
                super().save(update_fields=['imagen_ruta', 'imagen'])

            return

        super().save(*args, **kwargs)

    def get_imagen_url(self):
        if self.imagen_ruta:
            from django.templatetags.static import static
            return static(self.imagen_ruta)
        elif self.imagen:
            return self.imagen.url
        return None


class Testimonio(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, blank=True)
    empresa = models.CharField(max_length=200)
    trabajo_realizado = models.CharField(max_length=300, blank=True)
    texto = models.TextField()
    imagen = models.ImageField(upload_to='testimonios/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden', '-creado']
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'

    def __str__(self):
        return f"{self.nombre} - {self.empresa}"


class FAQ(models.Model):
    pregunta = models.CharField(max_length=300)
    respuesta = models.TextField()
    categoria = models.CharField(max_length=100, blank=True)
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'pregunta']
        verbose_name = 'Pregunta Frecuente'
        verbose_name_plural = 'Preguntas Frecuentes'

    def __str__(self):
        return self.pregunta


class Servicio(models.Model):
    titulo = models.TextField()
    slug = models.SlugField(unique=True)
    descripcion = models.TextField()
    beneficios = models.JSONField(default=list, blank=True)
    icono = models.CharField(max_length=500, blank=True, help_text="Ruta de imagen en static/ o clase CSS")
    imagen = models.CharField(max_length=500, blank=True, null=True, help_text="Ruta relativa de la imagen principal en static/")
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'titulo']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.titulo


class ServicioImagen(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(blank=True, null=True, help_text="La imagen se guardará automáticamente en static/img/servicios/")
    imagen_ruta = models.CharField(max_length=500, blank=True, null=True, help_text="Ruta de imagen en static/ (alternativo a subir archivo)")
    numero = models.CharField(max_length=10, blank=True, help_text="Número automático: 1.1, 1.2, 1.3...")
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']
        verbose_name = 'Imagen de Servicio'
        verbose_name_plural = 'Imágenes de Servicios'

    def __str__(self):
        return f"{self.numero} - {self.servicio.titulo}"

    def save(self, *args, **kwargs):
        import os
        import shutil
        from django.conf import settings
        
        # Auto-assign order
        if not self.orden:
            last_order = ServicioImagen.objects.filter(servicio=self.servicio).aggregate(models.Max('orden'))['orden__max'] or 0
            self.orden = last_order + 1
        
        self.numero = f"{self.servicio.orden}.{self.orden}"
        
        # If uploading a new file
        if self.imagen and hasattr(self.imagen, 'file'):
            # Let Django save the file first (to media/)
            super().save(*args, **kwargs)
            
            # Source path from media/
            source_path = os.path.join(settings.MEDIA_ROOT, self.imagen.name)
            
            if os.path.exists(source_path):
                # Destination: static/img/servicios/{orden}/
                static_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'servicios', str(self.servicio.orden))
                os.makedirs(static_dir, exist_ok=True)
                
                ext = os.path.splitext(self.imagen.name)[1].lower() or '.png'
                new_filename = f"{self.numero}{ext}"
                dest_path = os.path.join(static_dir, new_filename)
                
                shutil.copy2(source_path, dest_path)
                os.remove(source_path)
                
                # Save ruta and clear imagen
                self.imagen_ruta = f"img/servicios/{self.servicio.orden}/{new_filename}"
                self.imagen = None
                super().save(update_fields=['imagen_ruta', 'imagen'])
            
            return
        
        super().save(*args, **kwargs)

    def get_imagen_url(self):
        if self.imagen_ruta:
            from django.templatetags.static import static
            return static(self.imagen_ruta)
        elif self.imagen:
            return self.imagen.url
        return None


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    empresa = models.CharField(max_length=200, blank=True)
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    servicio_interes = models.CharField(max_length=100, blank=True)
    leido = models.BooleanField(default=False)
    respondido = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"
