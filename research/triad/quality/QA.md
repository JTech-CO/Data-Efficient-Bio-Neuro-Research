# v1.3 QA / 검증 범위

## 수행한 검사 / Executed checks

| 검사 / Check | 실제 결과 / Actual result |
|---|---|
| 최초 unit tests | 14 passed |
| v1.1 research unit tests | 63 passed |
| v1.2 follow-up unit tests | 43 passed |
| v1.3 numerical/contracts + lossless archive tests | 61 passed |
| 총 unit tests / Total unit tests | **181 passed** |
| 원시 실행 전수검사 / All raw runs | **16,320** |
| 직렬화 관측 계보·비용 / Serialized observations | **890,880** |
| 집계·짝지은 bootstrap 재계산 | All equal to published JSON |
| 대표 실행 전체 재실행 / Complete representative replays | **219 / 219 identical** |
| passive controller 간 동일 데이터 검사 | 480 world-policy groups match |
| F 고유 수집 데이터셋 / Unique F datasets | 1,200 |
| F 최종 적합 비수렴 / Unconverged final fits retained | 6 / 6,480 |
| F 수집 중 비수렴 snapshot / Acquisition fit snapshots retained | 267 |
| 브라우저+HTTP 검사 / Browser+HTTP checks | **106 passed: 100 rendering/DOM, 6 separate HTTP byte checks** |
| 예측 학습에 실측 생물 데이터 | **0** |

수치 입력·역할·rank·WLS·점수 수식·반복 관측·test 동결 순서를 시험했다. CRPS 수식은 수치적 적분과 비교한다. 테스트 통과는 일반적인 생물학적 유효성·절대 센서 참값·통계적 보장의 인증이 아니다.

Numerical tests cover contracts, rank, WLS, score formulas, technical pairs, and freeze-before-test order. CRPS formulas are compared with numerical integration. Passing tests do not certify biological validity, absolute sensor truth, or general statistical guarantees.

## 브라우저 경계 / Browser boundary

관리형 Chromium이 `http://127.0.0.1:8766/...` 및 `file://...` URL 이동을 `ERR_BLOCKED_BY_ADMINISTRATOR`로 거부했다. 정책을 끄거나 우회하지 않았다. 따라서 **실제 로컬 자산을 그대로 인라인 주입한 페이지**에서 한국어/영어·탭·시나리오·설계·예산·수집기·추정기 선택과 DOM·SVG 렌더링을 검사했다. 별도 Python HTTP 요청으로 HTML/CSS/JS/data와 대표 원본 JSON의 서버 전달 바이트·해시를 비교했다.

Managed Chromium rejected localhost and file navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. The policy was not disabled or bypassed. The exact local assets were inlined for bilingual rendering, tabs, scenario/design/budget/controller/estimator selection and DOM/SVG checks. Separate Python HTTP requests verified the delivered HTML/CSS/JS/data and representative full JSON bytes/hashes.

**검증하지 않은 것 / Not verified:** 브라우저 native localhost/file 전체 경로, 실제 브라우저 다운로드 완료, Windows/macOS 네이티브 설치, 모든 브라우저, 보조공학 접근성 감사, 원격 GitHub Pages 배포. The native browser-to-localhost/file path and completed browser download were not verified; nor were native Windows/macOS installs, all browsers, assistive technologies, or remote Pages deployment.

모바일390px에서는 문서 전체의 가로 넘침이 없고 넓은 표만 내부 가로 스크롤을 사용한다. SVG는 모바일용 좌표계로 다시 그려 축 레이블이 지나치게 축소되지 않도록 했다. desktop Korean/English와 mobile Korean 스크린샷을 검토했다.

At390px there is no page-wide horizontal overflow; wide tables scroll locally. SVG uses a mobile coordinate system to preserve legible axes. Desktop Korean/English and mobile Korean screenshots were inspected.

## 실패·수정 기록 / Failure and amendment history

1. 첫 평가 `evaluation-v130-b`에서 round된 반복 key와 원 소수 좌표의 parent 비교가 불일치하여 실행을 중단했다. 숫자 추정법·정책·임계값을 변경하지 않고 측정 전 좌표/첨가량을10자리로 정규화했다. 회귀 테스트를 추가하고 `evaluation-v130-c`, seed41000으로 전체를 새로 실행했다. 원 코드·잠금·로그·부분 결과 해시를 `aborted_attempt/`에 보존한다. 부분 raw 스트림 자체는 중복 배포하지 않는다. 일부D 결과를 보았으므로 완전히 보지 않은 외부 확인시험으로 주장하지 않는다.
2. 후처리 재실행 검사에서 비용48.0을 정수 예산 인수로 바꾸지 않아 검증 harness가 거부됐다. harness만 `int` 변환하도록 고친 뒤 전수검사와219재실행을 모두 다시 통과했다. 수치 코어·공개 결과는 변경하지 않았다. `validation-harness-type-error.log`를 남겼다.
3. 브라우저 native 접속 실패 로그와 자산 주입 검사 결과를 모두 보존했다.

The initial partial evaluation aborted on a canonical-coordinate lineage mismatch. Measurement coordinates/deltas were normalized before observation; estimator, policy and threshold formulas were unchanged. A regression test and a fresh full evaluation bank were used, with the earlier sources/lock/log and partial-stream hashes retained. Some D output had been inspected; no external-blinding claim is made. A later replay harness mistakenly supplied float cost48.0 to an integer-only budget; converting that harness argument to int fixed the check, after which all runs and219 replays passed without changing numerical results. Native browser-navigation failures are retained alongside injected-asset checks.

## 손실 없는 아카이브 / Lossless archive

원시 이벤트의 type/payload를 저장하고 각 이벤트의 index/previous/hash와 관측 digest를 재구성한다. 각 기록의 원 전체 digest와 chain tip을 모두 비교했다. D/E/F **16,320개 전부를 압축→복원하여 JSON 값의 동일성을 확인**했다. 관측값·추정치·점수·비용·실패·순서를 생략하지 않는다. 원 gzip 파일의 바이트 해시는 ARCHIVE_MANIFEST에 기록하지만 gzip 헤더 시각까지 byte-for-byte 재현을 요구하는 형식은 아니다. 복원된 JSON 객체와 해시 체인의 정확성이 검사 대상이다.

Event type/payloads are stored; deterministic index/previous/hash and measurement digests are reconstructed. Every original full-record digest and chain tip is verified. All16,320 records round-trip to identical JSON values, without omitting observations, fits, scores, costs, failures, or ordering. Original gzip byte hashes are recorded; reproducing gzip-header timestamps is not required. The guarantee is exact JSON-object and hash-chain reconstruction, not authentication.

## 실행 환경 / Executed environment

Python3.13.5 · NumPy2.3.5 · SciPy1.17.0 · jsonschema4.26.0 · Playwright1.57.0 · Linux x86_64. BLAS thread counts were1; full evaluation used4 worker processes. These are executed versions, not a claim that arbitrary newer/older environments are equivalent. See `environment.json`.

The added GitHub Actions workflow runs unit tests only. It has not been executed on remote GitHub in this session. A fresh environment should record its own numerical/library versions and verify tolerances/replay results.

## 자료

[수치검증 JSON](validation.json) · [브라우저/HTTP JSON](browser-checks.json) · [원시 압축 manifest](../results/v130/raw/ARCHIVE_MANIFEST.json) · [코드/프로토콜 lock](../results/v130/protocol.lock.json) · [환경](environment.json)
