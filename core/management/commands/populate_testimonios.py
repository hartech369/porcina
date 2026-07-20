from django.core.management.base import BaseCommand
from core.models import Testimonio


class Command(BaseCommand):
    help = 'Poblar testimonios de ElectriPorc'

    def handle(self, *args, **options):
        testimonios = [
            {
                'nombre': 'Eider Mira',
                'cargo': 'Administrador',
                'empresa': 'Granja La Argelia',
                'texto': 'Nuestra experiencia trabajando con ElectriPorc ha sido muy exitosa. Los trabajos de automatización y mantenimiento del sistema se realizaron adecuadamente, y valoramos especialmente la diligencia con la que atienden cada requerimiento.',
                'rating': 5,
                'orden': 1,
            },
            {
                'nombre': 'Jennyfer',
                'cargo': 'Administradora técnica de granja',
                'empresa': 'Agropecuaria La Montañita',
                'texto': 'Nuestra experiencia con ElectriPorc ha sido muy buena. Destacamos la calidad del trabajo, el excelente servicio, el acompañamiento técnico y su capacidad de respuesta frente a los problemas. Para nosotros, ElectriPorc es un aliado estratégico en la granja.',
                'rating': 5,
                'orden': 2,
            },
            {
                'nombre': 'Gabriel Vásquez',
                'cargo': 'Director técnico de porcicultura',
                'empresa': 'Granja La Lucha',
                'texto': 'Nuestra experiencia con ElectriPorc ha sido eficiente y responsable. Valoramos especialmente el cumplimiento de los compromisos adquiridos y la eficiencia de su trabajo. Es una empresa comprometida y responsable.',
                'rating': 5,
                'orden': 3,
            },
        ]

        for data in testimonios:
            testimonio, created = Testimonio.objects.get_or_create(
                empresa=data['empresa'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Testimonio creado: {testimonio.empresa}'))
            else:
                self.stdout.write(f'Testimonio ya existe: {testimonio.empresa}')

        self.stdout.write(self.style.SUCCESS('Proceso completado'))
