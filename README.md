##  🐍 Netcat Replica in Python — From Scratch

A lightweight reimplementation of the classic `netcat (nc)` utility in Python.  
Built as part of my deep-dive into **network programming**, **TCP sockets**, and **ethical hacking foundations**.

This project helped me learn how low-level network communication tools work under the hood — no libraries, no shortcuts — just raw `socket` magic.

---

## 🔧 Features

- 🔌 Connects to remote hosts over TCP
- 📤 Sends and receives messages interactively
- 🧠 Understands how Netcat handles input/output streams
- 🔁 Loop for continuous communication
- ❗ Error handling for connection issues

---

## 📦 Requirements

- Python 3.x
- Runs natively on Kali Linux (or any Linux distro)
- No external dependencies

---

## 🚀 Usage

### 1. Start the server:
```bash
nc -lvnp 9999

