# Research extension QA / 추가 구현 검증

**Date: 2026-09-22. Research-only slice 0.1.0.**

## Executed checks / 실행한 검증

| Check | Result | Evidence |
|---|---|---|
| Original tests, unchanged | 14 passed | [baseline_tests.log](baseline_tests.log) |
| New model, split, lineage, policy, server tests | 59 passed | [lab_tests.log](lab_tests.log) |
| Chromium DOM/render/interactions | Passed, 12 check categories | [browser_validation.json](browser_validation.json) |
| Artifact preservation, pilot aggregates, original schemas, local links | See machine-readable report | [package_validation.json](package_validation.json) |
| Detailed trace re-execution | 25 acquisition hashes and final ID metrics matched exactly | [replay_validation.json](replay_validation.json) |
| Synthetic pilot | 640 runs, no discarded planned runs | [execution.json](../pilot/execution.json) |

The original `quality/` results belong to the earlier research package and remain unchanged. This directory records only the new extension's checks.

기존 테스트 14개와 신규 테스트 59개가 통과했다. 기존 `quality/`는 최초 자료의 검증 기록으로 보존하고 이번 검증은 이 폴더에 별도로 기록했다. 테스트 통과는 연구 가설의 참, 임상 적용성 또는 모든 운영체제에서의 동작 보증이 아니다.

## Browser scope / 브라우저 검증 범위

The environment's managed Chromium policy blocks URL navigation. The test therefore loads the exact shipped HTML, CSS and JavaScript into an inline `set_content` rendering harness. This checks KR/EN switching, all tabs, actual recorded scenario data, SVG plots, timeline, keyboard tab navigation, JSON import, export Blob content, escaping and 390px layout. The observer labels and mobile charts were inspected and adjusted for readability.

HTTP API execution, input rejection and same-origin checks were exercised separately in Python integration tests. **Browser-to-server end-to-end navigation, direct `file://` opening, completed downloads, native clipboard/localStorage persistence and remote GitHub Pages deployment are not validated here.** The export smoke test inspects the generated Blob and deliberately suppresses the download action.

브라우저 환경 정책으로 URL 이동이 차단되어, 실제 배포 파일을 인라인 렌더링한 별도 하네스에서 화면과 상호작용을 검증했다. Python HTTP 통합 시험과 브라우저 화면 시험은 각각 통과했지만, 두 경로가 합쳐진 실제 URL 접속·다운로드 완료·운영체제별 동작까지 검증했다는 뜻은 아니다.

[Desktop screenshot](desktop.png) · [Evaluation screenshot](evaluation.png) · [Mobile screenshot](mobile.png)

Optional rendering recheck (not a required runtime dependency): install `playwright` and provide a Chromium executable, then run `python scripts/browser_smoke_lab.py --chromium /path/to/chromium`.

## Numerical and scientific boundaries

ODE solutions are compared with `solve_ivp`. Conjugate inference, positive-semidefinite covariance, quadrature bounds, mixture intervals and deterministic query noise have tests. Test labels never drive acquisition; audit labels affect the gate and are therefore validation, not test data. The caller may generate new research settings locally, but the runner only accepts synthetic observations.

Known failures are not test defects to hide: model non-identifiability under restricted observations, gate misses under sensor/noise misspecification, wider fallback intervals and degraded point predictions are preserved in the pilot. Follow-up proposals appear in chapters 11–12.

Not tested: real biological datasets, biological safety/ethics review, external data adapters, clinical inference, Windows/macOS native execution, GitHub-hosted CI, GPU acceleration, long-duration service operation or arbitrary user-supplied scientific models.
