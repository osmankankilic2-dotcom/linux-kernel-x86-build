# Linux Kernel x86_64 Automated Build

This repository automatically downloads and compiles the standard x86_64 Linux kernel using GitHub Actions.

## Features
- Downloads official Linux kernel source tarball from [kernel.org](https://kernel.org).
- Configures kernel with `x86_64 defconfig`.
- Builds kernel image (`bzImage`) and kernel modules on GitHub Actions `ubuntu-latest` runners.
- Uploads `bzImage` and `.config` as downloadable workflow artifacts.
- Supports manual triggers with custom kernel version via `workflow_dispatch`.

## How to Run Manually
1. Go to **Actions** tab in GitHub.
2. Select **Build x86_64 Linux Kernel**.
3. Click **Run workflow** and specify the desired kernel version (e.g. `6.12.1`).
