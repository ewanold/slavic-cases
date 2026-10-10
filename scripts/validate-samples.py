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
    pass

def require(condition,message):
    if not condition:
        raise ValidationError(message)

def nonempty(value):
    return isinstance(value,str) and bool(value.strip())

def text_map(value,locales,location):
    require(isinstance(value,dict), f'{location}: expected language-to-text mapping')
    require(all(nonempty(value.get(code)) for code in locales),f'{location}: missing translation for {locales}')
    require(all(nonempty(k) and nonempty(v) for k,v in value.items()),f'{location}: empty or non-text translation')

def read(path):
    try:
        data=yaml.load(path.read_text(encoding='utf-8'),Loader=UniqueLoader)
    except (OSError,UnicodeError,yaml.YAMLError,ValueError,TypeError) as exc:
        raise ValidationError(f'{path}: {exc}') from exc
    require(isinstance(data,dict),f'{path}: expected YAML mapping')
    require(data.get('schema_version')==1,f'{path}: unsupported schema_version')
    return data

def validate(root,release=False):
    require(root.is_dir(),f'{root}: sample directory does not exist')
    language_files=sorted(root.glob('*/language.yaml'))
    language_files=[p for p in language_files if p.parent.name!='templates']
    require(bool(language_files),f'{root}: no language sets found')
    seen=set()
    totals=Counter()
    subtypes=Counter()
    statuses=Counter()
    for language_file in language_files:
        lang=read(language_file)
        code=lang.get('learning_language')
        require(nonempty(code) and code==language_file.parent.name,f'{language_file}: folder/language mismatch')
        require(nonempty(lang.get('name')),f'{language_file}: missing language name')
        declared=lang.get('cases')
        require(isinstance(declared,list) and 1<=len(declared)<=8,f'{language_file}: declare 1–8 cases')
        require(all(isinstance(c,dict) and nonempty(c.get('id')) and nonempty(c.get('name')) for c in declared),f'{language_file}: invalid case declaration')
        cases=[c['id'] for c in declared]
        require(len(set(cases))==len(cases),f'{language_file}: duplicate case ID')
        tracks=lang.get('tracks')
        require(tracks==['nouns','adjectives'],f'{language_file}: declare nouns and adjectives tracks')
        locales=lang.get('native_languages')
        require(isinstance(locales,list) and locales and all(nonempty(x) for x in locales),f'{language_file}: missing native_languages')
        require(len(set(locales))==len(locales),f'{language_file}: duplicate native language')
        for track in tracks:
            folder=language_file.parent/track
            require(folder.is_dir(),f'{folder}: missing track folder')
            files=sorted(folder.glob('*.yaml'))
            require(bool(files),f'{folder}: no samples')
            covered=set()
            for path in files:
                data=read(path)
                where=str(path)
                case=data.get('case')
                require(case in cases,f'{where}: undeclared case {case!r}')
                covered.add(case)
                require(data.get('learning_language')==code and data.get('track')==track,f'{where}: language/track mismatch')
                sid=data.get('id')
                require(nonempty(sid) and sid not in seen,f'{where}: missing or duplicate sample ID')
                seen.add(sid)
                require(data.get('native_languages')==locales,f'{where}: native language list differs from language definition')
                for field in ('contributor','license','sources'):
                    require(nonempty(data.get(field)),f'{where}: missing {field}')
                status=data.get('review_status')
                require(status in ('draft','reviewed'),f'{where}: invalid review_status')
                if release:
                    require(status=='reviewed',f'{where}: linguistic review required for release')
                text_map(data.get('instruction'),locales,f'{where}/instruction')
                questions=data.get('sentences')
                require(isinstance(questions,list) and len(questions)==15,f'{where}: expected exactly 15 sentences')
                for q in questions:
                    require(isinstance(q,dict),f'{where}: question must be a mapping')
                    qid=q.get('id')
                    loc=f'{where}/{qid}'
                    require(nonempty(qid) and qid not in seen,f'{loc}: missing or duplicate question ID')
                    seen.add(qid)
                    subtype=q.get('word_type')
                    allowed=('noun',) if track=='nouns' else ('adjective','cardinal_numeral','ordinal_numeral')
                    require(subtype in allowed,f'{loc}: word_type does not belong to {track}')
                    require(nonempty(q.get('dictionary_form')),f'{loc}: dictionary_form required')
                    require(isinstance(q.get('features'),dict) and q['features'],f'{loc}: features required')
                    text_map(q.get('native_text'),locales,f'{loc}/native_text')
                    prompt=q.get('neutral_prompt')
                    require(nonempty(prompt) and prompt.count('___')==1,f'{loc}: prompt needs exactly one ___ blank')
                    require(q.get('answer_scope') in ('word','phrase'),f'{loc}: answer_scope must be word or phrase')
                    options=q.get('options')
                    require(isinstance(options,dict) and set(options)==set('abcd'),f'{loc}: exactly a,b,c,d options required')
                    require(all(nonempty(v) for v in options.values()),f'{loc}: empty/non-text option')
                    normalized=[unicodedata.normalize('NFC',v).strip().casefold() for v in options.values()]
                    require(len(set(normalized))==4,f'{loc}: duplicate answer text')
                    require(q.get('correct') in options,f'{loc}: correct must reference one option')
                    totals[(code,track)]+=1
                    subtypes[(code,subtype)]+=1
                    statuses[status]+=1
                if track=='adjectives':
                    require(any(q['word_type']=='adjective' for q in questions),f'{where}: missing adjective questions')
                    require(any(q['word_type'].endswith('_numeral') for q in questions),f'{where}: missing numeral questions')
            require(covered==set(cases),f'{folder}: missing cases: {sorted(set(cases)-covered)}')
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
