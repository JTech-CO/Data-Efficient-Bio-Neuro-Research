# 교육용 합성 GP 예제

**생물·뇌 데이터 0개. 외부 모델·데이터 다운로드 없음. 이 예제는 연구 논문의 재현이 아니다.**

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r examples/requirements-tested.txt
python examples/gp_active_learning_demo.py --seeds 20
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

하나의 고정 stationary RBF GP로 부드러운 함수와 좁은 peak가 추가된 함수를 추정한다. 초기점·측정잡음·예산은 같은 seed에서 정책 간 공유한다. Random과 maximum latent variance acquisition을 비교한다. acquisition은 테스트 정답을 보지 않는다. 고정 kernel과 동분산 조건에서 variance 정책은 관측 y가 아닌 관측 위치에 의존한다. 이는 일반적인 모든 GP active learning을 대표하지 않는다.

노이즈 표준편차 0.06, length scale 0.18, 예산 6/10/18/30, 20 seeds를 소스에 명시했다. hyperparameter 최적화·멀티피델리티·conformal·PINN·바이오 fine-tuning은 하지 않는다. Narrow peak 시험은 표현 가정 불일치를 의도적으로 만든 시험이다.

출력은 320개 budget-level 기록, 16개 집계 행, 환경 metadata, 그래프 4개, 식별가능성 반례다. 그래프의 error는 잠긴 synthetic grid에서 계산하며, coverage는 관측잡음이 없는 true latent function에 대한 pointwise 명목 95% 구간의 경험적 포함률이다. 개체 모집단의 통계적 보장이나 임상 calibration 결과가 아니다. seed 표준편차는 JSON에 있으며, 그래프는 평균선만 표시한다.

`y=(a+b)x`의 행렬 rank는 1이지만 파라미터는 2개다. prediction이 같아도 원 파라미터가 구분되지 않는다는 수학적 예시다.

[실행 결과](RESULTS.ko.md) · [English](README.en.md)
