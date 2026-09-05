# CausalWorld — نسخه نهایی GitHub + Three.js

پروژه بررسی می‌کند آیا یک مدل می‌تواند از مشاهده‌های passive یک نمایش پنهان از فیزیک یاد بگیرد و بعد با تغییر فقط همان `z_physics`، نتیجه counterfactual درست را بسازد.

## اجرای پژوهش

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python run_tests.py
```

Smoke test:

```bash
python run_suite.py --mode smoke --seeds 11 --output results_smoke
```

## لندینگ سه‌بعدی واقعی

لندینگ داخل `web/` با:

- Three.js
- WebGL
- Unreal Bloom post-processing
- هسته سه‌بعدی `z_physics`
- شبیه‌سازی collision
- سوییچ Factual / Counterfactual
- particle field
- scroll/pointer camera motion
- GitHub Pages deployment

ساخته شده.

برای تست روی مک:

```bash
cd web
npm install
npm run dev
```

برای build:

```bash
npm run build
```

## GitHub Pages

بعد از Push:

```text
Settings → Pages → Source: GitHub Actions
```

سایت:

```text
https://mobinveisy.github.io/CausalWorld/
```

راهنمای کامل:

```text
docs/GITHUB_PAGES_THREEJS_FA.md
```

## Colab

Demo:

```text
https://colab.research.google.com/github/mobinveisy/CausalWorld/blob/main/notebooks/01_CausalWorld_Quick_Demo.ipynb
```

Reproduce:

```text
https://colab.research.google.com/github/mobinveisy/CausalWorld/blob/main/notebooks/02_Reproduce_CausalWorld.ipynb
```

## Copyright

**Mobin Veisy**

© 2026 Mobin Veisy. All rights reserved for the project website and authored project materials.
