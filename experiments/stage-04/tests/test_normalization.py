import json, sys, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from catalog import load_catalog
from mapper import map_observation
from units import normalize_unit, convert_value
from comparability import classify

CATALOG=load_catalog(HERE/'terminology_catalog.json')

class MappingTests(unittest.TestCase):
    def test_method_disambiguates_le(self):
        a=map_observation({"local_test_name":"LE","system":"urine","scale":"ord","method":"test_strip","unit_source":None},CATALOG)
        b=map_observation({"local_test_name":"LE","system":"urine","scale":"ord","method":"test_strip_automated","unit_source":None},CATALOG)
        self.assertEqual(a["validated_code"],"5799-2")
        self.assertEqual(b["validated_code"],"60026-2")

    def test_missing_method_is_candidate_not_validated(self):
        r=map_observation({"local_test_name":"LE","system":"urine","scale":"ord","method":None,"unit_source":None},CATALOG)
        self.assertEqual(r["status"],"candidate")
        self.assertEqual(sorted(r["candidate_codes"]),["5799-2","60026-2"])

    def test_unknown_is_unmapped(self):
        r=map_observation({"local_test_name":"unknown marker","system":"urine","scale":"ord","method":"test_strip","unit_source":None},CATALOG)
        self.assertEqual(r["status"],"unmapped")

class UnitTests(unittest.TestCase):
    def test_hpf_normalizes(self):
        self.assertEqual(normalize_unit("/HPF"),"/[HPF]")

    def test_safe_linear_conversion(self):
        r=convert_value(30,"mg/dL","g/L")
        self.assertEqual(r["status"],"converted")
        self.assertAlmostEqual(r["value"],0.3)

    def test_molar_conversion_rejected(self):
        r=convert_value(30,"mg/dL","mmol/L")
        self.assertEqual(r["status"],"rejected")

class ComparabilityTests(unittest.TestCase):
    def test_same_code_convertible_units(self):
        r=classify({"status":"validated","code":"5804-0","unit":"mg/dL"},{"status":"validated","code":"5804-0","unit":"g/L"})
        self.assertEqual(r,"CONVERTIBLE_COMPARABLE")

    def test_related_methods_not_comparable(self):
        r=classify({"status":"validated","code":"5799-2","unit":None},{"status":"validated","code":"60026-2","unit":None})
        self.assertEqual(r,"RELATED_NOT_COMPARABLE")

    def test_candidate_is_indeterminate(self):
        r=classify({"status":"candidate","code":None,"unit":None},{"status":"validated","code":"5799-2","unit":None})
        self.assertEqual(r,"INDETERMINATE")

if __name__=='__main__': unittest.main()
