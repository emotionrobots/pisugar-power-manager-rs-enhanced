# pisugar-power-manager-rs

![Master](https://github.com/PiSugar/pisugar-power-manager-rs/workflows/Master/badge.svg)
![Nightly](https://github.com/PiSugar/pisugar-power-manager-rs/workflows/Nightly%20build%20on%20master/badge.svg)

<p align="center">
  <img width="320" src="https://raw.githubusercontent.com/JdaieLin/PiSugar/master/logo.jpg">
</p>

## Management program for PiSugar 2

PiSugar power manager in rust language.

## Install

These packages are hosted in QiNiu CDN (For zero/zerowh/pi3/pi3b/pi4 with 32bit os only, you need to download and install packages manually in pi4 with 64bit os)

    curl http://cdn.pisugar.com/release/Pisugar-power-manager.sh | sudo bash

or

    wget http://cdn.pisugar.com/release/Pisugar-power-manager.sh
    bash Pisugar-power-manager.sh -c release

Install script usage

    Install pisugar power manager tools.

    USAGE: Pisugar-power-manager.sh [OPTIONS]

    OPTIONS:
        -h|--help       Print this usage.
        -v|--version    Install a specified version, default: 1.4.0
        -c|--channel    Choose nightly or release channel, default: release

    For more details, see https://github.com/PiSugar/pisugar-power-manager-rs

**NOTE** In centos/redhat like linux, RPM could not ask question in interactive mode, PiSugar model **MUST** be configured manually. Available models are:

    PiSugar 2 (4-LEDs)
    PiSugar 2 (2-LEDs)
    PiSugar 2 Pro

Replace model in `/etc/default/pisugar-server`

    sed -e "s|--model '.*' |--model '<model>' |"
        -i /etc/default/pisugar-server

**NOTE** `auto_power_on` mode would prevent PiSugar falling into sleep, it could be useful in some cases. (since v1.4.8, `/etc/pisugar-server/config.json`)

## Prerequisites

On raspberry pi, enable I2C interface

    sudo raspi-config

`Interfacing Options -> I2C -> Yes`

Known conflicts and issues:

    HyperPixel: HyperPixel disables I2C interface

## Modules

1. pisugar-core: Core library
2. pisugar-server: Http/tcp/uds server that provide PiSugar battery status
3. pisugar-poweroff: Systemd service that shut down PiSugar battery

## Compilation (TL;DR)

CPU architecture of raspberry pi is different from your linux/windows PC or macbook, there are two ways of compiling the code:

1. directly on raspberry pi
2. cross compilation

**NOTE** Remove `replace-with=...` in .cargo/config if cargo reports `warning: spurious network error`.

**NOTE** Need a static link with libgcc when cross compiling for Pi4 with aarch64

    # linux
    LIBGCC=$(find /opt/aarch64-linux-musl-cross -name libgcc.a)
    sed -e "s|\"/opt/aarch64-linux-musl-cross/lib/gcc/aarch64-linux-musl/9.2.1\"|\"${LIBGCC%/*}\"|" -i .cargo/config

    # macos
    LIBGCC=$(find find /usr/local/Cellar/musl-cross -name libgcc.a | grep aarch64)
    sed -e "s|\"/opt/aarch64-linux-musl-cross/lib/gcc/aarch64-linux-musl/9.2.1\"|\"${LIBGCC%/*}\"|" -i .cargo/config

### On raspberry pi

Install rust

    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    rustup update

Build

    cargo build --release

### Cross compilation - macos (musl)

Install cross compiler utils

    brew install FiloSottile/musl-cross/musl-cross --without-x86_64 --with-arm-hf   # arm
    brew install FiloSottile/musl-cross/musl-cross --without-x86_64 --with-aarch64  # arm64

Install rust and armv6(zero/zerow) / armv7(3b/3b+) / arm64(i.e. aarch64, 4) target

    brew install rustup-init
    rustup update
    rustup target add arm-unknown-linux-musleabihf      # armv6
    rustup target add armv7-unknown-linux-musleabihf    # armv7
    rustup target add aarch64-unknown-linux-musl        # arm64

Build

    cargo build --target arm-unknown-linux-musleabihf --release     # armv6
    cargo build --target armv7-unknown-linux-musleabihf --release   # armv7
    cargo build --target aarch64-unknown-linux-musl                 # arm64

### Cross compilation - linux/ubuntu (musl)

Install cross compiler utils (prebuilt musl toolchain on x86_64 or i686)

    wget https://more.musl.cc/$(uname -m)-linux-musl/arm-linux-musleabihf-cross.tgz
    tar -xvf arm-linux-musleabihf-cross.tgz

Move the toolchain into `/opt`, and add it into `PATH`

    sudo mv arm-linux-musleabihf-cross /opt/
    echo 'export PATH=/opt/arm-linux-musleabihf-cross/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc

Arm64

    wget http://more.musl.cc/$(uname -m)-linux-musl/aarch64-linux-musl-cross.tgz
    tar -xvf aarch64-linux-musl-cross.tgz
    sudo mv aarch64-linux-musl-cross /opt/
    echo 'export PATH=/opt/aarch64-linux-musleabihf-cross/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc

Install rust and arm/armv7/arm64 target

    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    rustup update
    rustup target add arm-unknown-linux-musleabihf      # armv6
    rustup target add armv7-unknown-linux-musleabihf    # armv7
    rustup target add aarch64-unknown-linux-musl        # arm64

Build

    cargo build --target arm-unknown-linux-musleabihf --release      # armv6
    cargo build --target armv7-unknown-linux-musleabihf --release    # armv7
    cargo build --target aarch64-unknown-linux-musl

### Cross compilation - windows

Install WSL and follow the linux cross compilation steps.

### Build web content

Build web content

    (cd electron && npm install && npm run build:web)

Try other mirrors when electron could not be downloaded

    ELECTRON_MIRROR="https://npm.taobao.org/mirrors/electron/" npm install

### Build and install deb packages

Build deb with cargo-deb (need latest cargo-deb that support templates)

    cargo install --git https://github.com/mmstick/cargo-deb.git

    cargo deb --target arm-unknown-linux-musleabihf --manifest-path=pisugar-server/Cargo.toml
    cargo deb --target arm-unknown-linux-musleabihf --manifest-path=pisugar-poweroff/Cargo.toml
    cargo deb --target aarch64-unknown-linux-musl --manifest-path=pisugar-server/Cargo.toml
    cargo deb --target aarch64-unknown-linux-musl --manifest-path=pisugar-poweroff/Cargo.toml

Install

    # Install
    sudo dpkg -i pisugar-xxx_<version>_<arch>.deb

    # Uninstall/Purge
    sudo dpkg -P pisugar-xxx

To reconfigure after installation

    sudo dpkg-reconfigure pisugar-server
    sudo dpkg-reconfigure pisugar-poweroff

To preconfigure before installation

    sudo dpkg-preconfigure pisugar-server_<ver>_<arch>.deb
    sudo dpkg-preconfigure pisugar-poweroff_<ver>_<arch>.deb

### Build rpm packages

Install rpm on debian-like :

    sudo apt install rpm

Install cargo-rpm

    cargo install cargo-rpm

Build

    cargo rpm build --target arm-unknown-linux-musleabihf

Install

    rpm -i pisugar-server-<ver>-<arch>.rpm

### Controlling systemd service

Commands of controlling pisugar-server systemd service

    # reload daemon
    sudo systemctl daemon-reload

    # check status
    sudo systemctl status pisugar-server

    # start service
    sudo systemctl start pisugar-server

    # stop service
    sudo systemctl stop pisugar-server

    # disable service
    sudo systemctl disable pisugar-server

    # enable service
    sudo systemctl enable pisugar-server

 (pisugar-poweroff run once just before linux poweroff)

Now, navigate to `http://x.x.x.x:8421` on your browser and see PiSugar power status.

Configuration files of pisugar-server

    /etc/default/pisugar-server
    /etc/pisugar-server/config.json

Configuration files of pisugar-poweroff

    /etc/default/pisugar-poweroff


### RLS

RLS configuration of vscode `.vscode/settings.json`

    {
        "rust.target": "arm-unknown-linux-musleabihf"
    }

### Unix Domain Socket / Webscoket / TCP

Default ports:

    uds     /tmp/pisugar-server.sock
    tcp     0.0.0.0:8423
    ws      0.0.0.0:8422    # standalone websocket api
    http    0.0.0.0:8421    # web UI and websocket (/ws)

| Command | Description | Response/Usage |
| :- | :-: | :-: |
| get battery             | battery level % | battery: [number] |
| get battery_i           | BAT current in A | battery_i: [number] |
| get battery_v           | BAT votage in V | battery_v: [number] |
| get battery_charging    | charging status (for new model please use battery_power_plugged and battery_allow_charging to get charging status)  | battery_charging: [true\|false] |
| get model               | pisugar model | model: PiSugar 2 |
| get battery_led_amount  | charging led amount (2 is for new model) | battery_led_amount: [2\|4] |
| get battery_power_plugged  | charging usb plugged (new model only) | battery_power_plugged: [true\|false] |
| get battery_charging_range | charging range restart_point% stop_point% (new model only)  | battery_charging_range: [number, number]|
| get battery_allow_charging | whether charging is allowed when usb is plugged  (new model only)  | battery_allow_charging: [true\|false]|
| get rtc_time            | rtc clock | rtc_time: [ISO8601 time string] |
| get rtc_alarm_enabled   | rtc wakeup alarm enable | rtc_alarm_enabled: [true\|false] |
| get rtc_alarm_time      | rtc wakeup alarm time | rtc_alarm_time: [ISO8601 time string] |
| get alarm_repeat        | rtc wakeup alarm repeat in weekdays (127=1111111) | alarm_repeat: [number] |
| get button_enable       | custom button enable status | button_enable: [single\|double\|long] [true\|false] |
| get button_shell        | shell script when button is clicked  | button_shell: [single\|double\|long] [shell] |
| get safe_shutdown_level | auto shutdown level | safe_shutdown_level: [number] |
| get safe_shutdown_delay | auto shutdown delay | safe_shutdown_delay: [number] |
| rtc_pi2rtc | sync time pi => rtc | |
| rtc_rtc2pi | sync time rtc => pi | |
| rtc_web | sync time web => rtc & pi | |
| rtc_alarm_set | set rtc wakeup alarm | rtc_alarm_set [ISO8601 time string] [repeat] |
| rtc_alarm_disable | disable rtc wakeup alarm | |
| set_button_enable | auto shutdown level % | set_button_enable [single\|double\|long] [0\|1] |
| set_button_shell | auto shutdown level | safe_shutdown_level [single\|double\|long] [shell] |
| set_safe_shutdown_level | set auto shutdown level % | safe_shutdown_level [number] |
| set_safe_shutdown_delay | set auto shutdown delay in second | safe_shutdown_delay [number]|
| set_battery_charging_range | set charging range | set_battery_charging_range [number, number]|
| set_allow_charging | enable or disable charging | set_allow_charging [true\|false] |

Examples:

    nc -U /tmp/pisugar-server.sock
    get battery
    get model
    rtc_alarm_set 2020-06-26T16:09:34+08:00 127
    set_button_enable long 1
    set_button_enable long sudo shutdown now
    safe_shutdown_level 3
    safe_shutdown_delay 30
    <ctrl+c to break>

Or

    echo "get battery" | nc -q 0 127.0.0.1 8423

## Release

See https://github.com/PiSugar/pisugar-power-manager-rs/releases

## LICENSE

GPL v3
