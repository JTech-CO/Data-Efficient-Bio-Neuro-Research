# Implementation sources and attribution

This addendum is implementation and experimental evidence, not a replacement literature review. Original research sources remain in the [bibliography](../references/BIBLIOGRAPHY.md). Results in research/results were computed by the included code, not quoted from these sources.

Official technical documentation checked during implementation on 2026-09-22:

- [SciPy cho_solve](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.cho_solve.html): solving with a Cholesky factor.
- [NumPy parallel random generation / SeedSequence](https://numpy.org/doc/stable/reference/random/parallel.html): deterministic stream construction. The implementation derives query-specific inputs with SHA-256; it does not claim NumPy supplies biological independence.
- [python-jsonschema validation](https://python-jsonschema.readthedocs.io/en/stable/validate/): Draft 2020-12 validation interfaces.
- [GitHub Python build/test workflow](https://docs.github.com/en/actions/tutorials/build-and-test-code/python): workflow structure. Actions configuration is supplied; remote execution was not observed.
- [MDN DecompressionStream](https://developer.mozilla.org/en-US/docs/Web/API/DecompressionStream): native gzip decoding for the self-contained static result bundle.

The Bayesian linear update, finite-library information objective, and additive joint GP are explicit implementations of established constructions. Their combination and developmental gates are not claimed as a new theorem or a scientifically validated new algorithm. All numerical thresholds and synthetic truth functions are inspectable in source and config.
