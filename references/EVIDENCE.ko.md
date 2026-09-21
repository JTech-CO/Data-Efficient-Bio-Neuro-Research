# 핵심 주장·근거 지도

기존 문헌의 근거다. 본 패키지에서 재현한 생물학적 성능 결과가 아니다.

| ID | 주장 | 근거 유형 | 출처 | 제한 |
|---|---|---|---|---|
| E01 | GP 기반 실험 선택은 이미 구현되어 있다. | real_behavioral_and_in_vitro | [R02](BIBLIOGRAPHY.md#r02) [R03](BIBLIOGRAPHY.md#r03) | 과제별 효과이며 보편적인 절감 배율이 아니다. |
| E02 | Weak-form 방식은 미분 기반 잡음 민감도를 줄이는 선행 접근이다. | method_benchmarks | [R04](BIBLIOGRAPHY.md#r04) | 숨은 상태나 사전 밖 기전은 별도 문제다. |
| E03 | Ensemble-SINDy에 불확실성과 능동학습 결합이 존재한다. | synthetic_and_historical_data | [R05](BIBLIOGRAPHY.md#r05) | bootstrap 선택 빈도는 인과 확률이 아니다. |
| E04 | 희소하고 해석 가능한 모델도 식별 불가능할 수 있다. | biological_model_case_studies | [R06](BIBLIOGRAPHY.md#r06) | parameter combination을 보고하는 것이 필요할 수 있다. |
| E05 | BINN의 실제 세포 assay 적용이 있다. | in_vitro | [R07](BIBLIOGRAPHY.md#r07) | 사람의 전체 시스템 검증과 다르다. |
| E06 | PINN/SR와 hybrid-to-sparse 연결이 이미 존재한다. | synthetic_and_selected_biological_data | [R08](BIBLIOGRAPHY.md#r08) [R09](BIBLIOGRAPHY.md#r09) | 실제 데이터와 모델 생성 궤적의 역할을 분리해야 한다. |
| E07 | Foundation 전이는 가능하지만 단순 기준선이 경쟁력 있다. | task_specific_benchmarks | [R11](BIBLIOGRAPHY.md#r11) [R12](BIBLIOGRAPHY.md#r12) [R13](BIBLIOGRAPHY.md#r13) | zero-shot, fine-tuned, perturbation task를 구분한다. |
| E08 | 영상에서도 few-shot 이득과 domain 한계가 함께 존재한다. | real_imaging | [R14](BIBLIOGRAPHY.md#r14) [R16](BIBLIOGRAPHY.md#r16) | FOV 수와 donor 수는 다르다. |
| E09 | EEG 전이 평가에는 사전학습 중복 audit가 필요하다. | implementation_and_benchmark_documentation | [R17](BIBLIOGRAPHY.md#r17) [R18](BIBLIOGRAPHY.md#r18) | 특정 overlap 경고를 모든 결과로 확대하지 않는다. |
| E10 | fidelity 간 비선형 관계와 비용 기반 질의를 구현할 수 있다. | method_benchmarks_and_software | [R19](BIBLIOGRAPHY.md#r19) [R20](BIBLIOGRAPHY.md#r20) | 다른 종이 단순 low-fidelity인 것은 아니다. |
| E11 | 생성 증강은 평가 도구이지만 독립 관측이나 자동 privacy가 아니다. | generative_method_and_privacy_study | [R21](BIBLIOGRAPHY.md#r21) [R22](BIBLIOGRAPHY.md#r22) | 데이터 처리 이득과 새로운 정보의 출처를 구분한다. |
| E12 | 적응적 선택을 고려하는 conformal 방법이 있다. | theory_with_defined_assumptions | [R23](BIBLIOGRAPHY.md#r23) [R24](BIBLIOGRAPHY.md#r24) | 조건부 분포 안정성 등 전제를 넘어 보장하지 않는다. |
| E13 | SBI는 신경 동역학에서 가능한 파라미터 분포를 추정하는 대안이다. | neural_model_studies_and_benchmark | [R25](BIBLIOGRAPHY.md#r25) [R26](BIBLIOGRAPHY.md#r26) | 시뮬레이터 오류와 계산량을 따로 평가한다. |
| E14 | 2026년 추가 benchmark도 상황 의존적인 성능을 보고한다. | preprint_abstract | [R29](BIBLIOGRAPHY.md#r29) | 동료심사 완료 근거로 취급하지 않는다. |
