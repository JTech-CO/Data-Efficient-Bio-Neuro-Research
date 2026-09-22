# 17. 재현·검증·범위 기록

[English](../en/17_REPRODUCTION_QA.md) · [시작점](../../../FOLLOWUP.md) · [결과](15_FOLLOWUP_RESULTS.md) · [QA 원문](../../followup/quality/QA.md)

## 재현 단위

배포된 결과는 v1.2.0-research.1의 잠긴 합성 평가다. 출처와 원시 결과는 `research/followup/results/v120/`에 있다. `protocol.lock.json`은 코드·설정·정상 교정 bank의 SHA-256을 고정한다. 모델의 source/config 변경 뒤에는 동일 bank를 검증된 새 버전이라고 재사용하지 않는다.

```bash
python -m pip install -r research/requirements.txt
python -m research.diagnostic_loop verify-lock --out research/followup/results/v120
python research/followup/validate_followup.py
```

새 공개 demo는 잠긴 평가를 바꾸지 않는다.

```bash
python -m research.diagnostic_loop demo --scenario reference_mismatch --policy block_targeted --seed 27 --out research/followup/results/my-demo.json
```

전체 연구 재실행은 [시작점](../../../FOLLOWUP.md)의 prepare/evaluate 명령을 사용한다. 처리 중단 이후 무조건 새 평가로 시작하지 않는다. 동봉 `execute_shards.py`는 **진단 단계가 끝난 뒤 수집 셀이 중단된 경우**를 복구하는 한정된 실행 보조 도구다. 그것이 임의 단계의 완전한 분산 실행기라는 주장은 하지 않는다. 사용 경계는 파일 docstring과 실행 메타데이터를 확인한다.

## 실제 통과한 검사

| 검사 | 실제 범위 |
|---|---|
| 신규 단위·통합 테스트 | 43개 |
| 이전 research 테스트 | 63개 |
| 최초 연구 테스트 | 14개 |
| 진단 원시 궤적 | 1,900개, 세 탐지기 모두 재계산 |
| 수집 원시 실행 | 1,920개, 스키마·예산·분할·승인·hash chain·freeze·최종 test 순서 |
| 직렬화 관측 레코드 | 413,978건, 비용·출처·반복 계보. 독립 표본 수 아님 |
| 원 결과 재생산 | 진단 10개 + 수집 60개 전체 해시 동일 |
| 요약 | 모든 원시 결과에서 compact records와 summary.json 정확히 재생성 |
| 브라우저 자산 | 80개 검사, 60개 시나리오/정책 조합, 한·영·모바일·개입 그림·표 |

로그는 `research/followup/quality/`에 있다. 자동 테스트가 실제 생물학적 가정, 외부 도메인 성능, 보안 공격 차단, 임상적 사용을 인증하지 않는다.

## 브라우저 검사에서 하지 못한 것

이 환경의 Chromium 관리 정책이 file 및 localhost URL 이동을 `ERR_BLOCKED_BY_ADMINISTRATOR`로 막았다. 정책을 우회하거나 해제하지 않았다. 배포할 실제 CSS·JS·HTML·bundle을 빈 브라우저 페이지에 주입해 DOM·이벤트·그림을 검사했고, 별도 Python HTTP 서버와 HTTP 요청으로 네 파일의 바이트 전송을 확인했다.

따라서 네이티브 file 이동, 브라우저에서 실제 HTTP를 탐색한 전체 흐름, 브라우저 다운로드 완료, 원격 GitHub Pages는 검증하지 않았다. Windows/macOS Python 설치도 직접 시험하지 않았다. 화면 미리보기는 이 자산 주입 방식으로 렌더링한 것이다. 새 뷰어는 원래 정적 모드이며 Python 계산 API가 존재한다고 하지 않는다.

## 저장소 보존

기준 v1.1 전체 ZIP은 626개 파일(기존 체크섬 자체 포함)이다. 원 경로 623개는 바이트 그대로 보존하고 두 README에는 새 안내만 덧붙였으며 root CHECKSUMS는 재작성했다. 이 세 원본은 baseline에 보관했다. 기존 01~12 연구 문서, 기존 504개 결과와 코드, 기존 웹 실험실은 바꾸지 않았다.

`research/followup/baseline/manifest.json`에는 기준 ZIP 자체와 모든 기준 파일의 해시가 있다. 추가분 적용 후 전체 ZIP과 동일한 payload가 되는지 별도로 검사한다. baseline 안의 원문 사본은 상대 링크를 재배치하지 않은 기록물이므로 현재 문서 링크 검사에서 제외한다. 원 논문 PDF나 모델 가중치는 재배포하지 않았다.

## 해석상 제한

정상 세계의 오경보율은 귀무모형·정규성·동분산·유한 look 조건에 의존한다. 국소 delta 정보이득은 exact nonlinear mutual information이 아니다. 교정 불확실성은 1차 근사이고 잡음 분산은 plug-in이다. 참값은 synthetic evaluator만 사용했다. 세계 ID와 기저를 분리했어도 외부 맹검·사전등록이 아니며, 평가의 기저는 모델에 공개돼 있다. 진단 패널에서의 통과를 전체 영역이나 표본 내 교정의 인증으로 해석하지 않는다.
