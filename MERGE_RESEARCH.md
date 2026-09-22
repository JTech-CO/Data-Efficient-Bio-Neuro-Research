# Applying this extension / 동일 저장소에 적용

This is an extension of the previously supplied `Data-Efficient-Bio-Neuro-Research` package, not a new independent research repository.

The full ZIP contains the original research plus the new slice. The overlay ZIP contains only added files and the three intentionally updated original paths: `README.md`, `README.en.md`, `CHECKSUMS.sha256`. Both archives have the same top-level directory name.

1. Keep a backup or commit of the current working tree.
2. Extract to a temporary folder first. Compare against your working tree; do not overwrite uncommitted local changes blindly.
3. Copy the extension into the existing repository root. Keep its existing `.git` directory and remote configuration. Neither archive contains a `.git` directory.
4. The two README changes only append links. If your READMEs have changed since the original package, merge that new section manually. The baseline validator will flag other original-file differences; it does not delete them.
5. Run the commands in [RESEARCH_LAB.md](RESEARCH_LAB.md), inspect the new results and commit the intended additions using your normal Git workflow.

기존 연구 문서·예제·원본 스키마는 그대로 두고 `research_lab/`과 09~12장 등을 추가한다. 제공된 원본 ZIP을 기준으로 만든 변경분이므로 그 후 저장소에서 별도 수정한 파일이 있다면 먼저 비교·병합해야 한다. 원격 저장소의 현재 상태는 조회·수정하지 않았다.

A SHA-256 baseline manifest preserves the original package identity; it is not proof that this package matches subsequent remote edits. No remote GitHub commit or upload was performed.
