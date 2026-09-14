import sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from stats import zero_failure_upper_bound,zero_failure_required_n,wilson_interval,cohens_kappa

class StatsTests(unittest.TestCase):
    def test_zero_failure_24_not_zero_risk(self):
        u=zero_failure_upper_bound(24)
        self.assertGreater(u,0.11)
        self.assertLess(u,0.12)

    def test_n_for_one_percent(self):
        n=zero_failure_required_n(0.01)
        self.assertEqual(n,299)

    def test_wilson_inside_unit_interval(self):
        lo,hi=wilson_interval(2,10)
        self.assertGreaterEqual(lo,0)
        self.assertLessEqual(hi,1)
        self.assertLess(lo,hi)

    def test_kappa_perfect(self):
        self.assertEqual(cohens_kappa(["a","b"],["a","b"]),1.0)

if __name__=="__main__":
    unittest.main()
