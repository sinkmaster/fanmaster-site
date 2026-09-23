# -*- coding: utf-8 -*-
"""fan_homepage 배포 전 검사. 표준 라이브러리만 씁니다 (윈도우 python 그대로 실행).

사용:  python scripts/check.py            전체 사이트
       python scripts/check.py warehouse  한 사이트만

검사 항목
  1. HTML 태그 짝
  2. <img src> 파일 존재
  3. 내부 <a href> 파일 존재
  4. 다른 fanmaster 서브도메인으로 나가는 <a> 링크 없음 (CLAUDE.md 링크 규칙)
  5. ld+json 문법
  6. sitemap.xml 의 URL 이 실제 파일을 가리킴 / 중복 없음
  7. 전화·문자 링크 형식
문제가 하나라도 있으면 종료 코드 1 → 푸시하지 않는다.
"""
import os, re, sys, json
from html.parser import HTMLParser

# 윈도우 콘솔(cp949)에서 한글 출력이 깨지지 않게 UTF-8 로 고정
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITES = {'main': 'fanmaster.co.kr', 'window': 'window.fanmaster.co.kr',
         'kitchen': 'kitchen.fanmaster.co.kr', 'warehouse': 'warehouse.fanmaster.co.kr',
         'home': 'home.fanmaster.co.kr'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta',
        'param', 'source', 'track', 'wbr'}
PHONE = '010-2680-4538'
SMS = 'sms:01026804538?&body='


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f'닫는 태그 과잉 </{tag}>')
        elif self.stack[-1] != tag:
            self.errors.append(f'짝 안 맞음 </{tag}> (열린 것 <{self.stack[-1]}>)')
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()


def exists(site_dir, ref):
    ref = ref.split('#')[0].split('?')[0]
    if not ref:
        return True
    # "/info" 처럼 슬래시로 시작하는 주소는 그 사이트 폴더가 뿌리다
    ref = ref.lstrip('/')
    if not ref:
        return True
    p = os.path.normpath(os.path.join(site_dir, ref))
    if os.path.isfile(p):
        return True
    # 확장자 없는 깔끔한 주소(/case-30) 도 허용
    return os.path.isfile(p + '.html')


def check_site(name):
    site_dir = os.path.join(ROOT, name)
    if not os.path.isdir(site_dir):
        return [f'[{name}] 폴더 없음']
    my_host = SITES[name]
    other_hosts = [h for s, h in SITES.items() if s != name]
    probs = []
    htmls = sorted(f for f in os.listdir(site_dir) if f.endswith('.html'))

    for f in htmls:
        path = os.path.join(site_dir, f)
        try:
            doc = open(path, encoding='utf-8-sig').read()
        except UnicodeDecodeError:
            probs.append(f'[{name}/{f}] UTF-8 아님')
            continue
        tag = f'[{name}/{f}]'

        b = Balance()
        b.feed(doc)
        probs += [f'{tag} 태그 {e}' for e in b.errors[:3]]
        if b.stack:
            probs.append(f'{tag} 안 닫힌 태그 {b.stack[-3:]}')

        for src in re.findall(r'<img[^>]+src="([^"]+)"', doc):
            if src.startswith(('http', 'data:')):
                continue
            if not exists(site_dir, src):
                probs.append(f'{tag} 없는 이미지 {src}')

        for href in re.findall(r'<a[^>]+href="([^"]+)"', doc):
            if href.startswith(('tel:', 'sms:', 'mailto:', '#', 'javascript:')):
                continue
            if href.startswith('http'):
                if any(h in href for h in other_hosts):
                    probs.append(f'{tag} 다른 사이트로 나가는 링크 {href}')
                continue
            if not exists(site_dir, href):
                probs.append(f'{tag} 없는 링크 {href}')

        for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
            try:
                json.loads(m)
            except Exception as e:
                probs.append(f'{tag} ld+json 문법 오류: {e}')

        for t in re.findall(r'href="tel:([^"]+)"', doc):
            if t != PHONE:
                probs.append(f'{tag} 전화번호 이상 tel:{t}')
        for s in re.findall(r'href="(sms:[^"]+)"', doc):
            if not s.startswith(SMS):
                probs.append(f'{tag} 문자 링크 형식 이상 {s[:40]}')

    sm = os.path.join(site_dir, 'sitemap.xml')
    if os.path.isfile(sm):
        xml = open(sm, encoding='utf-8-sig').read()
        locs = re.findall(r'<loc>\s*(.*?)\s*</loc>', xml)
        if len(locs) != len(set(locs)):
            probs.append(f'[{name}/sitemap.xml] 중복 URL')
        for u in locs:
            if not u.startswith(f'https://{my_host}/'):
                probs.append(f'[{name}/sitemap.xml] 도메인 이상 {u}')
                continue
            rel = u[len(f'https://{my_host}/'):]
            if rel and not exists(site_dir, rel):
                probs.append(f'[{name}/sitemap.xml] 파일 없는 URL {u}')
    else:
        probs.append(f'[{name}] sitemap.xml 없음')

    print(f'  {name:10s} html {len(htmls):4d}개  '
          f'{"문제 " + str(len(probs)) + "건" if probs else "이상 없음"}')
    return probs


def main():
    targets = sys.argv[1:] or list(SITES)
    bad = [t for t in targets if t not in SITES]
    if bad:
        print('모르는 사이트:', bad, '/ 가능:', list(SITES))
        sys.exit(2)
    print('검사 중...')
    problems = []
    for t in targets:
        problems += check_site(t)
    print()
    if problems:
        print(f'문제 {len(problems)}건 — 푸시하지 마세요.')
        for p in problems[:60]:
            print('  -', p)
        if len(problems) > 60:
            print(f'  ... 외 {len(problems) - 60}건')
        sys.exit(1)
    print('통과 — 푸시해도 됩니다.')


if __name__ == '__main__':
    main()
