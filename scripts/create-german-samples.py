#!/usr/bin/env python3
"""Export original German starter drafts; refuses to overwrite edited YAML.
No downloads. Requires installed PyYAML. YAML becomes authoritative after export.
Usage: python3 scripts/create-german-samples.py --output samples
Paradigms and sentence frames below are authored explicitly, not guessed suffixes.
"""
import argparse
from pathlib import Path
import yaml

CASES = ['nominative', 'genitive', 'dative', 'accusative']
NAMES = ['Nominativ', 'Genitiv', 'Dativ', 'Akkusativ']
REFERENCES = ('Original AI-assisted sentences, MIT; grammar checked against IDS grammis: '
              'https://grammis.ids-mannheim.de/progr@mm/6915 ; '
              'https://grammis.ids-mannheim.de/fragen/28 ; '
              'https://grammis.ids-mannheim.de/progr@mm/6751 ; '
              'https://grammis.ids-mannheim.de/progr@mm/6752 . No source exercises copied.')
# lemma, gender, number, animacy, N|G|D|A phrases, deliberately invalid fallback,
# German N|G|D|A frames, English N|G|D|A sentences.
NOUNS = [
('Mann','masculine','singular','animate','der Mann|des Mannes|dem Mann|den Mann','die Mann',
 '___ wartet hier.|Das ist die Tasche ___.|Ich helfe ___.|Ich sehe ___.',
 'The man waits here.|This is the man’s bag.|I help the man.|I see the man.'),
('Frau','feminine','singular','animate','die Frau|der Frau|der Frau|die Frau','dem Frau',
 '___ liest.|Das ist die Tasche ___.|Ich helfe ___.|Ich besuche ___.',
 'The woman reads.|This is the woman’s bag.|I help the woman.|I visit the woman.'),
('Kind','neuter','singular','animate','das Kind|des Kindes|dem Kind|das Kind','den Kind',
 '___ spielt.|Das ist das Spielzeug ___.|Ich helfe ___.|Ich sehe ___.',
 'The child plays.|This is the child’s toy.|I help the child.|I see the child.'),
('Lehrer','masculine','singular','animate','der Lehrer|des Lehrers|dem Lehrer|den Lehrer','die Lehrer',
 '___ erklärt die Aufgabe.|Das ist das Buch ___.|Ich antworte ___.|Ich frage ___.',
 'The male teacher explains the task.|This is the male teacher’s book.|I answer the male teacher.|I ask the male teacher.'),
('Ärztin','feminine','singular','animate','die Ärztin|der Ärztin|der Ärztin|die Ärztin','dem Ärztin',
 '___ hilft mir.|Das ist die Praxis ___.|Ich danke ___.|Ich besuche ___.',
 'The female doctor helps me.|This is the female doctor’s practice.|I thank the female doctor.|I visit the female doctor.'),
('Bruder','masculine','singular','animate','der Bruder|des Bruders|dem Bruder|den Bruder','das Bruder',
 '___ kocht.|Das ist das Fahrrad ___.|Ich helfe ___.|Ich besuche ___.',
 'The brother cooks.|This is the brother’s bicycle.|I help the brother.|I visit the brother.'),
('Schwester','feminine','singular','animate','die Schwester|der Schwester|der Schwester|die Schwester','dem Schwester',
 '___ singt.|Das ist die Jacke ___.|Ich danke ___.|Ich sehe ___.',
 'The sister sings.|This is the sister’s jacket.|I thank the sister.|I see the sister.'),
('Freund','masculine','singular','animate','der Freund|des Freundes|dem Freund|den Freund','das Freund',
 '___ kommt heute.|Das ist die Wohnung ___.|Ich vertraue ___.|Ich besuche ___.',
 'The male friend comes today.|This is the male friend’s apartment.|I trust the male friend.|I visit the male friend.'),
('Student','masculine','singular','animate','der Student|des Studenten|dem Studenten|den Studenten','dem Student',
 '___ lernt.|Das ist das Heft ___.|Ich helfe ___.|Ich sehe ___.',
 'The male student studies.|This is the male student’s notebook.|I help the male student.|I see the male student.'),
('Nachbar','masculine','singular','animate','der Nachbar|des Nachbarn|dem Nachbarn|den Nachbarn','das Nachbar',
 '___ grüßt mich.|Das ist der Garten ___.|Ich antworte ___.|Ich besuche ___.',
 'The male neighbour greets me.|This is the male neighbour’s garden.|I answer the male neighbour.|I visit the male neighbour.'),
('Vater','masculine','singular','animate','der Vater|des Vaters|dem Vater|den Vater','das Vater',
 '___ arbeitet.|Das ist das Auto ___.|Ich helfe ___.|Ich sehe ___.',
 'The father works.|This is the father’s car.|I help the father.|I see the father.'),
('Mutter','feminine','singular','animate','die Mutter|der Mutter|der Mutter|die Mutter','dem Mutter',
 '___ lacht.|Das ist die Tasche ___.|Ich danke ___.|Ich besuche ___.',
 'The mother laughs.|This is the mother’s bag.|I thank the mother.|I visit the mother.'),
('Buch','neuter','singular','inanimate','das Buch|des Buches|dem Buch|das Buch','den Buch',
 '___ liegt hier.|Das ist der Titel ___.|Ich arbeite mit ___.|Ich lese ___.',
 'The book lies here.|This is the title of the book.|I work with the book.|I read the book.'),
('Hund','masculine','singular','animate','der Hund|des Hundes|dem Hund|den Hund','das Hund',
 '___ schläft.|Das ist der Name ___.|Ich spiele mit ___.|Ich sehe ___.',
 'The dog sleeps.|This is the dog’s name.|I play with the dog.|I see the dog.'),
('Kind','neuter','plural','animate','die Kinder|der Kinder|den Kindern|die Kinder','dem Kinder',
 '___ spielen.|Das sind die Spielsachen ___.|Ich spiele mit ___.|Ich sehe ___.',
 'The children play.|These are the children’s toys.|I play with the children.|I see the children.'),
]
# kind, neutral cue, gender, number, declension, N|G|D|A, wrong fallback, DE/EN frames
ADJECTIVES = [
('adjective','bestimmter Artikel; gut; Freund','masculine','singular','weak',
 'der gute Freund|des guten Freundes|dem guten Freund|den guten Freund','dem guter Freund',
 '___ kommt.|Das ist die Tasche ___.|Ich helfe ___.|Ich sehe ___.',
 'The good male friend comes.|This is the good male friend’s bag.|I help the good male friend.|I see the good male friend.'),
('adjective','bestimmter Artikel; freundlich; Nachbarin','feminine','singular','weak',
 'die freundliche Nachbarin|der freundlichen Nachbarin|der freundlichen Nachbarin|die freundliche Nachbarin','dem freundlichen Nachbarin',
 '___ grüßt mich.|Das ist der Garten ___.|Ich danke ___.|Ich besuche ___.',
 'The friendly female neighbour greets me.|This is the friendly female neighbour’s garden.|I thank the friendly female neighbour.|I visit the friendly female neighbour.'),
('adjective','bestimmter Artikel; klein; Kind','neuter','singular','weak',
 'das kleine Kind|des kleinen Kindes|dem kleinen Kind|das kleine Kind','dem kleine Kind',
 '___ spielt.|Das ist das Spielzeug ___.|Ich helfe ___.|Ich sehe ___.',
 'The small child plays.|This is the small child’s toy.|I help the small child.|I see the small child.'),
('adjective','bestimmter Artikel; neu; Buch','neuter','plural','weak',
 'die neuen Bücher|der neuen Bücher|den neuen Büchern|die neuen Bücher','den neuen Bücher',
 '___ liegen hier.|Die Einbände ___ sind blau.|Ich arbeite mit ___.|Ich lese ___.',
 'The new books lie here.|The covers of the new books are blue.|I work with the new books.|I read the new books.'),
('adjective','unbestimmter Artikel; jung; Lehrer','masculine','singular','mixed',
 'ein junger Lehrer|eines jungen Lehrers|einem jungen Lehrer|einen jungen Lehrer','einem junger Lehrer',
 '___ kommt.|Das ist das Buch ___.|Ich helfe ___.|Ich sehe ___.',
 'A young male teacher comes.|This is a young male teacher’s book.|I help a young male teacher.|I see a young male teacher.'),
('adjective','unbestimmter Artikel; erfahren; Ärztin','feminine','singular','mixed',
 'eine erfahrene Ärztin|einer erfahrenen Ärztin|einer erfahrenen Ärztin|eine erfahrene Ärztin','einem erfahrenen Ärztin',
 '___ hilft mir.|Das ist die Praxis ___.|Ich danke ___.|Ich besuche ___.',
 'An experienced female doctor helps me.|This is an experienced female doctor’s practice.|I thank an experienced female doctor.|I visit an experienced female doctor.'),
('adjective','unbestimmter Artikel; schön; Haus','neuter','singular','mixed',
 'ein schönes Haus|eines schönen Hauses|einem schönen Haus|ein schönes Haus','einem schönes Haus',
 '___ steht hier.|Das ist die Tür ___.|Ich wohne in ___.|Ich sehe ___.',
 'A beautiful house stands here.|This is the door of a beautiful house.|I live in a beautiful house.|I see a beautiful house.'),
('adjective','ohne Artikel; frisch; Tee','masculine','singular','strong',
 'frischer Tee|frischen Tees|frischem Tee|frischen Tee','frischer Tees',
 '___ steht auf dem Tisch.|Der Duft ___ ist angenehm.|Ich beginne mit ___.|Ich trinke ___.',
 'Fresh tea is on the table.|The aroma of fresh tea is pleasant.|I begin with fresh tea.|I drink fresh tea.'),
('adjective','ohne Artikel; warm; Suppe','feminine','singular','strong',
 'warme Suppe|warmer Suppe|warmer Suppe|warme Suppe','warmen Suppe',
 '___ steht bereit.|Der Duft ___ zieht durch die Küche.|Ich beginne mit ___.|Ich esse ___.',
 'Warm soup is ready.|The aroma of warm soup wafts through the kitchen.|I begin with warm soup.|I eat warm soup.'),
('adjective','ohne Artikel; kalt; Wasser','neuter','singular','strong',
 'kaltes Wasser|kalten Wassers|kaltem Wasser|kaltes Wasser','kaltem Wassers',
 '___ ist erfrischend.|Die Temperatur ___ ist niedrig.|Ich wasche mich mit ___.|Ich trinke ___.',
 'Cold water is refreshing.|The temperature of cold water is low.|I wash with cold water.|I drink cold water.'),
('cardinal_numeral','ein; Buch','neuter','singular','numeral',
 'ein Buch|eines Buches|einem Buch|ein Buch','einen Buch',
 '___ liegt hier.|Das ist der Titel ___.|Ich arbeite mit ___.|Ich lese ___.',
 'One book lies here.|This is the title of one book.|I work with one book.|I read one book.'),
('cardinal_numeral','zwei; Kind','neuter','plural','numeral',
 'zwei Kinder|zweier Kinder|zwei Kindern|zwei Kinder','zweien Kinder',
 '___ spielen.|Das sind die Spielsachen ___.|Ich spiele mit ___.|Ich sehe ___.',
 'Two children play.|These are the toys of two children.|I play with two children.|I see two children.'),
('cardinal_numeral','fünf; Buch; bestimmter Artikel','neuter','plural','numeral',
 'die fünf Bücher|der fünf Bücher|den fünf Büchern|die fünf Bücher','den fünf Bücher',
 '___ liegen hier.|Die Titel ___ stehen auf der Liste.|Ich arbeite mit ___.|Ich lese ___.',
 'The five books lie here.|The titles of the five books are on the list.|I work with the five books.|I read the five books.'),
('ordinal_numeral','bestimmter Artikel; erst; Zug','masculine','singular','weak',
 'der erste Zug|des ersten Zuges|dem ersten Zug|den ersten Zug','dem erste Zug',
 '___ kommt.|Das ist die Nummer ___.|Ich fahre mit ___.|Ich nehme ___.',
 'The first train arrives.|This is the number of the first train.|I travel on the first train.|I take the first train.'),
('ordinal_numeral','bestimmter Artikel; zweit; Lektion','feminine','singular','weak',
 'die zweite Lektion|der zweiten Lektion|der zweiten Lektion|die zweite Lektion','dem zweiten Lektion',
 '___ beginnt.|Das ist der Titel ___.|Ich beginne mit ___.|Ich wiederhole ___.',
 'The second lesson begins.|This is the title of the second lesson.|I begin with the second lesson.|I repeat the second lesson.'),
]

def choices(forms, correct, fallback, offset):
    wrong = list(dict.fromkeys(x for x in forms + [fallback] if x != correct))
    # German syncretism is intentional: never manufacture duplicate answer labels.
    # Add an explicit wrong ending when fewer than three distinct wrong forms exist.
    if len(wrong) < 3:
        extra = {
            'dem Frau': 'des Frau', 'dem Ärztin': 'des Ärztin',
            'dem Schwester': 'des Schwester', 'dem Mutter': 'des Mutter',
            'dem freundlichen Nachbarin': 'des freundlichen Nachbarin',
            'einem erfahrenen Ärztin': 'eines erfahrenen Ärztin',
            'warmen Suppe': 'warmes Suppe', 'den fünf Bücher': 'dem fünf Büchern',
            'dem zweiten Lektion': 'des zweiten Lektion',
        }
        wrong.append(extra[fallback])
    answers = wrong[:3]
    answers.insert(offset % 4, correct)
    assert len(set(answers)) == 4
    return dict(zip('abcd', answers)), 'abcd'[offset % 4]

def build():
    docs = {'language.yaml': dict(schema_version=1, learning_language='de', name='German simple',
        names={'en':'German simple', 'de':'Deutsch einfach'},
        native_languages=['en','de'], tracks=['nouns','adjectives'],
        cases=[dict(id=c, name=n) for c,n in zip(CASES,NAMES)])}
    for ci, case in enumerate(CASES):
        for track, rows in [('nouns',NOUNS), ('adjectives',ADJECTIVES)]:
            sentences = []
            for i, row in enumerate(rows):
                if track == 'nouns':
                    lemma,gender,number,animacy,paradigm,fallback,de,en = row
                    kind,declension = 'noun','noun'
                    cue = f'bestimmter Artikel; {lemma}'
                else:
                    kind,cue,gender,number,declension,paradigm,fallback,de,en = row
                    lemma = cue.split(';')[1].strip() if ';' in cue else cue
                    if kind == 'cardinal_numeral':
                        lemma = cue.split(';')[0]
                    animacy = 'animate' if any(n in cue for n in ['Freund','Nachbarin','Kind','Lehrer','Ärztin']) else 'inanimate'
                cue += '; ' + {'masculine':'maskulin', 'feminine':'feminin', 'neuter':'neutrum'}[gender]
                cue += '; ' + ('Plural' if number == 'plural' else 'Singular')
                forms = paradigm.split('|')
                frame = de.split('|')[ci]
                answer = forms[ci]
                options,key = choices(forms,answer,fallback,i)
                filled = frame.replace('___',answer)
                filled = filled[0].upper()+filled[1:]
                sentences.append(dict(id=f'de-{track}-{case}-{i+1:02}', word_type=kind,
                    dictionary_form=lemma, features=dict(gender=gender,number=number,animacy=animacy,
                    declension=declension), native_text=dict(en=en.split('|')[ci],de=filled),
                    neutral_prompt=f'{frame} ({cue})', answer_scope='phrase',options=options,correct=key))
            docs[f'{track}/{case}.yaml'] = dict(schema_version=1,id=f'de-{track}-{case}-starter',
                learning_language='de', track=track, case=case, native_languages=['en','de'],
                instruction=dict(en='Choose the complete noun phrase that fits the sentence and case. The cue specifies the article, gender and number.',
                    de='Wähle die vollständige Wortgruppe passend zum Satz und Fall. Die Hinweise geben Artikel, Geschlecht und Zahl an.'),
                contributor='Learn Grammatical Cases project (AI-assisted original material)',
                license='MIT', sources=REFERENCES, review_status='draft', sentences=sentences)
    return docs

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    docs=build()
    collisions=[str(args.output/'de'/name) for name in docs if (args.output/'de'/name).exists()]
    if collisions:
        parser.error('Refusing to overwrite: '+', '.join(collisions))
    for name,data in docs.items():
        path=args.output/'de'/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text('# Original German starter material; linguistic review pending.\n'+
            yaml.safe_dump(data,allow_unicode=True,sort_keys=False,width=110),encoding='utf-8')
    print('Exported 120 German draft questions in 8 case/track files.')

if __name__ == '__main__':
    main()
