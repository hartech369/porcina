import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Categoria, Subcategoria, Producto


class Command(BaseCommand):
    help = 'Reasigna imágenes del catálogo por orden numérico'

    def handle(self, *args, **options):
        origen = r'C:\Users\Arturo\Desktop\1. NUEVO CATALOGO'
        destino_base = os.path.join(settings.BASE_DIR, 'static', 'img', 'productos')

        # 1. Limpiar todas las imágenes existentes
        for root, dirs, files in os.walk(destino_base):
            for f in files:
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    os.remove(os.path.join(root, f))

        # 2. Mapeo: (carpeta_origen, cat_slug, sub_slug)
        #    Las imágenes se asignan por orden numérico a los productos de la DB
        mapeo = [
            # ALIMENTACIÓN
            ('1. ALIMENTACION/1. Comederos y papilleros', 'alimentacion', 'comederos-y-papilleros'),
            ('1. ALIMENTACION/2. Componentes para sistema  de alimentación', 'alimentacion', 'componentes-para-sistema-de-alimentacion'),
            ('1. ALIMENTACION/3. Sistemas automáticos', 'alimentacion', 'sistemas-automaticos'),
            # SILOS
            ('2. SILOS/1. silos-galvanizados', 'silos-y-almacenamiento', 'silos-galvanizados'),
            ('2. SILOS/2. Elevador de alimento para Silos', 'silos-y-almacenamiento', 'elevador-de-alimento-para-silos'),
            ('2. SILOS/3. Accesorios para Silos/Accesorios para Silos', 'silos-y-almacenamiento', 'accesorios-para-silos'),
            # MATERIALES
            ('3. MATERIALES PARA AUTOMATIZAR/1. Sistema de transporte de alimento', 'materiales-para-automatizar', 'sistema-de-transporte-de-alimento'),
            ('3. MATERIALES PARA AUTOMATIZAR/2. Sistema de pesaje', 'materiales-para-automatizar', 'sistema-de-pesaje'),
            # MOTORES (sin sub)
            ('4. MOTORES Y REDUCTORES', 'motores-y-reductores', 'general'),
            # PRODUCCIÓN
            ('5. EQUIPOS PARA PRODUCCION PORCINA/1.Bebederos', 'produccion-porcina', 'bebederos'),
            ('5. EQUIPOS PARA PRODUCCION PORCINA/2. Jaulas de materinidad', 'produccion-porcina', 'jaulas-de-maternidad-y-gestacion'),
            ('5. EQUIPOS PARA PRODUCCION PORCINA/3. Plaquetas para lechón y madre', 'produccion-porcina', 'plaquetas-para-lechon-y-madre'),
            ('5. EQUIPOS PARA PRODUCCION PORCINA/4. Slats en fibra de vidrio y Paneles en PVC', 'produccion-porcina', 'slats-en-fibra-de-vidrio'),
            ('5. EQUIPOS PARA PRODUCCION PORCINA/5. Corrales, paneles en PVC y puertas', 'produccion-porcina', 'corrales,-paneles-en-pvc-y-puertas'),
            ('5. EQUIPOS PARA PRODUCCION PORCINA/5. Corrales, paneles en PVC y puertas', 'produccion-porcina', 'corrales,-divisiones-y-puertas'),
            # REPUESTOS
            ('6. REPUESTOS Y ACCESORIOS/1. para comedero y Dosificador', 'repuestos-y-accesorios', 'para-comedero-y-dosificador'),
            ('6. REPUESTOS Y ACCESORIOS/2. Para automatizacion', 'repuestos-y-accesorios', 'para-automatizacion'),
            ('6. REPUESTOS Y ACCESORIOS/3. Tornillería y accesorios', 'repuestos-y-accesorios', 'tornilleria-y-accesorios'),
            # EQUIPOS COMPLEMENTARIOS (sin sub)
            ('7. EQUIPOS COMPLEMENTARIOS', 'equipos-complementarios', 'general'),
        ]

        copiadas = 0

        for carpeta_rel, cat_slug, sub_slug in mapeo:
            carpeta_origen = os.path.join(origen, carpeta_rel)

            if not os.path.isdir(carpeta_origen):
                self.stdout.write(f'NO EXISTE: {carpeta_origen}')
                continue

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
                self.stdout.write(f'ERROR DB: {cat_slug}/{sub_slug}: {e}')
                continue

            # Recoger imágenes (archivos directos + subcarpetas con imagen)
            imgs_info = []
            for item in sorted(os.listdir(carpeta_origen)):
                item_path = os.path.join(carpeta_origen, item)
                if os.path.isfile(item_path) and item.lower().endswith('.png'):
                    try:
                        num = int(item.replace('.png', '').replace('_', '').split('.')[0])
                    except ValueError:
                        continue
                    imgs_info.append((num, item_path))
                elif os.path.isdir(item_path):
                    # Subcarpeta: buscar imagen principal (X.png dentro)
                    main_img = os.path.join(item_path, f'{item}.png')
                    if os.path.exists(main_img):
                        num = int(item.replace('_', ''))
                        imgs_info.append((num, main_img))
                    else:
                        # Buscar cualquier png
                        for f in os.listdir(item_path):
                            if f.lower().endswith('.png') and not '.' in f.replace('.png', ''):
                                num = int(f.replace('.png', ''))
                                imgs_info.append((num, os.path.join(item_path, f)))
                                break

            imgs_info.sort(key=lambda x: x[0])

            # Asignar imagen[i] a producto[i]
            for i, (num, img_path) in enumerate(imgs_info):
                if i >= len(productos):
                    break

                prod = productos[i]
                # Obtener slug del producto
                if prod.imagen:
                    prod_slug = prod.imagen.rstrip('/').split('/')[-2]
                else:
                    prod_slug = prod.nombre.lower() \
                        .replace('á', 'a').replace('é', 'e').replace('í', 'i') \
                        .replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n') \
                        .replace(' ', '-').replace(',', '').replace('.', '') \
                        .replace('(', '').replace(')', '').replace('–', '-')

                carpeta_dest = os.path.join(destino_base, cat_slug, sub_slug, prod_slug)
                os.makedirs(carpeta_dest, exist_ok=True)

                destino = os.path.join(carpeta_dest, '1.1.png')
                shutil.copy2(img_path, destino)

                # Actualizar DB
                ruta_db = f'img/productos/{cat_slug}/{sub_slug}/{prod_slug}/1.1.png'
                Producto.objects.filter(id=prod.id).update(imagen=ruta_db)

                copiadas += 1
                self.stdout.write(f'  OK: [{i+1}] {prod.nombre} <- img {num}')

        # Verificar
        total = Producto.objects.filter(disponible=True).count()
        con_img = 0
        for p in Producto.objects.filter(disponible=True):
            if p.imagen:
                parts = p.imagen.split('/')
                carpeta = os.path.join(settings.BASE_DIR, 'static', *parts[:-1])
                if os.path.isdir(carpeta):
                    archs = [f for f in os.listdir(carpeta) if f.lower().endswith(('.png','.jpg','.jpeg'))]
                    if archs:
                        con_img += 1

        self.stdout.write(self.style.SUCCESS(f'\nLISTO: {copiadas} imagenes copiadas'))
        self.stdout.write(f'Total productos: {total} | Con imagen: {con_img} | Sin imagen: {total - con_img}')
