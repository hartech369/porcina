from django.core.management.base import BaseCommand
from core.models import Servicio


class Command(BaseCommand):
    help = 'Pobla la base de datos con los servicios de ElectriPorc'

    def handle(self, *args, **options):
        self.stdout.write('Poblando servicios...')

        servicios = [
            {
                'titulo': 'Instalación de cortinas',
                'slug': 'instalacion-cortinas',
                'descripcion': 'En Electriporc ofrecemos el servicio especializado de instalación de cortinas enrollables, mallas antiaves y sistemas de protección para granjas porcinas y avícolas. Nuestro equipo realiza un montaje profesional, seguro y personalizado, utilizando materiales de alta calidad para optimizar el control ambiental, fortalecer la bioseguridad y mejorar el bienestar animal.',
                'beneficios': [
                    'Control eficiente de la ventilación y la temperatura.',
                    'Protección contra aves y otros agentes externos.',
                    'Mayor bioseguridad para las instalaciones.',
                    'Mejor bienestar y confort para los animales.',
                    'Materiales resistentes y de larga vida útil.',
                    'Instalación profesional adaptada a cada proyecto.',
                    'Acompañamiento técnico antes, durante y después de la instalación.',
                    'Soluciones que contribuyen a una mayor productividad de la granja.',
                ],
                'imagen': 'img/servicios/1.png',
                'orden': 1,
            },
            {
                'titulo': 'Instalación de agitadores de estiércol',
                'slug': 'instalacion-agitadores',
                'descripcion': 'En Electriporc realizamos la instalación profesional de agitadores de estiércol para granjas porcinas, garantizando un montaje seguro y eficiente que optimiza el manejo de los purines. Nuestros sistemas favorecen la homogenización del estiércol, evitando la sedimentación de sólidos y facilitando las labores de almacenamiento, bombeo y aprovechamiento del material.',
                'beneficios': [
                    'Homogeneización eficiente del estiércol antes del bombeo.',
                    'Evita la acumulación y sedimentación de sólidos.',
                    'Facilita el vaciado de fosas y lagunas.',
                    'Mejora el funcionamiento de los sistemas de bombeo.',
                    'Reduce el tiempo y el esfuerzo en las labores de manejo de purines.',
                    'Contribuye a un manejo más eficiente de los residuos de la granja.',
                    'Instalación profesional y adaptada a las condiciones de cada proyecto.',
                    'Acompañamiento técnico y puesta en marcha del equipo.',
                ],
                'imagen': 'img/servicios/2.png',
                'orden': 2,
            },
            {
                'titulo': 'Instalación y fabricación de elevadores de alimento',
                'slug': 'instalacion-elevadores',
                'descripcion': 'En Electriporc ofrecemos el servicio de instalación de elevadores de alimento para granjas porcinas, garantizando un montaje seguro, eficiente y adaptado a las necesidades de cada proyecto. Nuestros sistemas permiten transportar el alimento de forma continua hacia silos, tolvas y líneas de alimentación, optimizando los procesos y mejorando la eficiencia operativa de la granja.',
                'beneficios': [
                    'Transporte eficiente y continuo del alimento.',
                    'Reduce el esfuerzo y la manipulación manual.',
                    'Optimiza el tiempo en las labores de alimentación.',
                    'Favorece un suministro uniforme del alimento.',
                    'Disminuye las pérdidas durante el transporte.',
                    'Compatible con diferentes sistemas de alimentación y almacenamiento.',
                    'Instalación profesional con materiales de alta calidad.',
                    'Acompañamiento técnico, pruebas de funcionamiento y puesta en marcha.',
                ],
                'imagen': 'img/servicios/3.png',
                'orden': 3,
            },
            {
                'titulo': 'Montaje de silos en pie',
                'slug': 'montaje-silos',
                'descripcion': 'En Electriporc ofrecemos el servicio especializado de montaje de silos en pie para granjas porcinas y avícolas, realizando una instalación segura, eficiente y adaptada a las condiciones de cada proyecto. Nuestro equipo técnico garantiza un montaje preciso que asegura la estabilidad, el correcto funcionamiento y la máxima vida útil del sistema de almacenamiento.',
                'beneficios': [
                    'Montaje seguro y profesional.',
                    'Optimiza el almacenamiento de alimento.',
                    'Garantiza la estabilidad y el correcto funcionamiento del silo.',
                    'Reduce los tiempos de instalación.',
                    'Adaptación a las condiciones de cada granja.',
                    'Personal técnico con experiencia en montaje de silos.',
                    'Cumplimiento de altos estándares de calidad y seguridad.',
                    'Acompañamiento técnico durante todo el proceso.',
                ],
                'imagen': 'img/servicios/4.png',
                'orden': 4,
            },
            {
                'titulo': 'Mantenimiento preventivo y correctivo',
                'slug': 'mantenimiento',
                'descripcion': 'En Electriporc ofrecemos servicios de mantenimiento preventivo y correctivo para equipos y sistemas de automatización en granjas porcinas y avícolas. Nuestro equipo técnico realiza inspecciones, diagnósticos, ajustes y reparaciones para garantizar el óptimo funcionamiento de los equipos, reducir tiempos de inactividad y prolongar su vida útil.',
                'beneficios': [
                    'Previene fallas y paradas inesperadas.',
                    'Prolonga la vida útil de los equipos.',
                    'Optimiza el rendimiento de los sistemas de automatización.',
                    'Reduce costos por reparaciones mayores.',
                    'Diagnóstico y solución oportuna de averías.',
                    'Atención técnica especializada.',
                    'Mayor continuidad y eficiencia en la operación de la granja.',
                    'Acompañamiento y soporte técnico.',
                ],
                'imagen': 'img/servicios/5.png',
                'orden': 5,
            },
            {
                'titulo': 'Asesoría técnica especializada',
                'slug': 'asesoria-tecnica',
                'descripcion': 'En Electriporc brindamos asesoría técnica especializada para el diseño, selección, instalación y optimización de equipos y sistemas para granjas porcinas y avícolas. Acompañamos a nuestros clientes en cada etapa del proyecto, ofreciendo soluciones personalizadas que mejoran la eficiencia, la productividad y el desempeño de sus instalaciones.',
                'beneficios': [
                    'Soluciones adaptadas a las necesidades de cada granja.',
                    'Acompañamiento técnico antes, durante y después del proyecto.',
                    'Optimización de procesos y recursos.',
                    'Selección adecuada de equipos y sistemas.',
                    'Mayor eficiencia operativa y productividad.',
                    'Personal técnico con experiencia en el sector.',
                    'Soporte para la implementación de nuevas tecnologías.',
                    'Atención personalizada y respaldo técnico.',
                ],
                'imagen': 'img/servicios/6.png',
                'orden': 6,
            },
        ]

        for data in servicios:
            Servicio.objects.update_or_create(
                slug=data['slug'],
                defaults=data
            )

        total = Servicio.objects.count()
        self.stdout.write(self.style.SUCCESS(f'¡Listo! {total} servicios creados.'))
