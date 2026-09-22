# 후속 연구 v1.2.0-research.1

[English](FOLLOWUP.en.md) · [연구 결과 화면](research/followup/web/index.html) · [새 설계](research/docs/ko/13_FOLLOWUP_DESIGN.md) · [전체 결과](research/docs/ko/15_FOLLOWUP_RESULTS.md) · [다음 결정](research/docs/ko/16_RESEARCH_DECISIONS.md)

## 무엇을 추가했는가

관측·가정·개입을 구분한 기존 연구의 A/B 작업을 구현했다. **실제 생물 관측·학습 모델·임상 진단 시스템은 없다.** 센서 gain·offset과 잠재 반응 계수의 혼동, 반복 측정의 잡음 추정, 진단 오경보, 교정 표준의 전달 실패를 합성 세계로 연구한다.

40개 개발 실행과 정상 2,000개 교정 궤적 뒤 로컬 프로토콜을 고정했다. 연구 A는 1,900개 진단 궤적(정상 1,000 + 오류 9종 각 100), 연구 B는 320개 세계 × 여섯 정책 = 1,920회다. 실제 생물학적 표본 수는 0이다. 결과를 보고 수치 코어나 threshold를 바꾸지 않았다. 로컬 해시는 독립 사전등록이 아니다.

## 먼저 확인할 결과

정상 세계의 경고율은 단순 반복 38.5%, Bonferroni 5.5%, 최대통계 교정 6.1%였다. 오류를 덜 경고하는 것이 원인 식별을 해결한 것은 아니다. 표준·표본의 센서가 다른 세계는 보정 검정 경고가 4%였고, 고정 진단 지점 사이의 국소 오류는 기전 채널 적중이 0%였다. 블록 정보이득도 공동 정보이득을 항상 이기지 않았다. 세부 지표, 실패·비용·같은 데이터 추정기 비교를 모두 결과 문서에 공개했다.

## 화면 보기와 계산은 다르다

압축을 모두 푼 뒤 `research/followup/web/index.html`을 열면 저장된 연구 A/B 표와 60개 대표 실행(index 20000)을 검토하는 구조다. 이 화면은 **정적 뷰어**이며 새 학습 버튼이나 Python 계산 API를 가장하지 않는다. 32개 세계 평균과 개별 실행 그림을 분리했다. 기존 루트 `index.html`과 v1.1 실험실은 그대로다.

현재 실행 환경은 브라우저의 file/localhost URL 이동을 관리 정책으로 차단했다. 따라서 화면 자산 주입 검증과 별도 HTTP 전송 검증을 수행했다. 사용자 PC에서 직접 열리는 전체 경로나 브라우저 다운로드 완료를 여기서 검증했다고 말하지 않는다. [QA](research/followup/quality/QA.md)

## 새 합성 실험

저장소 루트에서 다음을 실행한다. 외부 API 키·GPU·모델 가중치·데이터셋은 필요 없다.

```bash
python -m pip install -r research/requirements.txt
python -m research.diagnostic_loop demo --scenario gain_offset --policy block_targeted --seed 27 --out research/followup/results/my-demo.json
```

같은 출력 경로는 덮어쓰지 않는다. `demo`는 별도 공개 demo bank를 쓰며 잠긴 평가 bank를 수정하지 않는다. 새 결과는 JSON 파일로 읽으며, 이 버전 뷰어에는 임의 JSON 업로드 기능이 없다.

전체 프로토콜을 새 폴더에서 재현한다.

```bash
python -m research.diagnostic_loop prepare --out research/followup/results/new-study
python -m research.diagnostic_loop evaluate --out research/followup/results/new-study
python -m research.diagnostic_loop verify-lock --out research/followup/results/new-study
```

`prepare`는 먼저 40개 개발 실행과 2,000개 교정 궤적을 계산한다. 여러 BLAS 스레드의 과잉 병렬화를 피하려면 실행 환경에 `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`을 설정할 수 있다. 복제 환경은 [환경 기록](research/followup/quality/environment.json)을 확인한다. 정확한 패키지 버전 파일은 동일 환경 재현 보조용이며 모든 OS의 설치 가능성을 검증한 것은 아니다.

## 검증 명령

```bash
python -m unittest discover -s research/followup/tests -v
python -m unittest discover -s research/tests -v
python -m unittest discover -s tests -v
python research/followup/validate_followup.py
```

43개 신규 + 63개 이전 연구 + 14개 원 테스트가 통과했다. 원시 기록 413,978건의 구조·비용·출처, 수집 1,920개의 순서·해시, 진단 1,900개의 검정, 모든 요약을 재검산했다. 관측 건수는 정책 간 반복 사용도 포함한 검증 건수이지 독립 증거의 수가 아니다. 60개 수집 기록과 10개 진단 궤적을 완전히 재실행했다.

## 병합과 보존

기준 ZIP은 `Data-Efficient-Bio-Neuro-Research_v1.1.0_Closed-Loop-Lab_KO-EN.zip`이다. 다른 `research_lab/` 경로를 쓰는 오래된 대안 버전과 섞지 않는다. [병합 안내](MERGE_FOLLOWUP.md)를 확인한다. 원격 GitHub를 조회·수정·배포하지 않았다. 새 문서 13~17장은 `research/docs/ko/`, `research/docs/en/`에 있으며, 기존 01~12 계획과 결과는 변경하지 않았다. 라이선스는 기존 [LICENSE](LICENSE.md)의 범위를 따른다.
