#!/usr/bin/env python3
"""Validate contributor YAML. No downloads. Uses the host's existing PyYAML.
Default: validate drafts for implementation. --release also requires reviewed sets.
"""
import argparse
from collections import Counter
from pathlib import Path
import sys
import unicodedata
import yaml

class UniqueLoader(yaml.SafeLoader):
    pass

def mapping(loader,node,deep=False):
    result={}
    for key_node,value_node in node.value:
        key=loader.construct_object(key_node,deep=deep)
        if key in result:
            raise ValueError(f'duplicate YAML key {key!r} at line {key_node.start_mark.line+1}')
        result[key]=loader.construct_object(value_node,deep=deep)
    return result
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)

class ValidationError(Exception):
    def __init__(self, template, **params):
        self.template, self.params = template, params
        super().__init__(template.format(**params))

def require(condition,message,**params):
    if not condition:
        raise ValidationError(message,**params)

def nonempty(value):
    return isinstance(value,str) and bool(value.strip())

def text_map(value,locales,location):
    require(isinstance(value,dict), '{location}: expected language-to-text mapping', location=location)
    require(all(nonempty(value.get(code)) for code in locales),'{location}: missing translation for {locales}', location=location, locales=locales)
    require(all(nonempty(k) and nonempty(v) for k,v in value.items()),'{location}: empty or non-text translation', location=location)

def read(path):
    try:
        data=yaml.load(path.read_text(encoding='utf-8'),Loader=UniqueLoader)
    except (OSError,UnicodeError,yaml.YAMLError,ValueError,TypeError) as exc:
        raise ValidationError('{location}: {exc}', location=path, exc=exc) from exc
    require(isinstance(data,dict),'{location}: expected YAML mapping', location=path)
    require(data.get('schema_version')==1,'{location}: unsupported schema_version', location=path)
    return data

def validate(root,release=False,allow_incomplete=False):
    # Authoring may save complete lessons before every declared case has material.
    # Release/build callers retain strict coverage, even if the flag is supplied.
    allow_incomplete = allow_incomplete and not release
    require(root.is_dir(),'{location}: sample directory does not exist', location=root)
    language_files=sorted(root.glob('*/language.yaml'))
    language_files=[p for p in language_files if p.parent.name!='templates']
    require(bool(language_files),'{location}: no language sets found', location=root)
    seen=set()
    totals=Counter()
    subtypes=Counter()
    statuses=Counter()
    for language_file in language_files:
        seen=set() # IDs are scoped to a selectable language pack.
        lang=read(language_file)
        code=lang.get('learning_language')
        require(nonempty(code) and language_file.parent.name in (code, f'{code}-v2'),'{location}: folder/language mismatch', location=language_file)
        require(nonempty(lang.get('name')),'{location}: missing language name', location=language_file)
        if 'names' in lang:
            text_map(lang['names'], ['en','de'], f'{language_file}/names')
        if 'topic_names' in lang:
            require(isinstance(lang['topic_names'], dict), '{location}: topic_names must be a mapping', location=language_file)
            for topic_id, names in lang['topic_names'].items():
                require(nonempty(topic_id), '{location}: empty topic name ID', location=language_file)
                text_map(names, ['en','de'], f'{language_file}/topic_names/{topic_id}')
        if 'lesson_defaults' in lang:
            defaults = lang['lesson_defaults']
            require(isinstance(defaults, dict) and all(isinstance(defaults.get(k, ''), str)
                    for k in ('contributor', 'license', 'sources')),
                    '{location}: lesson defaults must be text', location=language_file)
        topic_profile=lang.get('content_profile') in ('apk-topic-import','polish-topic-adaptation')
        declared=lang.get('cases')
        require(isinstance(declared,list) and 1<=len(declared)<=8,'{location}: declare 1–8 cases', location=language_file)
        require(all(isinstance(c,dict) and nonempty(c.get('id')) and nonempty(c.get('name')) for c in declared),'{location}: invalid case declaration', location=language_file)
        cases=[c['id'] for c in declared]
        require(len(set(cases))==len(cases),'{location}: duplicate case ID', location=language_file)
        tracks=lang.get('tracks')
        require(tracks==['nouns','adjectives'],'{location}: declare nouns and adjectives tracks', location=language_file)
        locales=lang.get('native_languages')
        require(isinstance(locales,list) and locales and all(nonempty(x) for x in locales),'{location}: missing native_languages', location=language_file)
        require(len(set(locales))==len(locales),'{location}: duplicate native language', location=language_file)
        for track in tracks:
            folder=language_file.parent/track
            require(folder.is_dir(),'{location}: missing track folder', location=folder)
            files=sorted(folder.glob('*.yaml'))
            require(bool(files) or allow_incomplete,'{location}: no samples', location=folder)
            covered=set()
            for path in files:
                data=read(path)
                where=str(path)
                require(data.get('content_profile') == lang.get('content_profile'),'{location}: content profile mismatch', location=where)
                if topic_profile:
                    topic=data.get('topic')
                    require(isinstance(topic,dict) and nonempty(topic.get('id')) and nonempty(topic.get('name')),'{location}: topic id/name required', location=where)
                case=data.get('case')
                require(case in cases,'{location}: undeclared case {case!r}', location=where, case=case)
                covered.add(case)
                require(data.get('learning_language')==code and data.get('track')==track,'{location}: language/track mismatch', location=where)
                sid=data.get('id')
                require(nonempty(sid) and sid not in seen,'{location}: missing or duplicate sample ID', location=where)
                seen.add(sid)
                require((set(locales).issubset(data.get('native_languages', [])) if topic_profile else data.get('native_languages')==locales),'{location}: native language list differs from language definition', location=where)
                unknown_import_author = data.get('content_profile') == 'apk-topic-import' and not nonempty(data.get('contributor'))
                if unknown_import_author:
                    require(all(isinstance(q, dict) and isinstance(q.get('source'), dict) and q['source']
                        for q in data.get('sentences', [])), '{location}: unknown import author requires per-question source metadata', location=where)
                for field in (('license','sources') if unknown_import_author else ('contributor','license','sources')):
                    require(nonempty(data.get(field)),'{location}: missing {field}', location=where, field=field)
                status=data.get('review_status')
                require(status in ('draft','reviewed'),'{location}: invalid review_status', location=where)
                if release:
                    require(data.get('license') not in ('unspecified','unknown'),'{location}: redistribution permission required', location=where)
                    require(status=='reviewed','{location}: linguistic review required for release', location=where)
                text_map(data.get('instruction'),locales,f'{where}/instruction')
                questions=data.get('sentences')
                require(isinstance(questions,list) and (bool(questions) if topic_profile else len(questions)==15),'{location}: expected exactly 15 sentences', location=where)
                for q in questions:
                    require(isinstance(q,dict),'{location}: question must be a mapping', location=where)
                    qid=q.get('id')
                    loc=f'{where}/{qid}'
                    require(nonempty(qid) and qid not in seen,'{location}: missing or duplicate question ID', location=loc)
                    seen.add(qid)
                    subtype=q.get('word_type')
                    allowed=('noun',) if track=='nouns' else ('adjective','cardinal_numeral','ordinal_numeral')
                    require(subtype in allowed,'{location}: word_type does not belong to {track}', location=loc, track=track)
                    require(nonempty(q.get('dictionary_form')),'{location}: dictionary_form required', location=loc)
                    require(isinstance(q.get('features'),dict) and q['features'],'{location}: features required', location=loc)
                    text_map(q.get('native_text'),locales,f'{loc}/native_text')
                    prompt=q.get('neutral_prompt')
                    require(nonempty(prompt) and prompt.count('___')==1,'{location}: prompt needs exactly one ___ blank', location=loc)
                    require(q.get('answer_scope') in ('word','phrase'),'{location}: answer_scope must be word or phrase', location=loc)
                    options=q.get('options')
                    require(isinstance(options,dict) and (set(options) in (set('abc'),set('abcd')) if topic_profile else set(options)==set('abcd')),'{location}: exactly a,b,c,d options required', location=loc)
                    require(all(nonempty(v) for v in options.values()),'{location}: empty/non-text option', location=loc)
                    normalized=[unicodedata.normalize('NFC',v).strip().casefold() for v in options.values()]
                    require(topic_profile or len(set(normalized))==4,'{location}: duplicate answer text', location=loc)
                    require(q.get('correct') in options,'{location}: correct must reference one option', location=loc)
                    totals[(code,track)]+=1
                    subtypes[(code,subtype)]+=1
                    statuses[status]+=1
                if track=='adjectives' and not topic_profile:
                    require(any(q['word_type']=='adjective' for q in questions),'{location}: missing adjective questions', location=where)
                    require(any(q['word_type'].endswith('_numeral') for q in questions),'{location}: missing numeral questions', location=where)
            require(allow_incomplete or covered==set(cases),'{location}: missing cases: {details}', location=folder, details=sorted(set(cases)-covered))
    return totals,subtypes,statuses

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',nargs='?',type=Path,default=Path(__file__).resolve().parents[1]/'samples')
    parser.add_argument('--release',action='store_true')
    args=parser.parse_args()
    try:
        totals,subtypes,statuses=validate(args.root,args.release)
    except (ValidationError,TypeError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        return 1
    for (lang,track),count in sorted(totals.items()):
        print(f'{lang}/{track}: {count} questions')
    for (lang,kind),count in sorted(subtypes.items()):
        print(f'  {lang}/{kind}: {count}')
    print(f'PASS: {sum(totals.values())} questions; review status: {dict(statuses)}')
    print('Structural validation does not establish linguistic correctness.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
