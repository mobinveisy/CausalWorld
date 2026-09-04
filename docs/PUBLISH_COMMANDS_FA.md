# دستورات انتشار CausalWorld روی GitHub

## 1) یک Repository بساز
نام پیشنهادی:

```text
CausalWorld
```

اگر مقاله قرار است برای کنفرانس double-blind ارسال شود، قبل از public کردن repo سیاست همان کنفرانس را بررسی کن.

## 2) داخل پوشه پروژه

```bash
cd CausalWorld_release_candidate
```

لینک‌ها را برای اکانت خودت تنظیم کن:

```bash
python scripts/configure_repo.py \
  --github-user YOUR_USERNAME \
  --repo CausalWorld
```

تست:

```bash
python scripts/verify_release.py
```

## 3) Git

```bash
git init
git add .
git commit -m "CausalWorld v0.9.0-rc1"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/CausalWorld.git
git push -u origin main
```

## 4) Colab Demo

بعد از push:

```text
https://colab.research.google.com/github/YOUR_USERNAME/CausalWorld/blob/main/notebooks/01_CausalWorld_Quick_Demo.ipynb
```

Reproduction:

```text
https://colab.research.google.com/github/YOUR_USERNAME/CausalWorld/blob/main/notebooks/02_Reproduce_CausalWorld.ipynb
```

Public-data setup:

```text
https://colab.research.google.com/github/YOUR_USERNAME/CausalWorld/blob/main/notebooks/03_Public_Data_Setup.ipynb
```

## 5) GitHub Pages اختیاری

فایل آماده‌ی صفحه پروژه:

```text
site/index.html
```

می‌توانی آن را برای GitHub Pages استفاده کنی یا بعداً صفحه حرفه‌ای‌تر بسازیم.

## 6) Zenodo

Zenodo را بعد از اینکه:
- نتایج نهایی ثابت شدند،
- نسخه release/tag فریز شد،
- و محدودیت anonymity اجازه داد،

به GitHub وصل کن و برای release نهایی DOI بگیر.
