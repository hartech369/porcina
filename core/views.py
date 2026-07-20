import json
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
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
    servicios = Servicio.objects.filter(activo=True).prefetch_related('imagenes').order_by('orden')
    return render(request, 'core/servicios.html', {'servicios': servicios})


def productos(request):
    """Página de Productos/Catálogo - imágenes leídas directo de carpetas"""
    categorias_db = Categoria.objects.filter(activa=True).prefetch_related(
        'subcategorias', 'subcategorias__productos', 'productos'
    ).order_by('orden')

    def get_imagenes_producto(prod):
        """Lee todas las imágenes de la carpeta del producto en disco"""
        if not prod.imagen:
            return []
        img_parts = prod.imagen.split('/')
        if len(img_parts) < 2:
            return []
        carpeta = os.path.join(settings.BASE_DIR, 'static', *img_parts[:-1])
        if not os.path.isdir(carpeta):
            return []
        extensiones = ('.png', '.jpg', '.jpeg', '.webp')
        archivos = sorted([f for f in os.listdir(carpeta) if f.lower().endswith(extensiones)])
        ruta_carpeta = '/'.join(img_parts[:-1])
        return [f'{ruta_carpeta}/{a}' for a in archivos]

    def get_product_data(prod):
        """Retorna diccionario con todos los datos del producto"""
        imagenes = get_imagenes_producto(prod)
        return {
            'id': prod.id,
            'nombre': prod.nombre,
            'desc': prod.descripcion_corta,
            'descripcion': prod.descripcion,
            'materiales': prod.materiales,
            'capacidad': prod.capacidad,
            'dimensiones': prod.dimensiones,
            'regulacion': prod.regulacion,
            'componentes': prod.componentes,
            'aplicaciones': prod.aplicaciones,
            'beneficios': [b.strip() for b in prod.beneficios.replace('. ', '.|').split('|') if b.strip()] if prod.beneficios else [],
            'especificaciones': prod.especificaciones,
            'imagen': imagenes[0] if imagenes else '',
            'imagenes': imagenes,
            'features': prod.caracteristicas if prod.caracteristicas else [],
        }

    categorias = []
    for cat in categorias_db:
        subcategorias = []
        for sub in cat.subcategorias.filter(activa=True).order_by('orden'):
            productos_sub = []
            for prod in sub.productos.filter(disponible=True).order_by('orden', 'nombre'):
                productos_sub.append(get_product_data(prod))
            if productos_sub:
                subcategorias.append({
                    'nombre': sub.nombre,
                    'productos': productos_sub,
                })
        productos_sin_sub = cat.productos.filter(subcategoria__isnull=True, disponible=True).order_by('orden', 'nombre')
        if productos_sin_sub.exists():
            productos_directos = []
            for prod in productos_sin_sub:
                productos_directos.append(get_product_data(prod))
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
    proyectos = Proyecto.objects.filter(activo=True).prefetch_related('imagenes').order_by('orden', '-destacado')
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
    return render(request, 'core/faq.html')


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


def terminos(request):
    """Página de Términos y Condiciones"""
    return render(request, 'core/terminos.html')


def privacidad(request):
    """Página de Política de Privacidad"""
    return render(request, 'core/privacidad.html')


def tratamiento_datos(request):
    """Página de Política de Tratamiento de Datos Personales"""
    return render(request, 'core/tratamiento-datos.html')
