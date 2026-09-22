# 폐루프 연구 실험실 v1.1.0

[English](README.en.md) · [기존 연구](../README.md) · [실험 화면](../index.html)

관측·가정·개입의 분리를 실제로 시험하는 **합성 연구 모듈**이다. 원 연구 01~08은 보존되며 실제 생명·뇌과학 모델이나 프로덕션 모델의 완성이 아니다.

| 먼저 읽을 자료 | 내용 |
|---|---|
| [09 구현 명세](docs/ko/09_IMPLEMENTATION.md) | 코드 구조, 수식, 사용 방법, 경계 |
| [10 실행 프로토콜](docs/ko/10_EVALUATION_PROTOCOL.md) | 비교 셀, 비용, 누수 방지, 지표 |
| [11 파일럿 결과](docs/ko/11_PILOT_RESULTS.md) | 전체 셀 결과와 실패 해석 |
| [12 후속 연구](docs/ko/12_RESEARCH_DIRECTION.md) | H1~H6 상태, 다음 질문과 반증 조건 |
| [QA](quality/QA.md) | 실제 수행한 검사와 미검증 범위 |

```bash
python -m pip install -r research/requirements.txt
python -m research.closed_loop serve
```

저장소 루트에서 실행한 뒤 `http://127.0.0.1:8765`를 연다. API key, GPU, 별도 데이터셋이 필요하지 않다. Python 없이 `index.html`을 열면 수록된 시드 0 기록과 12개 시드 통계를 본다. 이 정적 재생은 새 계산이 아니다. Chrome/Edge/Firefox 등 `DecompressionStream` 지원 브라우저를 사용한다.

전체 실험은 [config](configs/pilot.json)에 따라 504개 실행을 저장한다. 반복 계산은 `python -m research.closed_loop suite`, 한 실행은 `python -m research.closed_loop run`, 무결성 검사는 `python -m research.closed_loop audit <경로>`다. `.json.gz`는 CLI에서 직접 읽을 수 있고, UI의 JSON 가져오기는 압축하지 않은 상세 기록을 사용한다.

[전체 요약](results/pilot/summary.json) · [동결 실행 행렬](results/pilot/protocol.lock.json) · [원본 보존 manifest](baseline/manifest.json) · [구현 출처](SOURCES.md)

저장소의 기존 공개 라이선스 미선택 상태를 유지했다. 실행용 코드를 추가했다는 이유로 기존 자료·제3자 자료에 새 라이선스를 임의로 부여하지 않았다. 원격 GitHub 업로드·Pages 배포·Actions 실행은 이 패키지 자체가 수행하지 않는다.
