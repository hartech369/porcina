from django.core.management.base import BaseCommand
from core.models import Categoria, Subcategoria, Producto


class Command(BaseCommand):
    help = 'Pobla la base de datos con el catálogo actual de productos'

    def handle(self, *args, **options):
        self.stdout.write('Poblando base de datos...')

        # ============================================
        # CATEGORÍA 1: ALIMENTACIÓN
        # ============================================
        cat_alimentacion, _ = Categoria.objects.update_or_create(
            slug='alimentacion',
            defaults={
                'nombre': 'Alimentación',
                'descripcion': 'Sistemas de alimentación para optimizar el suministro de alimento y reducir desperdicios.',
                'descripcion_corta': 'Comederos, tolvas, dosificadores y sistemas automáticos de alimentación.',
                'icono': 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10',
                'orden': 1,
            }
        )

        # Subcategoría: Comederos
        sub_comederos, _ = Subcategoria.objects.update_or_create(
            categoria=cat_alimentacion,
            nombre='Comederos',
            defaults={'orden': 1}
        )

        comederos = [
            ('Comedero Ceba Seco Húmedo 140 LT', 'Estructura en acero galvanizado en caliente, 20 puntos de regulación de alimento.', 'img/productos/alimentacion/comederos/1.png', ['Capacidad: 140 LT / 80 kg', 'Acero galvanizado en caliente', '20 puntos de regulación', 'Alimenta hasta 50 cerdos', 'Bandeja acero inoxidable', 'Válvula automática de agua']),
            ('Comedero Seco y Húmedo para Ceba – 100 kg', 'Comedero para cerdos de ceba con sistema de alimentación seca o húmeda.', 'img/productos/alimentacion/comederos/2.png', ['Capacidad: 100 kg', 'Dimensiones: 76 × 60 × 120 cm', 'Tolva plástico alta resistencia', 'Estructura galvanizada', 'Plato acero inoxidable redondo', 'Regulación del flujo de alimento']),
            ('Comedero Ceba Ajustable Doble Cara 8 Bocas', 'Comedero de dos caras regulable en 8 puntos para evitar desperdicio.', 'img/productos/alimentacion/comederos/3.png', ['8 bocas doble cara', 'Acero inoxidable 304 calibre 1.2mm', 'Capacidad: 100 kg', 'Alimenta 90-100 cerdos en ceba', 'Tamaño: 124×50×90 cm', 'Boquillas de agua integradas']),
            ('Comedero Precebo Seco Húmedo 65 LT', 'Estructura en acero galvanizado al caliente con 20 puntos de regulación.', 'img/productos/alimentacion/comederos/4.png', ['Capacidad: 65 LT / 40 kg', 'Alimenta hasta 50 lechones', 'Tolva diámetro 46 cm', 'Alto: 96 cm, Bandeja: 54×38 cm', 'Acero inoxidable bandeja', 'Peso: 20 kg']),
            ('Comedero Doble Cara 10 Bocas Inoxidable Precebo', 'Comedero ajustable de dos caras con 12 puntos de regulación.', 'img/productos/alimentacion/comederos/5.png', ['10 bocas doble cara', 'Acero inoxidable calibre 1.2mm', 'Capacidad: 50 kg', 'Alimenta hasta 50 cerdos en precebo', 'Tamaño: 97.5×46×61 cm', 'Esquinas redondeadas para limpieza']),
            ('Comedero Segunda Edad', 'Comedero de plástico de alta calidad para lechones en segunda edad.', 'img/productos/alimentacion/comederos/6.png', ['Plástico de alta calidad', 'Medidas: 63×44 cm', 'Capacidad: 17 kg', 'Alimenta hasta 30 lechones', '10 puestos, 7 niveles de regulación', 'Peso: 2.78 kg']),
            ('Comedero Verde Redondo', 'Polipropileno de alta densidad con 8 compartimentos para precebo.', 'img/productos/alimentacion/comederos/7.png', ['Polipropileno alta densidad', '8 compartimentos de 15 cm', 'Capacidad: 5 kg total', 'Alimenta hasta 20 lechones', 'Cero desperdicio', 'Ideal para precebo']),
            ('Comedero Madre Paridera con Refuerzo', 'Comedero para madres en paridera con refuerzo en acero inoxidable.', 'img/productos/alimentacion/comederos/8.png', ['Polietileno alta densidad', 'Refuerzo acero inoxidable', 'Medidas: 36×27 cm', 'Diseño ergonómico', 'Fácil mantenimiento', 'Evita acumulación de residuos']),
            ('Comedero Madre Paridera en Acero Inoxidable', 'Comedero de acero inoxidable 304 para cerdas.', 'img/productos/alimentacion/comederos/9.png', ['Acero inoxidable 304', 'Medidas: 37×45 cm', 'Higiénico y resistente', 'Fácil de limpiar', 'Aumenta eficiencia alimenticia', 'Para granjas porcinas']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(comederos, 1):
            Producto.objects.update_or_create(
                slug=f'comedero-{i}',
                defaults={
                    'categoria': cat_alimentacion,
                    'subcategoria': sub_comederos,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # Subcategoría: Dosificadores
        sub_dosificadores, _ = Subcategoria.objects.update_or_create(
            categoria=cat_alimentacion,
            nombre='Dosificadores',
            defaults={'orden': 2}
        )

        dosificadores = [
            ('Dosificador Verde y Rojo 6 LT', 'Diseñado para dispensar porciones específicas de alimento.', 'img/productos/alimentacion/dosificadores/10.png', ['Polipropileno 100%', 'Capacidad: 6 LT', 'Cubo transparente', 'Bola de control de cantidad', 'Automatiza transporte de alimento', 'Ahorra mano de obra']),
            ('Dosificador 8 LT', 'Diseñado para dispensar porciones específicas de alimento.', 'img/productos/alimentacion/dosificadores/11.png', ['Polipropileno 100%', 'Capacidad: 8 LT', 'Cubo transparente', 'Bola de control de cantidad', 'Automatiza transporte de alimento', 'Ahorra mano de obra']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(dosificadores, 10):
            Producto.objects.update_or_create(
                slug=f'dosificador-{i}',
                defaults={
                    'categoria': cat_alimentacion,
                    'subcategoria': sub_dosificadores,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # Subcategoría: Papilleros
        sub_papilleros, _ = Subcategoria.objects.update_or_create(
            categoria=cat_alimentacion,
            nombre='Papilleros',
            defaults={'orden': 3}
        )

        papilleros = [
            ('Papillero Inoxidable', 'Con 4 separadores en acero inoxidable de alta resistencia.', 'img/productos/alimentacion/papilleros/12.png', ['Acero inoxidable alta resistencia', '4 separadores', 'Capacidad: 10-20 lechones', 'Fácil de limpiar', 'Minimiza desperdicio', 'Para parideras']),
            ('Papillero Turbo Pig', 'Plástico 100% virgen con alta resistencia. Se fija en piso de rejilla.', 'img/productos/alimentacion/papilleros/13.png', ['Plástico 100% virgen', 'Fija en piso de rejilla', 'Comedero redondo + varilla inox', 'Mayor peso de camada', 'Mejor uniformidad', 'Superficies lisas para lavado']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(papilleros, 12):
            Producto.objects.update_or_create(
                slug=f'papillero-{i}',
                defaults={
                    'categoria': cat_alimentacion,
                    'subcategoria': sub_papilleros,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # Subcategoría: Sistemas Automáticos
        sub_sistemas_auto, _ = Subcategoria.objects.update_or_create(
            categoria=cat_alimentacion,
            nombre='Sistemas Automáticos de Alimentación',
            defaults={'orden': 4}
        )

        sistemas_auto = [
            ('Tolva Automática para Jaula', 'Material acero inoxidable y plástico de alta densidad.', 'img/productos/alimentacion/sistemas-automaticos/14.png', ['Acero inoxidable y plástico', 'Medidas: 48×37 cm', 'Capacidad: 8 kg', 'Sistema dosificador', 'Regulación de 6 posiciones', 'Fácil de instalar']),
            ('Sensor de Paro con Lengüeta', 'Control automático de nivel de alimento.', 'img/productos/alimentacion/sistemas-automaticos/15.png', ['Control automático de nivel', 'Cable alta resistencia impermeable', 'Carcasa polipropileno', 'Resistente a humedad y corrosión', 'Compatible con aguas residuales', 'Fácil instalación']),
            ('Sensor de Proximidad Inductivo', 'Sensor electrónico para detectar presencia de objetos sin contacto.', 'img/productos/alimentacion/sistemas-automaticos/16.png', ['Detección sin contacto', 'Alta precisión y respuesta rápida', 'Carcasa metálica resistente', 'Resistente a vibraciones', '4 cables: 2 alimentación 24V + 2 contacto', 'Ideal ambientes agropecuarios']),
            ('Tolva Manual con Boya', 'Tolva para suministro manual con sistema de boya automático.', 'img/productos/alimentacion/sistemas-automaticos/17.png', ['Plástico alta resistencia', 'Sistema de boya automático', 'Reduce desperdicio', 'Fácil instalación y limpieza', 'Resistente a corrosión y humedad', 'Aplica: maternidad, precebo, destete, corrales']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(sistemas_auto, 14):
            Producto.objects.update_or_create(
                slug=f'sistema-auto-{i}',
                defaults={
                    'categoria': cat_alimentacion,
                    'subcategoria': sub_sistemas_auto,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # ============================================
        # CATEGORÍA 2: SILOS Y ALMACENAMIENTO
        # ============================================
        cat_silos, _ = Categoria.objects.update_or_create(
            slug='silos',
            defaults={
                'nombre': 'Silos y Almacenamiento',
                'descripcion': 'Soluciones para almacenar, conservar y manejar alimento de forma segura y eficiente.',
                'descripcion_corta': 'Silos galvanizados, accesorios, transporte de alimento y sistemas de pesaje.',
                'icono': 'M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4',
                'orden': 2,
            }
        )

        # Subcategoría: Accesorios para Silo
        sub_accesorios_silo, _ = Subcategoria.objects.update_or_create(
            categoria=cat_silos,
            nombre='Accesorios para Silo',
            defaults={'orden': 1}
        )

        accesorios_silo = [
            ('Salida de Silo Inoxidable', 'Salida de silo en acero inoxidable con diseño cónico para flujo eficiente del alimento. Instalación mediante brida.', 'img/productos/silos/accesorios-silo/1.png', ['Acero inoxidable', 'Diseño cónico eficiente', 'Instalación por brida', 'Alta resistencia a corrosión', 'Fácil limpieza', 'Compatible con sinfín']),
            ('Salida de Silo Transparente', 'Salida de silo en policarbonato transparente para inspección visual del flujo de alimento.', 'img/productos/silos/accesorios-silo/2.png', ['Policarbonato transparente', 'Resistente a impactos', 'Visualización del flujo', 'Diseño ligero', 'Fácil instalación', 'Fácil limpieza']),
            ('Cajetín Doble de 60 mm', 'Cajetín doble en acero inoxidable para distribuir alimento a dos líneas de transporte de 60 mm.', 'img/productos/silos/accesorios-silo/3.png', ['Acero inoxidable', 'Diámetro: 60 mm', 'Configuración doble salida', 'Resistente a corrosión', 'Fácil limpieza', 'Uso continuo']),
            ('Cajetín de 60 mm', 'Cajetín en acero inoxidable para conducir alimento a una línea de transporte de 60 mm.', 'img/productos/silos/accesorios-silo/4.png', ['Acero inoxidable', 'Diámetro: 60 mm', 'Salida sencilla', 'Alta resistencia', 'Fácil limpieza', 'Uso continuo']),
            ('Cajetín de 75 mm con Rasera', 'Cajetín en acero inoxidable con rasera de cierre para controlar paso de alimento a línea de 75 mm.', 'img/productos/silos/accesorios-silo/5.png', ['Acero inoxidable', 'Diámetro: 75 mm', 'Rasera de cierre manual', 'Resistente a corrosión', 'Fácil limpieza', 'Mantenimiento sencillo']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(accesorios_silo, 1):
            Producto.objects.update_or_create(
                slug=f'accesorio-silo-{i}',
                defaults={
                    'categoria': cat_silos,
                    'subcategoria': sub_accesorios_silo,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # Subcategoría: Silos Galvanizados
        sub_silos_galv, _ = Subcategoria.objects.update_or_create(
            categoria=cat_silos,
            nombre='Silos Galvanizados 8-22 TN',
            defaults={'orden': 2}
        )

        Producto.objects.update_or_create(
            slug='silo-galvanizado',
            defaults={
                'categoria': cat_silos,
                'subcategoria': sub_silos_galv,
                'nombre': 'Silo Galvanizado para Alimento',
                'descripcion_corta': 'Silo en acero galvanizado para almacenamiento seguro de alimento balanceado. Capacidades de 10, 12, 18 y 22 toneladas.',
                'imagen': 'img/productos/silos/silos-galvanizados/6.png',
                'caracteristicas': ['Acero galvanizado', 'Capacidades: 10-22 toneladas', 'Diseño cónico descarga eficiente', 'Escalera y plataforma acceso', 'Resistente a intemperie', 'Fácil instalación'],
                'orden': 6,
            }
        )

        # Subcategoría: Sistema de Transporte de Alimento
        sub_transporte, _ = Subcategoria.objects.update_or_create(
            categoria=cat_silos,
            nombre='Sistema de Transporte de Alimento',
            defaults={'orden': 3}
        )

        transporte = [
            ('Elevador de Alimento', 'Elevador con sistema sinfín para transportar granos y alimento hacia silos. Diseño portátil.', 'img/productos/silos/transporte-alimento/7.png', ['Sistema sinfín', 'Motorreductor', 'Diseño portátil', 'Bajo mantenimiento', 'Operación continua', 'Carga de silos']),
            ('Máquina de Arrastre', 'Máquina para accionar sistemas de alimentación por cadena. Visor transparente para inspección.', 'img/productos/silos/transporte-alimento/8.png', ['Acero inoxidable', 'Transmisión por cadena', 'Visor transparente', 'Diseño robusto', 'Trabajo continuo', 'Fácil acceso limpieza']),
            ('Cadena Eslabonada', 'Cadena eslabonada con discos de arrastre para transporte eficiente de alimento en sistemas automatizados.', 'img/productos/silos/transporte-alimento/9.png', ['Acero galvanizado', 'Discos plástico técnico', 'Resistente al desgaste', 'Funcionamiento silencioso', 'Larga vida útil', 'Fácil instalación']),
            ('Sinfín', 'Sinfín flexible en acero de alta resistencia para transporte continuo de alimento. Disponible en varios diámetros.', 'img/productos/silos/transporte-alimento/10.png', ['Acero alta resistencia', 'Diseño espiral flexible', 'Resistente al desgaste', 'Funcionamiento continuo', 'Varios diámetros disponibles', 'Compatible con automatización']),
            ('Corner Azul', 'Corner en plástico técnico para cambios de dirección en sistema de alimentación por cadena.', 'img/productos/silos/transporte-alimento/11.png', ['Plástico técnico', 'Color azul', 'Rodamiento central', 'Resistente a desgaste', 'Resistente a humedad', 'Fácil instalación']),
            ('Corner en Acero Inoxidable', 'Corner en acero inoxidable con polea interna para cambios de dirección. Diseño desmontable.', 'img/productos/silos/transporte-alimento/12.png', ['Acero inoxidable', 'Polea interna de precisión', 'Rodamiento suave', 'Resistente a corrosión', 'Diseño desmontable', 'Fácil limpieza']),
            ('Unión Transparente', 'Unión en policarbonato transparente para inspección visual de cadena en sistemas de alimentación.', 'img/productos/silos/transporte-alimento/13.png', ['Policarbonato transparente', 'Resistente a impactos', 'Inspección visual cadena', 'Fácil instalación', 'Compatible con cadena', 'Desmontaje sencillo']),
            ('Unión Inoxidable', 'Unión en acero inoxidable para conectar tramos de tubería en sistemas de alimentación automatizada.', 'img/productos/silos/transporte-alimento/14.png', ['Acero inoxidable', 'Unión por tornillería', 'Resistente a corrosión', 'Fácil instalación', 'Larga vida útil', 'Conexión de tuberías']),
            ('Bajante para Sistema de Alimentación', 'Bajante en acero galvanizado para conducir alimento desde línea de transporte hasta puntos de descarga.', 'img/productos/silos/transporte-alimento/15.png', ['Acero galvanizado', 'Ángulo de descarga eficiente', 'Flujo uniforme', 'Fácil instalación', 'Larga vida útil', 'Resistente a corrosión']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(transporte, 7):
            Producto.objects.update_or_create(
                slug=f'transporte-{i}',
                defaults={
                    'categoria': cat_silos,
                    'subcategoria': sub_transporte,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # Subcategoría: Sistemas de Pesaje
        sub_pesaje, _ = Subcategoria.objects.update_or_create(
            categoria=cat_silos,
            nombre='Sistemas de Pesaje',
            defaults={'orden': 4}
        )

        Producto.objects.update_or_create(
            slug='kit-bascula-silos',
            defaults={
                'categoria': cat_silos,
                'subcategoria': sub_pesaje,
                'nombre': 'Kit de Báscula para Silos – 4 y 6 Celdas',
                'descripcion_corta': 'Sistema de pesaje para silos metálicos con celdas de alta precisión. Monitoreo de inventario en tiempo real.',
                'imagen': 'img/productos/silos/pesaje/16.png',
                'caracteristicas': ['4 y 6 celdas de carga', 'Celdas alta precisión', 'Indicador digital de peso', 'Cableado para exteriores', 'Protección humedad y polvo', 'Compatible con automatización'],
                'orden': 16,
            }
        )

        # ============================================
        # CATEGORÍA 3: EQUIPOS PARA PRODUCCIÓN PORCINA
        # ============================================
        cat_equipos, _ = Categoria.objects.update_or_create(
            slug='equipos',
            defaults={
                'nombre': 'Equipos para Producción Porcina',
                'descripcion': 'Tecnología para reducir trabajo manual, mejorar el control operativo y optimizar procesos dentro de la granja.',
                'descripcion_corta': 'Bebederos, jaulas, plaquetas y corrales para producción porcina.',
                'icono': 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z',
                'orden': 3,
            }
        )

        # Subcategoría: Bebederos
        sub_bebederos, _ = Subcategoria.objects.update_or_create(
            categoria=cat_equipos,
            nombre='Bebederos',
            defaults={'orden': 1}
        )

        bebederos = [
            ('Chupón Lechón y Adulto', 'Bebedero tipo chupete en acero inoxidable para suministro continuo de agua limpia. Reduce desperdicio.', 'img/productos/equipos/bebederos/1.png', ['Acero inoxidable alta calidad', 'Resistente a corrosión y desgaste', 'Accionamiento suave', 'Reduce desperdicio de agua', 'Fácil instalación', 'Larga vida útil']),
            ('Bebedero en H con Manguera', 'Bebedero tipo H para ceba o precebo con dos chupetes y manguera flexible. Estructura galvanizada.', 'img/productos/equipos/bebederos/2.png', ['Estructura tipo H galvanizada', 'Dos bebederos tipo chupete', 'Manguera flexible', 'Acceso simultáneo varios animales', 'Reduce desperdicio', 'Bajo mantenimiento']),
            ('Bebedero Automático Paridera y Precebo', 'Bebedero automático con cazoleta para lechones en paridera y precebo. Anclaje a pared.', 'img/productos/equipos/bebederos/3.png', ['Acero inoxidable', 'Cazoleta con bebedero automático', 'Instalación por anclaje a pared', 'Uso continuo porcícola', 'Reduce desperdicio', 'Fácil limpieza']),
            ('Bebedero en L para Gestación', 'Bebedero en L para cerdas gestantes con chupete automático. Estructura galvanizada robusta.', 'img/productos/equipos/bebederos/4.png', ['Acero galvanizado alta resistencia', 'Chupete automático inoxidable', 'Diseño en L optimiza espacio', 'Anclaje a pared o corral', 'Resistente a corrosión', 'Larga vida útil']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(bebederos, 1):
            Producto.objects.update_or_create(
                slug=f'bebedero-{i}',
                defaults={
                    'categoria': cat_equipos,
                    'subcategoria': sub_bebederos,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # Subcategoría: Jaulas
        sub_jaulas, _ = Subcategoria.objects.update_or_create(
            categoria=cat_equipos,
            nombre='Jaulas Maternidad y Gestación',
            defaults={'orden': 2}
        )

        jaulas = [
            ('Jaula de Maternidad', 'Jaula para parto y lactancia con estructura galvanizada, piso abertura posterior, calefacción para lechones.', 'img/productos/equipos/jaulas/5.png', ['Acero galvanizado alta resistencia', 'Piso cerda con abertura posterior', 'Piso plástico para lechones', 'Divisiones laterales PVC', 'Área calefaccionada lechones', 'Comedero y bebida incluidos']),
            ('Jaula de Gestación', 'Jaula para alojamiento individual de cerdas gestantes. Puertas frontal y posterior con cierre seguro.', 'img/productos/equipos/jaulas/6.png', ['Acero galvanizado alta resistencia', 'Puertas frontal y posterior', 'Cierre seguro', 'Comedero acero inoxidable', 'Patas con placas anclaje', 'Componentes desmontables']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(jaulas, 5):
            Producto.objects.update_or_create(
                slug=f'jaula-{i}',
                defaults={
                    'categoria': cat_equipos,
                    'subcategoria': sub_jaulas,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # Subcategoría: Plaquetas
        sub_plaquetas, _ = Subcategoria.objects.update_or_create(
            categoria=cat_equipos,
            nombre='Plaquetas Lechón y Madre',
            defaults={'orden': 3}
        )

        plaquetas = [
            ('Slat 60×40 Madres Adultas', 'Piso plástico PP para madres adultas en gestación y maternidad. Antideslizante con drenaje.', 'img/productos/equipos/plaquetas/7.png', ['Polipropileno alta resistencia', '60×40 cm', 'Antideslizante', 'Ranuras drenaje', 'Alta capacidad carga', 'Ensamblaje modular']),
            ('Slat 60×60 Precebo y Lechoneras', 'Piso plástico PP para precebo y lechoneras. Disponible en naranja y verde.', 'img/productos/equipos/plaquetas/8.png', ['Polipropileno alta resistencia', '60×60 cm', 'Color naranja y verde', 'Antideslizante', 'Ranuras drenaje', 'Ensamblaje modular']),
            ('Slat 60×70 Precebo y Lechoneras', 'Piso plástico PP para precebo y lechoneras. Diseño modular de fácil instalación.', 'img/productos/equipos/plaquetas/9.png', ['Polipropileno alta resistencia', '60×70 cm', 'Antideslizante', 'Ranuras drenaje eficiente', 'Ensamblaje modular', 'Resistente a químicos']),
            ('Slat BMC Maternidad o Paridera', 'Piso BMC reforzado con fibra de vidrio para maternidad. 60cm×2.40m, altura 6cm.', 'img/productos/equipos/plaquetas/10.png', ['BMC fibra de vidrio', '60 cm × 2.40 m, altura 6 cm', 'Alta capacidad carga', 'Antideslizante', 'Ranuras drenaje', 'Resistente a humedad y químicos']),
            ('Slat BMC Cárcamo Gestación y Ceba', 'Piso BMC para cárcamo en gestación y ceba. Drenaje eficiente hacia cárcamo.', 'img/productos/equipos/plaquetas/11.png', ['BMC fibra de vidrio', '60 cm × 2.40 m, altura 6 cm', 'Alta resistencia peso', 'Antideslizante', 'Drenaje hacia cárcamo', 'Fácil limpieza']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(plaquetas, 7):
            Producto.objects.update_or_create(
                slug=f'slat-{i}',
                defaults={
                    'categoria': cat_equipos,
                    'subcategoria': sub_plaquetas,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # Subcategoría: Corrales
        sub_corrales, _ = Subcategoria.objects.update_or_create(
            categoria=cat_equipos,
            nombre='Corrales y Divisiones',
            defaults={'orden': 4}
        )

        corrales = [
            ('Panel Divisorio PVC', 'Panel PVC multicámara reforzada para separación de corrales. Alturas 50cm y 70cm.', 'img/productos/equipos/corrales/12.png', ['PVC alta resistencia', 'Alturas: 50 cm y 70 cm', 'Estructura multicámara', 'Superficie lisa fácil limpieza', 'Resistente a humedad', 'Compatible con accesorios']),
            ('Pletina T12 Fibra de Vidrio', 'Perfil estructural PRFV para soporte de pisos slat. Presentaciones de 0.60m a 6m.', 'img/productos/equipos/corrales/13.png', ['Fibra de vidrio reforzada', 'Presentaciones: 0.60-6.00 m', 'No se oxida', 'Sin mantenimiento', 'Alta estabilidad estructural', 'Compatible con slats']),
            ('Reja Metálica Galvanizada', 'Reja galvanizada para división de corrales de ceba. Medida estándar 1.78m.', 'img/productos/equipos/corrales/14.png', ['Acero galvanizado', 'Largo estándar: 1.78 m', 'Medidas especiales disponibles', 'Tubería con refuerzos', 'Compatible con postes', 'Alta resistencia']),
            ('Puerta Metálica Galvanizada', 'Puerta galvanizada para corrales de ceba. 96cm alto × 126cm ancho.', 'img/productos/equipos/corrales/15.png', ['Acero galvanizado inmersión caliente', '96 cm alto × 126 cm ancho', 'Barras horizontales', 'Fácil apertura y cierre', 'Medidas especiales disponibles', 'Bajo mantenimiento']),
            ('Herrajes Galvanizados para Panel', 'Línea de herrajes galvanizados para instalación de puertas, paneles y divisiones.', 'img/productos/equipos/corrales/16.png', ['Acero galvanizado', 'Alturas: 50 cm y 70 cm', 'Alta resistencia mecánica', 'Protección anticorrosiva', 'Fácil instalación', 'Compatibles diversos sistemas']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(corrales, 12):
            Producto.objects.update_or_create(
                slug=f'corral-{i}',
                defaults={
                    'categoria': cat_equipos,
                    'subcategoria': sub_corrales,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # ============================================
        # CATEGORÍA 4: REPUESTOS Y ACCESORIOS
        # ============================================
        cat_repuestos, _ = Categoria.objects.update_or_create(
            slug='repuestos',
            defaults={
                'nombre': 'Repuestos y Accesorios',
                'descripcion': 'Refacciones y accesorios para mantenimiento de equipos porcícolas.',
                'descripcion_corta': 'Repuestos para comederos, automatización, motorreductores y tornillería.',
                'icono': 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
                'orden': 4,
            }
        )

        # Subcategoría: Repuesto Comedero
        sub_rep_comedero, _ = Subcategoria.objects.update_or_create(
            categoria=cat_repuestos,
            nombre='Repuesto para Comedero y Dosificador',
            defaults={'orden': 1}
        )

        rep_comedero = [
            ('Repuestos Dosificador', 'Regla dosificadora, cierre y tapa para dosificador de alimento. Plástico de alta resistencia.', 'img/productos/repuestos/repuesto-comedero/1.png', ['Plástico alta resistencia', 'Regla, cierre y tapa', 'Resistente a desgaste y humedad', 'Fácil instalación', 'Compatible con dosificadores', 'Prolonga vida útil equipo']),
            ('Repuesto Tapa Comedero Tolva 140 LT', 'Tapa de repuesto para comedero tolva de 140 litros. Protege alimento de humedad y polvo.', 'img/productos/repuestos/repuesto-comedero/2.png', ['Plástico alta resistencia', 'Compatible tolva 140 L', 'Protege de humedad y suciedad', 'Resistente a intemperie', 'Uso continuo granjas', 'Fácil reemplazo']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(rep_comedero, 1):
            Producto.objects.update_or_create(
                slug=f'rep-comedero-{i}',
                defaults={
                    'categoria': cat_repuestos,
                    'subcategoria': sub_rep_comedero,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # Subcategoría: Repuesto Automatización
        sub_rep_auto, _ = Subcategoria.objects.update_or_create(
            categoria=cat_repuestos,
            nombre='Repuesto para Automatización',
            defaults={'orden': 2}
        )

        rep_auto = [
            ('Boca Descarga 60 mm y 75 mm', 'Bocas de descarga en plástico para tubería de 60mm y 75mm.', 'img/productos/repuestos/repuesto-automatizacion/3.png', ['Plástico alta resistencia', '60 mm y 75 mm', 'Resistente a desgaste', 'Fácil instalación', 'Compatible sistemas automáticos', 'Alta durabilidad']),
            ('Acople en Y para Doble Bajante', 'Acople en Y para distribuir alimento desde una línea hacia dos bajantes.', 'img/productos/repuestos/repuesto-automatizacion/4.png', ['Plástico alta resistencia', 'Diseño en Y doble bajante', 'Distribución uniforme', 'Compatible sistemas automáticos', 'Resistente a humedad', 'Fácil reemplazo']),
            ('Cajetín de 60 mm', 'Cajetín inoxidable para recibir y conducir alimento a línea de transporte de 60mm.', 'img/productos/repuestos/repuesto-automatizacion/5.png', ['Acero inoxidable', 'Diámetro: 60 mm', 'Salida sencilla', 'Alta resistencia corrosión', 'Fácil limpieza', 'Uso continuo']),
            ('Eslabón para Empate de Cadena', 'Eslabón galvanizado para unir o empatar cadena de transporte de alimento.', 'img/productos/repuestos/repuesto-automatizacion/6.png', ['Acero galvanizado', 'Empate o unión de cadena', 'Resistente a desgaste', 'Fácil instalación', 'Compatible sistemas automáticos', 'Alta durabilidad']),
            ('Corner para Sistemas de Alimentación', 'Corner de repuesto en acero inoxidable o plástico azul para guiar cadena en cambios de dirección.', 'img/productos/repuestos/repuesto-automatizacion/7.png', ['Acero inoxidable o plástico azul', 'Guía cadena en cambios dirección', 'Reduce desgaste', 'Resistente a corrosión', 'Fácil instalación', 'Uso continuo']),
            ('Bajante para Sistema de Alimentación', 'Bajante galvanizado para conducir alimento desde línea de transporte hasta puntos de descarga.', 'img/productos/repuestos/repuesto-automatizacion/8.png', ['Acero galvanizado', 'Ángulo descarga eficiente', 'Flujo uniforme', 'Fácil instalación', 'Larga vida útil', 'Resistente corrosión']),
            ('Cajetín de 75 mm con Rasera', 'Cajetín inoxidable con rasera de cierre para controlar paso de alimento a línea de 75mm.', 'img/productos/repuestos/repuesto-automatizacion/9.png', ['Acero inoxidable', 'Diámetro: 75 mm', 'Rasera cierre manual', 'Alta resistencia corrosión', 'Fácil limpieza', 'Operación segura']),
            ('Eje Giratorio para Sinfín', 'Eje giratorio para transmitir movimiento al sistema de sinfín.', 'img/productos/repuestos/repuesto-automatizacion/10.png', ['Materiales alta resistencia', 'Transmisión eficiente', 'Resistente a desgaste', 'Fácil instalación', 'Compatible con sinfín', 'Uso continuo']),
            ('Dosificador Verde y Rojo 6 LT', 'Dosificador en polipropileno 100% con cubo transparente y bola de control de cantidad.', 'img/productos/repuestos/repuesto-automatizacion/11.png', ['Polipropileno 100%', 'Capacidad: 6 LT', 'Cubo transparente', 'Bola control cantidad', 'Automatiza transporte alimento', 'Ahorra mano de obra']),
            ('Dosificador 8 LT', 'Dosificador en polipropileno 100% con cubo transparente y bola de control de cantidad.', 'img/productos/repuestos/repuesto-automatizacion/12.png', ['Polipropileno 100%', 'Capacidad: 8 LT', 'Cubo transparente', 'Bola control cantidad', 'Automatiza transporte alimento', 'Ahorra mano de obra']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(rep_auto, 3):
            Producto.objects.update_or_create(
                slug=f'rep-auto-{i}',
                defaults={
                    'categoria': cat_repuestos,
                    'subcategoria': sub_rep_auto,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # Subcategoría: Motor y Reductores
        sub_motores, _ = Subcategoria.objects.update_or_create(
            categoria=cat_repuestos,
            nombre='Motor y Reductores',
            defaults={'orden': 3}
        )

        motores = [
            ('Motorreductor para Alimentación por Espiral', 'Motorreductor para sistemas de alimentación por espiral (sinfín). Relación 5:1, motor 2HP.', 'img/productos/repuestos/motor-reductores/13.png', ['Relación reducción 5:1', 'Motor monofásico 2 HP', '1,800 RPM', 'Carcasa aluminio', 'Bajo mantenimiento', 'Compatible con espiral']),
            ('Motorreductor para Sistema de Cadena', 'Motorreductor para sistemas de alimentación por cadena. Relación 20:1, alto torque.', 'img/productos/repuestos/motor-reductores/14.png', ['Motor monofásico 2 HP', '1,800 RPM', 'Caja reductora 20:1', 'Alto torque', 'Carcasa alta resistencia', 'Compatible con cadena']),
            ('Caja Prereductora + Motor para Sinfín', 'Conjunto caja prereductora y motor para sinfín de 30m y 60m.', 'img/productos/repuestos/motor-reductores/15.png', ['Para sinfín 30m y 60m', 'Caja prereductora alto torque', 'Motor alto rendimiento', 'Transmisión eficiente', 'Bajo mantenimiento', 'Trabajo continuo']),
            ('Caja Reductora NMRV 130', 'Caja reductora NMRV 130 para agitadores de estiércol. Relación 40:1.', 'img/productos/repuestos/motor-reductores/16.png', ['Modelo NMRV 130', 'Relación 40:1', 'Eje 35 mm', 'Alto torque', 'Trabajo pesado', 'Bajo mantenimiento']),
            ('Motor para Agitador de Estiércol', 'Motor monofásico 3HP para agitadores de estiércol. 1,750 RPM.', 'img/productos/repuestos/motor-reductores/17.png', ['Potencia 3 HP', 'Motor monofásico', '1,750 RPM', 'Carcasa aluminio', 'Trabajo continuo', 'Bajo mantenimiento']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(motores, 13):
            Producto.objects.update_or_create(
                slug=f'motor-{i}',
                defaults={
                    'categoria': cat_repuestos,
                    'subcategoria': sub_motores,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # Subcategoría: Tornillería
        sub_tornilleria, _ = Subcategoria.objects.update_or_create(
            categoria=cat_repuestos,
            nombre='Tornillería y Accesorios',
            defaults={'orden': 4}
        )

        tornilleria = [
            ('Tornillería para Instalación', 'Línea de tornillería: grilletes, tornillos autoperforantes, cáncamos y chazos de expansión.', 'img/productos/repuestos/tornilleria/18.png', ['Acero alta resistencia', 'Diferentes medidas', 'Grilletes, tornillos, cáncamos', 'Resistente a corrosión', 'Fácil instalación', 'Montaje equipos y estructuras']),
            ('Guaya Acerada 3/16"', 'Guaya acerada de 3/16" para suspensión, soporte y fijación en sistemas porcícolas.', 'img/productos/repuestos/tornilleria/19.png', ['Diámetro: 3/16"', 'Acero alta resistencia', 'Alta resistencia tracción', 'Resistente a corrosión', 'Flexible', 'Sistemas suspensión']),
            ('Resorte Galvanizado 20 cm', 'Resorte galvanizado de 20cm para tensión y absorción de movimiento en suspensión.', 'img/productos/repuestos/tornilleria/20.png', ['Longitud: 20 cm', 'Acero galvanizado', 'Alta resistencia tensión', 'Resistente corrosión', 'Fácil instalación', 'Sistemas suspensión']),
            ('Poleas Metálicas 3" y 7/8"', 'Poleas metálicas para desplazamiento de guayas y cables en sistemas de suspensión.', 'img/productos/repuestos/tornilleria/21.png', ['3" y 7/8"', 'Acero galvanizado', 'Giro suave', 'Resistente corrosión', 'Fácil instalación', 'Sistemas elevación']),
            ('Malacates de Diferente Capacidad', 'Malacates manuales de 1,600 lb y 2,000 lb para izaje y tensionado de cargas.', 'img/productos/repuestos/tornilleria/22.png', ['1,600 lb y 2,000 lb', 'Acero alta resistencia', 'Engranajes suaves', 'Guaya acero', 'Fácil operación', 'Sistemas elevación']),
            ('Base para Malacate', 'Base metálica reforzada para instalación y fijación segura de malacates.', 'img/productos/repuestos/tornilleria/23.png', ['Acero alta resistencia', 'Diseño reforzado', 'Múltiples perforaciones', 'Resistente corrosión', 'Fácil montaje', 'Compatible varios malacates']),
            ('Rollo de Piola', 'Rollo de piola de alta resistencia para amarre, suspensión y sujeción.', 'img/productos/repuestos/tornilleria/24.png', ['Alta resistencia', 'Resistente a tensión', 'Flexible', 'Resistente a humedad', 'Presentación por rollo', 'Amarre y suspensión']),
            ('Cortina Laminada Importada', 'Cortina laminada en azul y amarillo para control ambiental en galpones porcícolas.', 'img/productos/repuestos/tornilleria/25.png', ['Azul y amarillo', 'Lona laminada alta resistencia', 'Resistente UV y desgarros', 'Flexible', 'Larga vida útil', 'Control ambiental']),
            ('Malla Hexagonal Plastificada', 'Malla hexagonal plastificada para cerramiento y protección de instalaciones agropecuarias.', 'img/productos/repuestos/tornilleria/26.png', ['Diferentes medidas', 'Alambre galvanizado plastificado', 'Resistente UV', 'Flexible', 'Larga vida útil', 'Cerramientos y divisiones']),
            ('Arrancador Eléctrico', 'Arrancador eléctrico para protección de motores en sistemas de alimentación y ventilación.', 'img/productos/repuestos/tornilleria/27.png', ['Protección sobrecargas', 'Arranque seguro', 'Alta calidad componentes', 'Fácil instalación', 'Compatible varias potencias', 'Sistemas automáticos']),
            ('Tubo Galvanizado con Rosca para Cortina', 'Tubo galvanizado con rosca para instalación de sistemas de cortinas en galpones.', 'img/productos/repuestos/tornilleria/28.png', ['Acero galvanizado', 'Extremos con rosca', 'Resistente corrosión', 'Alta durabilidad', 'Fácil instalación', 'Sistemas cortinas']),
            ('Tuberías para Sistemas de Alimentación', 'Tuberías en galvanizado (sinfín) y PVC (cadena) para transporte de alimento. Longitud 6m.', 'img/productos/repuestos/tornilleria/29.png', ['Galvanizado y PVC', 'Longitud: 6 m', 'Resistente a desgaste', 'Compatible sistemas automáticos', 'Galvanizado para sinfín', 'PVC para cadena']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(tornilleria, 18):
            Producto.objects.update_or_create(
                slug=f'tornilleria-{i}',
                defaults={
                    'categoria': cat_repuestos,
                    'subcategoria': sub_tornilleria,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        # ============================================
        # CATEGORÍA 5: EQUIPOS COMPLEMENTARIOS
        # ============================================
        cat_complementarios, _ = Categoria.objects.update_or_create(
            slug='complementarios',
            defaults={
                'nombre': 'Equipos Complementarios',
                'descripcion': 'Cortinas, mallas antiaves, agitadores, elevadores, básculas, repuestos y accesorios.',
                'descripcion_corta': 'Criadoras, lámparas, bombillas infrarrojas, tejas termoacústicas y más.',
                'icono': 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10',
                'orden': 5,
            }
        )

        sub_complementarios, _ = Subcategoria.objects.update_or_create(
            categoria=cat_complementarios,
            nombre='Equipos Complementarios',
            defaults={'orden': 1}
        )

        complementarios = [
            ('Criadora para Lechones', 'Proporciona ambiente cálido y seguro durante primeras etapas de vida. Reduce estrés y mortalidad neonatal.', 'img/productos/complementarios/1.png', ['Temperatura óptima para lechones', 'Reduce mortalidad neonatal', 'Materiales resistentes', 'Fácil limpieza', 'Facilita instalación', 'Ideal maternidad']),
            ('Panel Arreador', 'Panel en plástico de alta resistencia para manejo y desplazamiento seguro de cerdos. Medidas 121×76×3cm.', 'img/productos/complementarios/2.png', ['121×76×3 cm', 'Plástico alta resistencia', 'Liviano y fácil manipulación', 'Resistente a humedad', 'Diseño ergonómico', 'Múltiples puntos agarre']),
            ('Carrillo de Mortalidad', 'Carrillo en tubo galvanizado con malacate 400kg y llantas antipinchazos para retiro seguro de animales.', 'img/productos/complementarios/3.png', ['Capacidad: 400 kg', 'Tubo galvanizado', 'Malacate manual + guaya', 'Llantas antipinchazos', 'Resistente corrosión', 'Mejora bioseguridad']),
            ('Prueba de Detección Temprana de Preñez', 'Prueba rápida para confirmar estado reproductivo en vacas y cerdas. Resultado en 5 minutos.', 'img/productos/prueba-preñez.png', ['Resultado en 5 minutos', 'Alta precisión', 'Para vacas y cerdas', 'Detección temprana', 'Fácil de usar', 'Optimiza gestión reproductiva']),
            ('Tejas Termoacústicas', 'Tejas con aislamiento térmico y acústico. Disponibles en cresta alta y cresta baja.', 'img/productos/complementarios/5.png', ['Aislamiento térmico y acústico', 'Cresta alta y baja', 'Ancho: 1.075-1.13 m', 'Espesor: 2-2.5 mm', 'Resistente humedad', 'Bajo mantenimiento']),
            ('Caballete Termoacústico', 'Complemento para cumbrera del techo. Mantiene continuidad del aislamiento.', 'img/productos/complementarios/6.png', ['Acabado profesional', 'Continuidad aislamiento', 'Resistente intemperie', 'Fácil instalación', 'Alta durabilidad', 'Compatible cresta alta/baja']),
            ('Lámpara de Calefacción para Parideras', 'Lámpara con reflector de aluminio para calor uniforme en lechones recién nacidos.', 'img/productos/complementarios/7.png', ['Calor uniforme', 'Reflector aluminio', 'Rejilla protección', 'Fácil instalación', 'Materiales resistentes', 'Ideal maternidad']),
            ('Lámpara de Calefacción para Precebo', 'Lámpara con reflector de aluminio para mantener temperatura en etapa de precebo.', 'img/productos/complementarios/8.png', ['Calor uniforme y eficiente', 'Reflector aluminio', 'Rejilla protección', 'Bajo consumo energía', 'Materiales resistentes', 'Compatible infrarrojos']),
            ('Bombilla Infrarroja Paridera 175W', 'Bombilla infrarroja 175W/110V para calefacción de nidos y parideras porcinas.', 'img/productos/complementarios/9.png', ['175W, 110V', 'Rosca E27', 'Vidrio templado', 'Calor constante', 'Reduce hipotermia', 'Fácil instalación']),
            ('Bombilla Infrarroja Precebo 250W', 'Bombilla infrarroja 250W/220V para calefacción en corrales de precebo.', 'img/productos/complementarios/10.png', ['250W, 220V', 'Rosca E27', 'Vidrio templado', 'Calor uniforme', 'Bajo mantenimiento', 'Compatible campanas']),
        ]

        for i, (nombre, desc, imagen, features) in enumerate(complementarios, 1):
            Producto.objects.update_or_create(
                slug=f'complementario-{i}',
                defaults={
                    'categoria': cat_complementarios,
                    'subcategoria': sub_complementarios,
                    'nombre': nombre,
                    'descripcion_corta': desc,
                    'imagen': imagen,
                    'caracteristicas': features,
                    'orden': i,
                }
            )

        total_categorias = Categoria.objects.count()
        total_subcategorias = Subcategoria.objects.count()
        total_productos = Producto.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'¡Listo! {total_categorias} categorías, {total_subcategorias} subcategorías, {total_productos} productos creados.'
        ))
