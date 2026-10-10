#!/usr/bin/env python3
"""Export the original starter material. Never overwrites hand-edited files.
Requires the already available PyYAML package; no network or installation.
Usage: python3 scripts/create-starter-samples.py --output /new/empty/directory
Editable YAML, not this authoring script, is the source of truth after export.
"""
import argparse
from pathlib import Path
import yaml

CASES = ['nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'prepositional']
PL_CASES = CASES[:-1] + ['locative', 'vocative']
# Explicit hand-authored paradigms: N G D A I P/L [V], not inferred suffixes.
RU = [
('brother','m','брат брата брату брата братом брате','brother','Bruder'),
('sister','f','сестра сестры сестре сестру сестрой сестре','sister','Schwester'),
('friend-m','m','друг друга другу друга другом друге','male friend','Freund'),
('friend-f','f','подруга подруги подруге подругу подругой подруге','female friend','Freundin'),
('teacher-m','m','учитель учителя учителю учителя учителем учителе','male teacher','Lehrer'),
('teacher-f','f','учительница учительницы учительнице учительницу учительницей учительнице','female teacher','Lehrerin'),
('student-m','m','студент студента студенту студента студентом студенте','male student','Student'),
('student-f','f','студентка студентки студентке студентку студенткой студентке','female student','Studentin'),
('neighbor-m','m','сосед соседа соседу соседа соседом соседе','male neighbor','Nachbar'),
('neighbor-f','f','соседка соседки соседке соседку соседкой соседке','female neighbor','Nachbarin'),
('doctor','m','врач врача врачу врача врачом враче','doctor','Arzt'),
('mother','f','мама мамы маме маму мамой маме','mother','Mutter'),
('father','m','папа папы папе папу папой папе','father','Vater'),
('grandfather','m','дедушка дедушки дедушке дедушку дедушкой дедушке','grandfather','Großvater'),
('grandmother','f','бабушка бабушки бабушке бабушку бабушкой бабушке','grandmother','Großmutter'),
]
PL = [
('brother','m','brat brata bratu brata bratem bracie bracie','brother','Bruder'),
('sister','f','siostra siostry siostrze siostrę siostrą siostrze siostro','sister','Schwester'),
('friend-m','m','przyjaciel przyjaciela przyjacielowi przyjaciela przyjacielem przyjacielu przyjacielu','male friend','Freund'),
('friend-f','f','przyjaciółka przyjaciółki przyjaciółce przyjaciółkę przyjaciółką przyjaciółce przyjaciółko','female friend','Freundin'),
('teacher-m','m','nauczyciel nauczyciela nauczycielowi nauczyciela nauczycielem nauczycielu nauczycielu','male teacher','Lehrer'),
('teacher-f','f','nauczycielka nauczycielki nauczycielce nauczycielkę nauczycielką nauczycielce nauczycielko','female teacher','Lehrerin'),
('student-m','m','student studenta studentowi studenta studentem studencie studencie','male student','Student'),
('student-f','f','studentka studentki studentce studentkę studentką studentce studentko','female student','Studentin'),
('neighbor-m','m','sąsiad sąsiada sąsiadowi sąsiada sąsiadem sąsiedzie sąsiedzie','male neighbor','Nachbar'),
('neighbor-f','f','sąsiadka sąsiadki sąsiadce sąsiadkę sąsiadką sąsiadce sąsiadko','female neighbor','Nachbarin'),
('doctor','m','lekarz lekarza lekarzowi lekarza lekarzem lekarzu lekarzu','doctor','Arzt'),
('mother','f','mama mamy mamie mamę mamą mamie mamo','mother','Mutter'),
('father','m','tata taty tacie tatę tatą tacie tato','father','Vater'),
('grandfather','m','dziadek dziadka dziadkowi dziadka dziadkiem dziadku dziadku','grandfather','Großvater'),
('grandmother','f','babcia babci babci babcię babcią babci babciu','grandmother','Großmutter'),
]
# 10 adjective questions per case: alternating masculine and feminine agreement.
# Feminine paradigms add a plural distractor because only three singular forms
# may be distinct; the fixed singular noun makes this distractor unambiguous.
RU_ADJ = [
('добрый','добрый доброго доброму доброго добрым добром','kind','freundlich'),
('добрый','добрая доброй доброй добрую доброй доброй добрые','kind','freundlich'),
('старый','старый старого старому старого старым старом','old','alt'),
('старый','старая старой старой старую старой старой старые','old','alt'),
('новый','новый нового новому нового новым новом','new','neu'),
('новый','новая новой новой новую новой новой новые','new','neu'),
('молодой','молодой молодого молодому молодого молодым молодом','young','jung'),
('молодой','молодая молодой молодой молодую молодой молодой молодые','young','jung'),
('хороший','хороший хорошего хорошему хорошего хорошим хорошем','good','gut'),
('хороший','хорошая хорошей хорошей хорошую хорошей хорошей хорошие','good','gut'),
]
PL_ADJ = [
('dobry','dobry dobrego dobremu dobrego dobrym dobrym dobry','kind','freundlich'),
('dobry','dobra dobrej dobrej dobrą dobrą dobrej dobra dobre','kind','freundlich'),
('stary','stary starego staremu starego starym starym stary','old','alt'),
('stary','stara starej starej starą starą starej stara stare','old','alt'),
('nowy','nowy nowego nowemu nowego nowym nowym nowy','new','neu'),
('nowy','nowa nowej nowej nową nową nowej nowa nowe','new','neu'),
('młody','młody młodego młodemu młodego młodym młodym młody','young','jung'),
('młody','młoda młodej młodej młodą młodą młodej młoda młode','young','jung'),
('dobry','dobry dobrego dobremu dobrego dobrym dobrym dobry','good','gut'),
('dobry','dobra dobrej dobrej dobrą dobrą dobrej dobra dobre','good','gut'),
]
# Cardinal answers include the noun, exposing numeral government as well as endings.
RU_CARD = [
('один', 'одна книга|одной книги|одной книге|одну книгу|одной книгой|одной книге', 'one book', 'ein Buch'),
('два', 'две книги|двух книг|двум книгам|две книги|двумя книгами|двух книгах', 'two books', 'zwei Bücher'),
('пять', 'пять книг|пяти книг|пяти книгам|пять книг|пятью книгами|пяти книгах', 'five books', 'fünf Bücher'),
]
PL_CARD = [
('jeden', 'jedna książka|jednej książki|jednej książce|jedną książkę|jedną książką|jednej książce', 'one book', 'ein Buch'),
('dwa', 'dwie książki|dwóch książek|dwóm książkom|dwie książki|dwiema książkami|dwóch książkach', 'two books', 'zwei Bücher'),
('pięć', 'pięć książek|pięciu książek|pięciu książkom|pięć książek|pięcioma książkami|pięciu książkach', 'five books', 'fünf Bücher'),
]
RU_ORD = [
('первый','первый первого первому первого первым первом',6,'first','erst'),
('второй','вторая второй второй вторую второй второй вторые',7,'second','zweit'),
]
PL_ORD = [
('pierwszy','pierwszy pierwszego pierwszemu pierwszego pierwszym pierwszym pierwszy',6,'first','erst'),
('drugi','druga drugiej drugiej drugą drugą drugiej druga drugie',7,'second','zweit'),
]
VOC_ORD = [
('pierwszy','pierwszy pierwszego pierwszemu pierwszym','first','erst'),
('drugi','drugi drugiego drugiemu drugim','second','zweit'),
('trzeci','trzeci trzeciego trzeciemu trzecim','third','dritt'),
('czwarty','czwarty czwartego czwartemu czwartym','fourth','viert'),
('piąty','piąty piątego piątemu piątym','fifth','fünft'),
]
RU_FRAMES = ['Здесь живёт {}.', 'Здесь нет {}.', 'Я помогаю {}.', 'Я вижу {}.', 'Я гуляю с {}.', 'Я думаю о {}.']
PL_FRAMES = ['Tutaj mieszka {}.', 'Nie ma tutaj {}.', 'Pomagam {}.', 'Widzę {}.', 'Idę z {}.', 'Myślę o {}.', '{}, proszę, posłuchaj mnie!']
DE_ARTICLES = {
'm': ['der','des','dem','den','dem','den',''],
'f': ['die','der','der','die','der','die',''],
}
DE_NOUN_FORMS = {
'Bruder': ['Bruder','Bruders','Bruder','Bruder','Bruder','Bruder','Bruder'],
'Freund': ['Freund','Freundes','Freund','Freund','Freund','Freund','Freund'],
'Lehrer': ['Lehrer','Lehrers','Lehrer','Lehrer','Lehrer','Lehrer','Lehrer'],
'Student': ['Student','Studenten','Studenten','Studenten','Studenten','Studenten','Student'],
'Nachbar': ['Nachbar','Nachbarn','Nachbarn','Nachbarn','Nachbarn','Nachbarn','Nachbar'],
'Arzt': ['Arzt','Arztes','Arzt','Arzt','Arzt','Arzt','Arzt'],
'Vater': ['Vater','Vaters','Vater','Vater','Vater','Vater','Vater'],
'Großvater': ['Großvater','Großvaters','Großvater','Großvater','Großvater','Großvater','Großvater'],
}

def native_person(row, index, adjective=None):
    _, gender, _, en, de = row
    en_adj, de_adj = adjective or ('', '')
    en_phrase = 'the ' + (en_adj + ' ' if en_adj else '') + en
    de_noun = DE_NOUN_FORMS.get(de, [de]*7)[index]
    if index == 6:
        en_phrase = (en_adj + ' ' if en_adj else '') + en
        # Native German direct-address adjective has strong -er/-e inflection.
        de_phrase = (de_adj + ('er ' if gender == 'm' else 'e ') if de_adj else '') + de_noun
    else:
        ending = 'e' if index == 0 or (index in (3,5) and gender == 'f') else 'en'
        de_phrase = DE_ARTICLES[gender][index] + ' ' + (de_adj + ending + ' ' if de_adj else '') + de_noun
    en_frames = ['{} lives here.','{} is not here.','I help {}.','I see {}.','I walk with {}.','I think about {}.','{}, please listen to me!']
    de_frames = ['{} wohnt hier.','{} ist nicht hier.','Ich helfe {}.','Ich sehe {}.','Ich gehe mit {} spazieren.','Ich denke an {}.','{}, bitte hör mir zu!']
    # Genitive governed absence in target language uses a nominative subject in
    # the native-language paraphrase; regenerate German NP for that frame.
    if index == 1:
        article = DE_ARTICLES[gender][0]
        de_phrase = article + ' ' + (de_adj + 'e ' if de_adj else '') + de
    en_text = en_frames[index].format(en_phrase)
    de_text = de_frames[index].format(de_phrase)
    return {'en': en_text[0].upper()+en_text[1:], 'de': de_text[0].upper()+de_text[1:]}

def options(forms, correct, offset):
    distinct = list(dict.fromkeys(forms))
    wrong = [x for x in distinct if x != correct]
    if len(wrong) < 3:
        raise ValueError(f'Not enough distinct distractors: {forms}')
    answers = wrong[:3]
    position = offset % 4
    answers.insert(position, correct)
    return dict(zip('abcd', answers)), 'abcd'[position]

def question(identifier, subtype, lemma, prompt, forms, index, native, features, scope='word', offset=0):
    answer = forms[index]
    choices, key = options(forms, answer, offset)
    return {'id': identifier, 'word_type': subtype, 'dictionary_form': lemma,
            'features': features, 'native_text': native, 'neutral_prompt': prompt,
            'answer_scope': scope, 'options': choices, 'correct': key}

def features(row):
    return {'number': 'singular', 'gender': 'masculine' if row[1]=='m' else 'feminine', 'animacy': 'animate'}

def card_native(lang, index, count):
    en_phrase = ['one book','two books','five books'][count]
    de = [
      ['Ein Buch liegt auf dem Tisch.','Zwei Bücher liegen auf dem Tisch.','Fünf Bücher liegen auf dem Tisch.'],
      ['Mir fehlt ein Buch.','Mir fehlen zwei Bücher.','Mir fehlen fünf Bücher.'],
      ['Ich freue mich über ein Buch.','Ich freue mich über zwei Bücher.','Ich freue mich über fünf Bücher.'] if lang=='ru' else
      ['Ich sehe mir ein Buch genauer an.','Ich sehe mir zwei Bücher genauer an.','Ich sehe mir fünf Bücher genauer an.'],
      ['Ich lese ein Buch.','Ich lese zwei Bücher.','Ich lese fünf Bücher.'],
      ['Ich bin mit einem Buch gekommen.','Ich bin mit zwei Büchern gekommen.','Ich bin mit fünf Büchern gekommen.'],
      ['Ich spreche über ein Buch.','Ich spreche über zwei Bücher.','Ich spreche über fünf Bücher.'],
    ][index][count]
    en = [
      f'There {"is" if count==0 else "are"} {en_phrase} on the table.',
      ['I am missing one book.','I am missing two books.','I am missing five books.'][count],
      f'I am happy about {en_phrase}.' if lang=='ru' else f'I look closely at {en_phrase}.',
      f'I read {en_phrase}.', f'I came with {en_phrase}.', f'I talk about {en_phrase}.',
    ][index]
    return {'en':en, 'de':de}

def build(lang):
    rows, adjectives, cardinals, ordinals, cases, frames = (
      (RU,RU_ADJ,RU_CARD,RU_ORD,CASES,RU_FRAMES) if lang=='ru' else
      (PL,PL_ADJ,PL_CARD,PL_ORD,PL_CASES,PL_FRAMES))
    names = (['Именительный','Родительный','Дательный','Винительный','Творительный','Предложный'] if lang=='ru' else
             ['Mianownik','Dopełniacz','Celownik','Biernik','Narzędnik','Miejscownik','Wołacz'])
    documents = {'language.yaml': {'schema_version':1,'learning_language':lang,
      'name':'Русский' if lang=='ru' else 'Polski','native_languages':['en','de'],
      'tracks':['nouns','adjectives'], 'cases':[{'id':c,'name':n} for c,n in zip(cases,names)]}}
    for index, case in enumerate(cases):
        for track in ('nouns','adjectives'):
            sentences=[]
            if track=='nouns':
                for n,row in enumerate(rows):
                    forms=row[2].split()
                    sentences.append(question(f'{lang}-{track}-{case}-{row[0]}','noun',forms[0],
                      frames[index].format('___')+f' ({forms[0]})',forms,index,native_person(row,index),features(row),offset=n))
            else:
                for n,(row,adj) in enumerate(zip(rows,adjectives)):
                    lemma,paradigm,en,de=adj
                    forms=paradigm.split()
                    noun=row[2].split()[index]
                    prompt=frames[index].format('___ '+noun)+f' ({lemma})'
                    sentences.append(question(f'{lang}-{track}-{case}-{row[0]}','adjective',lemma,prompt,
                      forms,index,native_person(row,index,(en,de)),features(row),offset=n))
                if case=='vocative':
                    for n,(lemma,paradigm,en,de) in enumerate(VOC_ORD,10):
                        forms=paradigm.split()
                        sentences.append(question(f'pl-adjectives-vocative-ordinal-{n-9}','ordinal_numeral',lemma,
                          f'___ zawodniku, podejdź do linii startu! ({lemma})', forms,0,
                          {'en':f'{en.capitalize()} competitor, come to the starting line!',
                           'de':f'{de.capitalize()}er Teilnehmer, komm zur Startlinie!'},
                          {'number':'singular','gender':'masculine','animacy':'animate'},offset=n))
                else:
                    card_frames = (['На столе {}.','Мне не хватает {}.','Я рад {}.','Я читаю {}.','Я пришёл с {}.','Я говорю о {}.'] if lang=='ru' else
                                   ['Na stole {}.','Brakuje mi {}.','Przyglądam się {}.','Czytam {}.','Przyszedłem z {}.','Mówię o {}.'])
                    for count,(lemma,paradigm,en,de) in enumerate(cardinals):
                        forms=paradigm.split('|')
                        dictionary_noun='книга' if lang=='ru' else 'książka'
                        prompt=card_frames[index].format('___')+f' ({lemma}; {dictionary_noun})'
                        sentences.append(question(f'{lang}-adjectives-{case}-cardinal-{[1,2,5][count]}',
                          'cardinal_numeral',lemma,prompt,forms,index,card_native(lang,index,count),
                          {'quantity':[1,2,5][count],'noun_dictionary_form':dictionary_noun,'noun_gender':'feminine','animacy':'inanimate'},
                          scope='phrase',offset=10+count))
                    for n,(lemma,paradigm,row_index,en,de) in enumerate(ordinals,13):
                        row=rows[row_index]
                        forms=paradigm.split()
                        prompt=frames[index].format('___ '+row[2].split()[index])+f' ({lemma})'
                        sentences.append(question(f'{lang}-adjectives-{case}-ordinal-{n-12}',
                          'ordinal_numeral',lemma,prompt,forms,index,native_person(row,index,(en,de)),features(row),offset=n))
            instruction={'en':'Choose the form that fits the sentence and the selected case.',
                         'de':'Wähle die Form, die zum Satz und zum ausgewählten Fall passt.'}
            if case=='vocative':
                instruction={'en':'Use the traditional vocative for direct address, even where colloquial nominative address is possible.',
                             'de':'Verwende für die Anrede den traditionellen Vokativ, auch wenn umgangssprachlich der Nominativ möglich ist.'}
            documents[f'{track}/{case}.yaml']={'schema_version':1,'id':f'{lang}-{track}-{case}-starter',
              'learning_language':lang,'track':track,'case':case,'native_languages':['en','de'],
              'instruction':instruction,'contributor':'Slavic Cases project (AI-assisted original starter material)',
              'license':'MIT','sources':'Original sentences; grammar references are recorded in AI/LINKS.md.',
              'review_status':'draft','sentences':sentences}
    return documents

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    docs={f'{lang}/{name}':value for lang in ('ru','pl') for name,value in build(lang).items()}
    collisions=[str(args.output/name) for name in docs if (args.output/name).exists()]
    if collisions:
        parser.error('Refusing to overwrite existing files: '+', '.join(collisions))
    for name,value in docs.items():
        path=args.output/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text('# Original starter material; linguistic review is pending.\n'+
                        yaml.safe_dump(value,allow_unicode=True,sort_keys=False,width=110),encoding='utf-8')
    count=sum(len(value.get('sentences',[])) for value in docs.values())
    print(f'Exported {count} questions in {len(docs)-2} case/track sample files to {args.output}')

if __name__=='__main__':
    main()
