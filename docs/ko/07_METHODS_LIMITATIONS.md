# 조사 방법·날짜·한계

## 범위

2026-09-22를 기준으로 Consensus의 학술 검색을 중심에 두고, 출판사·원논문·저자 저장소·공식 문서로 보강한 **목적 지향적 비판적 문헌 조사**다. 완전한 systematic review, 메타분석, PRISMA 연구 또는 ‘모든 관련 논문’의 목록이 아니다. 효과 크기를 서로 다른 데이터셋 간에 합산하거나 평균 절감률을 만들지 않았다.

## 검색과 채택

질문을 GP/획득, 방정식 발견, biological constraint/UDE, foundation adaptation, multifidelity/생성의 영역으로 나눴다. 성공 결과뿐 아니라 identifiability, misspecification, leakage, simple baseline, noise를 함께 검색했다. 정확한 Consensus query는 [검색 로그](../../references/search_log.json)에 있다. 검색 결과의 핵심 논문은 fetch 후 사용했고, 추가 영역은 web으로 확인했다. EEG 복합 검색 한 번은 rate limit 오류가 있었으며 후속 공식 자료 조사로 보완했다.

참고문헌 35개는 연구 논문·서적·공식 소프트웨어/데이터 문서를 합한 수다. 35편의 실험 논문이라는 의미가 아니다. 논문별 DOI, 출판 상태, 접근일, 읽은 범위, 제한은 JSON/BibTeX/Markdown에 기록했다. `full_text_html`은 접근 가능한 본문을 읽었다는 의미이지 모든 보충자료·PDF·실험 코드를 재현했다는 뜻이 아니다. `abstract_or_primary_page`, `author_repository`는 그보다 제한된 근거 수준이다.

## 메타데이터 정정

Consensus index의 연도와 journal 연도가 다른 경우가 있었다. Weak SINDy는 2021, Ensemble-SINDy는 2022, AI-Aristotle는 2024, Wu model discovery는 2025의 journal publication으로 기록했다. AI-Aristotle의 첫 저자를 포함해 출판사 저자 정보로 정정했다. scDesign3는 online 2023과 issue 2024를 구분했다. 공식 문서의 2026은 접근 연도이지 출판 연도가 아니다.

2026년 7월의 R29는 **preprint**로 별도 표시했다. R28은 공식 문서가 연결하는 preprint source로 인용했고 이후 출판 경로는 확정하지 않았다. CellSAM과 Cellpose-SAM을 다른 프로젝트로 구분했다. 메타데이터가 충분하지 않은 tissue multifidelity 후보는 핵심 근거 목록에서 제외했다.

## 근거의 제한

동물·세포·인간·합성·후향적 벤치마크는 동일 수준의 검증이 아니다. 한 데이터셋에서의 비교를 다른 질환·기관으로 확대하지 않는다. 자기 연구의 성공 보고와 외부 benchmark의 비판을 함께 두되, 평가 task가 다르면 모순처럼 단정하지 않는다. 정량적 문구를 인용할 때 조건부·추정 비교인지 먼저 확인한다.

접근한 HTML·초록·문서에서 얻은 범위로만 정리했으며 paywall의 숨은 본문을 읽었다고 주장하지 않는다. 모든 supplementary data, package release, upstream license, 외부 링크의 장기 접근성은 완전히 감사하지 않았다. OpenNeuro·BioModels의 일부 browser 조회는 불충분했으며 실제 dataset 채택으로 계산하지 않았다.

## 수행한 것과 수행하지 않은 것

수행: 한·영 연구 문서, 근거·실패 지도, 개선 설계, 실제 검증 계획, provenance schema, synthetic-only GP 예제 작성·실행, 내부 링크·참조·schema·ZIP 점검.

미수행: 공개 생물 데이터 다운로드·모델 학습, 바이오 foundation fine-tuning, upstream 연구 코드의 전면 재현, 실험실/임상 실험, GitHub 원격 업로드. 예제 수치는 생명과학 성능의 증거가 아니다.

기존 구조의 개선 아이디어는 제안이며 새 이론의 정리·최적성·우월성이 증명된 것은 아니다. 결과가 불확실하다는 사실과 연구를 진행할 수 없다는 판단은 다르다. 본 자료는 다음 검증을 작게 설계하기 위한 출발점이다.
