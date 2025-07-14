![AWXpress icon](./icon.png)
# AWXpress

Home Assistant integration for controlling Ansible AWX / Tower job templates directly from your dashboard.

[![AWXpress](https://my.home-assistant.io/badge/customrepository?owner=jualfoar&repository=awxpress)](https://my.home-assistant.io/create-link/?redirect=hacs_repository)

## Features

- **Browse** your AWX job templates as Home Assistant switches  
- **Launch** jobs on demand and wait for completion  
- **Sensor** reporting connection status, template count, next scheduled poll, and last job result  
- **Cron-style polling** to keep template list up to date  
- **Persistent notifications** in HA when jobs complete or fail  
- **Weekly log rotation** stub for future expansion  

## Requirements

- Home Assistant **2021.12.0** or newer  
- HACS **1.17.0** or newer (for HACS install)  
- No extra manual Python installs — `awxkit` and `croniter` are auto-installed  

## Installation

### Via HACS (recommended)

1. In Home Assistant UI, go to **Settings → Integrations → HACS → Integrations → +**.  
2. Click **⋯ Custom Repositories** (bottom), add:
   - **URL**: `https://github.com/jualfoar/awxpress`  
   - **Category**: `Integration`  
3. After adding, search for **AWXpress**, click **Install**, then **Restart Home Assistant**.

### Manual

1. Clone or download this repo into your HA `custom_components` folder:
```

custom\_components/awxpress/
├─ **init**.py
├─ manifest.json
├─ coordinator.py
├─ config\_flow\.py
├─ sensor.py
├─ switch.py
├─ notifications.py
└─ const.py

```
2. Restart Home Assistant.

## Configuration

After installation, go to **Settings → Devices & Services** and click **Add Integration → AWXpress**. Enter:

- **AWX/Tower URL** (e.g. `https://awx.example.com`)  
- **OAuth Token** (stored securely in Home Assistant’s secrets)  
- **SSL Verification** on/off  
- **Poll Schedule** (cron expression)  
- **Debug Level**  

## Usage

- **Sensor**: `sensor.awx_awxpress_status`  
- **State**: `connected` / `unavailable`  
- **Attributes**:
 - `templates_count`: number of templates  
 - `next_poll`: next scheduled refresh time  
 - `last_job_id` / `last_job_status`: result of your last launched job  

- **Switches**: one per AWX job template, named  
```

switch.awx\_\<template\_id>\_\<template\_name>

```
- **Turn on** to launch the template; the switch stays “on” until the job finishes.  
- A persistent notification appears when the job completes.

## Logbook & History

- The sensor’s **state** changes on each poll, so you’ll see Logbook entries whenever it goes `connected` → `unavailable` or vice versa.  
- Job launches and completions appear as persistent notifications.

## Development & Contributing

1. Fork this repo on GitHub.  
2. Open a pull request with bugfixes or new features.  
3. Ensure your code follows HA integration guidelines and passes linting.

## License

MIT © Julian Forero  
