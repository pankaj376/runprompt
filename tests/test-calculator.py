#!/usr/bin/env python3
"""Tests for the builtin calculator tool."""
import os
import sys
import math

# Import calculator from runprompt
runprompt_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "runprompt"
)
import importlib.util
loader = importlib.machinery.SourceFileLoader("runprompt", runprompt_path)
spec = importlib.util.spec_from_loader("runprompt", loader)
runprompt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runprompt)
calculator = runprompt.calculator

passed = 0
failed = 0


def test(name, func):
    global passed, failed
    try:
        func()
        print("✓ %s" % name)
        passed += 1
    except AssertionError as e:
        print("✗ %s: %s" % (name, e))
        failed += 1
    except Exception as e:
        print("✗ %s: %s: %s" % (name, type(e).__name__, e))
        failed += 1


def test_basic_arithmetic():
    assert calculator("2 + 3") == 5
    assert calculator("10 - 4") == 6
    assert calculator("3 * 4") == 12
    assert calculator("15 / 3") == 5.0
    assert calculator("17 // 5") == 3
    assert calculator("17 % 5") == 2
    assert calculator("2 ** 10") == 1024


def test_operator_precedence():
    assert calculator("2 + 3 * 4") == 14
    assert calculator("(2 + 3) * 4") == 20
    assert calculator("10 - 2 - 3") == 5


def test_unary_operators():
    assert calculator("-5") == -5
    assert calculator("+5") == 5
    assert calculator("--5") == 5
    assert calculator("-(-5)") == 5


def test_trig_functions():
    assert abs(calculator("sin(0)") - 0) < 1e-10
    assert abs(calculator("cos(0)") - 1) < 1e-10
    assert abs(calculator("sin(pi / 2)") - 1) < 1e-10
    assert abs(calculator("tan(pi / 4)") - 1) < 1e-10


def test_inverse_trig():
    assert abs(calculator("asin(0.5)") - math.asin(0.5)) < 1e-10
    assert abs(calculator("acos(0.5)") - math.acos(0.5)) < 1e-10
    assert abs(calculator("atan(1)") - math.atan(1)) < 1e-10


def test_hyperbolic():
    assert abs(calculator("sinh(1)") - math.sinh(1)) < 1e-10
    assert abs(calculator("cosh(1)") - math.cosh(1)) < 1e-10
    assert abs(calculator("tanh(1)") - math.tanh(1)) < 1e-10


def test_exp_log():
    assert abs(calculator("exp(1)") - math.e) < 1e-10
    assert abs(calculator("log(e)") - 1) < 1e-10
    assert abs(calculator("log10(100)") - 2) < 1e-10
    assert abs(calculator("log2(8)") - 3) < 1e-10


def test_sqrt_pow():
    assert calculator("sqrt(16)") == 4.0
    assert calculator("sqrt(2)") == math.sqrt(2)
    assert calculator("pow(2, 10)") == 1024


def test_rounding():
    assert calculator("abs(-42)") == 42
    assert calculator("ceil(3.2)") == 4
    assert calculator("floor(3.8)") == 3
    assert calculator("trunc(3.8)") == 3
    assert calculator("trunc(-3.8)") == -3
    assert calculator("round(3.7)") == 4
    assert calculator("round(3.5)") == 4


def test_angle_conversion():
    assert abs(calculator("degrees(pi)") - 180) < 1e-10
    assert abs(calculator("radians(180)") - math.pi) < 1e-10


def test_factorial():
    assert calculator("factorial(0)") == 1
    assert calculator("factorial(5)") == 120
    assert calculator("factorial(10)") == 3628800


def test_gcd_lcm():
    assert calculator("gcd(48, 18)") == 6
    if hasattr(math, 'lcm'):
        assert calculator("lcm(12, 18)") == 36


def test_min_max_sum():
    assert calculator("max(1, 5, 3)") == 5
    assert calculator("min(1, 5, 3)") == 1
    assert calculator("sum([1, 2, 3, 4, 5])") == 15


def test_constants():
    assert calculator("pi") == math.pi
    assert calculator("e") == math.e
    assert calculator("tau") == math.tau
    assert calculator("tau / 2") == math.pi


def test_complex_expressions():
    # Trig identity: sin^2 + cos^2 = 1
    result = calculator("sin(pi/6) ** 2 + cos(pi/6) ** 2")
    assert abs(result - 1) < 1e-10
    # Pythagorean theorem
    assert calculator("sqrt(3**2 + 4**2)") == 5.0
    # log(e^x) = x
    assert abs(calculator("log(exp(5))") - 5) < 1e-10


def test_lists_tuples():
    assert calculator("[1, 2, 3]") == [1, 2, 3]
    assert calculator("(1, 2, 3)") == (1, 2, 3)
    assert calculator("sum([1, 2, 3])") == 6


def test_blocked_imports():
    # Direct __import__ call should be blocked as unknown function
    try:
        calculator("__import__('os')")
        assert False, "Should have raised"
    except ValueError as e:
        assert "function not allowed" in str(e).lower(), "Got: %s" % e
    # Method call on result should be blocked as non-simple call
    try:
        calculator("__import__('os').system('ls')")
        assert False, "Should have raised"
    except ValueError as e:
        assert "simple function calls" in str(e).lower(), "Got: %s" % e


def test_blocked_builtins():
    try:
        calculator("open('/etc/passwd')")
        assert False, "Should have raised"
    except ValueError as e:
        assert "not allowed" in str(e).lower()


def test_blocked_exec():
    try:
        calculator("exec('print(123)')")
        assert False, "Should have raised"
    except ValueError as e:
        assert "not allowed" in str(e).lower()


def test_blocked_eval():
    try:
        calculator("eval('1+1')")
        assert False, "Should have raised"
    except ValueError as e:
        assert "not allowed" in str(e).lower()


def test_blocked_lambda():
    try:
        calculator("lambda x: x + 1")
        assert False, "Should have raised"
    except ValueError as e:
        assert "not allowed" in str(e).lower()


def test_blocked_comprehension():
    try:
        calculator("[x for x in range(10)]")
        assert False, "Should have raised"
    except ValueError as e:
        assert "not allowed" in str(e).lower()


def test_blocked_unknown_name():
    try:
        calculator("x + 1")
        assert False, "Should have raised"
    except ValueError as e:
        assert "not allowed" in str(e).lower()


def test_blocked_print():
    try:
        calculator("print(123)")
        assert False, "Should have raised"
    except ValueError as e:
        assert "not allowed" in str(e).lower()


def test_blocked_strings():
    try:
        calculator("'hello'")
        assert False, "Should have raised"
    except ValueError as e:
        assert "only numbers allowed" in str(e).lower()


def test_safe_attribute():
    assert calculator.safe is True


def main():
    test("basic arithmetic", test_basic_arithmetic)
    test("operator precedence", test_operator_precedence)
    test("unary operators", test_unary_operators)
    test("trig functions", test_trig_functions)
    test("inverse trig", test_inverse_trig)
    test("hyperbolic functions", test_hyperbolic)
    test("exp and log", test_exp_log)
    test("sqrt and pow", test_sqrt_pow)
    test("rounding functions", test_rounding)
    test("angle conversion", test_angle_conversion)
    test("factorial", test_factorial)
    test("gcd and lcm", test_gcd_lcm)
    test("min max sum", test_min_max_sum)
    test("constants", test_constants)
    test("complex expressions", test_complex_expressions)
    test("lists and tuples", test_lists_tuples)
    test("blocked imports", test_blocked_imports)
    test("blocked builtins", test_blocked_builtins)
    test("blocked exec", test_blocked_exec)
    test("blocked eval", test_blocked_eval)
    test("blocked lambda", test_blocked_lambda)
    test("blocked comprehension", test_blocked_comprehension)
    test("blocked unknown name", test_blocked_unknown_name)
    test("blocked print", test_blocked_print)
    test("blocked strings", test_blocked_strings)
    test("safe attribute", test_safe_attribute)

    print("\n%d passed, %d failed" % (passed, failed))
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
