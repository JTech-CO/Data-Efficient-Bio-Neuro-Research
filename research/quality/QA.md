# v1.1.0 검증 범위 / Validation scope

## 수행한 검사 / Executed checks

| 항목 / Check | 실제 결과 / Result |
|---|---|
| 신규 Python 계약·수치·폐루프·실제 로컬 HTTP API 테스트 | 63 tests passed |
| 원 v1.0.0 회귀 테스트 | 14 tests passed |
| 합성 파일럿 | 504 runs, 42 cells, 12 seeds; complete outputs retained |
| 브라우저 자산·DOM·상호작용 | 70 checks passed; native gzip, 42 replays, 9 comparisons, language, timeline, import/export, responsive overflow |
| 원자료 보존·링크·전체 실행 schema/hash 검사 | See [machine-readable release report](validation_report.json) |

[신규 테스트 로그](unit-tests.log) · [원 회귀 로그](original-regression-tests.log) · [파일럿 실행 로그](pilot-execution.log) · [브라우저 검사](browser_checks.json)

## 브라우저 검사의 중요한 제한 / Important browser limitation

관리형 Chromium 144.0.7559.96에서 `file://`와 localhost URL로 실제 탐색을 시도했으나 `ERR_BLOCKED_BY_ADMINISTRATOR`로 차단되었다. 정책을 우회하지 않았다. 대신 실제 배포 HTML/CSS/JS를 독립 페이지에 주입하여 gzip 해제, DOM 동작, 1440px 데스크톱·390px 모바일 렌더링, JSON 파일 내보내기·가져오기를 검사했다. JavaScript page error는 0개였고 모바일의 페이지 가로 넘침을 수정한 뒤 다시 검사했다.

Managed Chromium blocked real file and localhost navigation. The 70 checks used isolated `set_content` with the shipped assets, not real URL navigation. Local HTTP/API execution was separately tested with actual HTTP requests in ServerTests. **Browser-to-server end-to-end navigation, direct file opening, cross-browser behavior, GitHub Pages deployment, and remote Actions execution were not verified.** They must not be described as passing E2E tests.

[Desktop Korean](desktop-ko.png) · [Desktop English](desktop-en.png) · [Mobile Korean](mobile-ko.png) · [Mobile English](mobile-en.png)

## 정확히 무엇이 보존되는가 / Preservation

63개 원 파일 중 60개는 기존 경로에서 byte-identical이다. 루트 README 두 개는 새 연구 입구를 추가하며, 원 README 두 개와 원 CHECKSUMS는 `research/baseline/`에 byte-identical 원본으로 보존한다. 원 01~08 한국어/영문 연구 장, 참고문헌, 예제, schema와 과거 QA 결과는 바꾸지 않는다. 원 SHA-256 manifest는 비교 기준이며 새 버전의 전체 checksum을 대신하지 않는다.

The manifest binds the original ZIP and every original file. Historical QA stays historical; new QA is stored here. Root CHECKSUMS.sha256 is regenerated for the complete new release after checks finish. The new checksum file excludes itself.

## 비검증 영역 / Not established

단위 테스트·schema·hash 통과는 생물학적 타당성, 인과적 효과, 기전 진실성, 개인정보 보호, 실험실 안전성, 임상적 유용성 또는 프로덕션 보안을 증명하지 않는다. 모든 실험은 알려진 잡음·고정 함수·유한 설계 공간을 사용하는 synthetic pilot이다. 시드는 독립 생물학적 개체가 아니며 diagnostic validation은 재사용된다. Bayesian 구간에 분포 변화·온라인·conformal 보장을 부여하지 않는다.

No real data, model weights, instrument control, donor-level external validation, or production deployment was executed. Public licensing remains undecided as in the original package. Screenshots document rendered UI states, not biological findings.
