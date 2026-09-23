# 버전별 연구 자료

[English](VERSIONS.en.md) · [메인 README](README.md)

메인 README에는 현재 버전만 표시한다. 아래는 각 릴리스의 연구 범위, 실행 입구, 결과와 검증 기록이다. 과거 숫자는 해당 버전의 정의를 유지하며 독립 생물 표본 수가 아니다.

| Version | Focus | Guide | Results | Viewer / QA | Executions |
|---|---|---|---|---|---:|
| 1.4.0-research.1 | 부분 식별 · 미지 분산 대조 · 반복 분해 | [Guide](BOUNDED.md) | [Results](research/docs/ko/29_BOUNDED_RESULTS.md) | [Viewer](research/bounded/web/index.html) · [QA](research/bounded/quality/QA.md) | 8,208 |
| 1.3.0-research.1 | 교정 전달 · 진단 위치/비용 · 잡음/정책 | [Guide](TRIAD.md) | [Results](research/docs/ko/22_TRIAD_RESULTS.md) | [Viewer](research/triad/web/index.html) · [QA](research/triad/quality/QA.md) | 16,320 |
| 1.2.0-research.1 | 가정 탐지 · 측정 종류 선택 | [Guide](FOLLOWUP.md) | [Results](research/docs/ko/15_FOLLOWUP_RESULTS.md) | [Viewer](research/followup/web/index.html) · [QA](research/followup/quality/QA.md) | 3,820 |
| 1.1.0 | 첫 실행 폐루프 | [Guide](research/README.ko.md) | [Results](research/docs/ko/11_PILOT_RESULTS.md) | [Viewer](index.html) · [QA](research/quality/QA.md) | 504 |
| 1.0.0 | 문헌 조사·연구 계획 | [Guide](docs/ko/01_RESEARCH_REPORT.md) | [Results](examples/RESULTS.ko.md) | — | 초기 GP 예제 / initial GP example |

## 이력 보존

기존 누적 README 전문은 [한국어 스냅샷](research/bounded/baseline/README.md)과 [영문 스냅샷](research/bounded/baseline/README.en.md)에 바이트 단위로 보존했다. 스냅샷의 상대 경로는 원문 그대로이므로 실제 이동은 위 표를 사용한다. 원본 파일 해시는 [보존 목록](research/bounded/baseline/manifest.json)에 있다. 이전 버전의 문서·수치 결과·수치 코드는 수정하지 않았다.

이 저장소의 기준 실행 계보는 `Closed-Loop-Lab`의 `research/closed_loop`에서 이어진다. 이전 대안 패키지의 `research_lab/` 경로와 혼합하지 않는다. 새 버전은 이 문서에 한 행과 필요 문서 링크만 추가하고 메인 README 아래에 과거 본문을 붙이지 않는다.
