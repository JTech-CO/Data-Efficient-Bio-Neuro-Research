# 구현·공개 데이터 지도

## 1. 구현체의 역할과 확인 수준

아래는 직접 조사한 공식 문서 또는 논문이 제시한 구현 경로다. **전체 저장소 clone, 의존성 설치, pretrained checkpoint 실행을 완료한 목록이 아니다.** API와 라이선스는 채택할 정확한 release/commit에서 다시 확인한다. 모델 가중치·논문·원자료를 이 ZIP에 재배포하지 않는다.

| 도구·선행 구현 | 권장 역할 | 진입점 | 사용 전 확인 |
|---|---|---|---|
| GPAL | 행동 실험의 능동 설계 참고 | [논문·코드 안내](https://doi.org/10.1016/j.cogpsych.2020.101360) | 해당 task와 acquisition 목적 |
| BoTorch qMFKG | 비용 기반 multi-fidelity BO | [버전 고정 예제](https://botorch.org/docs/v0.16.1/tutorials/multi_fidelity_bo) | 목표 fidelity, cost model, 제약 |
| PySINDy | sparse/weak 동역학 추정 | [문서](https://pysindy.readthedocs.io/en/stable/) | derivative estimator, library, optimizer |
| PySR | 제한된 식 구조 탐색 | [물리 단위 예제](https://ai.damtp.cam.ac.uk/pysr/dev/examples/physics) | Julia 설치, operator, complexity, unit 검증 |
| DeepXDE | PINN/BINN형 학습 구성 | [문서](https://deepxde.readthedocs.io/en/latest/) | backend, loss scale, BC/IC |
| AI-Aristotle | gray-box + SR 참고 구현 | [저장소](https://github.com/mariodeflorio/AI-Aristotle) | 합성 데이터 중심 검증 범위 |
| Wu model-discovery | hybrid → sparse model selection | [저장소](https://github.com/maclean-lab/model-discovery) | simulated trajectory의 계보 |
| Massonis 식별가능성 | sparse model의 재매개화 참고 | [연구 코드 archive](https://zenodo.org/records/7713048) | MATLAB/toolbox 요구와 버전 |
| NARGP | 비선형 fidelity 관계 | [저장소](https://github.com/paraklas/NARGP) | low/high correspondence, old dependency |
| LaBraM | EEG frozen representation baseline | [저장소](https://github.com/935963004/LaBraM) | montage, scaling, overlap |
| SBI/sbibm | likelihood-free inference 평가 | [benchmark](https://github.com/sbi-benchmark/sbibm) | simulator adequacy, posterior diagnostics |

근거: [R02](../../references/BIBLIOGRAPHY.md#r02) [R08](../../references/BIBLIOGRAPHY.md#r08) [R09](../../references/BIBLIOGRAPHY.md#r09) [R17](../../references/BIBLIOGRAPHY.md#r17) [R19](../../references/BIBLIOGRAPHY.md#r19) [R20](../../references/BIBLIOGRAPHY.md#r20) [R26](../../references/BIBLIOGRAPHY.md#r26) [T01](../../references/BIBLIOGRAPHY.md#t01) [T02](../../references/BIBLIOGRAPHY.md#t02) [T03](../../references/BIBLIOGRAPHY.md#t03). PySR의 unit penalty는 hard guarantee가 아니므로 산출식을 별도 검사한다. [T02](../../references/BIBLIOGRAPHY.md#t02)

## 2. 데이터는 원본을 복사하기 전에 작은 manifest부터

| 자원 | 우선 활용 | 주의사항 |
|---|---|---|
| [CELLxGENE Census](https://chanzuckerberg.github.io/cellxgene-census/) | metadata 조건으로 작은 reference slice | 원 연구 인용, release pin, duplicates, donor availability |
| [DANDI](https://dandiarchive.org/) | 공개 신경생리·optophysiology 자료 탐색 | Dandiset별 조건·종·readout·version 확인 |
| [PhysioNet EEG](https://physionet.org/content/eegmmidb/1.0.0/) | 기본 EEG decoding 시험 | run별 label 의미, subject split, 사전학습 중복 |
| R07/R14 논문 연결 데이터 | 세포 영상과 assay | 이미지 수와 독립 실험 수 분리 |
| R13 연결 perturbation 데이터 | control/response 평가 | 세포주·개입·반복·원본 license 확인 |
| R09 연결 GEO 원자료 | 공개 생물 동역학 사례 추적 | accession과 실제 시간·lineage 정의 확인 |

공식 Census는 효율적 부분 조회와 중복 관련 정보를 제공한다. DANDI는 여러 신경생리 자료 형식을 포함한다. PhysioNet 해당 release는 ODC-By 1.0 조건을 명시한다. 포털이 공개되었다고 모든 파생 모델·재배포에 같은 라이선스가 적용된다고 가정하지 않는다. [D01](../../references/BIBLIOGRAPHY.md#d01) [D02](../../references/BIBLIOGRAPHY.md#d02) [D03](../../references/BIBLIOGRAPHY.md#d03)

OpenNeuro와 BioModels도 탐색 후보로 확인했지만, 이번 브라우저 조회에서는 각각 동적 페이지의 본문 확보가 되지 않거나 오류가 발생했다. 따라서 이 패키지의 검증 완료 dataset inventory에 넣지 않았다. 이는 해당 자원이 없거나 사용할 수 없다는 뜻이 아니다.

## 3. 구현 순서

첫 commit은 ingest manifest, 그룹 분할, 단순 기준선과 저장 가능한 metric이어야 한다. 그 다음 GP 획득 정책을 추가하고, 이후 observation-aware dynamics를 독립 모듈로 만든다. 마지막으로 foundation adapters와 multifidelity를 추가한다. 각 단계가 이전 단계와 비교 가능하도록 `run_id`, seed, code commit, package versions를 고정한다.

원시 자료의 다운로드·처리와 결과 해석을 모두 LLM에 자유롭게 맡기는 구조보다, typed schema·작은 검증 함수·명시적 승인으로 경계를 둔다. LLM은 문서 탐색, 메타데이터 후보 추출, equation card 설명에 보조적으로 사용할 수 있지만 수치 지표나 원문 근거를 만들어내는 주체가 되어서는 안 된다.

## 4. 계산 자원 계획

작은 exact GP·단순 회귀·작은 sparse library는 CPU baseline으로 먼저 실행한다. 대형 encoder는 매번 fine-tune하기 전에 frozen embedding을 캐시하여 분할별 재사용을 평가한다. 캐시도 training release와 transform hash를 갖는다. GPU 필요량은 입력 해상도·sequence length·batch size·optimizer state에 따라 달라지므로 특정 노트북에서 전체 stack이 동작한다고 미검증 보장하지 않는다.

실제 테스트된 의존성은 `examples/requirements-tested.txt`, 예제 환경은 `examples/results/environment.json`에 따로 있다. 이는 연구 대상 upstream stack 전체의 호환성 lockfile이 아니다.
