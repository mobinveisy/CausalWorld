from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    required = [
        "README.md",
        "README_FA.md",
        "LICENSE",
        "CITATION.cff",
        "pyproject.toml",
        "requirements.txt",
        "notebooks/01_CausalWorld_Quick_Demo.ipynb",
        "notebooks/02_Reproduce_CausalWorld.ipynb",
        "notebooks/03_Public_Data_Setup.ipynb",
        "docs/REPRODUCIBILITY.md",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            raise SystemExit(f"FAIL: missing {rel}")

    large = [
        str(p.relative_to(ROOT))
        for p in ROOT.rglob("*")
        if p.is_file() and p.stat().st_size > 50 * 1024 * 1024
    ]
    if large:
        raise SystemExit("FAIL: large files in source tree: " + ", ".join(large))

    if "YOUR_GITHUB_USER" in (ROOT / "README.md").read_text(encoding="utf-8"):
        print("WARN: GitHub username placeholder is still present.")

    subprocess.check_call([sys.executable, "run_tests.py"], cwd=ROOT)
    print("RELEASE VERIFICATION PASSED")

if __name__ == "__main__":
    main()
