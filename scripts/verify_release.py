from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
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
    "docs/GITHUB_PAGES_THREEJS_FA.md",
    "web/index.html",
    "web/package.json",
    "web/vite.config.js",
    "web/src/main.js",
    "web/src/scene.js",
    "web/src/style.css",
    ".github/workflows/pages.yml",
    ".github/workflows/tests.yml",
]


def run(cmd, cwd=ROOT):
    print("+", " ".join(map(str, cmd)))
    subprocess.check_call(cmd, cwd=cwd)


def main():
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            raise SystemExit(f"FAIL: missing {rel}")

    large = [
        str(p.relative_to(ROOT))
        for p in ROOT.rglob("*")
        if p.is_file() and p.stat().st_size > 50 * 1024 * 1024
    ]
    if large:
        raise SystemExit("FAIL: large files in source tree: " + ", ".join(large))

    placeholders = []
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".html", ".js", ".yml", ".yaml", ".cff", ".ipynb", ".toml"}:
            try:
                text = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "YOUR_GITHUB_USER" in text:
                placeholders.append(str(p.relative_to(ROOT)))
    if placeholders:
        raise SystemExit("FAIL: unresolved GitHub placeholders: " + ", ".join(placeholders))

    run([sys.executable, "run_tests.py"])

    if shutil.which("node"):
        run(["node", "--check", "web/src/main.js"])
        run(["node", "--check", "web/src/scene.js"])
        run(["node", "--check", "web/vite.config.js"])
    else:
        print("WARN: Node is not installed; JS syntax check skipped.")

    print("RELEASE VERIFICATION PASSED")
    print("NOTE: npm install/build requires network access; GitHub Actions performs the production build.")


if __name__ == "__main__":
    main()
