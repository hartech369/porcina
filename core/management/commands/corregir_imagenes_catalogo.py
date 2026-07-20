import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Producto


class Command(BaseCommand):
    help = 'Busca TODAS las imágenes PNG del catálogo y las copia al destino correcto'

    def handle(self, *args, **options):
        origen = r'C:\Users\Arturo\Desktop\1. NUEVO CATALOGO'
        destino_base = os.path.join(settings.BASE_DIR, 'static', 'img', 'productos')

        # Obtener todos los productos ordenados
        productos = list(Producto.objects.filter(disponible=True).order_by('id'))

        # Mapa manual carpeta_cat -> lista ordenada de (sub_folder, cat_slug, sub_slug)
        categorias = [
            ('1. ALIMENTACION', [
                ('1. Comederos y papilleros', 'alimentacion', 'comederos-y-papilleros'),
                ('2. Componentes para sistema de alimentación', 'alimentacion', 'componentes-para-sistema-de-alimentacion'),
                ('3. Sistemas automáticos', 'alimentacion', 'sistemas-automaticos'),
            ]),
            ('2. SILOS', [
                ('1. silos-galvanizados', 'silos-y-almacenamiento', 'silos-galvanizados'),
                ('2. Elevador de alimento para Silos', 'silos-y-almacenamiento', 'elevador-de-alimento-para-silos'),
                ('3. Accesorios para Silos', 'silos-y-almacenamiento', 'accesorios-para-silos'),
            ]),
            ('3. MATERIALES PARA AUTOMATIZAR', [
                ('1. Sistema de transporte de alimento', 'materiales-para-automatizar', 'sistema-de-transporte-de-alimento'),
                ('2. Sistema de pesaje', 'materiales-para-automatizar', 'sistema-de-pesaje'),
            ]),
            ('4. MOTORES Y REDUCTORES', [
                (None, 'motores-y-reductores', 'general'),
            ]),
            ('5. EQUIPOS PARA PRODUCCION PORCINA', [
                ('1.Bebederos', 'produccion-porcina', 'bebederos'),
                ('2. Jaulas de materinidad', 'produccion-porcina', 'jaulas-de-maternidad-y-gestacion'),
                ('3. Plaquetas para lechón y madre', 'produccion-porcina', 'plaquetas-para-lechon-y-madre'),
                ('4. Slats en fibra de vidrio y Paneles en PVC', 'produccion-porcina', 'slats-en-fibra-de-vidrio'),
                ('5. Corrales, paneles en PVC y puertas', 'produccion-porcina', 'corrales,-paneles-en-pvc-y-puertas'),
                (None, 'produccion-porcina', 'corrales,-divisiones-y-puertas'),
            ]),
            ('6. REPUESTOS Y ACCESORIOS', [
                ('1. para comedero y Dosificador', 'repuestos-y-accesorios', 'para-comedero-y-dosificador'),
                ('2. Para automatizacion', 'repuestos-y-accesorios', 'para-automatizacion'),
                ('3. Tornillería y accesorios', 'repuestos-y-accesorios', 'tornilleria-y-accesorios'),
            ]),
            ('7. EQUIPOS COMPLEMENTARIOS', [
                (None, 'equipos-complementarios', 'general'),
            ]),
        ]

        # Crear diccionario de productos por subcategoría
        prods_por_sub = {}
        for p in productos:
            if p.subcategoria:
                key = (p.subcategoria.categoria.slug, p.subcategoria.slug)
            else:
                key = (p.subcategoria.categoria.slug if p.subcategoria else p.categoria.slug, 'general')
            if key not in prods_por_sub:
                prods_por_sub[key] = []
            prods_por_sub[key].append(p)

        copiadas = 0
        errores = []
        contador = {}  # Para llevar cuenta de cuántas imágenes tiene cada producto

        for carpeta_cat, subs in categorias:
            cat_origen = os.path.join(origen, carpeta_cat)

            for carpeta_sub, cat_slug, sub_slug in subs:
                if carpeta_sub:
                    sub_origen = os.path.join(cat_origen, carpeta_sub)
                else:
                    sub_origen = cat_origen

                if not os.path.isdir(sub_origen):
                    errores.append(f"Carpeta no encontrada: {sub_origen}")
                    continue

                key = (cat_slug, sub_slug)
                lista_prods = prods_por_sub.get(key, [])

                # Buscar todas las imágenes PNG en esta carpeta (no subcarpetas)
                imgs = sorted([f for f in os.listdir(sub_origen)
                               if os.path.isfile(os.path.join(sub_origen, f))
                               and f.lower().endswith('.png')])

                for i, img_file in enumerate(imgs):
                    if i >= len(lista_prods):
                        errores.append(f"Más imágenes ({len(imgs)}) que productos ({len(lista_prods)}) en {carpeta_cat}/{carpeta_sub}")
                        break

                    prod = lista_prods[i]
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

                    # Numeración: si ya tiene imágenes, continuar la secuencia
                    num = len(contador.get(f"{cat_slug}/{sub_slug}/{prod_slug}", [])) + 1
                    nombre_final = f'{num}.1.png'
                    destino_path = os.path.join(carpeta_dest, nombre_final)
                    origen_path = os.path.join(sub_origen, img_file)

                    shutil.copy2(origen_path, destino_path)

                    if f"{cat_slug}/{sub_slug}/{prod_slug}" not in contador:
                        contador[f"{cat_slug}/{sub_slug}/{prod_slug}"] = []
                    contador[f"{cat_slug}/{sub_slug}/{prod_slug}"].append(nombre_final)

                    # Actualizar DB con la primera imagen
                    if num == 1:
                        ruta_db = f'img/productos/{cat_slug}/{sub_slug}/{prod_slug}/{nombre_final}'
                        Producto.objects.filter(id=prod.id).update(imagen=ruta_db)

                    copiadas += 1
                    self.stdout.write(f"  OK: {prod.nombre} <- {img_file} -> {nombre_final}")

        # Manejar imágenes adicionales en subcarpetas de Tornillería, Corrales, etc.
        subcarpetas_extra = [
            ('6. REPUESTOS Y ACCESORIOS/3. Tornillería y accesorios/1', 'repuestos-y-accesorios', 'tornilleria-y-accesorios', 0),
            ('6. REPUESTOS Y ACCESORIOS/3. Tornillería y accesorios/4', 'repuestos-y-accesorios', 'tornilleria-y-accesorios', 3),
            ('6. REPUESTOS Y ACCESORIOS/3. Tornillería y accesorios/5', 'repuestos-y-accesorios', 'tornilleria-y-accesorios', 4),
            ('6. REPUESTOS Y ACCESORIOS/3. Tornillería y accesorios/12', 'repuestos-y-accesorios', 'tornilleria-y-accesorios', 11),
            ('6. REPUESTOS Y ACCESORIOS/2. Para automatizacion/5', 'repuestos-y-accesorios', 'para-automatizacion', 4),
            ('5. EQUIPOS PARA PRODUCCION PORCINA/5. Corrales, paneles en PVC y puertas/3', 'produccion-porcina', 'corrales,-paneles-en-pvc-y-puertas', None),
        ]

        for carpeta_rel, cat_slug, sub_slug, prod_idx in subcarpetas_extra:
            sub_origen = os.path.join(origen, carpeta_rel)
            if not os.path.isdir(sub_origen):
                continue

            key = (cat_slug, sub_slug)
            lista_prods = prods_por_sub.get(key, [])

            if prod_idx is not None and prod_idx < len(lista_prods):
                prod = lista_prods[prod_idx]
                if prod.imagen:
                    prod_slug = prod.imagen.rstrip('/').split('/')[-2]
                else:
                    prod_slug = prod.nombre.lower() \
                        .replace('á', 'a').replace('é', 'e').replace('í', 'i') \
                        .replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n') \
                        .replace(' ', '-').replace(',', '').replace('.', '') \
                        .replace('(', '').replace(')', '').replace('–', '-')
            else:
                continue

            carpeta_dest = os.path.join(destino_base, cat_slug, sub_slug, prod_slug)
            os.makedirs(carpeta_dest, exist_ok=True)

            # Copiar todas las imágenes de la subcarpeta
            for f in os.listdir(sub_origen):
                f_path = os.path.join(sub_origen, f)
                if os.path.isfile(f_path) and f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    num = len(contador.get(f"{cat_slug}/{sub_slug}/{prod_slug}", [])) + 1
                    nombre_final = f'{num}.1.png'
                    destino_path = os.path.join(carpeta_dest, nombre_final)
                    shutil.copy2(f_path, destino_path)

                    if f"{cat_slug}/{sub_slug}/{prod_slug}" not in contador:
                        contador[f"{cat_slug}/{sub_slug}/{prod_slug}"] = []
                    contador[f"{cat_slug}/{sub_slug}/{prod_slug}"].append(nombre_final)

                    copiadas += 1
                    self.stdout.write(f"  OK (extra): {prod.nombre} <- {f} -> {nombre_final}")

        self.stdout.write(self.style.SUCCESS(f'\nLISTO: {copiadas} imagenes copiadas'))
        if errores:
            self.stdout.write(self.style.WARNING(f'\nNOTAS ({len(errores)}):'))
            for e in errores:
                self.stdout.write(f'  - {e}')
