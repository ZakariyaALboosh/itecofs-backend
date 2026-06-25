import base64
import html
import json
import logging
import urllib.error
import urllib.request
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)

BREVO_ENDPOINT = 'https://api.brevo.com/v3/smtp/email'

SUPPLIER_FILE_FIELDS = [
    ('CR Certificate', 'cr_certificate'),
    ('Organisation Chart', 'organisation_chart'),
    ('Company Profile', 'company_profile'),
    ('Tax Registration Certificate', 'tax_registration_certificate'),
    ('VAT Registration Certificate', 'vat_registration_certificate'),
    ('ISO 9001 Certificate', 'iso9001_certificate'),
    ('ISO 14001 Certificate', 'iso14001_certificate'),
    ('ISO 45001 Certificate', 'iso45001_certificate'),
    ('API Q1 Certificate', 'apiq1_certificate'),
    ('API Q2 Certificate', 'apiq2_certificate'),
]

SUPPLIER_SECTIONS = [
    ('Company Profile', [
        ('Vendor Name', 'vendor_name'),
        ('Country of Registration', 'country'),
        ('CR Number', 'cr_number'),
        ('Year of Establishment', 'est_year'),
        ('Supplier Type', 'supplier_type'),
        ('Headquarters Address', 'hq_address'),
        ('Operates / Supplies to Libya', 'operates_libya'),
    ]),
    ('Supplier Focal Point', [
        ('Full Name', 'fp_name'),
        ('Position / Title', 'fp_position'),
        ('Phone Number', 'fp_phone'),
        ('Email Address', 'fp_email'),
    ]),
    ('Bank Details', [
        ('Bank Name', 'bank_name'),
        ('Account Name', 'account_name'),
        ('Account Number / IBAN', 'iban'),
        ('Swift / BIC Code', 'swift'),
        ('Branch Name', 'branch_name'),
        ('Branch Address', 'branch_address'),
        ('Currency', 'currency'),
    ]),
    ('Products & Services', [
        ('Registration Type', 'registration_type'),
        ('Product Types / Segments', 'product_types'),
        ('Warranty Terms', 'warranty_terms'),
        ('After-sales Support', 'support_info'),
    ]),
    ('Quality, HSE & Compliance', [
        ('Certifications', 'certs'),
    ]),
    ('Logistics', [
        ('Lead Time', 'lead_time'),
        ('Export Ports', 'export_ports'),
        ('Main Logistics Office Address', 'logistics_address'),
    ]),
    ('Declaration & Submission', [
        ('Accepted Declaration', 'accepted'),
        ('Authorized Representative', 'representative'),
        ('Position / Title', 'position'),
        ('Email Address', 'email'),
        ('Submitted At', 'created_at'),
    ]),
]

CONTACT_FIELDS = [
    ('Name', 'name'),
    ('Email', 'email'),
    ('Phone Number', 'phone_number'),
    ('Service', 'service'),
    ('Description', 'description'),
    ('Submitted At', 'created_at'),
]


def notify_contact_submission(contact_form):
    subject = f'New Contact Form Submission - {contact_form.name}'
    html_content = _build_html_email('New Contact Form Submission', [
        ('Contact Details', _field_rows(contact_form, CONTACT_FIELDS)),
    ])
    _send_brevo_email(
        subject=subject,
        html_content=html_content,
        reply_to_email=contact_form.email,
        reply_to_name=contact_form.name,
        tags=['contact-form'],
    )


def notify_supplier_registration(registration):
    subject = f'New Supplier Registration - {registration.vendor_name}'
    sections = [
        (title, _field_rows(registration, fields))
        for title, fields in SUPPLIER_SECTIONS
    ]
    file_rows = _file_rows(registration)
    if file_rows:
        sections.append(('Uploaded Files', file_rows))

    html_content = _build_html_email('New Supplier Registration Form Submission', sections)
    _send_brevo_email(
        subject=subject,
        html_content=html_content,
        reply_to_email=registration.email or registration.fp_email,
        reply_to_name=registration.representative or registration.fp_name,
        attachments=_file_attachments(registration),
        tags=['supplier-registration'],
    )


def _send_brevo_email(subject, html_content, reply_to_email=None, reply_to_name=None, attachments=None, tags=None):
    api_key = getattr(settings, 'BREVO_API_KEY', '')
    if not api_key:
        logger.warning('BREVO_API_KEY is not configured; skipping Brevo email for %s', subject)
        return

    payload = {
        'sender': {
            'email': settings.BREVO_SENDER_EMAIL,
            'name': settings.BREVO_SENDER_NAME,
        },
        'to': [{'email': settings.CLIENT_INBOX_EMAIL, 'name': settings.CLIENT_INBOX_NAME}],
        'subject': subject,
        'htmlContent': html_content,
        'tags': tags or [],
    }
    if reply_to_email:
        payload['replyTo'] = {'email': reply_to_email, 'name': reply_to_name or reply_to_email}
    if attachments:
        payload['attachment'] = attachments

    request = urllib.request.Request(
        BREVO_ENDPOINT,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'api-key': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(request, timeout=settings.BREVO_TIMEOUT_SECONDS) as response:
            logger.info('Brevo email sent for %s with status %s', subject, response.status)
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode('utf-8', errors='replace')
        logger.exception('Brevo rejected email for %s: %s %s', subject, exc.code, error_body)
    except urllib.error.URLError:
        logger.exception('Brevo email request failed for %s', subject)
    except TimeoutError:
        logger.exception('Brevo email request timed out for %s', subject)


def _build_html_email(title, sections):
    section_html = ''.join(
        f'<h2>{html.escape(section_title)}</h2><table>{rows}</table>'
        for section_title, rows in sections
    )
    return f'''
<html>
  <body>
    <h1>{html.escape(title)}</h1>
    {section_html}
  </body>
</html>
'''


def _field_rows(instance, fields):
    return ''.join(
        f'<tr><th>{html.escape(label)}</th><td>{html.escape(_stringify_value(getattr(instance, field_name, "")))}</td></tr>'
        for label, field_name in fields
    )


def _file_rows(instance):
    rows = []
    for label, field_name in SUPPLIER_FILE_FIELDS:
        file_field = getattr(instance, field_name, None)
        if file_field:
            rows.append((label, file_field.name))
    return ''.join(
        f'<tr><th>{html.escape(label)}</th><td>{html.escape(file_name)}</td></tr>'
        for label, file_name in rows
    )


def _file_attachments(instance):
    attachments = []
    for label, field_name in SUPPLIER_FILE_FIELDS:
        file_field = getattr(instance, field_name, None)
        if not file_field:
            continue
        try:
            file_field.open('rb')
            content = base64.b64encode(file_field.read()).decode('ascii')
        except OSError:
            logger.exception('Could not read supplier registration attachment %s', file_field.name)
            continue
        finally:
            file_field.close()

        attachments.append({
            'name': Path(file_field.name).name or f'{label}.pdf',
            'content': content,
        })
    return attachments


def _stringify_value(value):
    if value is None:
        return ''
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)
