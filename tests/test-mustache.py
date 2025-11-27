#!/usr/bin/env python3
import sys
import os
import importlib.util
import importlib.machinery

# Import from runprompt by path (no .py extension)
runprompt_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "runprompt"
)
loader = importlib.machinery.SourceFileLoader("runprompt", runprompt_path)
spec = importlib.util.spec_from_loader("runprompt", loader)
runprompt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runprompt)
render_template = runprompt.render_template


def test(name, template, variables, expected):
    result = render_template(template, variables)
    if result == expected:
        print("✅ %s" % name)
        return True
    else:
        print("❌ %s" % name)
        print("   Expected: %r" % expected)
        print("   Got:      %r" % result)
        return False


def main():
    passed = 0
    failed = 0

    # Basic variable interpolation
    if test("simple variable", "Hello {{name}}!", {"name": "World"}, "Hello World!"):
        passed += 1
    else:
        failed += 1

    if test("multiple variables", "{{a}} and {{b}}", {"a": "X", "b": "Y"}, "X and Y"):
        passed += 1
    else:
        failed += 1

    if test("missing variable", "Hello {{name}}!", {}, "Hello !"):
        passed += 1
    else:
        failed += 1

    if test("variable with spaces", "{{ name }}", {"name": "World"}, "World"):
        passed += 1
    else:
        failed += 1

    if test("number variable", "Count: {{n}}", {"n": 42}, "Count: 42"):
        passed += 1
    else:
        failed += 1

    if test("empty template", "", {"name": "World"}, ""):
        passed += 1
    else:
        failed += 1

    if test("no variables", "Hello World!", {"name": "Test"}, "Hello World!"):
        passed += 1
    else:
        failed += 1

    print("")
    print("Passed: %d, Failed: %d" % (passed, failed))
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
