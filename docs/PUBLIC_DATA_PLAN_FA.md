# مسیر جدید CausalWorld با دیتاست‌های آماده

از این نسخه به بعد **هیچ فیلم‌برداری شخصی لازم نیست**.

## 1) Physion++ — دیتاست اصلی counterfactual

Physion++ دارای ویژگی‌های فیزیکی پنهان مثل جرم، اصطکاک، کشسانی و deformability است. در test set پوشه‌های `copy0` و `copy1` دو آزمایش matched را نگه می‌دارند که initial conditions یکسان/همسان دارند اما property یا outcome فیزیکی متفاوت است.

استفاده ما:
- train/readout: یادگیری latent فیزیک
- test copy0/copy1: Causal Latent Swap و CEE
- مرحله اول: Mass
- مرحله دوم: Friction و Elasticity

دانلود:
```bash
python public_data/download_public_data.py physion-train
python public_data/download_public_data.py physion-readout
python public_data/download_public_data.py physion-test
```

بعد از unzip:
```bash
python public_data/build_physionpp_index.py --root data_public/physionpp/extracted --output data_public/physionpp/index.csv
```

## 2) GAUGE 2026 — اعتبارسنجی real-world بدون ضبط ویدئو

GAUGE شامل آزمایش‌های واقعی motion-capture و metadata کالیبره‌شده است. برای پروژه ما لازم نیست کل ویدئوها دانلود شوند؛ JSONهای rigid-body کافی‌اند.

دانلود subset سبک‌تر:
```bash
python public_data/download_public_data.py gauge-rigid-json
```

تمرکز اولیه:
- Newton's cradle: momentum transfer / collision
- Bouncing ball: restitution
- Slope slider: friction
- Pendulum: oscillation/damping

## 3) Morpheus — تست real-video اختیاری

Morpheus 124 ویدئوی واقعی دارد و سه دسته برخورد مفید برای ما دارد:
- collision_equal
- collision_big_hits_small
- collision_small_hits_big

دانلود فقط collisionها:
```bash
python public_data/download_public_data.py morpheus-collisions
```

این مجموعه برای تست انتقال مدل به video-derived trajectories مناسب است.

# طراحی مقاله بعد از این تغییر

ادعای مقاله دیگر وابسته به dataset شخصی نیست:

> آیا یک مدل می‌تواند از مشاهده‌های passive یک latent فیزیکی قابل‌ویرایش یاد بگیرد، به‌طوری‌که تعویض latent باعث counterfactual dynamics صحیح شود؟

### Dataset A: Physion++
کنترل دقیق + matched counterfactual.

### Dataset B: GAUGE
real-world motion capture + calibrated physics.

### Dataset C: Morpheus (اختیاری)
real video transfer.

این طراحی برای reproducibility بهتر است چون تمام داده‌ها عمومی‌اند و پژوهشگر دیگر می‌تواند دقیقاً آزمایش ما را تکرار کند.
