import argparse
from pathlib import Path

TEXT_EXTS = {".md", ".cff", ".ipynb", ".yml", ".yaml", ".toml", ".html", ".txt"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--github-user", required=True)
    ap.add_argument("--repo", default="CausalWorld")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    full = f"{args.github_user}/{args.repo}"
    changed = 0

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new = text.replace("YOUR_GITHUB_USER/CausalWorld", full)
        new = new.replace("YOUR_GITHUB_USER", args.github_user)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1

    print(f"Updated {changed} files for https://github.com/{full}")

if __name__ == "__main__":
    main()
