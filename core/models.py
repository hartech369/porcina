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
    caracteristicas = models.JSONField(default=list, blank=True)
    imagen = models.CharField(max_length=500, blank=True, null=True, help_text="Ruta relativa de la imagen, ej: img/productos/alimentacion/comederos/1.png")
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


class Proyecto(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='proyectos/')
    cliente = models.CharField(max_length=200, blank=True)
    ubicacion = models.CharField(max_length=200, blank=True)
    fecha = models.DateField(blank=True, null=True)
    galeria = models.JSONField(default=list, blank=True, help_text="Lista de URLs de imágenes adicionales")
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-destacado', 'orden', '-fecha']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        return self.titulo


class Testimonio(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, blank=True)
    empresa = models.CharField(max_length=200)
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
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField()
    beneficios = models.JSONField(default=list, blank=True)
    icono = models.CharField(max_length=500, blank=True, help_text="Ruta de imagen en static/ o clase CSS")
    imagen = models.CharField(max_length=500, blank=True, null=True, help_text="Ruta relativa de la imagen en static/")
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'titulo']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.titulo


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
