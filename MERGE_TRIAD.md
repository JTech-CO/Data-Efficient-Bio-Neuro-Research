# v1.3 병합 / Merge v1.3

기준은 `Data-Efficient-Bio-Neuro-Research_v1.2.0_Diagnostic-Research_KO-EN.zip`이다. 다른 `research_lab/` 대안 구현이나 원격 저장소의 최신 변경을 자동 병합하지 않는다.

The exact baseline is the v1.2 Diagnostic-Research ZIP, not an older alternative `research_lab/` implementation or a freshly fetched remote repository.

전체 ZIP은 새 폴더에서 바로 사용할 수 있다. 추가분 ZIP은 기준 v1.2에만 덮어씌우면 동일한 전체 파일 집합을 만든다. 기준 이후 수정한 저장소라면 임시 폴더에서 비교하고 README·체크섬을 수동 병합한다. 로컬 변경을 자동 삭제하는 스크립트는 포함하지 않았다.

The full ZIP is self-contained. Overlay the additive ZIP only onto the exact baseline to obtain the identical full tree. Compare in a temporary directory and reconcile README/checksum changes when your repository has later edits. No script automatically deletes local changes.

기존825파일 중 README 두 개와 루트 체크섬만 갱신한다. 원본 세 파일은 `research/triad/baseline/v120/`에 보존하고 모든 기준 파일 해시를 manifest에 기록했다. 기존 계획 01~17, 코드, 실험 자료, 뷰어는 변경하지 않는다. 원격 GitHub 커밋·업로드·배포는 수행하지 않았다.

Of825 baseline files, only two root READMEs and the root checksum list are updated. Their originals and a complete baseline manifest are retained. Chapters01–17, old code, outputs, and viewers remain unchanged. No remote GitHub commit, upload, or deployment was performed.
