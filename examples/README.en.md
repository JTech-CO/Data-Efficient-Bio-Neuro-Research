# Educational synthetic GP example

**Zero biological/neural observations. No external data or model downloads. This is not reproduction of a reviewed paper.**

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r examples/requirements-tested.txt
python examples/gp_active_learning_demo.py --seeds 20
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

A fixed stationary RBF GP models a smooth function and a function with an added narrow peak. Policies share initialization, measurement noise, and budget at each seed. Random acquisition is compared with maximum latent variance. Acquisition never accesses test targets. With fixed kernel and homoscedastic noise, variance acquisition depends on observation locations rather than y values; it does not represent all GP active learning.

Source settings are noise SD 0.06, length scale 0.18, budgets 6/10/18/30, and 20 seeds. There is no hyperparameter optimization, multifidelity model, conformal procedure, PINN, or biological fine-tuning. The narrow-peak case deliberately violates the representation's smoothness assumptions.

The run writes 320 budget-level records, 16 aggregate rows, environment metadata, four plots, and an identifiability counterexample. Errors use a locked synthetic grid. Coverage is empirical pointwise inclusion of the noiseless latent truth in nominal 95% intervals; it is not a population-level or clinical guarantee. Across-seed SDs are in JSON; plots show mean curves only.

In `y=(a+b)x`, the design rank is one for two parameters: identical predictions do not identify the original coefficients.

[Executed results](RESULTS.en.md) · [한국어](README.ko.md)
