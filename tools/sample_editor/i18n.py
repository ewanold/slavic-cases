"""Runtime gettext; .po sources and compiled .mo catalogs live beside the editor."""
import gettext
import locale
import os
from pathlib import Path

LOCALES = Path(__file__).with_name('locales')
_translations = gettext.NullTranslations()


def configure(language=None):
    global _translations
    languages = [language] if language else None
    if not language and not any(os.environ.get(k) for k in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG')):
        code = locale.getlocale()[0]
        languages = [code] if code else ['en']
    _translations = gettext.translation('sample-editor', LOCALES, languages=languages, fallback=True)


def _(message):
    return _translations.gettext(message)


def language():
    return _translations.info().get('language', 'en').split('_')[0].split('-')[0]
