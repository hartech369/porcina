import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Producto, ProductoImagen


class Command(BaseCommand):
    help = 'Vincula imágenes adicionales de static/img/productos/ a cada producto en la BD'

    def handle(self, *args, **options):
        productos = Producto.objects.filter(imagen__isnull=False).exclude(imagen='')
        
        for producto in productos:
            # Get the directory from the product's main image
            # Example: img/productos/alimentacion/comederos/1.png -> static/img/productos/alimentacion/comederos/
            img_parts = producto.imagen.split('/')
            if len(img_parts) < 3:
                continue
            
            # Build the directory path
            static_dir = os.path.join(settings.BASE_DIR, 'static', *img_parts[:-1])
            
            if not os.path.exists(static_dir):
                continue
            
            # Get the main image number
            main_filename = img_parts[-1]
            main_number = os.path.splitext(main_filename)[0]
            
            # Get all images in the directory
            archivos = sorted([f for f in os.listdir(static_dir) 
                             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
            
            # Link additional images (skip the main one)
            for archivo in archivos:
                archivo_numero = os.path.splitext(archivo)[0]
                
                # Skip the main image
                if archivo_numero == main_number:
                    continue
                
                # Build the relative path
                ruta_relativa = os.path.join('img', *img_parts[1:-1], archivo).replace('\\', '/')
                
                # Check if already exists
                if ProductoImagen.objects.filter(producto=producto, imagen_ruta=ruta_relativa).exists():
                    continue
                
                # Create the record
                img = ProductoImagen(
                    producto=producto,
                    imagen_ruta=ruta_relativa,
                    activa=True
                )
                img.save()
                self.stdout.write(f'  Vinculada: {producto.nombre} -> {archivo}')
            
            if len(archivos) > 1:
                self.stdout.write(f'Producto "{producto.nombre}": {len(archivos) - 1} imágenes adicionales')
        
        total = ProductoImagen.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal imágenes adicionales vinculadas: {total}'))
