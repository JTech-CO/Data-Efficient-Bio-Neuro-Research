# 12. 구현 결정·비목표·연구 원본 보존

## ADR-001: 같은 저장소에 추가한다

기존 63개 파일의 SHA-256을 `research_lab/provenance/baseline_manifest.json`에 저장했다. 01~08장, 원래 예제·스키마·문헌·tests·quality 파일은 변경하지 않는다. README 두 개에는 추가 단계의 입구만 붙이고 루트 CHECKSUMS는 새 패키지로 갱신한다. 원 README와 원 CHECKSUMS의 바이트 사본은 provenance에 별도 보존한다. 이전 quality 결과를 이번 검증 결과처럼 덮어쓰지 않는다.

## ADR-002: 알려진 ODE 후보와 정확한 작은 추론부터 시작한다

임의 식 발견이나 큰 PINN을 모사하는 더미 클래스를 두지 않는다. 계수에 선형인 두 후보의 posterior와 evidence를 정확히 계산하므로 모델 선택, 관측 연산자, 정보이득, 비용, 평가 경계를 검사하기 쉽다. ODE의 동적 구조를 학습한 것이 아니며, 모델 밖의 법칙을 자동 생성하는 기능도 없다.

## ADR-003: 원본 observation schema를 수정하지 않는다

기존 schema의 `additionalProperties=false`를 존중한다. query/role/hash/cost는 새로운 envelope로 붙인다. 기존 record를 억지로 확장해 다른 소비자의 계약을 깨지 않는다. 원본 스키마 적합성과 의미적 split·simulator-only 제한은 별도 테스트한다.

## ADR-004: audit와 test를 다르게 취급한다

audit는 행동에 영향을 줄 수 있으므로 final test가 아니다. 그 label은 fit에 쓰지 않지만 경고와 fallback 선택에는 사용한다. test와 외삽 정답은 완료된 실행을 평가할 때만 연다. 사후 metric을 온라인 stopping criterion으로 사용하지 않는다.

## ADR-005: 자동 승인은 합성 허용 목록만 의미한다

`approval.type=synthetic_allowlist`와 `real_world_authorized=false`를 매번 기록한다. 실제 기관의 승인, 사람의 클릭, 생물 안전성 검토를 받은 것처럼 표시하지 않는다. HTTP 서버는 127.0.0.1에만 bind하고 입력은 소규모 설정 JSON으로 제한한다. 파일 업로드·명령 실행·외부 API 키·실험 장치 연결은 없다. 이 서버를 인터넷에 노출하지 않는다.

## ADR-006: 예측을 계속하더라도 기전 주장은 보류할 수 있다

GP fallback은 숫자를 출력하지만 candidate preference는 보류한다. 그 숫자의 정확성과 구간도 별도로 평가한다. 경고와 abstention만 늘려 성공했다고 부르지 않는다. 현재 coverage 상승의 상당 부분은 interval widening이며 문서와 UI에 함께 표시한다.

## ADR-007: 정적 UI는 계산하는 척하지 않는다

25개 실제 실행 trace와 640개 반복 실험 집계를 번들로 제공한다. 정적 사이트에서는 검토와 JSON import/export만 가능하다. Python backend가 없을 때 실행 버튼을 비활성화한다. timeline 재생과 새 실행을 명확히 다르게 표시한다. 외부 CDN·폰트·분석 스크립트는 쓰지 않는다.

## ADR-008: 문헌의 발행 연도와 구현 근거를 분리한다

Consensus에서 선택한 세 record를 fetch하고 출판사·학회 자료로 연도를 확인했다. 일부 Consensus 연도는 preprint 연도였으므로 원본 metadata와 version-of-record 정보를 함께 남겼다. 이번 코드가 CIV, R-IDeA, profile-likelihood 최적제어의 구현이라고 주장하지 않는다. [추가 문헌 기록](../../research_lab/provenance/LITERATURE.md)

## 비목표

실제 생명·뇌과학 프로덕션 모델, 임상 판단, 실험 장비 제어, 자동 기전 확정, PINN/BINN/SINDy 학습, 바이오 foundation 미세조정, multi-fidelity 선택, 생성 증강, 실제 환자·donor 데이터 처리는 구현 범위 밖이다. 미래용 query 필드가 있다고 기능이 구현된 것으로 보지 않는다.

## 남은 기술적 한계

정적 파일은 상세 보안 검증기가 아니다. JSON import는 로컬 연구 출력의 검토 기능이며 임의 데이터 포맷 지원을 목표로 하지 않는다. hash chain은 변경 탐지에 유용하지만 공격자가 전체를 다시 해시할 수 있는 환경의 진본성 증명이 아니다. 모델의 marginal evidence는 후보와 prior에 조건부다. 소수 audit의 통계적 검출력을 보장하지 않는다. OOD 테스트는 같은 simulator의 다른 x 범위일 뿐 새로운 생물군의 external validation이 아니다.
