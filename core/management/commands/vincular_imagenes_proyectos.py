import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Proyecto, ProyectoImagen


class Command(BaseCommand):
    help = 'Vincula las imágenes de static/img/proyectos/ a cada proyecto en la BD'

    def handle(self, *args, **options):
        proyectos_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'proyectos')
        
        if not os.path.exists(proyectos_dir):
            os.makedirs(proyectos_dir)
            self.stdout.write(self.style.WARNING('Carpeta static/img/proyectos/ creada. Coloca imágenes en subcarpetas (1/, 2/, etc.)'))
            return
        
        for proyecto in Proyecto.objects.all():
            proyecto_dir = os.path.join(proyectos_dir, str(proyecto.orden))
            
            if not os.path.exists(proyecto_dir):
                self.stdout.write(f'Carpeta no encontrada: proyectos/{proyecto.orden}/ para "{proyecto.titulo}"')
                continue
            
            archivos = sorted([f for f in os.listdir(proyecto_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
            
            for archivo in archivos:
                ruta_relativa = f"img/proyectos/{proyecto.orden}/{archivo}"
                
                if ProyectoImagen.objects.filter(proyecto=proyecto, imagen_ruta=ruta_relativa).exists():
                    self.stdout.write(f'  Ya existe: {archivo}')
                    continue
                
                img = ProyectoImagen(
                    proyecto=proyecto,
                    imagen_ruta=ruta_relativa,
                    activa=True
                )
                img.save()
                self.stdout.write(f'  Vinculada: {img.numero} - {archivo}')
            
            self.stdout.write(f'Proyecto "{proyecto.titulo}": {len(archivos)} imágenes')
        
        total = ProyectoImagen.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal imágenes vinculadas: {total}'))
