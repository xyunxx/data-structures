# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest"]
# ///
"""
TDD Challenge Scoreboard
Run with: uv run run_score.py [data_structure ...]

Examples:
    uv run run_score.py              # run all
    uv run run_score.py linked_list  # run just linked list
    uv run run_score.py stack_queue binary_search_tree  # run two
"""

import re
import subprocess
import sys
import time

SUITES = {
    "Linked List": "test_linked_list.py",
    "Stack & Queue": "test_stack_queue.py",
    "Deque": "test_deque.py",
    "Binary Search Tree": "test_binary_search_tree.py",
    "Hash Map": "test_hash_map.py",
}

# Map CLI shorthand to display names
ALIASES = {
    "linked_list": "Linked List",
    "stack_queue": "Stack & Queue",
    "deque": "Deque",
    "binary_search_tree": "Binary Search Tree",
    "hash_map": "Hash Map",
}


def run_suite(name, test_file):
    """Run a single test suite and return (passed, failed, errors, duration)."""
    start = time.time()
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_file, "-v", "--tb=no", "-q"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    duration = time.time() - start
    output = result.stdout + result.stderr

    # Parse pytest summary line like "171 passed, 3 failed" or "211 passed"
    passed = failed = errors = 0
    m = re.search(r"(\d+) passed", output)
    if m:
        passed = int(m.group(1))
    m = re.search(r"(\d+) failed", output)
    if m:
        failed = int(m.group(1))
    m = re.search(r"(\d+) error", output)
    if m:
        errors = int(m.group(1))

    return passed, failed, errors, duration


def bar(fraction, width=30):
    filled = int(fraction * width)
    return "█" * filled + "░" * (width - filled)


def main():
    # Determine which suites to run
    if len(sys.argv) > 1:
        selected = {}
        for arg in sys.argv[1:]:
            key = arg.lower().replace("-", "_")
            if key in ALIASES:
                display = ALIASES[key]
                selected[display] = SUITES[display]
            else:
                print(f"Unknown data structure: {arg}")
                print(f"Options: {', '.join(ALIASES.keys())}")
                sys.exit(1)
    else:
        selected = SUITES

    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║              TDD CHALLENGE  —  SCOREBOARD                        ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    results = {}
    total_passed = 0
    total_tests = 0
    total_time = 0.0

    for name, test_file in selected.items():
        sys.stdout.write(f"  Running {name}... ")
        sys.stdout.flush()
        try:
            passed, failed, errors, duration = run_suite(name, test_file)
        except subprocess.TimeoutExpired:
            passed, failed, errors, duration = 0, 0, 1, 120.0
            print("TIMEOUT")
            continue
        except FileNotFoundError:
            print("SKIPPED (pytest not found)")
            continue

        total = passed + failed + errors
        results[name] = (passed, total, duration)
        total_passed += passed
        total_tests += total
        total_time += duration
        print(f"done ({duration:.1f}s)")

    print()
    print("─" * 66)
    print(f"  {'Data Structure':<24} {'Score':>12}  {'':>30}  {'Time':>6}")
    print("─" * 66)

    for name, (passed, total, duration) in results.items():
        pct = passed / total if total > 0 else 0
        score_str = f"{passed:>3} / {total:<3}"
        pct_str = f"({pct:5.1%})"
        b = bar(pct)
        t = f"{duration:.1f}s"
        print(f"  {name:<24} {score_str} {pct_str}  {b}  {t:>6}")

    print("─" * 66)

    overall_pct = total_passed / total_tests if total_tests > 0 else 0
    print(
        f"  {'TOTAL':<24} {total_passed:>3} / {total_tests:<3} ({overall_pct:5.1%})  {bar(overall_pct)}  {total_time:.1f}s"
    )
    print()

    if overall_pct == 1.0:
        print("  ★ PERFECT SCORE — All tests passing! ★")
    elif overall_pct >= 0.9:
        print("  Almost there — just a few more to go!")
    elif overall_pct >= 0.5:
        print("  Great progress — over halfway!")
    elif overall_pct > 0:
        print("  Off to a good start — keep implementing!")
    else:
        print("  No tests passing yet — time to start coding!")
    print()


if __name__ == "__main__":
    main()
