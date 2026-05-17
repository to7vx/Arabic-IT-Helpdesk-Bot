---
title: Fix VPN error 720 on Windows
tags: [network, vpn, windows]
---

VPN error 720 usually means the WAN Miniport adapter is in a bad state. This is the standard fix.

## Quick fix

1. Open **Device Manager** (`devmgmt.msc`).
2. Expand **Network adapters**.
3. Right-click every adapter starting with **WAN Miniport** and choose **Uninstall device**. Confirm the prompts. Don't reboot yet.
4. From the **Action** menu, choose **Scan for hardware changes**. Windows will reinstall the miniports.
5. Try the VPN again.

## If error 720 persists

* Check that the VPN policy allows your account from outside the corporate network.
* Confirm your laptop has the latest network drivers from your vendor.
* Submit a ticket including the output of `ipconfig /all` and the exact time of the failed connection.
