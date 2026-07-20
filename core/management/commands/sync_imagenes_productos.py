import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Producto, ProductoImagen


class Command(BaseCommand):
    help = 'Limpia registros ProductoImagen huérfanos y verifica carpetas'

    def handle(self, *args, **options):
        deleted = 0
        for img in ProductoImagen.objects.all():
            if img.imagen_ruta:
                full_path = os.path.join(settings.BASE_DIR, 'static', img.imagen_ruta)
                if not os.path.exists(full_path):
                    img.delete()
                    deleted += 1
                    self.stdout.write(f'  Eliminada: {img.imagen_ruta}')

        self.stdout.write(self.style.SUCCESS(f'\nRegistros huérfanos eliminados: {deleted}'))
        self.stdout.write(self.style.SUCCESS(f'Restantes: {ProductoImagen.objects.count()}'))
