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
