# 🖥️ NutryGym Desktop Application

## 📌 Overview

**NutryGym Desktop** is an informational desktop application built with **Electron** as part of the **NutriGym UCE distributed system**.

The application loads the NutryGym web platform when online and provides a **fully branded offline fallback interface** when the backend or network is unavailable, ensuring continuity and a professional user experience.

---

## 🎯 Objectives

- Provide a **desktop version** of the NutryGym platform.
- Reuse the existing **web frontend** without duplicating business logic.
- Implement an **offline fallback UI** for resilience.
- Maintain **UI/UX consistency** with the NutryGym web application.
- Follow **industry best practices** for Electron security and packaging.

---

## 🛠️ Technologies Used

### Core Technologies
- ⚡ **Electron** – Desktop application framework
- 🟢 **Node.js** – JavaScript runtime
- 🌐 **HTML5 / CSS3 / JavaScript** – Offline UI and interactions

### Tooling
- 📦 **electron-builder** – Packaging and installer generation
- 📥 **npm** – Dependency management
- 🪟 **NSIS** – Windows installer target

---

## 🔢 Versions and Environment

| Tool | Version |
|---|---|
| Node.js | 18.x (defined in `.nvmrc`) |
| Electron | ^40.x |
| electron-builder | ^26.x |
| OS | Windows 10 / 11 |

---

## 📂 Project Structure

```

apps/desktop/
├─ assets/
│  └─ logo.svg
├─ main.js
├─ preload.js
├─ offline.html
├─ offline.css
├─ package.json
├─ package-lock.json
└─ README.md

````

---

## 🧩 File Responsibilities

- **main.js**  
  Electron entry point. Handles:
  - Window creation
  - Loading the online NutryGym web platform
  - Detecting connectivity issues
  - Falling back to the offline UI

- **preload.js**  
  Secure preload layer using:
  - `contextIsolation: true`
  - No Node.js exposure to the renderer
  - Read-only environment data

- **offline.html / offline.css**  
  Offline fallback interface:
  - Uses NutryGym brand colors and typography
  - Displays connection status
  - Includes retry animation and feedback

- **assets/logo.svg**  
  NutryGym official logo for consistent branding.

---

## 🔁 Offline Fallback Mechanism

The application follows this logic:

1. On startup, Electron attempts to load the NutryGym web platform via its public URL.
2. If the request fails (server down, DNS error, no internet):
   - The app automatically loads a **local offline interface**.
3. The offline interface provides:
   - Clear user feedback
   - Retry action with loading animation
   - Brand-consistent design

This ensures the desktop app **never appears broken**.

---

## 🔐 Security Considerations

The desktop application follows Electron security best practices:

- ❌ `nodeIntegration` disabled
- ✅ `contextIsolation` enabled
- 🚫 No direct access to Node.js APIs from the renderer
- 📄 Static and trusted local offline files

---

## 🚀 Installation (Development)

Install dependencies:

```bash
npm install
````

Run the app in development mode:

```bash
npm start
```

---

## 🏗️ Build and Packaging

Generate the Windows installer:

```bash
npm run dist
```

Generated artifacts:

* `dist/NutryGym Setup <version>.exe`
* `dist/win-unpacked/`

> ⚠️ Build artifacts and binaries are intentionally excluded from the repository.

---

## 📁 Repository Policy

The following are **not committed** to GitHub:

* `node_modules/`
* `dist/`
* `.exe` installers

✔ The repository contains **source code and configuration only**, ensuring reproducible builds and clean version control.

---

## 🎓 Academic Context

This desktop application is part of the **NutriGym UCE platform**, which includes:

* Web frontend deployed on AWS
* Multiple backend microservices
* API Gateway and containerized services
* Desktop and mobile informational applications

This component demonstrates:

* Distributed system design
* Fault tolerance
* Separation of concerns
* Professional software delivery practices

---

## 👨‍💻 Author

* **Juan Tulcanaza**
* Developed as part of the **NutriGym UCE** platform
* Degree: Information Systems Engineering
* Central University of Ecuador
