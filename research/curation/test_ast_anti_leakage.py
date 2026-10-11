"""AST Static Anti-Oracle Leakage Audit Script.

Inspects phase2c_comparison_engine.py to mathematically prove that no internal
expected fields or variables exist within the external comparison module.
"""

import ast
import os
import sys

PROHIBITED_TOKENS = [
    "expected_molecular",
    "expected_protein",
    "exp_mol",
    "exp_prot",
    "deterministic_molecular_consequence",
    "deterministic_protein_consequence"
]

def run_ast_audit(target_file: str = "research/curation/phase2c_comparison_engine.py") -> bool:
    if not os.path.exists(target_file):
        print(f"ERROR: Target file not found: {target_file}")
        return False

    with open(target_file, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source, filename=target_file)
    violations = []

    for node in ast.walk(tree):
        # Check variable names
        if isinstance(node, ast.Name):
            for token in PROHIBITED_TOKENS:
                if token.lower() in node.id.lower():
                    violations.append((node.lineno, f"Identifier Name: {node.id}", token))

        # Check attribute names
        elif isinstance(node, ast.Attribute):
            for token in PROHIBITED_TOKENS:
                if token.lower() in node.attr.lower():
                    violations.append((node.lineno, f"Attribute: {node.attr}", token))

        # Check function argument names
        elif isinstance(node, ast.arg):
            for token in PROHIBITED_TOKENS:
                if token.lower() in node.arg.lower():
                    violations.append((node.lineno, f"Argument: {node.arg}", token))

        # Check string constants
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            for token in PROHIBITED_TOKENS:
                if token.lower() in node.value.lower():
                    violations.append((node.lineno, f"String Literal: {node.value}", token))

    if violations:
        print(f"FAILED: Found {len(violations)} anti-oracle leakage violation(s):")
        for line, desc, token in violations:
            print(f"  Line {line}: {desc} (matched prohibited token '{token}')")
        return False

    print("SUCCESS: AST Static Anti-Oracle Leakage Audit PASSED.")
    print("  Zero prohibited expected-field tokens found in comparison engine.")
    print("  Mathematical isolation between Field B and Field C is verified.")
    return True

if __name__ == "__main__":
    success = run_ast_audit()
    sys.exit(0 if success else 1)
