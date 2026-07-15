import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Producto, Categoria, Subcategoria, Proyecto, Testimonio, FAQ, Servicio, MensajeContacto


def home(request):
    """Vista de presentación - Página de inicio"""
    categorias_home = Categoria.objects.filter(activa=True).order_by('orden')[:4]
    return render(request, 'core/home.html', {'categorias_home': categorias_home})


def nosotros(request):
    """Página Quiénes Somos"""
    return render(request, 'core/nosotros.html')


def servicios(request):
    """Página de Servicios - desde la base de datos"""
    servicios = Servicio.objects.filter(activo=True).order_by('orden')
    return render(request, 'core/servicios.html', {'servicios': servicios})


def productos(request):
    """Página de Productos/Catálogo - desde la base de datos"""
    categorias_db = Categoria.objects.filter(activa=True).prefetch_related(
        'subcategorias', 'subcategorias__productos', 'productos'
    ).order_by('orden')

    categorias = []
    for cat in categorias_db:
        subcategorias = []
        # Subcategorías con productos
        for sub in cat.subcategorias.filter(activa=True).order_by('orden'):
            productos_sub = []
            for prod in sub.productos.filter(disponible=True).order_by('orden', 'nombre'):
                imagen_path = ''
                if prod.imagen:
                    imagen_path = prod.imagen if prod.imagen else ''
                productos_sub.append({
                    'nombre': prod.nombre,
                    'desc': prod.descripcion_corta,
                    'imagen': imagen_path,
                    'features': prod.caracteristicas if prod.caracteristicas else [],
                })
            if productos_sub:
                subcategorias.append({
                    'nombre': sub.nombre,
                    'productos': productos_sub,
                })
        # Productos sin subcategoría (directos en la categoría)
        productos_sin_sub = cat.productos.filter(subcategoria__isnull=True, disponible=True).order_by('orden', 'nombre')
        if productos_sin_sub.exists():
            productos_directos = []
            for prod in productos_sin_sub:
                imagen_path = ''
                if prod.imagen:
                    imagen_path = prod.imagen if prod.imagen else ''
                productos_directos.append({
                    'nombre': prod.nombre,
                    'desc': prod.descripcion_corta,
                    'imagen': imagen_path,
                    'features': prod.caracteristicas if prod.caracteristicas else [],
                })
            subcategorias.append({
                'nombre': cat.nombre,
                'productos': productos_directos,
            })

        categorias.append({
            'id': cat.slug,
            'nombre': cat.nombre,
            'subcategorias': subcategorias,
        })

    context = {'categorias': categorias}
    return render(request, 'core/productos.html', context)


def galeria(request):
    """Página de Galería/Proyectos"""
    proyectos = Proyecto.objects.filter(activo=True).order_by('-destacado', 'orden', '-fecha')
    context = {'proyectos': proyectos}
    return render(request, 'core/galeria.html', context)


def testimonios(request):
    """Página de Testimonios"""
    testimonials = Testimonio.objects.filter(activo=True).order_by('orden', '-creado')
    stats = [
        {'value': '15+', 'label': 'Años de Experiencia'},
        {'value': '500+', 'label': 'Granjas Atendidas'},
        {'value': '50+', 'label': 'Tipos de Productos'},
        {'value': '98%', 'label': 'Clientes Satisfechos'},
    ]
    context = {'testimonials': testimonials, 'stats': stats}
    return render(request, 'core/testimonios.html', context)


def faq(request):
    """Página de FAQ/Preguntas Frecuentes"""
    faqs = FAQ.objects.filter(activa=True).order_by('orden', 'pregunta')
    context = {'faqs': faqs}
    return render(request, 'core/faq.html', context)


def contacto(request):
    """Página de Contacto"""
    return render(request, 'core/contacto.html')


@csrf_exempt
@require_http_methods(["POST"])
def api_contacto(request):
    """API endpoint para recibir mensajes de contacto"""
    try:
        data = json.loads(request.body)
        mensaje = MensajeContacto.objects.create(
            nombre=data.get('nombre', ''),
            email=data.get('email', ''),
            telefono=data.get('telefono', ''),
            empresa=data.get('empresa', ''),
            asunto=data.get('asunto', 'Cotización desde la web'),
            mensaje=data.get('mensaje', ''),
            servicio_interes=data.get('servicio', '')
        )
        return JsonResponse({
            'success': True,
            'message': 'Mensaje enviado correctamente',
            'id': mensaje.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
