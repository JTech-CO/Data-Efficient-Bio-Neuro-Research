# 데이터 효율적 생명·뇌과학 AI 연구 | v1.3.0-research.1

[한국어 연구 시작](TRIAD.md) · [English](TRIAD.en.md) · [D/E/F 결과 화면](research/triad/web/index.html) · [16,320개 실행 결과](research/docs/ko/22_TRIAD_RESULTS.md)

교정의 표본 전달 가능성, 진단 위치와 비용, 잡음 모형과 수집 정책을 모두 연구·구현했다. 원 연구와 이전 코드·결과는 보존했다. 실제 생물학적 관측은 0개이며, 합성 연구 모듈이다.

---
## 아래는 보존된 v1.2 이하 안내다

# 데이터 효율적 생명·뇌과학 AI 연구 | 후속 v1.2.0-research.1

**한국어** · [English](README.en.md)

관측·가정·측정 선택의 후속 연구 A/B를 추가했다. 이전 계획과 v1.1 실행 코드는 보존했다.

[새 연구 시작](FOLLOWUP.md) · [후속 결과 화면](research/followup/web/index.html) · [3,820개 평가 실행의 결과](research/docs/ko/15_FOLLOWUP_RESULTS.md) · [다음 연구 결정](research/docs/ko/16_RESEARCH_DECISIONS.md) · [검증 범위](research/followup/quality/QA.md)

이 수는 1,900개 진단 궤적 + 1,920개 수집 실행이다. 생물 표본 수는 0이다. 원시 결과와 실패 사례를 포함하며 프로덕션 모델이 아니다.

---

## 아래의 v1.1 연구 안내는 보존된 이전 내용이다

# 데이터 효율적 생명·뇌과학 AI 연구 | v1.1.0

**한국어** · [English](README.en.md) · [실험 화면](index.html)

## 추가된 실행 연구: Closed-loop Research Lab

기존 연구 계획을 보존하고, 관측·가정·개입을 구분하는 **실행 가능한 합성 연구 모듈**을 추가했다. 실제 생물 데이터·임상 검증·프로덕션 모델은 포함하지 않는다.

[설치와 사용](research/README.ko.md) · [구현 명세](research/docs/ko/09_IMPLEMENTATION.md) · [504개 파일럿 결과](research/docs/ko/11_PILOT_RESULTS.md) · [후속 연구 방향](research/docs/ko/12_RESEARCH_DIRECTION.md) · [변경 기록](CHANGELOG.md)

```bash
python -m pip install -r research/requirements.txt
python -m research.closed_loop serve
```

압축을 모두 풀고 `index.html`을 열면 설치 없이 수록 기록을 재생한다. 새 계산은 로컬 Python 서버에서만 실행한다. 기존 01~08 한·영 연구 문서는 변경하지 않았다. [보존 기록](research/baseline/manifest.json)과 [검증 범위](research/quality/QA.md)를 확인한다.

---

## 아래는 보존된 v1.0.0 연구 안내다

# 데이터 효율적 생명·뇌과학 AI 연구

**한국어** · [English](README.en.md)

GP/베이지안 회귀, 능동학습, SINDy/PySR, PINN/BINN/UDE, 바이오 파운데이션 전이와 멀티피델리티·생성 증강을 비교한 연구 자료다.

> 핵심 판단: 확장은 가능하고 선행 구현도 많다. 그러나 적은 새 관측으로 얻는 이득은 사전정보·관측계·평가 방식에 의존하며, 모든 단계에서 일반 AI를 이기는 새 이론으로 입증된 것은 아니다. [R02](references/BIBLIOGRAPHY.md#r02) [R07](references/BIBLIOGRAPHY.md#r07) [R13](references/BIBLIOGRAPHY.md#r13)

**기준일:** 2026-09-22 · **버전:** 1.0.0 · **범위:** 문헌 조사와 연구 설계, 임상/실험실 검증 아님.

## 읽기 순서

| 문서 | 장 번호 |
|---|---|
| [종합 조사 보고서](docs/ko/01_RESEARCH_REPORT.md) | 01 |
| [제안 아키텍처·수식·인터페이스](docs/ko/02_ARCHITECTURE.md) | 02 |
| [평가·누수·중단 기준](docs/ko/03_EVALUATION.md) | 03 |
| [세포 영상·오믹스·EEG·SBI](docs/ko/04_CASE_STUDIES.md) | 04 |
| [구현체·공개 데이터 지도](docs/ko/05_IMPLEMENTATION_MAP.md) | 05 |
| [개선 가설 6개와 반증 계획](docs/ko/06_RESEARCH_AGENDA.md) | 06 |
| [검색 방법과 근거의 제한](docs/ko/07_METHODS_LIMITATIONS.md) | 07 |
| [실패 모드 12개 비교표](docs/ko/08_FAILURE_MATRIX.md) | 08 |

[용어](docs/GLOSSARY.md) · [근거 지도](references/EVIDENCE.ko.md) · [참고문헌](references/BIBLIOGRAPHY.md) · [서지 JSON](references/references.json) · [BibTeX](references/references.bib)

## 포함 자료

```text
Data-Efficient-Bio-Neuro-Research/
├── README.md / README.en.md
├── docs/ko/ · docs/en/        # 8 paired research chapters
├── references/              # 35 sources, 14 claims, search log, BibTeX
├── diagrams/                # editable Mermaid
├── schemas/                 # provenance + model-card JSON Schemas
├── configs/                 # proposed experiment configuration
├── templates/               # paired preregistration and equation cards
├── examples/                # executable synthetic GP demonstration
│   └── results/             # 20-seed results, 4 figures, environment
├── scripts/                 # internal consistency validation
├── tests/                   # numerical and schema regression tests
└── quality/                 # actual validation report
```

참고문헌 35개는 논문·서적·공식 소프트웨어/데이터 자료를 합친 수다. 모두 실험 논문이거나 전부 독립 재현된 것은 아니다. Preprint와 원논문·문서의 읽은 범위를 구분했다.

## 실행 가능한 범위

[합성 예제 설명](examples/README.ko.md)과 [실제 실행 결과](examples/RESULTS.ko.md)를 참고한다. 원 데이터/가중치는 내려받지 않는다. 이 예제는 GP 가정 불일치와 식별가능성의 한계를 보여주는 교육 자료이며 생물 성능 결과가 아니다.

```bash
python -m pip install -r examples/requirements-tested.txt
python examples/gp_active_learning_demo.py --seeds 20
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

## 출판과 권리

원논문 PDF·데이터·모델 가중치는 포함하지 않았다. 본 패키지의 공개 라이선스는 사용자가 결정할 수 있도록 [선택 전 상태](LICENSE.md)로 두었다. [인용 안내](CITATION.md), [제3자 자료 안내](THIRD_PARTY_NOTICES.md), [검증 범위](quality/QA.md)를 확인한다. GitHub에 올릴 때 저장소 소유자·저자 정보를 추가하되, 본 설계가 새 이론으로 입증되었다고 표시하지 않는다.
