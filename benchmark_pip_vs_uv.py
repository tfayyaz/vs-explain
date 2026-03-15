#!/usr/bin/env python3
"""Benchmark: pip install vs uv pip install for 5 packages across 5 cold runs."""

import json
import math
import os
import shutil
import subprocess
import statistics
import time

PACKAGES = ["duckdb", "polars", "pyarrow", "pyspark[pipelines]", "dbt-databricks"]
NUM_RUNS = 5
VENV_BASE = "/tmp/bench_venvs"
UV = os.path.expanduser("~/.local/bin/uv")
PYTHON = "/usr/local/bin/python3"

# Clear pip cache before benchmarks
def clear_caches():
    subprocess.run(["pip3", "cache", "purge"], capture_output=True)
    subprocess.run([UV, "cache", "clean"], capture_output=True)


def run_pip_install(venv_path, package):
    """Create venv with python3 -m venv, install with pip."""
    subprocess.run([PYTHON, "-m", "venv", venv_path], check=True, capture_output=True)
    pip_bin = os.path.join(venv_path, "bin", "pip")
    # Upgrade pip first
    subprocess.run([pip_bin, "install", "--upgrade", "pip"], check=True, capture_output=True)
    start = time.monotonic()
    result = subprocess.run(
        [pip_bin, "install", package],
        capture_output=True, text=True
    )
    elapsed = time.monotonic() - start
    success = result.returncode == 0
    if not success:
        print(f"  ERROR (pip): {result.stderr[:200]}")
    return elapsed, success


def run_uv_pip_install(venv_path, package):
    """Create venv with uv venv, install with uv pip install."""
    subprocess.run([UV, "venv", venv_path, "--python", PYTHON], check=True, capture_output=True)
    start = time.monotonic()
    result = subprocess.run(
        [UV, "pip", "install", package, "--python", os.path.join(venv_path, "bin", "python")],
        capture_output=True, text=True
    )
    elapsed = time.monotonic() - start
    success = result.returncode == 0
    if not success:
        print(f"  ERROR (uv): {result.stderr[:200]}")
    return elapsed, success


def analyze(times):
    """Return dict with min, max, avg, median, stddev."""
    if not times:
        return {}
    return {
        "min": round(min(times), 3),
        "max": round(max(times), 3),
        "avg": round(statistics.mean(times), 3),
        "median": round(statistics.median(times), 3),
        "stddev": round(statistics.stdev(times), 3) if len(times) > 1 else 0.0,
    }


def main():
    results = {}

    for pkg in PACKAGES:
        print(f"\n{'='*60}")
        print(f"Benchmarking: {pkg}")
        print(f"{'='*60}")

        pip_times = []
        uv_times = []

        # --- pip install runs ---
        for run in range(1, NUM_RUNS + 1):
            venv_path = os.path.join(VENV_BASE, f"pip_{pkg.replace('[', '_').replace(']', '')}_{run}")
            if os.path.exists(venv_path):
                shutil.rmtree(venv_path)

            clear_caches()
            print(f"  pip run {run}/{NUM_RUNS}...", end=" ", flush=True)
            elapsed, success = run_pip_install(venv_path, pkg)
            pip_times.append(elapsed)
            print(f"{elapsed:.2f}s {'OK' if success else 'FAIL'}")
            # Clean up venv
            shutil.rmtree(venv_path, ignore_errors=True)

        # --- uv pip install runs ---
        for run in range(1, NUM_RUNS + 1):
            venv_path = os.path.join(VENV_BASE, f"uv_{pkg.replace('[', '_').replace(']', '')}_{run}")
            if os.path.exists(venv_path):
                shutil.rmtree(venv_path)

            clear_caches()
            print(f"  uv  run {run}/{NUM_RUNS}...", end=" ", flush=True)
            elapsed, success = run_uv_pip_install(venv_path, pkg)
            uv_times.append(elapsed)
            print(f"{elapsed:.2f}s {'OK' if success else 'FAIL'}")
            # Clean up venv
            shutil.rmtree(venv_path, ignore_errors=True)

        pip_stats = analyze(pip_times)
        uv_stats = analyze(uv_times)
        speedup = round(pip_stats["avg"] / uv_stats["avg"], 2) if uv_stats.get("avg") else "N/A"

        results[pkg] = {
            "pip": {"times": [round(t, 3) for t in pip_times], "stats": pip_stats},
            "uv": {"times": [round(t, 3) for t in uv_times], "stats": uv_stats},
            "speedup_factor": speedup,
        }

        print(f"\n  pip  -> avg: {pip_stats['avg']:.3f}s | median: {pip_stats['median']:.3f}s | min: {pip_stats['min']:.3f}s | max: {pip_stats['max']:.3f}s | stddev: {pip_stats['stddev']:.3f}s")
        print(f"  uv   -> avg: {uv_stats['avg']:.3f}s | median: {uv_stats['median']:.3f}s | min: {uv_stats['min']:.3f}s | max: {uv_stats['max']:.3f}s | stddev: {uv_stats['stddev']:.3f}s")
        print(f"  Speedup: {speedup}x faster with uv")

    # Save JSON results
    with open("/home/user/vs-explain/benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Print summary table
    print(f"\n\n{'='*80}")
    print("SUMMARY: pip vs uv pip install (5 cold runs each, caches cleared)")
    print(f"{'='*80}")
    print(f"{'Package':<25} {'pip avg (s)':<14} {'uv avg (s)':<14} {'Speedup':<10}")
    print(f"{'-'*63}")
    for pkg, data in results.items():
        pip_avg = data["pip"]["stats"]["avg"]
        uv_avg = data["uv"]["stats"]["avg"]
        speedup = data["speedup_factor"]
        print(f"{pkg:<25} {pip_avg:<14.3f} {uv_avg:<14.3f} {speedup}x")

    print(f"\nDetailed results saved to benchmark_results.json")


if __name__ == "__main__":
    main()
