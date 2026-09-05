# Push کامل CausalWorld از صفر

اگر می‌خواهی نسخه فعلی GitHub را کامل با این نسخه نهایی جایگزین کنی:

```bash
cd CausalWorld_final_threejs
```

اگر پوشه هنوز Git ندارد:

```bash
git init
git branch -M main
git remote add origin https://github.com/mobinveisy/CausalWorld.git
```

اگر remote از قبل وجود دارد:

```bash
git remote set-url origin https://github.com/mobinveisy/CausalWorld.git
```

سپس:

```bash
git add .
git commit -m "CausalWorld v1.0 — research code, Colab and Three.js landing"
git push -u origin main
```

اگر GitHub به خاطر وجود commit قبلی اجازه Push نداد، اول وضعیت repo را بررسی کن. **بدون بکاپ سراغ force push نرو.**

## تست قبل از Push

### Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python run_tests.py
```

### Landing

```bash
cd web
npm install
npm run build
```

## بعد از Push

1. `Settings → Pages`
2. Source = `GitHub Actions`
3. برو تب `Actions`
4. منتظر workflow `Deploy Three.js site to Pages` باش
5. سایت: `https://mobinveisy.github.io/CausalWorld/`
