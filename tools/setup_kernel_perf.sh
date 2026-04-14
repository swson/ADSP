#!/usr/bin/env bash
set -euo pipefail

KERNEL_VERSION="5.15.0-122-generic"
PERF_SRC_DIR="$HOME/linux"

echo "========== STEP 1: Current Kernel =========="
uname -r
uname -a

echo "========== STEP 2: Update =========="
sudo apt update -y

echo "========== STEP 3: Install Kernel =========="
sudo apt install -y \
  linux-image-${KERNEL_VERSION} \
  linux-headers-${KERNEL_VERSION}

echo "========== STEP 4: Install Kernel Tools =========="
sudo apt install -y \
  linux-tools-${KERNEL_VERSION} \
  linux-cloud-tools-${KERNEL_VERSION}

echo "========== STEP 5: Set GRUB Default =========="
sudo sed -i "s|^GRUB_DEFAULT=.*|GRUB_DEFAULT=\"Advanced options for Ubuntu>Ubuntu, with Linux ${KERNEL_VERSION}\"|" /etc/default/grub
sudo update-grub

echo "========== STEP 6: Install perf dependencies =========="
sudo apt install -y \
  flex bison libelf-dev libbfd-dev libunwind-dev \
  libnuma-dev libdw-dev libcap-dev libiberty-dev \
  libzstd-dev libslang2-dev libperl-dev python3-dev \
  libtraceevent-dev pkg-config git

echo "========== STEP 7: Build perf =========="

if [ ! -d "$PERF_SRC_DIR" ]; then
  git clone https://github.com/torvalds/linux.git "$PERF_SRC_DIR"
fi

cd "$PERF_SRC_DIR/tools/perf"
make -j$(nproc)

echo "========== STEP 8: Install perf =========="
if [ -f /usr/bin/perf ]; then
  sudo mv /usr/bin/perf /usr/bin/perf.backup || true
fi

sudo cp ./perf /usr/bin/perf

echo "========== STEP 9: Reboot =========="
echo "Rebooting system..."
sudo reboot
