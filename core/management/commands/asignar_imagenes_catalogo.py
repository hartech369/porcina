import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Categoria, Subcategoria, Producto


class Command(BaseCommand):
    help = 'Copia imágenes del catálogo a las carpetas correctas de static/img/productos'

    def handle(self, *args, **options):
        origen = r'C:\Users\Arturo\Desktop\1. NUEVO CATALOGO'
        destino_base = os.path.join(settings.BASE_DIR, 'static', 'img', 'productos')

        # Mapeo manual: carpeta_origen -> (cat_slug, sub_slug, [números de imagen en orden])
        mapeo = [
            # ALIMENTACIÓN - Comederos y Papilleros
            ('1. ALIMENTACION/1. Comederos y papilleros', 'alimentacion', 'comederos-y-papilleros',
             [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]),
            # ALIMENTACIÓN - Componentes
            ('1. ALIMENTACION/2. Componentes para sistema de alimentación', 'alimentacion', 'componentes-para-sistema-de-alimentacion',
             [1, 2, 3, 4, 5]),
            # ALIMENTACIÓN - Sistemas automáticos
            ('1. ALIMENTACION/3. Sistemas automáticos', 'alimentacion', 'sistemas-automaticos',
             [1, 2]),
            # SILOS - Galvanizados
            ('2. SILOS/1. silos-galvanizados', 'silos-y-almacenamiento', 'silos-galvanizados',
             [1]),
            # SILOS - Elevador
            ('2. SILOS/2. Elevador de alimento para Silos', 'silos-y-almacenamiento', 'elevador-de-alimento-para-silos',
             [2]),
            # SILOS - Accesorios
            ('2. SILOS/3. Accesorios para Silos/Accesorios para Silos', 'silos-y-almacenamiento', 'accesorios-para-silos',
             [1, 2, 3, 4, 5, 6]),
            # MATERIALES - Transporte
            ('3. MATERIALES PARA AUTOMATIZAR/1. Sistema de transporte de alimento', 'materiales-para-automatizar', 'sistema-de-transporte-de-alimento',
             [1, 2, 3, 4, 5, 6, 7, 8]),
            # MATERIALES - Pesaje
            ('3. MATERIALES PARA AUTOMATIZAR/2. Sistema de pesaje', 'materiales-para-automatizar', 'sistema-de-pesaje',
             [1]),
            # MOTORES (sin sub)
            ('4. MOTORES Y REDUCTORES', 'motores-y-reductores', 'general',
             [1, 2, 3, 4, 5]),
            # PRODUCCIÓN - Bebederos
            ('5. EQUIPOS PARA PRODUCCION PORCINA/1. Bebederos', 'produccion-porcina', 'bebederos',
             [1, 2, 3, 4]),
            # PRODUCCIÓN - Jaulas
            ('5. EQUIPOS PARA PRODUCCION PORCINA/2. Jaulas de maternidad', 'produccion-porcina', 'jaulas-de-maternidad-y-gestacion',
             [1, 2]),
            # PRODUCCIÓN - Plaquetas
            ('5. EQUIPOS PARA PRODUCCION PORCINA/3. Plaquetas para lechón y madre', 'produccion-porcina', 'plaquetas-para-lechon-y-madre',
             [7, 8, 9]),
            # PRODUCCIÓN - Slats
            ('5. EQUIPOS PARA PRODUCCION PORCINA/4. Slats en fibra de vidrio y Paneles en PVC', 'produccion-porcina', 'slats-en-fibra-de-vidrio',
             [1, 2]),
            # PRODUCCIÓN - Corrales PVC
            ('5. EQUIPOS PARA PRODUCCION PORCINA/5. Corrales, paneles en PVC y puertas', 'produccion-porcina', 'corrales,-paneles-en-pvc-y-puertas',
             [1, 2, 3, 4, 5]),
            # REPUESTOS - Comedero
            ('6. REPUESTOS Y ACCESORIOS/1. para comedero y Dosificador', 'repuestos-y-accesorios', 'para-comedero-y-dosificador',
             [1, 2]),
            # REPUESTOS - Automatización
            ('6. REPUESTOS Y ACCESORIOS/2. Para automatizacion', 'repuestos-y-accesorios', 'para-automatizacion',
             [1, 2, 3, 4, 5, 6, 7, 8]),
            # REPUESTOS - Tornillería
            ('6. REPUESTOS Y ACCESORIOS/3. Tornillería y accesorios', 'repuestos-y-accesorios', 'tornilleria-y-accesorios',
             [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
            # EQUIPOS COMPLEMENTARIOS (sin sub)
            ('7. EQUIPOS COMPLEMENTARIOS', 'equipos-complementarios', 'general',
             [1, 2, 3, 4, 5, 7, 8, 9, 10]),
        ]

        copiadas = 0
        errores = []

        for carpeta_rel, cat_slug, sub_slug, numeros_img in mapeo:
            carpeta_origen = os.path.join(origen, carpeta_rel)

            # Obtener productos de la DB
            try:
                cat_db = Categoria.objects.get(slug=cat_slug)
                if sub_slug == 'general':
                    productos = list(cat_db.productos.filter(
                        subcategoria__isnull=True, disponible=True
                    ).order_by('orden', 'nombre'))
                else:
                    sub_db = cat_db.subcategorias.get(slug=sub_slug)
                    productos = list(sub_db.productos.filter(
                        disponible=True
                    ).order_by('orden', 'nombre'))
            except Exception as e:
                errores.append(f"Error DB {cat_slug}/{sub_slug}: {e}")
                continue

            for i, num in enumerate(numeros_img):
                if i >= len(productos):
                    errores.append(f"Menos productos ({len(productos)}) que imágenes ({len(numeros_img)}) en {carpeta_rel}")
                    break

                prod = productos[i]
                # Obtener slug del producto desde la imagen actual
                if prod.imagen:
                    prod_slug = prod.imagen.rstrip('/').split('/')[-2]
                else:
                    prod_slug = prod.nombre.lower() \
                        .replace('á', 'a').replace('é', 'e').replace('í', 'i') \
                        .replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n') \
                        .replace(' ', '-').replace(',', '').replace('.', '') \
                        .replace('(', '').replace(')', '').replace('–', '-')

                # Buscar imagen origen
                img_origen = None
                for ext in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG']:
                    candidata = os.path.join(carpeta_origen, f'{num}{ext}')
                    if os.path.exists(candidata):
                        img_origen = candidata
                        break
                    # Con guión bajo
                    candidata2 = os.path.join(carpeta_origen, f'{num}_{ext}')
                    if os.path.exists(candidata2):
                        img_origen = candidata2
                        break

                if not img_origen:
                    errores.append(f"No existe: {carpeta_origen}/{num}.png")
                    continue

                # Crear carpeta destino y copiar
                carpeta_dest = os.path.join(destino_base, cat_slug, sub_slug, prod_slug)
                os.makedirs(carpeta_dest, exist_ok=True)

                destino = os.path.join(carpeta_dest, '1.1.png')
                shutil.copy2(img_origen, destino)

                # Actualizar DB
                ruta_db = f'img/productos/{cat_slug}/{sub_slug}/{prod_slug}/1.1.png'
                Producto.objects.filter(id=prod.id).update(imagen=ruta_db)

                copiadas += 1
                self.stdout.write(f"  OK: {prod.nombre} <- {os.path.basename(img_origen)}")

        self.stdout.write(self.style.SUCCESS(f'\nLISTO: {copiadas} imagenes copiadas'))
        if errores:
            self.stdout.write(self.style.WARNING(f'\nPROBLEMAS ({len(errores)}):'))
            for e in errores:
                self.stdout.write(f'  - {e}')
