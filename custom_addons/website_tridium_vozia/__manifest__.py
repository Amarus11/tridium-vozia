{
    'name': 'Tridium Vozia Academy Website',
    'summary': 'Landing page profesional para Tridium Vozia Academy — formación lingüística integral.',
    'description': """
        Módulo website para Tridium Vozia Academy.
        - Landing page con secciones: Hero, Metodología, Media Beca, Precios, Panamá.
        - Formulario de captación de leads integrado con CRM.
        - Diseño responsive con Bootstrap 5 y SCSS custom.
        - Precios por módulo CEFR: A1–C2.
        - Preparado para futura integración con e-commerce (website_sale).
    """,
    'category': 'Website/Theme',
    'version': '19.0.1.0.0',
    'author': 'Syntropy / Skysize',
    'license': 'LGPL-3',
    'depends': [
        'website',
        'crm',
    ],
    'data': [
        'data/crm_data.xml',
        'data/pages/homepage.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'website_tridium_vozia/static/src/scss/primary_variables.scss',
        ],
        'web.assets_frontend': [
            'website_tridium_vozia/static/src/scss/theme.scss',
        ],
    },
    'images': [
        'static/description/icon.svg',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
