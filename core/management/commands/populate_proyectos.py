from django.core.management.base import BaseCommand
from core.models import Proyecto


class Command(BaseCommand):
    help = 'Pobla la base de datos con los proyectos de ElectriPorc'

    def handle(self, *args, **options):
        proyectos = [
            {
                'titulo': 'Montaje de silos metálicos sin grúa',
                'cliente': 'Cliente del sector porcícola',
                'ubicacion': 'Antioquia, Colombia',
                'periodo_ejecucion': '2025',
                'tipo_trabajo': 'Armado e instalación vertical de silos metálicos directamente en sitio, sin necesidad de grúa.',
                'descripcion': 'Realizamos el armado y la instalación de silos metálicos directamente en la granja mediante un sistema de montaje vertical en sitio, sin necesidad de grúa. Con esta metodología reducimos los costos asociados al uso de maquinaria pesada, facilitamos el montaje en espacios con acceso limitado y garantizamos un proceso seguro, eficiente y con altos estándares de calidad.',
                'orden': 1,
            },
            {
                'titulo': 'Sistema de cortinas laterales enrollables para galpones porcícolas',
                'cliente': 'Cliente del sector porcícola',
                'ubicacion': 'Antioquia, Colombia',
                'periodo_ejecucion': '2025–2026',
                'tipo_trabajo': 'Suministro e instalación de un sistema de cortinas laterales enrollables para galpones porcícolas.',
                'descripcion': 'Suministramos e instalamos un sistema de cortinas laterales enrollables para mejorar el control de la ventilación y las condiciones ambientales dentro de los galpones. Con esta solución favorecemos el bienestar animal, protegemos las instalaciones frente a las variaciones climáticas y facilitamos la operación diaria de la granja.',
                'orden': 2,
            },
            {
                'titulo': 'Elevadores de alimento para sistemas de alimentación porcícola',
                'cliente': 'Cliente del sector porcícola',
                'ubicacion': 'Sector porcícola a nivel nacional',
                'periodo_ejecucion': '2024–2026',
                'tipo_trabajo': 'Fabricación e instalación de elevadores de alimento para sistemas de alimentación porcícola.',
                'descripcion': 'Fabricamos e instalamos elevadores de alimento adaptados a los requerimientos de cada proyecto, diseñados para transportar el alimento de forma eficiente desde el silo hasta las áreas de distribución o consumo. Con esta solución mejoramos la continuidad del suministro, reducimos la manipulación manual y optimizamos la operación del sistema de alimentación.',
                'orden': 3,
            },
            {
                'titulo': 'Sistemas automáticos de alimentación por cadena y sinfín',
                'cliente': 'Cliente del sector porcícola',
                'ubicacion': 'Sector porcícola a nivel nacional y Latinoamérica',
                'periodo_ejecucion': '2025–2026',
                'tipo_trabajo': 'Suministro e instalación de sistemas automáticos de alimentación por cadena y sinfín para producción porcícola.',
                'descripcion': 'Suministramos e instalamos sistemas automáticos de alimentación por cadena y sinfín, diseñados para transportar y distribuir el alimento de manera eficiente y uniforme en las diferentes áreas de producción. Con estos sistemas reducimos la carga operativa, mejoramos el control del proceso y contribuimos a una alimentación más continua y productiva.',
                'orden': 4,
            },
            {
                'titulo': 'Construcción integral de galpones porcícolas',
                'cliente': 'Cliente del sector porcícola',
                'ubicacion': 'Sector porcícola a nivel nacional y Latinoamérica',
                'periodo_ejecucion': 'Desde 2022',
                'tipo_trabajo': 'Construcción integral de galpones porcícolas, incluyendo estructuras metálicas, cubiertas y adecuaciones.',
                'descripcion': 'Desde 2022, desarrollamos proyectos integrales para la construcción de galpones porcícolas, incluyendo la fabricación y el montaje de estructuras metálicas, la instalación de cubiertas y la adecuación de los espacios según las necesidades de operación. En cada proyecto ofrecemos soluciones funcionales, resistentes y adaptadas a las condiciones y requerimientos de nuestros clientes.',
                'orden': 5,
            },
        ]

        for p in proyectos:
            obj, created = Proyecto.objects.update_or_create(
                titulo=p['titulo'],
                defaults=p
            )
            action = 'CREADO' if created else 'ACTUALIZADO'
            self.stdout.write(f'{action}: {obj.titulo}')

        self.stdout.write(self.style.SUCCESS(f'\n{len(proyectos)} proyectos procesados correctamente'))
