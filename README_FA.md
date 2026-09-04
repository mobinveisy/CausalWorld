# CausalWorld — نسخه Release Candidate قبل از مقاله

پروژه بررسی می‌کند آیا مدل می‌تواند از چند مشاهده‌ی passive یک نمایش پنهان از physics
یاد بگیرد و سپس با تغییر فقط همان نمایش، counterfactual درست را پیش‌بینی کند.

```text
Passive observations
      ↓
Physics Encoder
      ↓
z_physics
      ↓
Dynamics Decoder
      ↓
Future
```

در counterfactual، initial state ثابت می‌ماند و فقط `z_physics` عوض می‌شود.

## دیتاست‌ها

- **Physion++**: دیتاست اصلی hidden-property و pairهای matched `copy0/copy1`
- **GAUGE**: اعتبارسنجی real-world با motion-capture و metadata فیزیکی کالیبره

پس برای مقاله نیازی به فیلم‌برداری شخصی نداریم.

## تست

```bash
pip install -e .
python run_tests.py
python run_suite.py --mode smoke --seeds 11 --output results_smoke
```

## اجرای نهایی synthetic

```bash
python run_suite.py   --mode full   --seeds 11 22 33 44 55   --output results_full
```

## Colab آماده

```text
notebooks/01_CausalWorld_Quick_Demo.ipynb
notebooks/02_Reproduce_CausalWorld.ipynb
notebooks/03_Public_Data_Setup.ipynb
```

بعد از ساخت GitHub:

```bash
python scripts/configure_repo.py   --github-user USERNAME   --repo CausalWorld
```

این نسخه `0.9.0-rc1` است. از نظر ساختار repo، Colab، citation و reproducibility آماده‌ی
انتشار است. مرحله بعد اجرای کامل آزمایش‌های public-data و سپس نوشتن مقاله با نتایج واقعی است.
