from django.core.management.base import BaseCommand
from core.models import Categoria, Producto
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Crea las carpetas para todos los productos: static/img/productos/{categoria}/{subcategoria}/{producto}/'

    def handle(self, *args, **options):
        # Eliminar carpetas existentes de la estructura vieja (categoria/producto)
        productos_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'productos')
        carpetas_eliminadas = 0
        
        if os.path.exists(productos_path):
            for cat_dir in os.listdir(productos_path):
                cat_path = os.path.join(productos_path, cat_dir)
                if os.path.isdir(cat_path):
                    for item in os.listdir(cat_path):
                        item_path = os.path.join(cat_path, item)
                        if os.path.isdir(item_path):
                            # Check if this is a product folder (not a subcategory folder)
                            # by checking if it has image files or is empty
                            has_images = any(f.endswith(('.png', '.jpg', '.jpeg', '.webp')) for f in os.listdir(item_path))
                            if has_images or len(os.listdir(item_path)) == 0:
                                # This is an old-style product folder, remove it
                                import shutil
                                shutil.rmtree(item_path)
                                carpetas_eliminadas += 1

        # Crear nueva estructura: categoria/subcategoria/producto
        productos = Producto.objects.select_related('categoria', 'subcategoria').all()
        carpetas_creadas = 0

        for prod in productos:
            cat_slug = prod.categoria.slug
            sub_slug = prod.subcategoria.slug if prod.subcategoria else 'general'
            prod_slug = prod.slug
            
            # Build folder path: static/img/productos/{categoria}/{subcategoria}/{producto}/
            folder_path = os.path.join(
                settings.BASE_DIR, 'static', 'img', 'productos', cat_slug, sub_slug, prod_slug
            )
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                carpetas_creadas += 1
                self.stdout.write(f'  Creada: img/productos/{cat_slug}/{sub_slug}/{prod_slug}/')
            
            # Update the product's imagen field to point to the correct folder
            expected_path = f'img/productos/{cat_slug}/{sub_slug}/{prod_slug}/1.1.png'
            if prod.imagen != expected_path:
                prod.imagen = expected_path
                prod.save(update_fields=['imagen'])

        self.stdout.write(self.style.SUCCESS(
            f'\nResumen:'
            f'\n  Carpetas antiguas eliminadas: {carpetas_eliminadas}'
            f'\n  Carpetas nuevas creadas: {carpetas_creadas}'
            f'\n  Total productos: {productos.count()}'
            f'\n  Estructura: static/img/productos/categoria/subcategoria/producto/'
        ))
