# 📱 NutryGym Mobile Application (Demo)

## 📌 Overview

**NutryGym Mobile** is an informational mobile application built with **Expo and React Native** as part of the **NutriGym UCE distributed system**.

The application provides a **native mobile experience** that presents the NutriGym platform branding, informational content, and controlled access to the **web platform via WebView**, serving as a foundation for future native development.

---

## 🎯 Objectives

* Provide a **mobile demo application** for the NutriGym platform.
* Offer a **native-like user experience** on Android and iOS.
* Centralize access to the **web platform** using an in-app WebView.
* Present informational sections such as:

  * Home
  * About
  * Plans
* Maintain **brand consistency** with the NutriGym web and desktop applications.
* Establish a **scalable base** for future native features.

---

## 🛠️ Technologies Used

### Core Technologies

* ⚛️ **React Native** – Cross-platform mobile framework
* 🚀 **Expo** – Mobile development and runtime environment
* 🧭 **Expo Router** – File-based navigation system
* 🌐 **react-native-webview** – Embedded web platform access

### Tooling

* 📦 **npm** – Dependency management
* 📱 **Expo Go** – Development and testing on real devices

---

## 🔢 Versions and Environment

| Tool         | Version       |
| ------------ | ------------- |
| Node.js      | 18.x          |
| Expo         | ^50.x         |
| React Native | Expo-managed  |
| OS           | Android / iOS |

---

## 📂 Project Structure

```
apps/mobile/
├─ app/                     # Expo Router routes
│  ├─ home.tsx
│  ├─ about.tsx
│  ├─ plans.tsx
│  ├─ platform.tsx
│  ├─ webview.tsx
│  └─ _layout.tsx
├─ assets/                  # Images and branding
│  ├─ logo.png
│  └─ splash-bg.png
├─ src/
│  └─ screens/
│     ├─ SplashScreen.js
│     └─ OfflineScreen.js
├─ components/
├─ hooks/
├─ constants/
├─ app.json
├─ package.json
└─ README.md
```

---

## 🧩 Screen Responsibilities

### Splash Screen

* Displays NutryGym branding.
* Uses a dark background and branded image.
* Serves as a visual introduction to the app (demo purpose).

### Home

* Presents NutryGym branding.
* Displays demo status and application version.
* Acts as the main entry point of the mobile app.

### About

* Provides a description of the NutriGym project.
* Lists key modules and architectural concepts.

### Plans

* Displays available modules:

  * **NutriGym (AI Nutrition)**
  * **Gym (Training)**
* Conceptual representation of platform capabilities.

### Platform

* Provides a call-to-action button.
* Redirects users to the NutriGym web platform using WebView.

### WebView

* Loads the deployed NutriGym web platform.
* Includes a custom top bar with navigation controls.
* Handles URL parameters dynamically.

### Offline Screen

* Acts as a fallback when the web platform is unreachable.
* Ensures the app never appears broken.

---

## 🔁 Web Platform Access Flow

1. User navigates to **Platform** or **Plans**.
2. The app opens the NutriGym web platform inside a **WebView**.
3. If the platform is unavailable:

   * An offline fallback screen is displayed.
4. User can return to the mobile Home screen at any time.

---

## 🚀 Installation (Development)

Install dependencies:

```bash
cd apps/mobile
npm install
```

Run the app:

```bash
npx expo start
```

Scan the QR code using **Expo Go** on Android or iOS.

---

## 📁 Repository Policy

The following files and directories are **not committed** to GitHub:

* `node_modules/`
* `.expo/`
* Build artifacts
* Local environment files

✔ The repository contains **source code and configuration only**, ensuring clean version control and reproducibility.

---

## 🎓 Academic Context

This mobile application is part of the **NutriGym UCE platform**, which includes:

* Web frontend deployed on AWS
* Backend microservices architecture
* API Gateway and containerized services
* Desktop and mobile informational applications

This component demonstrates:

* Cross-platform mobile development
* Navigation architecture with Expo Router
* Web-to-mobile integration
* Clean separation of concerns
* Professional project structuring

---

## 👨‍💻 Author

* **Juan Tulcanaza**
* Developed as part of the **NutriGym UCE** platform
* Degree: Information Systems Engineering
* Central University of Ecuador
