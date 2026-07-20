import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Subcategoria, Producto


class Command(BaseCommand):
    help = 'Reorganiza imágenes compartidas en carpetas individuales por producto'

    def handle(self, *args, **options):
        static_productos = os.path.join(settings.BASE_DIR, 'static', 'img', 'productos')
        moved = 0

        for sub in Subcategoria.objects.filter(activa=True).order_by('orden'):
            productos = list(Producto.objects.filter(subcategoria=sub, disponible=True).order_by('orden', 'nombre'))
            if not productos:
                continue

            # Find folder from the first product's imagen field
            primer_prod = productos[0]
            if not primer_prod.imagen:
                continue

            img_parts = primer_prod.imagen.split('/')
            if len(img_parts) < 3:
                continue

            # The folder is everything except the filename
            sub_dir = os.path.join(settings.BASE_DIR, 'static', *img_parts[:-1])

            if not os.path.isdir(sub_dir):
                continue

            # Check for loose images at root
            images = sorted(
                [f for f in os.listdir(sub_dir)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
                 and os.path.isfile(os.path.join(sub_dir, f))],
                key=lambda x: x
            )

            if not images:
                continue

            self.stdout.write(f'\n  {sub.nombre}: {len(productos)} productos, {len(images)} imágenes sueltas')

            for idx, prod in enumerate(productos, start=1):
                if idx > len(images):
                    self.stdout.write(self.style.WARNING(f'    SIN IMAGEN: {prod.nombre}'))
                    continue

                prod_dir = os.path.join(sub_dir, str(idx))
                os.makedirs(prod_dir, exist_ok=True)

                src = os.path.join(sub_dir, images[idx - 1])
                new_name = f'{idx}.1.png'
                dest = os.path.join(prod_dir, new_name)
                shutil.move(src, dest)

                rel_path = os.path.relpath(dest, static_productos).replace('\\', '/')
                prod.imagen = f'img/productos/{rel_path}'
                prod.save(update_fields=['imagen'])
                moved += 1

                self.stdout.write(f'    {prod.nombre} -> {idx}/{new_name}')

        self.stdout.write(self.style.SUCCESS(f'\nTotal imágenes reorganizadas: {moved}'))
