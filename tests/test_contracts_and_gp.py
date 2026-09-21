from __future__ import annotations
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path
import numpy as np
from jsonschema import Draft202012Validator, FormatChecker
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("demo", ROOT / "examples/gp_active_learning_demo.py")
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


class TestGP(unittest.TestCase):
    def test_kernel_symmetric_positive(self):
        x = np.array([0.0, 0.2, 0.7, 1.0])
        k = demo.kernel(x, x)
        np.testing.assert_allclose(k, k.T)
        self.assertGreater(np.linalg.eigvalsh(k).min(), 0)

    def test_bad_length_scale(self):
        with self.assertRaises(ValueError):
            demo.kernel(np.array([0.]), np.array([1.]), -1)

    def test_predict_shapes_and_bounds(self):
        mean, var = demo.predict(np.array([0., 1.]), np.array([0., 0.]), np.linspace(0, 1, 20))
        self.assertEqual(mean.shape, (20,))
        self.assertTrue(np.all((var >= 0) & (var <= 1)))

    def test_more_locations_reduce_variance(self):
        q = np.linspace(0, 1, 30)
        _, v1 = demo.predict(np.array([0., 1.]), np.zeros(2), q)
        _, v2 = demo.predict(np.array([0., .5, 1.]), np.zeros(3), q)
        self.assertTrue(np.all(v2 <= v1 + 1e-10))

    def test_input_shape_rejection(self):
        with self.assertRaises(ValueError):
            demo.predict(np.array([0., 1.]), np.array([0.]), np.array([.5]))

    def test_nonfinite_rejection(self):
        with self.assertRaises(ValueError):
            demo.predict(np.array([0., 1.]), np.array([0., np.nan]), np.array([.5]))

    def test_acquisition_records_unique(self):
        records = demo.one_run(4, "smooth", "max_variance")
        for r in records:
            self.assertEqual(len(set(r["selected_indices"])), r["n_queries"])

    def test_identifiability_counterexample(self):
        x = np.linspace(-1, 1, 31)
        d = np.column_stack((x, x))
        self.assertEqual(np.linalg.matrix_rank(d), 1)
        np.testing.assert_allclose(d @ [1, 2], d @ [2, 1])


class TestSchemas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads((ROOT / "schemas/observation.schema.json").read_text())
        cls.validator = Draft202012Validator(schema, format_checker=FormatChecker())
        cls.record = json.loads((ROOT / "schemas/examples/observation.valid.json").read_text())

    def test_valid_synthetic(self):
        self.assertTrue(self.validator.is_valid(self.record))

    def test_reject_synthetic_as_new_biology(self):
        record = copy.deepcopy(self.record)
        record["counts_as_new_biological_unit"] = True
        self.assertFalse(self.validator.is_valid(record))

    def test_generated_requires_parent(self):
        record = copy.deepcopy(self.record)
        record["kind"] = "generated"
        self.assertFalse(self.validator.is_valid(record))

    def test_test_fitted_producer_rejected(self):
        record = copy.deepcopy(self.record)
        record["producer"]["fit_split"] = "test"
        self.assertFalse(self.validator.is_valid(record))

    def test_real_new_unit_needs_group(self):
        record = copy.deepcopy(self.record)
        record["kind"] = "real"
        record["counts_as_new_biological_unit"] = True
        del record["producer"]
        self.assertFalse(self.validator.is_valid(record))
        record["independent_group_id"] = "illustrative-donor-1"
        self.assertTrue(self.validator.is_valid(record))

    def test_valid_model_card(self):
        schema = json.loads((ROOT / "schemas/model_card.schema.json").read_text())
        record = json.loads((ROOT / "schemas/examples/model_card.valid.json").read_text())
        self.assertTrue(Draft202012Validator(schema).is_valid(record))


if __name__ == "__main__":
    unittest.main()
