---
title: Outlook crashes on launch
tags: [email, outlook, office]
---

If Outlook crashes within seconds of opening, walk through these steps in order. Stop as soon as one fixes it.

## 1. Start in safe mode

Press **Windows + R**, type `outlook.exe /safe`, press Enter. If Outlook stays open, the culprit is an add-in. Disable add-ins one at a time under **File → Options → Add-ins → Go**, then restart normally.

## 2. Repair the Office installation

* **Settings → Apps → Installed apps → Microsoft Office → Modify → Quick Repair**.
* If Quick Repair doesn't help, choose **Online Repair**.

## 3. Recreate the Outlook profile

* **Control Panel → Mail (Microsoft Outlook) → Show Profiles → Add**.
* Name it `New`, enter your account, set it as the default profile, restart Outlook.

## 4. Escalate

If the crash persists, capture the **Event Viewer** entry under *Windows Logs → Application* at the moment Outlook closes, and attach it to a ticket with the **Application Event ID**.
