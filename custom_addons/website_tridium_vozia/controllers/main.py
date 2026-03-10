import logging
import re

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

# Mapping of country codes used in the form to Odoo res.country codes (ISO 3166-1 alpha-2)
COUNTRY_MAP = {
    'PA': 'PA',  # Panamá
    'CO': 'CO',  # Colombia
    'MX': 'MX',  # México
    'BR': 'BR',  # Brasil
    'US': 'US',  # Estados Unidos
}


class TridiumVoziaWebsite(http.Controller):

    @http.route(
        '/website_tridium_vozia/apply',
        type='http',
        auth='public',
        methods=['POST'],
        website=True,
        csrf=True,
    )
    def apply_media_beca(self, **kwargs):
        """Handle the 'Postula Ahora' form submission and create a CRM lead."""
        name = (kwargs.get('name') or '').strip()
        email = (kwargs.get('email') or '').strip()
        phone = (kwargs.get('phone') or '').strip()
        country_code = (kwargs.get('country') or '').strip()
        level = (kwargs.get('level') or '').strip()

        # ----- Basic server-side validation -----
        if not name or not email:
            return request.redirect('/#x_tva_becas')

        # Simple email pattern check
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            return request.redirect('/#x_tva_becas')

        # ----- Resolve country_id from code -----
        country_id = False
        iso_code = COUNTRY_MAP.get(country_code)
        if iso_code:
            country = request.env['res.country'].sudo().search(
                [('code', '=', iso_code)], limit=1
            )
            if country:
                country_id = country.id

        # ----- Resolve tags -----
        tag_ids = []
        tag_beca = request.env.ref(
            'website_tridium_vozia.crm_tag_media_beca', raise_if_not_found=False
        )
        if tag_beca:
            tag_ids.append(tag_beca.id)
        tag_landing = request.env.ref(
            'website_tridium_vozia.crm_tag_landing', raise_if_not_found=False
        )
        if tag_landing:
            tag_ids.append(tag_landing.id)

        # ----- Resolve UTM source -----
        utm_source = request.env.ref(
            'website_tridium_vozia.utm_source_website_landing', raise_if_not_found=False
        )

        # ----- Build description -----
        description_parts = ['Solicitud desde landing page Tridium Vozia.']
        if level:
            description_parts.append(f'Nivel de interés: {level}')
        if country_code:
            description_parts.append(f'País seleccionado: {country_code}')
        description = '\n'.join(description_parts)

        # ----- Create CRM lead -----
        lead_vals = {
            'name': f'Media Beca — {name}',
            'contact_name': name,
            'email_from': email,
            'phone': phone or False,
            'country_id': country_id,
            'tag_ids': [(6, 0, tag_ids)],
            'description': description,
            'type': 'lead',
        }
        if utm_source:
            lead_vals['source_id'] = utm_source.id

        try:
            request.env['crm.lead'].sudo().create(lead_vals)
        except Exception:
            _logger.exception('Error creating CRM lead from Tridium Vozia landing page')
            return request.redirect('/#x_tva_becas')

        return request.render('website_tridium_vozia.apply_thanks')
