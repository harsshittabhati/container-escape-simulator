# 🔐 Container Escape Simulator and Host Intrusion Automation

## 📌 Overview

This project simulates advanced Linux container escape attacks (via `chroot`, `mount`, `/proc`, etc.) and implements automated detection pipelines using host-based tools like Sysdig and Auditd. Detected events are parsed and forwarded to OpenSearch for central analysis and alerting.


## 🧩 Components and Stack

| Component   | Purpose                                         |
|------------|--------------------------------------------------|
| Docker      | Run privileged container with host mount        |
| Sysdig      | Capture and parse container behavior            |
| Auditd      | Monitor critical syscalls and escape attempts   |
| Python      | Custom parsing & forwarding scripts             |
| OpenSearch  | Central log aggregation and alerting platform   |


## 🖥️ Architecture Diagram

![Architecture](architecture/diagram.png)


## 🚀 How to Run

### 1. Clone and Setup

```
git clone https://github.com/your-username/container-escape-simulator.git
cd container-escape-simulator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Build and Launch Vulnerable Container
```
docker build -t escape-test .
docker run -d --privileged --name escape-test -v /:/host escape-test sleep infinty
docker exec -it escape-test bash
chroot /host && cat /etc/shadow  # Trigger escape behavior
```

### 3. Auditd Installation
```
sudo apt update && sudo apt install auditd audispd-plugins –y
systemctl enable --now auditd
systemctl start auditd
systemctl status auditd
```

### 4. Configure and Run Auditd Monitoring
```
sudo cp auditd/container_escape.rules /etc/audit/rules.d/
sudo systemctl restart auditd

```

### 5. Sysdig Automatic Installation

To install sysdig automatically in one step, simply run the following command. This is the recommended installation method.

```
curl -s https://s3.amazonaws.com/download.draios.com/stable/install-sysdig | sudo bash
```
For detail guide check this github [Repository](https://github.com/annulen/sysdig-wiki/blob/master/How-to-Install-Sysdig-for-Linux.md)

### 6. Capture Container Activity with Sysdig
```
sudo sysdig -w sysdig/sysdig_escape.scap
sudo sysdig -r sysdig/sysdig_escape.scap -p "%evt.time %user.name %proc.name %evt.type %evt.args" > escape_logs.txt
```
- Run Sysdig with root privileges and capture all system activity into a file called sysdig_escape.scap inside the sysdig directory.

### 7. Opensearch & Opensearch Dashboard Installation

- For Opensearch check the [Medium](https://medium.com/@cybertoolguardian/installing-and-setting-up-opensearch-6fbf88b544ec) or [Official Documentation](https://docs.opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/) or this [Youtube video](https://www.youtube.com/watch?v=4LMpWmW52T8&t=1s)
-  For Opensearch Dashboard check the [Medium](https://medium.com/@cybertoolguardian/installing-and-setting-up-opensearch-dashboards-78b540905a29) or [Official Documentation](https://docs.opensearch.org/docs/latest/install-and-configure/install-dashboards/debian/) or this [Youtube video](https://www.youtube.com/watch?v=kABS1fCoxDg)

Recommendation- Follow the Youtube video for clear and detailed guidance.

### 8. Detect Escape Events from Sysdig Logs
```
python3 sysdig/detect_escape_from_sysdig.py
python3 sysdig/push_to_opensearch.py
```
