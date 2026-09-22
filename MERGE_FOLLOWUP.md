# 후속 연구 병합 / Merging the follow-up

기준은 `Data-Efficient-Bio-Neuro-Research_v1.1.0_Closed-Loop-Lab_KO-EN.zip`이다. 전체 ZIP과 추가분 ZIP은 같은 `Data-Efficient-Bio-Neuro-Research/` 루트를 사용한다.

전체 ZIP은 별도 디렉터리에 풀어 비교하는 것이 안전하다. 추가분은 기준 v1.1 폴더 위에 적용한다. 이전 답변의 `research_lab/` 대안 패키지에 적용하지 않는다. 원격에서 변경한 파일이 있다면 먼저 diff로 확인하고 병합한다. 강제 덮어쓰기나 git reset 명령은 제공하지 않는다.

기준 626개 파일 중 623개는 같은 경로에서 바이트 동일하다. README.md·README.en.md에는 새 입구를 덧붙였고 CHECKSUMS.sha256은 새 파일 목록으로 교체했다. 이 세 원본은 `research/followup/baseline/`에 바이트 그대로 보존한다. 기존 연구 문서 01~12, 코드, 504개 결과, 기존 웹앱은 변경하지 않는다. baseline 안의 보존 README는 바이트 비교 목적이며 상대 링크를 새 위치에 맞춰 수정하지 않았다.

The base is the **Closed-Loop-Lab** v1.1 archive above, not an older research_lab alternative. Full and additive archives share the same repository root. Inspect differences before applying over a remotely modified checkout. No destructive reset or forced overwrite is required.

Of 626 base files, 623 remain byte-identical at their original paths. The two root READMEs receive an additive entry, and the root checksum inventory is regenerated. Byte-exact copies of all three original files remain under research/followup/baseline. Earlier chapters 01–12, code, results and viewer are untouched. Archived README links intentionally retain their original bytes.

[보존 해시 / Preservation hashes](research/followup/baseline/manifest.json) · [새 시작점 / New entry](FOLLOWUP.md) · [English entry](FOLLOWUP.en.md)

An automated comparison of base + additive payload versus the full payload is recorded in the packaging validation. No GitHub commit, push or deployment was performed.
