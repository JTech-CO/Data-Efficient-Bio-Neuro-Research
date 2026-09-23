# D/E/F 후속 연구 | v1.3.0-research.1

[English](TRIAD.en.md) · [한영 결과 화면](research/triad/web/index.html) · [전체 결과](research/docs/ko/22_TRIAD_RESULTS.md) · [다음 연구 결정](research/docs/ko/23_RESEARCH_DECISIONS.md) · [QA](research/triad/quality/QA.md)

교정의 표본 전달 가능성, 진단 위치와 비용, 잡음 모형과 수집 정책의 분리 **세 과제를 모두 코드로 구현하고 합성 실험으로 평가**했다. 이전 v1.2 계획과 결과는 보존했다. 완성된 생물학 AI, 임상 장치, 실제 데이터 학습 모델이 아니다.

| 과제 | 구현 | 평가 |
|---|---|---|
| D | 외부 교정·표준 첨가·공백·독립 기준·교차 점검 | 9세계 유형 × 5설계 × 80 = 3,600회 |
| E | 고정·무작위·층화·최대 공백·적응 진단, 같은 비용과 α 규칙 | 정상256 + 다른7종64씩, 5정책 × 3비용 조건 = 10,560회 |
| F | 수집기 × 정책 × 최종 추정기의 완전 교차 | 6세계 유형 × 40 × 3수집기 × 3정책 = 2,160회, 최종 적합 6,480개 |

총 16,320개 실행/궤적이며 실제 생물학적 관측은 0개다. F의 고유 수집 데이터셋은 1,200개로, 같은 passive 데이터를 여러 추정기에 넣은 것을 독립 표본으로 세지 않는다.

## 먼저 확인할 결론

표준 첨가는 gain을 분리하지만 offset과 잠재 절편의 혼동은 제거하지 못했다. 독립 기준을 더하면 특정 가정 아래 rank가 충분해지지만 모든 기준이 함께 편향되면 오차를 놓친다. 같은 비용에서 고정 세 지점보다 공간을 넓게 덮는 진단이 국소 오류를 더 자주 감지했다. Student-t는 큰 잡음 오염에서 유리했지만 정상 잡음이나 누락된 평균식을 항상 개선하지 않았다. 전체 셀과 불리한 결과를 22장에 공개했다.

## 설치와 새 합성 계산

저장소 루트에서 실행한다. GPU·API 키·모델 가중치·외부 데이터셋은 필요 없다. 실제 생물 표본을 받는 업로더나 장치 실행 API는 없다. 검증한 환경의 정확한 버전은 QA에 있다.

```bash
python -m pip install -r research/requirements.txt

python -m research.triad_loop demo --study D --scenario both_shift --policy triangulated --seed 27 --out research/triad/results/demo-D.json
python -m research.triad_loop demo --study E --scenario narrow --policy adaptive_cover --seed 27 --out research/triad/results/demo-E.json
python -m research.triad_loop demo --study F --scenario contamination --policy ivr --controller student_t --seed 27 --out research/triad/results/demo-F.json
```

기존 출력은 덮어쓰지 않는다. demo 결과는 별도 공개 demo bank를 쓰며 수록된 평가 자료를 변경하지 않는다.

## 결과 화면

압축을 모두 풀고 `research/triad/web/index.html`을 열거나 다음처럼 정적 서버를 실행한다.

```bash
python -m http.server 8766 --bind 127.0.0.1
```

브라우저 주소는 `http://127.0.0.1:8766/research/triad/web/`이다. GitHub Pages에서는 같은 하위 경로로 정적 열람할 수 있는 구성이다. 이번 세션에서 원격 Pages 배포를 수행하지 않았다.

화면은 저장된 전체 집계와 219개 대표 실행을 보여준다. 집계는 여러 세계의 평균, 그래프는 시드41000의 개별 실행이다. 원본 JSON을 내려받을 수 있다. 새 계산은 CLI에서 하며 뷰어가 모델을 재학습하지 않는다. 임의 demo JSON을 화면에 불러오는 기능은 이번 뷰어에 없다.

## 전체 평가 재현

```bash
python -m research.triad_loop prepare --out research/triad/results/new-study
python -m research.triad_loop evaluate --workers 4 --out research/triad/results/new-study
python -m research.triad_loop verify-lock --out research/triad/results/new-study
```

`prepare`는 38개 개발 smoke run과 코드·설정 해시를 기록한다. 시작된 평가 폴더는 재실행으로 덮어쓸 수 없다. 현재 결과는 독립 사전등록이나 외부 블라인드 평가가 아니다. 첫 부분 평가의 좌표 계보 오류, 수정과 새 평가 bank 재실행을 [설계](research/docs/ko/18_TRIAD_DESIGN.md)에 기록했다.

## 원시 아카이브와 검사

모든 원시 관측·모형·비용·점수를 보존했다. 결과의 반복 이벤트 해시/인덱스는 손실 없이 복원되는 형식으로 배포하며 복원할 때 전체 기록 digest를 검사한다.

```bash
python -m research.triad.archive research/triad/results/v130/raw/D.compact.jsonl.gz research/triad/results/restored-D.jsonl.gz --restore
python research/triad/validate_triad.py
python -m unittest discover -s research/triad/tests -v
```

E/F도 같은 방식이다. 새 평가 CLI가 생성하는 읽기 쉬운 전체 JSONL과 수록된 compact 아카이브는 같은 기록을 표현한다. 암호학적으로 서명한 증명서가 아니라 재현성·우발적 변경 검사용 해시다.

## 문서 지도

18장 설계, 19장 교정 전달과 rank, 20장 공간 진단과 조건부 검정, 21장 잡음 요인 분리, 22장 모든 결과, 23장 연구 결정, 24장 재현성과 QA를 `research/docs/ko/`와 `en/`에 추가했다. [새 참고문헌](research/triad/references/REFERENCES.md)은 8개이며 Consensus 검색·fetch와 원문 메타데이터 검증 범위를 구분했다. 논문 원문이나 가중치를 재배포하지 않는다.

[병합 안내](MERGE_TRIAD.md) · [변경 기록](CHANGELOG-TRIAD.md)
