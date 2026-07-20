import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Servicio, ServicioImagen


class Command(BaseCommand):
    help = 'Vincula las imágenes de static/img/servicios/ a cada servicio en la BD'

    def handle(self, *args, **options):
        servicios_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'servicios')
        
        if not os.path.exists(servicios_dir):
            self.stdout.write(self.style.ERROR('No existe la carpeta static/img/servicios/'))
            return
        
        for servicio in Servicio.objects.all():
            servicio_dir = os.path.join(servicios_dir, str(servicio.orden))
            
            if not os.path.exists(servicio_dir):
                self.stdout.write(f'Carpeta no encontrada: servicios/{servicio.orden}/ para "{servicio.titulo}"')
                continue
            
            archivos = sorted([f for f in os.listdir(servicio_dir) if f.endswith('.png')])
            
            for archivo in archivos:
                ruta_relativa = f"img/servicios/{servicio.orden}/{archivo}"
                
                # Verificar si ya existe
                if ServicioImagen.objects.filter(servicio=servicio, imagen_ruta=ruta_relativa).exists():
                    self.stdout.write(f'  Ya existe: {archivo}')
                    continue
                
                # Crear registro
                img = ServicioImagen(
                    servicio=servicio,
                    imagen_ruta=ruta_relativa,
                    activa=True
                )
                # El save() asigna numero y orden automáticamente
                img.save()
                self.stdout.write(f'  Vinculada: {img.numero} - {archivo}')
            
            self.stdout.write(f'Servicio "{servicio.titulo}": {len(archivos)} imágenes')
        
        total = ServicioImagen.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nTotal imágenes vinculadas: {total}'))
