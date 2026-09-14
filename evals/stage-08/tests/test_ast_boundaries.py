import ast
import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGE08_DIR = HERE.parent
sys.path.insert(0, str(STAGE08_DIR))

from canonical import canonical_digest, canonical_json, verify_attestation

FORBIDDEN_MODULES = {
    # No premature distributed infrastructure / databases
    "redis", "psycopg2", "asyncpg", "sqlalchemy", "celery", "kafka", "dbos", "docker", "kubernetes",
    # No direct production apps import
    "apps",
    # No ambient out-of-band networking in core evaluation code
    "requests", "httpx", "urllib.request", "aiohttp", "socket",
}

FORBIDDEN_CALLS = {
    "eval", "exec", "__import__", "os.system", "subprocess.call", "subprocess.Popen"
}

class ASTBoundaryTests(unittest.TestCase):
    def get_py_files(self):
        py_files = []
        for root, _, files in os.walk(STAGE08_DIR):
            for f in files:
                if f.endswith(".py"):
                    py_files.append(Path(root) / f)
        return py_files

    def test_no_forbidden_imports_in_evaluation_package(self):
        """Ensures evaluation logic remains pure, local, and isolated from premature infra or ambient networking."""
        violations = []
        for file_path in self.get_py_files():
            tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        base = alias.name.split(".")[0]
                        if base in FORBIDDEN_MODULES:
                            violations.append((file_path.name, node.lineno, base))
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        base = node.module.split(".")[0]
                        if base in FORBIDDEN_MODULES:
                            violations.append((file_path.name, node.lineno, base))
        self.assertEqual(violations, [], f"Forbidden imports detected: {violations}")

    def test_no_dangerous_dynamic_code_execution(self):
        """Ensures no dangerous dynamic code execution (eval, exec) exists in evaluation code."""
        violations = []
        for file_path in self.get_py_files():
            tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    func_name = ""
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                    elif isinstance(node.func, ast.Attribute):
                        if isinstance(node.func.value, ast.Name):
                            func_name = f"{node.func.value.id}.{node.func.attr}"
                    if func_name in FORBIDDEN_CALLS:
                        violations.append((file_path.name, node.lineno, func_name))
        self.assertEqual(violations, [], f"Dangerous dynamic execution detected: {violations}")

    def test_no_tautological_constant_assertions_in_tests(self):
        """Detects circular/pseudo-assertions (e.g. self.assertEqual('a', 'a')) in test files."""
        violations = []
        for file_path in (STAGE08_DIR / "tests").glob("*.py"):
            tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if node.func.attr in {"assertEqual", "assertIs"}:
                        if len(node.args) >= 2:
                            arg0, arg1 = node.args[0], node.args[1]
                            # Check if both arguments are exact same constant literal (tautology)
                            if isinstance(arg0, ast.Constant) and isinstance(arg1, ast.Constant):
                                if arg0.value == arg1.value:
                                    violations.append((file_path.name, node.lineno, arg0.value))
        self.assertEqual(violations, [], f"Circular constant assertions detected: {violations}")

    def test_canonical_rfc8785_attestation_determinism(self):
        """Verifies deterministic key sorting and attestation verification under permutation."""
        dict_a = {"z": 1, "a": 2, "m": {"nested_b": [3, 2, 1], "nested_a": True}}
        dict_b = {"a": 2, "m": {"nested_a": True, "nested_b": [3, 2, 1]}, "z": 1}

        self.assertEqual(canonical_json(dict_a), canonical_json(dict_b))
        digest_a = canonical_digest(dict_a)
        digest_b = canonical_digest(dict_b)
        self.assertEqual(digest_a, digest_b)
        self.assertTrue(verify_attestation(dict_a, digest_b))
        self.assertFalse(verify_attestation(dict_a, "0" * 64))

if __name__ == "__main__":
    unittest.main()
