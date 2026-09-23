# 추가 패키지 병합 / Additive package merge

기준은 `Data-Efficient-Bio-Neuro-Research_v1.3.0_Transport-Audit-Noise_KO-EN.zip`이다. 원격 GitHub의 최신 상태를 조회·수정하지 않았다.

1. 현재 저장소를 백업한다. 이전 ZIP 이후의 로컬 변경이 있으면 먼저 diff한다.
2. 추가분 ZIP을 임시 폴더에 풀고 동일한 저장소 루트 아래로 병합한다.
3. 변경되는 기존 파일은 `README.md`, `README.en.md`, `CHECKSUMS.sha256` 세 개뿐이다. 원문은 `research/bounded/baseline/`에 보존한다.
4. `VERSIONS.md` / `VERSIONS.en.md`가 버전별 탐색의 기준이다. 이전 README 본문을 새 README에 다시 붙이지 않는다.
5. 생성 로그·캐시와 원격 변경 때문에 로컬 해시가 달라질 수 있다. 수록 체크섬은 배포한 바이트의 무결성 목록이지 로컬 변경 금지 장치가 아니다.

The overlay targets the exact v1.3.0 Transport-Audit-Noise package. Merge into a backup or compare local changes first. Only the two READMEs and checksum file change among baseline files. New code and documentation live under `research/bounded_loop/`, `research/bounded/`, and chapters 25–31. Existing research modules and results are preserved. No remote GitHub commit or deployment was performed.
