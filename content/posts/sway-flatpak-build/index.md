---
title: "Sway Flatpak Build"
date: 2025-01-25T14:00:00-07:00
draft: false
slug: "sway-flatpak-build"
tags: ["sway", "flatpak", "wayland", "linux", "containerization"]
---

This post explains how I run the latest Sway window manager on Ubuntu LTS using Flatpak's build system.

# Some context

I run an absolutely minimal Ubuntu Desktop setup, because the more I install into the system, the more problems I have with dependencies, conflicts, etc.

Also, I want to install as little as possible to the root system, because it is harder to manage, debug, and also harder to reproduce on my work PC.

Another big challenge that I often run into is that even though Ubuntu LTS is extremely stable (in comparison to distros like Arch), it comes at the cost of extremely outdated packages. Sway is not an exception here - the current version of sway in LTS Ubuntu is two major versions behind.

So having said all of that, I needed somehow to get the latest sway in my rotten Ubuntu setup.

# Why can't you just use nix-shell?

I run all my environments in a [nix-shell](https://nixos.wiki/wiki/Development_environment_with_nix-shell), which allows me to have almost zero dependencies on the host system. So basically I need Ubuntu just to boot up the Linux kernel and start systemd - everything else is handled by nix. 99% of things "just work" this way. But desktop environments are unfortunately not one of them:

```txt
$ nix-shell -p sway --run sway
00:00:00.002 [wlr] [render/egl.c:208] EGL_EXT_platform_base not supported
00:00:00.002 [wlr] [render/egl.c:523] Failed to create EGL context
00:00:00.002 [wlr] [render/gles2/renderer.c:499] Could not initialize EGL
00:00:00.002 [wlr] [render/wlr_renderer.c:272] Could not initialize renderer
00:00:00.002 [sway/server.c:236] Failed to create renderer
```

If the error doesn't make sense to you, don't worry, it doesn't make sense to me either. The important thing is that there is a workaround to make this partially work https://github.com/nix-community/nixGL. It makes sway run, but it is still crashing on some random stuff.

# Why can't you backport it from a newer version of Ubuntu?

Some packages can be successfully backported from later, less stable releases. But desktop environments, even as lightweight as sway, are not one of them. They have so many dependencies that trying to backport all of them is not only a tedious process, it also breaks many other packages that require older versions of those packages. This is exactly the reason why I don't generally want to touch the base system.

So I tried going this way and I wasted a lot of time and failed miserably.

# Why flatpak?

Flatpak, as it turned out, provides an amazing build mechanism. You can think about it as crates in Rust, except you resolve and define all the dependencies manually (but after you do it the first time, it kind of just works).

So basically, I rely on the flatpak build system to compile all the required binaries and libraries and pack them as an archive that I can later use in my system.

Here is how the dependencies look for sway:

```txt
sway
├── json-c
└── wlroots
    ├── wayland-protocols
    ├── libxcb-errors
    ├── libliftoff
    ├── libdisplay-info: [hwdata]
    ├── meson
    ├── libseat
    ├── libdrm
    ├── libinput: [mtdev, libevdev]
    ├── wayland
    └── xorg-xwayland
        ├── pixman
        ├── xcb-util
        ├── xcb-util-wm
        ├── xcb-util-image
        ├── xcb-util-keysyms
        ├── xcb-util-renderutil
        ├── libxcb: [xcb-proto]
        ├── libxcvt
        └── libxfont2
            ├── xtrans
            ├── xorgproto
            └── fontenc: [xorg-font-util]

```

So a lot of stuff. Downloading and building all of that manually would require too much effort.

But if you describe it all in a flatpak, it looks much more manageable: [org.swaywm.sway.yaml on github](https://github.com/fspv/flatpaks/blob/608c1c389cdf261ed4257cac1a43cda6eec75d34/org.swaywm.sway/org.swaywm.sway.yaml). The file contains the description of all the git repos you need to fetch to build the package and its dependencies, and defines the build method for each one of them (make, cmake, meson, etc.).

So now you just have to run `flatpak-builder`, which will download, compile, and package everything for you and install it into your system. On the other side, you will have an archive bundle with all the binaries and required shared libraries to run sway, and you can use them without overriding the ones from your system.

# But can I run a desktop environment from flatpak?

Well, no. BUT you can use files from the installed flatpak and run them directly. You just need to make sure that all the paths are correct, so this sway instance can pick up the correct shared libraries and binaries. Here is the command I use to run flatpak sway:

```sh
#!/bin/sh --norc

export QT_QPA_PLATFORM=wayland
export QT_QPA_PLATFORMTHEME=gtk3
export ECORE_EVAS_ENGINE=wayland_egl
export ELM_ENGINE=wayland_egl
export SDL_VIDEODRIVER=wayland
export _JAVA_AWT_WM_NONREPARENTING=1
export MOZ_ENABLE_WAYLAND=1
export QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb

export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx

export XDG_CURRENT_DESKTOP=sway

APP=$(flatpak info -l org.swaywm.sway)/files

export LD_LIBRARY_PATH="${APP}/lib:${LD_LIBRARY_PATH}"
export PATH="${APP}/bin:${PATH}"
echo "MANDATORY_MANPATH ${APP}/share/man" > ${HOME}/.manpath
export WLR_XWAYLAND=${APP}/bin/Xwayland
export LIBINPUT_QUIRKS_DIR=${APP}/share/libinput

sway >sway.log 2>&1
```

Some of the env variables may vary in different setups, but the idea will stay the same.

The last remaining part I have is this

```txt
$ cat /usr/local/bin/wayland-user
#!/bin/sh
${XDG_DATA_HOME:="${HOME}/.local/share"}/bin/wayland-user

$ cat /usr/share/wayland-sessions/wayland-user.desktop
[Desktop Entry]
Name=User-defined Wayland session
Comment=Run arbitrary file configured by user
Exec=/usr/local/bin/wayland-user
Type=Application
```

This will create a menu entry in your login manager (I use gdm3):

![GDM login screen showing wayland-user session option](/2025/01/sway-flatpak-build/gdm.png)

So now you can just log out, and log in again with the latest sway running in your old system.

# Other alternatives

I also tried to build an AppImage, but for some reason this failed (I don't remember why exactly). And also, you have to manage all the dependencies yourself.

# Final remarks

I used this method across two Ubuntu releases: 22.04 and 24.04 (now). Both times it solved some critical problems for me.

- In 22.04, the wayland version was not supporting `ext-session-lock-v1`, which resulted in a huge security issue where you can see the screen of the locked desktop when the machine wakes up from sleep. Also, touchpad gestures were not supported.
- In 24.04, there were scaling issues where window DPI was set incorrectly after the second monitor is connected.

Both times after upgrading to the latest version everything worked like a charm.

I'm generally very happy with how sway and wayland development is going, and right now I enjoy a perfectly stable and rock-solid desktop environment, which has never happened to me with X11. Also, the battery life is amazing (still far from macOS, but not the couple of hours you got 5 years ago).

The only caveat is that you always need to run the latest version of sway, because fixes are not backported to the older versions and they become obsolete after a few months. And here is where my method helps a lot.

So feel free to try it and let me know if it worked for you!

I'll try to keep the flatpak definition updated moving forward, but no promises here, because even with AI it still takes a couple of hours every time to get the build working with the new version. I intentionally didn't post full instructions and prerequisites here, because things get outdated quite quickly. But I will try to keep instructions in the repo up to date https://github.com/fspv/flatpaks/
