"""Translate structured editor/validator errors without modifying authored data."""
from i18n import _
from vocabulary import label


def localize_error(error):
    template = getattr(error, 'template', None)
    if template is None:
        return str(error)  # Native OS/parser diagnostics retain their original detail.
    params = dict(getattr(error, 'params', {}))
    fields = {'contributor': _('Contributor'), 'license': _('License'), 'sources': _('Sources')}
    if 'field' in params:
        params['field'] = fields.get(params['field'], params['field'])
    if isinstance(params.get('track'), str):
        params['track'] = {'nouns': _('Nouns'), 'adjectives': _('Adjectives and numerals')}.get(params['track'], params['track'])
    if isinstance(params.get('details'), list):
        params['details'] = ', '.join(label(value) for value in params['details'])
    for key in ('case',):
        if isinstance(params.get(key), str):
            params[key] = label(params[key])
    message = _(template)
    return message.format(**params) if params else message
