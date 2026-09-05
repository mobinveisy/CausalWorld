# راه‌اندازی لندینگ Three.js روی GitHub Pages

این نسخه با **Vite + Three.js** ساخته شده و از GitHub Actions به Pages deploy می‌شود.

## 1) فایل‌ها را Push کن

در ریشه پروژه:

```bash
git add .
git commit -m "Add CausalWorld Three.js research landing"
git push origin main
```

## 2) GitHub Pages را روی Actions بگذار

داخل Repository برو:

```text
Settings → Pages
```

در بخش **Build and deployment** مقدار Source را روی:

```text
GitHub Actions
```

بگذار.

Workflow آماده است:

```text
.github/workflows/pages.yml
```

بعد از Push، در تب Actions اجرای:

```text
Deploy Three.js site to Pages
```

را می‌بینی.

آدرس سایت:

```text
https://mobinveisy.github.io/CausalWorld/
```

## اجرای لندینگ روی مک قبل از Push

```bash
cd web
npm install
npm run dev
```

برای build نهایی:

```bash
npm run build
```

## دکمه‌های Colab

Demo:

```text
https://colab.research.google.com/github/mobinveisy/CausalWorld/blob/main/notebooks/01_CausalWorld_Quick_Demo.ipynb
```

Reproduce:

```text
https://colab.research.google.com/github/mobinveisy/CausalWorld/blob/main/notebooks/02_Reproduce_CausalWorld.ipynb
```

## نکته

در `vite.config.js` مقدار `base` روی `/CausalWorld/` تنظیم شده چون سایت روی GitHub Project Pages همین repo منتشر می‌شود.
