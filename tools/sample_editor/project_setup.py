"""Project setup defaults shared by both desktop views."""
from i18n import _, language

CASE_IDS = ('nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'prepositional', 'locative', 'vocative')
PRESETS = {
    'ru': {'name': 'Русский', 'cases': dict(zip(
        ('nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'prepositional'),
        ('Именительный', 'Родительный', 'Дательный', 'Винительный', 'Творительный', 'Предложный')))},
    'pl': {'name': 'Polski', 'cases': dict(zip(
        ('nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative', 'vocative'),
        ('Mianownik', 'Dopełniacz', 'Celownik', 'Biernik', 'Narzędnik', 'Miejscownik', 'Wołacz')))},
    'de': {'name': 'Deutsch', 'cases': dict(zip(
        ('nominative', 'genitive', 'dative', 'accusative'), ('Nominativ', 'Genitiv', 'Dativ', 'Akkusativ')))},
}


def languages():
    return [('ru', _('Russian')), ('pl', _('Polish')), ('de', _('German')), ('other', _('Other language'))]


def defaults(code):
    locale = language()
    native = locale if locale in ('en', 'de', 'ru', 'pl') and locale != code else ('de' if code == 'en' else 'en')
    return {'cases': list(PRESETS.get(code, {}).get('cases', {})), 'native_languages': [native]}
