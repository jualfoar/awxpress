![AWXpress icon](./icon.png)

# AWXpress

**Home Assistant integration to control Ansible AWX / Tower job templates from your dashboard.**

[![Open your Home Assistant instance and install AWXpress](https://my.home-assistant.io/badges/custom_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jualfoar&repository=awxpress)

---

## ✨ Features

- 🔘 Control your AWX Job Templates as **switches** in HA
- 📡 Poll job templates periodically via **cron expression**
- 👁️ Sensor to monitor **connection**, **template count**, **next poll**, and **last job**
- 🔔 Show **persistent notifications** when jobs finish or fail
- 🔄 Auto-scheduling using `croniter`
- 🧹 Weekly log cleanup (stub for now)

---

## 📦 Requirements

- Home Assistant **2021.12.0** or newer
- HACS **1.17.0** or newer *(for easy install)*
- No manual Python setup — `awxkit` and `croniter` are auto-installed

---

## 🧠 Installation

### ✅ Via HACS (recommended)

1. Open **Settings → Devices & Services → HACS → Integrations**
2. Click **⋯ → Custom repositories**
3. Add repository:
   - **URL**: `https://github.com/jualfoar/awxpress`
   - **Category**: `Integration`
4. Install **AWXpress**, then **Restart Home Assistant**

### 🛠 Manual installation (dev/testing)

1. Clone or download this repo into your HA `custom_components/` folder:
```

custom_components/awxpress/
├── __init__.py
├── manifest.json
├── config_flow.py
├── coordinator.py
├── sensor.py
├── switch.py
├── notifications.py
├── const.py

```
2. Restart Home Assistant

---

## ⚙️ Configuration

After install, go to **Settings → Devices & Services → Add Integration → AWXpress**.  
Provide the following:

| Field | Example |
|-------|---------|
| AWX/Tower URL | `https://awx.example.com` |
| OAuth Token   | your bearer token |
| SSL Verify    | `true` / `false` |
| Poll Schedule | `0 * * * *` |
| Debug Level   | `INFO`, `DEBUG`, `WARNING`, `ERROR` |

---

## 📈 Usage

### 🔍 Sensor
- Entity: `sensor.awx_awxpress_status`
- State: `connected` / `unavailable`
- Attributes:
  - `templates_count`
  - `next_poll`
  - `last_job_id`
  - `last_job_status`

### ⏯️ Switches
- One switch per AWX job template:
```

switch.awx\_\<template\_id>\_\<template\_name>

```
- Turning it on **launches the template**
- Switch stays ON until job completes
- When done: a **persistent notification** appears with result

---

## 📚 Logbook & History

- Sensor state changes appear in HA **Logbook**
- Jobs show **persistent notifications**
- `last_job_*` data is preserved across reloads

---

## 🤝 Contributing

1. Fork this repo
2. Submit Pull Requests for features or bugfixes
3. Follow HA coding standards

---

## 📄 License

Apache 2.0 © Julian Forero  
See [`LICENSE`](LICENSE)
