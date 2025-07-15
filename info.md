# AWXpress

Integration for Home Assistant to control [Ansible AWX / Tower](https://github.com/ansible/awx) job templates.

---

## 🔧 What it does

- Adds a **switch** per AWX job template.
- Lets you **launch jobs on demand**.
- Provides a **status sensor**:
  - Number of job templates
  - Next poll time (via cron)
  - Last job ID and result
- Shows **persistent notifications** when jobs complete.
- Includes basic **log cleanup** logic (extensible).

---

## 🚀 Installation via HACS

1. Go to **HACS → Integrations → Custom Repositories**
2. Add:
   - URL: `https://github.com/jualfoar/awxpress`
   - Category: `Integration`
3. Search for `AWXpress` and install
4. Restart Home Assistant
5. Configure via **Settings → Devices & Services → Add Integration → AWXpress**

---

## ⚙️ Setup Parameters

- **AWX/Tower URL** (e.g. `https://awx.example.com`)
- **Bearer Token** for authentication
- **Verify SSL** (on/off)
- **Poll Schedule** in cron format (`0 * * * *`)
- **Debug Level** (INFO, DEBUG...)

---

## 🧠 Requirements

- Home Assistant `>= 2021.12`
- `awxkit`, `croniter` are installed automatically

---

## 📦 License

Apache 2.0 — see `LICENSE` file  
Maintained by [@jualfoar](https://github.com/jualfoar)
