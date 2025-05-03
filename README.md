# Catan Dice Roller 🎲 🌙/☀️

![License: CC BY-NC 4.0](https://img.shields.io/badge/License-BY--NC%204.0-lightgrey.svg)
[![Pay Pal](https://img.shields.io/badge/buy%20me-a%20coffee-ffdd00?logo=paypal)](https://paypal.me/ximocm)

Light-weight, cross-platform utility that rolls **two virtual 6-sided dice** at fixed
intervals for _The Settlers of Catan™_ (and any other board game that needs 2 d6).

* Transparent, responsive UI – windowed on PC, fullscreen on Android.  
* Dark / Light mode toggle.  
* Custom roll timer: **15 | 30 | 60 | 90 s** (tap ±).  
* Stops automatically when a **7** is rolled – tap anywhere to resume.  
* “Roll now” button for manual throws.  
* Info overlay with credits, licence and donation link.  
* **Portable**: only needs Python ≥ 3.10 and `pygame-ce`.

> _Not affiliated with Catan GmbH or any publisher. 100 % fan project._

---

## Quick start (desktop)

```bash
git clone https://github.com/ximocm/catan-dice-roller.git
cd catan-dice-roller
python -m pip install pygame-ce
python catan_dice_roller.py
