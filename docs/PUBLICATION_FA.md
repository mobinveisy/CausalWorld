# انتشار CausalWorld برای مقاله

ساختار پیشنهادی نهایی:

1. GitHub برای سورس اصلی
2. Google Colab برای Demo و Reproduction
3. Zenodo برای DOI نسخه فریز شده
4. GitHub Pages به‌عنوان صفحه معرفی اختیاری

بعد از ساخت repo:

```bash
python scripts/configure_repo.py   --github-user USERNAME   --repo CausalWorld
```

سپس:

```bash
python run_tests.py
python scripts/verify_release.py
```

لینک Colab بعد از انتشار:

```text
https://colab.research.google.com/github/USERNAME/CausalWorld/blob/main/notebooks/01_CausalWorld_Quick_Demo.ipynb
```

برای کنفرانس‌های double-blind قبل از قرار دادن لینک عمومی شخصی داخل مقاله، policy همان کنفرانس را بررسی کن.
