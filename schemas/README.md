# Schema scope / 스키마 범위

The JSON Schemas enforce structure and selected provenance constraints, not scientific truth. Synthetic or derived records cannot count as new independent biological units. Fitted producers cannot declare a fitting split of `test`; external pretraining is explicitly represented. Generated, imputed and derived observations require parents.

스키마는 데이터가 진짜인지, 동의가 유효한지, 모든 계보가 완전한지를 증명하지 않는다. 파일 간 parent resolution, group별 중복 집계, preprocessing 누수, 라이선스 판단은 별도 audit가 필요하다. `counts_as_new_biological_unit`는 집단별 대표 레코드에만 부여해야 하며, 실제 독립 표본 수는 group 식별자로 교차 점검한다.

`observation.invalid.json` is intentionally invalid: it tries to count a simulated value as a new biological unit. This negative fixture must be rejected by validation tests. / invalid 파일은 의도적으로 잘못된 테스트다.
