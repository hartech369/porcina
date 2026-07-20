import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Producto, ProductoImagen


class Command(BaseCommand):
    help = 'Reorganiza imágenes de productos en carpetas por posición (1/, 2/, 3/...)'

    def handle(self, *args, **options):
        # First, delete all existing ProductoImagen records
        ProductoImagen.objects.all().delete()
        self.stdout.write('Registros anteriores eliminados')
        
        # Process each product
        for subcategoria in ['comederos', 'dosificadores', 'papilleros', 'sistemas-automaticos',
                             'silos-galvanizados', 'transporte-alimento', 'accesorios-silo', 'pesaje',
                             'bebederos', 'corrales', 'jaulas', 'plaquetas',
                             'motor-reductores', 'repuesto-automatizacion', 'repuesto-comedero', 'tornilleria',
                             'complementarios']:
            
            # Find the subcategory directory
            sub_dir = None
            for cat_dir in ['alimentacion', 'silos', 'equipos', 'repuestos', 'complementarios']:
                test_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'productos', cat_dir, subcategoria)
                if os.path.exists(test_dir):
                    sub_dir = test_dir
                    break
            
            if not sub_dir:
                continue
            
            self.stdout.write(f'\nProcesando: {subcategoria}')
            
            # Get all products in this subcategory
            from core.models import Subcategoria
            try:
                sub_obj = Subcategoria.objects.get(slug=subcategoria)
            except Subcategoria.DoesNotExist:
                # Try by nombre
                sub_objs = Subcategoria.objects.filter(nombre__icontains=subcategoria.replace('-', ' '))
                if sub_objs.exists():
                    sub_obj = sub_objs.first()
                else:
                    self.stdout.write(f'  Subcategoría no encontrada: {subcategoria}')
                    continue
            
            productos = list(Producto.objects.filter(subcategoria=sub_obj).order_by('orden', 'nombre'))
            
            for idx, producto in enumerate(productos, start=1):
                # Get the current main image filename
                if not producto.imagen:
                    continue
                
                main_filename = os.path.basename(producto.imagen)
                main_number = os.path.splitext(main_filename)[0]
                
                # Create product folder: sub_dir/1/, sub_dir/2/, etc.
                product_dir = os.path.join(sub_dir, str(idx))
                os.makedirs(product_dir, exist_ok=True)
                
                # Move/copy main image to product folder
                main_src = os.path.join(sub_dir, main_filename)
                main_dest = os.path.join(product_dir, f"{idx}.1.png")
                
                if os.path.exists(main_src) and not os.path.exists(main_dest):
                    shutil.copy2(main_src, main_dest)
                    self.stdout.write(f'  {producto.nombre} -> {idx}/  (imagen principal)')
                
                # Update product image path
                rel_path = f"img/productos/{os.path.relpath(product_dir, os.path.join(settings.BASE_DIR, 'static'))}/{idx}.1.png"
                producto.imagen = rel_path.replace('\\', '/')
                producto.save(update_fields=['imagen'])
                
                # Find and move additional images
                additional_count = 1
                for archivo in sorted(os.listdir(sub_dir)):
                    if archivo == main_filename:
                        continue
                    if not archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        continue
                    if os.path.isdir(os.path.join(sub_dir, archivo)):
                        continue
                    
                    archivo_num = os.path.splitext(archivo)[0]
                    
                    # Move the file
                    src = os.path.join(sub_dir, archivo)
                    additional_count += 1
                    new_filename = f"{idx}.{additional_count}.png"
                    dest = os.path.join(product_dir, new_filename)
                    
                    if not os.path.exists(dest):
                        shutil.copy2(src, dest)
                    
                    # Create ProductoImagen record
                    ruta_relativa = f"img/productos/{os.path.relpath(product_dir, os.path.join(settings.BASE_DIR, 'static'))}/{new_filename}"
                    ProductoImagen.objects.create(
                        producto=producto,
                        imagen_ruta=ruta_relativa.replace('\\', '/'),
                        orden=additional_count - 1,
                        activa=True
                    )
                
                self.stdout.write(f'  {producto.nombre} -> {idx}/ ({additional_count} imágenes)')
        
        total = ProductoImagen.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal imágenes adicionales creadas: {total}'))
