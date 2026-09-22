# 같은 저장소에 적용 / Apply within the same repository

## 한국어

전체 ZIP은 이전 연구 자료와 새 모듈을 포함한다. 추가분 ZIP은 기존 패키지와 비교해 추가되거나 바뀐 경로만 포함한다. **둘 다 동일한 `Data-Efficient-Bio-Neuro-Research/` 루트 구조**이며 새 저장소를 요구하지 않는다.

기존 저장소를 백업하거나 현재 변경사항을 commit한 다음, 압축 내부 루트의 내용을 저장소 루트에 합친다. 중첩된 `Data-Efficient-Bio-Neuro-Research/Data-Efficient-Bio-Neuro-Research/` 폴더를 만들지 않는다. 원 01~08과 문헌 자료는 추가분 ZIP에 포함되지 않아 덮어쓰지 않는다. 루트 README 2개와 현재 checksum은 갱신한다.

이 업데이트의 기준은 이 대화에서 전달한 2026-09-22 ZIP이다. 사용자가 이후 원격 저장소에서 별도로 수정한 파일을 조회하거나 병합한 것은 아니다. 그런 변경이 있으면 특히 README의 차이를 검토한다. 적용 후 `python research/validate_research.py`로 기준 원본 보존과 파일럿 일관성을 검사한다. 원래 연구 문서를 의도적으로 수정했다면 보존 검사 실패를 무시하지 말고 별도 연구 버전으로 기록한다.

`index.html`이 정적 입구이고 `lab/`와 수록 데이터도 함께 있어야 한다. GitHub Pages로 게시하는 경우 저장소의 루트 파일이 정적으로 제공되도록 설정한다. Python 서버나 새 실험 계산은 Pages에서 실행되지 않는다. 배포 설정 변경이나 원격 push는 이 패키지가 수행하지 않았다.

## English

The full ZIP includes the original research plus the new module. The additive ZIP includes only added or changed paths. Both use the same `Data-Efficient-Bio-Neuro-Research/` root; a new repository is not required.

Back up or commit local changes, then merge the archive root contents into the existing repository root. Avoid a duplicate nested directory. The additive ZIP does not overwrite unchanged original research chapters or source material. It updates two root READMEs and the current checksum file.

The baseline is the 2026-09-22 ZIP supplied in this conversation. Later remote edits were not fetched or merged; review such changes, especially README edits. After merging, run `python research/validate_research.py`. Intentional changes to original research require a new documented baseline rather than ignoring preservation errors.

`index.html`, `lab/`, and the bundled data form the static entry. A root-based GitHub Pages deployment can serve these files, but cannot run the Python API or new computations. No remote push or deployment configuration change was performed.
