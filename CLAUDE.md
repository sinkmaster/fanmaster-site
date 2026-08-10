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

- GitHub 저장소: `sinkmaster/fanmaster-site`
- Production branch: `main`
- Build command 없음 (정적 HTML 그대로 서빙)
- 도메인 DNS는 Cloudflare에서 관리

## 폴더 구조

```
main/       메인 사이트 (환기 설비 전문) — index.html + photos/cases (시공사례 26건)
window/     창문형 환풍기 — index.html, sitemap.html, case-01~02, area-*.html 41개
kitchen/    주방·상가 고압환풍기 — index.html, case-01~02
warehouse/  창고·공장 환풍기 — index.html, case-01~02
환풍기사진/  원본 사진 보관용 (사이트에 직접 쓰이지 않음)
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

### 작업 후 확인할 것
- HTML 태그 짝이 맞는지
- 내부 링크가 실제로 존재하는 파일을 가리키는지
- `<img src>` 파일이 실제로 있는지
- 다른 사이트로 나가는 `<a>` 링크가 0개인지
