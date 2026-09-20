# 튼튼환풍시스템 홈페이지 저장소

## 배포 방식 (중요)

이 저장소는 **Cloudflare Pages가 GitHub을 지켜보다가 자동 배포**합니다.
`git push` 하면 1~2분 안에 실제 사이트에 반영됩니다.
**FTP나 별도 업로드 절차는 필요 없습니다.** GitHub Pages도 사용하지 않습니다.

저장소에 배포 설정 파일(`.github/workflows`, `wrangler.toml` 등)이 없는 것은 정상입니다.
설정이 저장소가 아니라 Cloudflare 대시보드 쪽에 있기 때문입니다.

| Cloudflare Pages 프로젝트 | 배포 폴더 | 실제 주소 |
|---|---|---|
| fanmaster-main-pages | `main/` | fanmaster.co.kr, www.fanmaster.co.kr |
| fanmaster-window | `window/` | window.fanmaster.co.kr |
| fanmaster-kitchen | `kitchen/` | kitchen.fanmaster.co.kr |
| fanmaster-warehouse | `warehouse/` | warehouse.fanmaster.co.kr |
| fanmaster-home | `home/` | home.fanmaster.co.kr |

- GitHub 저장소: `sinkmaster/fanmaster-site`
- Production branch: `main`
- Build command 없음 (정적 HTML 그대로 서빙)
- 도메인 DNS는 Cloudflare에서 관리
- 각 프로젝트는 **Build watch paths** 로 자기 폴더만 감시합니다 (2026-09-19 설정).
  그래서 warehouse 폴더만 바꾸면 warehouse 하나만 빌드됩니다. 푸시 1번 = 빌드 1개.

## "빌드하고 푸시해줘" — 사장님이 이렇게 말하면

이 저장소는 빌드 단계가 없으니 **빌드 = 검사** 입니다. 순서를 바꾸지 않습니다.

1. **검사** — `python scripts/check.py` 실행. (윈도우에서 `python` 이 안 되면 `py -3`)
   - 바뀐 폴더가 하나뿐이면 `python scripts/check.py warehouse` 처럼 그 폴더만 넘겨도 됩니다.
   - **문제가 한 건이라도 나오면 푸시하지 않습니다.** 문제 목록을 그대로 보여드리고 멈춥니다.
2. **변경 확인** — `git status --short` 로 어떤 폴더의 무슨 파일이 바뀌었는지 한 줄로 요약해 드립니다.
   - 루트의 작업 메모(`*.md`, `*.txt`)나 `환풍기사진/` 원본이 끼어 있으면 **커밋에서 빼고** 말씀드립니다.
3. **커밋·푸시** — `git add -A && git commit -m "<폴더>: <한 줄 요약>" && git push`
   - 커밋 메시지 예: `warehouse: 수원 어린이집 화장실 환풍기 시공사례(case-18) 추가`
   - 윈도우가 파일 쓰기를 막아서 `index.NEW.html` 같은 파일이 있으면, 원본을 `attrib -r` 로 풀고 NEW 를 원본 이름으로 덮어쓴 뒤 커밋합니다.
4. **결과 보고** — 커밋 해시와 바뀐 사이트 주소를 알려드립니다.
   - 새 시공사례가 있으면 그 페이지 주소(`https://warehouse.fanmaster.co.kr/case-18.html` 형식)를 적어 드립니다.
   - 1~2분 뒤 `curl -s <주소> | grep -o "<title>[^<]*"` 로 실제로 올라갔는지 확인해 드립니다.
   - 다 되면 **구글 서치콘솔 URL 검사 → 색인 요청**, **네이버 서치어드바이저 → 웹 페이지 수집** 에 그 주소를 넣으시라고 한 줄로 안내합니다.

"푸시해줘" 만 말씀하셔도 같은 순서입니다. 검사를 건너뛰지 않습니다.

## 시공사례 올리는 흐름

- 페이지 만들기(사진 가공·제목·본문·index/sitemap 연결)는 **Cowork(클로드 앱)** 에서 합니다.
  거기서 완성된 파일을 이 폴더에 직접 넣습니다.
- 여기(Claude Code)는 **검사하고 푸시하는 역할**입니다. 페이지 내용을 다시 쓰지 않습니다.
- 파일을 받았을 때 문장이 어색해 보여도, 먼저 물어보고 고칩니다. 지난번에 "지역, 1명 2시간 작업으로 당일 마무리했습니다" 를 비문으로 보고 되돌린 적이 있는데, 그건 「시공사례 올리는 법」 문서의 고정 형식이었습니다.
- 시공사례 파일 규칙: `case-NN.html` + `photos/idx/wNN-*.jpg`, `index.html` 카드, `sitemap.html` 카드, `sitemap.xml` URL, 지역 페이지(`work-<지역>-1.html`) 링크. 이 다섯 군데가 한 세트입니다.

## 폴더 구조

```
main/        메인 사이트 (환기 설비 전문) — index.html + case-01~26 + info.css(공용 스타일)
window/      창문형 환풍기 — case-03~31, 가이드 3건(toilet-fan / bathroom-fan / kitchen-fan), area-*.html
kitchen/     주방·상가 고압환풍기 — case-01~03, work-*.html 지역 페이지
warehouse/   창고·공장·업소 환풍기 — case-01~18, work-*.html 지역 페이지 (현재 사례를 집중해서 올리는 곳)
home/        콘센트 증설 (환풍기 아님)
scripts/     check.py — 배포 전 검사
환풍기사진/   원본 사진 보관용 (사이트에 직접 쓰이지 않음, 커밋하지 않음)
```

`window/photos/` 안에는 `areas/`(지역 페이지용), `works/`(시공사례용),
`services/`(서비스 카드용) 폴더가 있습니다. 같은 원본에서 밝기·대비·잘린 위치를
조금씩 다르게 만든 파일들이라 **서로 겹치는 이미지가 없습니다. 임의로 합치지 마세요.**

## 사이트 공통 규칙

- 상호: **튼튼환풍시스템** (예전 이름 "튼튼환풍기"는 쓰지 않음)
- 전화: `010-2680-4538` / 문자: `sms:01026804538`
- 상담 시간: **08:00 ~ 20:00** (평일·주말)
- 사업자등록번호: 636-13-02485 · 경기도 용인시 기흥구 공세로 150-29

### 링크 규칙
- **다른 사이트로 나가는 링크를 만들지 않습니다.** 각 사이트는 자기 폴더 안에서만
  이동합니다. 헤더 로고, footer, 상세페이지 모두 `index.html` 기준 상대 경로를 씁니다.
- 문자 링크는 문구가 미리 채워지도록 아래 형태를 씁니다.
  `sms:01026804538?&body=환풍기%20설치%20문의드립니다.%20사진%20첨부합니다`
  (`?&` 형태여야 아이폰·안드로이드 양쪽에서 문구가 채워집니다)

### 작업 후 확인할 것 (scripts/check.py 가 전부 봅니다)
- HTML 태그 짝이 맞는지
- 내부 링크가 실제로 존재하는 파일을 가리키는지
- `<img src>` 파일이 실제로 있는지
- 다른 사이트로 나가는 `<a>` 링크가 0개인지
- sitemap.xml 의 주소가 실제 파일을 가리키는지
