# راه‌اندازی GitHub Pages برای CausalWorld

## فایل‌های لندینگ
لندینگ داخل این پوشه است:

```text
site/
├── index.html
├── styles.css
└── script.js
```

## روش پیشنهادی خیلی راحت

### حالت 1: پوشه docs
اگر می‌خواهی بدون workflow خاص خیلی راحت بالا بیاید:
1. محتوای پوشه `site/` را داخل پوشه `docs/` کپی کن.
2. در GitHub برو به:
   `Settings > Pages`
3. بخش **Build and deployment** را روی:
   - **Source:** Deploy from a branch
   - **Branch:** `main`
   - **Folder:** `/docs`
   بگذار.
4. Save بزن.

بعد از چند دقیقه سایتت بالا می‌آید.

## حالت 2: GitHub Actions
اگر خواستی بعداً حرفه‌ای‌ترش کنیم، می‌شود workflow هم برایش گذاشت.

## لینک‌ها
الان داخل لندینگ این لینک‌ها ست شده‌اند:

- Repo: `https://github.com/mobinveisy/CausalWorld`
- Colab Demo:
  `https://colab.research.google.com/github/mobinveisy/CausalWorld/blob/main/notebooks/01_CausalWorld_Quick_Demo.ipynb`
- Reproduce Notebook:
  `https://colab.research.google.com/github/mobinveisy/CausalWorld/blob/main/notebooks/02_Reproduce_CausalWorld.ipynb`

## کپی‌رایت
Footer لندینگ:

```text
© 2026 Mobin Veisy. All rights reserved.
```
