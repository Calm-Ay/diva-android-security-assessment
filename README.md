# DIVA Android Security Assessment

![Type](https://img.shields.io/badge/Type-Mobile%20Application%20Security-e62020?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![Framework](https://img.shields.io/badge/Framework-OWASP%20MASVS-6f42c1?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-12%20Challenges%20Completed-brightgreen?style=for-the-badge)

> A hands-on security assessment of DIVA (Damn Insecure and Vulnerable App), covering static analysis, Android component testing, insecure storage, injection, and runtime instrumentation with Frida.

## Overview

This project documents an authorized assessment of the deliberately vulnerable DIVA Android application in an isolated Genymotion lab. Twelve exercises were completed using a repeatable workflow: inspect the implementation, form a test hypothesis, confirm it on the device, preserve evidence, and document remediation.

Challenge 13, a native memory-corruption exercise, is outside the completed scope and is not claimed here.

## Lab Environment

| Component | Configuration |
|---|---|
| Device | Genymotion Android 11 (API 30), x86_64 |
| Access | Rooted local emulator over ADB |
| Static analysis | JADX, Android manifest review, `strings` |
| Dynamic analysis | Frida 16.6.6, ADB, Android content and activity tools |
| Target | DIVA (`jakhar.aseem.diva`) |

## Results

| # | Exercise | Confirmed issue | Area |
|---:|---|---|---|
| 1 | Insecure Logging | Sensitive payment data written to Logcat | MASVS-STORAGE |
| 2 | Hardcoding 1 | Secret embedded in Java bytecode | MASVS-CRYPTO |
| 3 | Insecure Storage 1 | Credentials stored in plaintext SharedPreferences | MASVS-STORAGE |
| 4 | Insecure Storage 2 | Credentials stored in a plaintext SQLite database | MASVS-STORAGE |
| 5 | Insecure Storage 3 | Credentials stored in a plaintext private file | MASVS-STORAGE |
| 6 | Insecure Storage 4 | Sensitive data written to shared external storage | MASVS-STORAGE |
| 7 | Input Validation 1 | SQL injection returned all seeded user records | MASVS-CODE |
| 8 | Input Validation 2 | WebView accepted an untrusted `data:` URI | MASVS-PLATFORM |
| 9 | Access Control 1 | Exported activity disclosed API credentials | MASVS-PLATFORM |
| 10 | Access Control 2 | Caller-controlled Intent extra bypassed a PIN flow | MASVS-PLATFORM |
| 11 | Access Control 3 | Exported ContentProvider exposed private notes | MASVS-PLATFORM |
| 12 | Hardcoding 2 | Native secret extracted and observed with Frida | MASVS-CRYPTO |

## Key Findings

- Sensitive data appeared in logs and multiple plaintext storage locations.
- Client-side secrets remained recoverable from both DEX and native ELF code.
- Raw SQL construction allowed authentication-independent record disclosure.
- Exported Android components exposed protected data without caller authorization.
- An untrusted URI reached a WebView without a scheme and host allow-list.
- Runtime instrumentation proved the native access check received the secret in plaintext and returned success.

## Frida Compatibility Investigation

Frida 17.7.3 could enumerate processes but aborted during injection on this Android 11 x86_64 image with `Unsupported Android linker`. A version-matched Frida 16.6.6 client/server pair was installed in an isolated virtual environment. Attach, script loading, `Java.perform`, and the DIVA JNI observation then succeeded.

The compatibility failure was an instrumentation problem in the lab, not an application defense.

## Repository Contents

| Path | Description |
|---|---|
| [`REPORT.md`](REPORT.md) | Assessment narrative, evidence, impact, and remediation |
| [`evidence/findings.md`](evidence/findings.md) | Sanitized proof collected during testing |
| [`scripts/`](scripts/) | Frida setup, attach test, and JNI observation scripts |
| [`index.html`](index.html) | GitHub Pages case study |

## Ethics and Scope

Testing was limited to a deliberately vulnerable application on a locally owned emulator. The APK and decompiled third-party application source are excluded from this repository.

## Author

**Rasaq Ayomide** — Penetration Tester · AppSec Analyst · Security Researcher

- Portfolio: [calm-ay.github.io](https://calm-ay.github.io/)
- GitHub: [@Calm-Ay](https://github.com/Calm-Ay)

