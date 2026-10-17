"""Explicit gettext messages for schema IDs; file contents retain canonical IDs."""
from i18n import _


def label(value):
    labels = {
        'nominative': _('Nominative'), 'genitive': _('Genitive'), 'dative': _('Dative'),
        'accusative': _('Accusative'), 'instrumental': _('Instrumental'),
        'prepositional': _('Prepositional'), 'locative': _('Locative'), 'vocative': _('Vocative'),
        'noun': _('Noun'), 'adjective': _('Adjective'), 'cardinal_numeral': _('Cardinal numeral'),
        'ordinal_numeral': _('Ordinal numeral'), 'word': _('Word'), 'phrase': _('Phrase'),
        'inflection': _('Inflection'), 'gender': _('Gender'), 'number': _('Number'),
        'animacy': _('Animacy'), 'noun_gender': _('Noun gender'), 'declension': _('Declension'),
        'plural_gender': _('Plural gender'), 'quantity': _('Quantity'),
        'noun_dictionary_form': _('Noun dictionary form'), 'singular': _('Singular'),
        'plural': _('Plural'), 'masculine': _('Masculine'), 'feminine': _('Feminine'),
        'neuter': _('Neuter'), 'animate': _('Animate'), 'inanimate': _('Inanimate'),
        'weak': _('Weak'), 'mixed': _('Mixed'), 'strong': _('Strong'), 'numeral': _('Numeral'),
        'masculine-personal': _('Masculine personal'), 'non-masculine-personal': _('Non-masculine personal'),
        'draft': _('Draft'), 'reviewed': _('Reviewed'),
    }
    return labels.get(value, value)
