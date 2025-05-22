# 🔐 ESP32 OTP Smart Lock Web Interface

This project is a **responsive, mobile-friendly web interface** for controlling an OTP-based smart lock system built using the **ESP32**. The interface includes features like OTP request/validation, lock/unlock controls, lockdown protection after multiple failed attempts, and a secure admin password override.

---

## 📱 Features

- 🔒 Lock and unlock control through OTP
- 🔄 Generate and validate OTPs via web
- 🔁 Auto-status refresh every 5 seconds
- ⚠️ Lockdown mode after 3 incorrect attempts
- 🛡️ Admin password override to unlock system
- 🌗 Light/Dark mode toggle with persistent theme
- 📱 Mobile-first design with phone-like frame styling

---

## 📷 Interface Preview

![Screenshot 2025-05-22 122906](https://github.com/user-attachments/assets/9db13504-28ec-4d05-b982-09ab0b2c7b47)

## 🧰 Technologies Used

- **HTML/CSS/JavaScript**
- Mobile-responsive layout with CSS
- Dark/Light theme using CSS Variables
- ESP32 as backend (assumed via Flask, MicroPython, or Arduino HTTP server)

---

## 🚀 Getting Started

### 1. Upload Web Files to ESP32
You can serve the HTML via:
- MicroPython using `uasyncio` and `picoweb` or `microdot`
- ESPAsyncWebServer in Arduino IDE

### 2. Backend Endpoints Required

The front-end expects these API endpoints from your ESP32:

| Endpoint              | Method | Description                          |
|-----------------------|--------|--------------------------------------|
| `/generate_otp`       | POST   | Generates a new OTP                  |
| `/validate_otp`       | POST   | Validates user-entered OTP           |
| `/lock_system`        | POST   | Immediately locks the system         |
| `/verify_password`    | POST   | Validates admin override password    |
| `/get_status`         | GET    | Returns system status + lockdown flag|

### 3. File Structure

esp32-otp-lock/
├── index.html
├── style.css (optional, embedded in HTML)
├── script.js (optional, embedded in HTML)
Lockdown Logic
Lock the system after 3 wrong attempts and require the admin password to unlock.

Deployment
Upload your HTML to the ESP32 SPIFFS or embed it directly into a C/C++ or Python string if using Arduino/MicroPython. Make sure the backend endpoints match the expected paths.

 Author
Made with ❤️ by [Swetha M]
If you find this useful, feel free to ⭐ the repo!

