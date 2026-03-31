# DevStack Setup Guide
## Windows, Mac (Apple Silicon), and Ubuntu 24.04

> **Important:** DevStack is for development and learning only — never run it on a production machine. It makes significant changes to the system. Always use a dedicated VM.

---

## System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 2 cores | 4 cores |
| RAM | 8 GB | 16 GB |
| Disk | 40 GB | 60 GB |
| OS | Ubuntu 24.04 LTS | Ubuntu 24.04 LTS |

---

## Part 1: Windows Setup (via Multipass)

Windows users run DevStack inside an Ubuntu 24.04 VM managed by Multipass.

### Step 1 — Install Multipass

1. Download the Multipass installer from: https://canonical.com/multipass/install
2. Run the installer — administrator privileges are required
3. Multipass uses **Hyper-V** by default on Windows 10/11 Pro or Enterprise. If you have Windows 10 Home, install VirtualBox first and Multipass will use that instead.
4. Open a Command Prompt or PowerShell and verify:

```powershell
multipass version
```

### Step 2 — Create the Ubuntu 24.04 VM

```powershell
multipass launch 24.04 --name devstack --cpus 4 --memory 8G --disk 60G
```

This downloads and launches Ubuntu 24.04 LTS. It may take a few minutes on first run.

### Step 3 — Open a shell into the VM

```powershell
multipass shell devstack
```

You are now inside the Ubuntu 24.04 VM. All subsequent steps are identical to the Ubuntu section below. Jump to **Part 3: DevStack Installation**.

### Useful Multipass Commands (Windows)

```powershell
multipass list                  # list all VMs
multipass stop devstack         # stop the VM
multipass start devstack        # start the VM
multipass shell devstack        # open a shell
multipass delete devstack       # delete the VM
multipass purge                 # permanently remove deleted VMs
```

---

## Part 2: Mac Setup (via Multipass)

Mac users (both Intel and Apple Silicon M-series) run DevStack inside an Ubuntu 24.04 VM managed by Multipass.

### Step 1 — Install Multipass

**Option A — Download installer (recommended):**

1. Download from: https://canonical.com/multipass/install
2. Run the `.pkg` installer
3. Administrator privileges are required

**Option B — Homebrew:**

```bash
brew install --cask multipass
```

Verify installation:

```bash
multipass version
```

### Step 2 — Create the Ubuntu 24.04 VM

```bash
multipass launch 24.04 --name devstack --cpus 4 --memory 8G --disk 60G
```

> **Note for Apple Silicon (M1/M2/M3/M4/M5):** Multipass uses QEMU with Apple's Hypervisor framework on ARM Macs. The VM will be ARM64 Ubuntu — this is fully supported by DevStack on Ubuntu 24.04.

### Step 3 — Open a shell into the VM

```bash
multipass shell devstack
```

You are now inside the Ubuntu 24.04 VM. Continue with **Part 3: DevStack Installation**.

### Useful Multipass Commands (Mac)

```bash
multipass list                  # list all VMs
multipass stop devstack         # stop the VM
multipass start devstack        # start the VM
multipass shell devstack        # open a shell
multipass info devstack         # show VM details including IP
multipass delete devstack       # mark VM for deletion
multipass purge                 # permanently remove deleted VMs
```

---

## Part 3: Ubuntu 24.04 — Native Setup

If you are running Ubuntu 24.04 natively (bare metal or cloud VM), start here directly. Windows and Mac users arrive here after completing Parts 1 or 2.

### Step 1 — Update the system

```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

### Step 2 — Handle MySQL / MariaDB (Critical Step)

Ubuntu 24.04 ships MariaDB as the default MySQL provider. DevStack installs its own MySQL and the two conflict. Clean the slate before running DevStack.

**Check what is currently installed:**

```bash
dpkg -l | grep -E "mysql|mariadb"
```

**Remove everything:**

```bash
sudo systemctl stop mysql mariadb 2>/dev/null || true

sudo apt purge -y \
  mysql-server mysql-server-8.0 mysql-server-core-8.0 \
  mysql-client-8.0 mysql-client-core-8.0 mysql-common \
  mariadb-server mariadb-client mariadb-common \
  mariadb-plugin-provider-bzip2 mariadb-plugin-provider-lz4 \
  mariadb-plugin-provider-lzma mariadb-plugin-provider-lzo \
  mariadb-plugin-provider-snappy libmariadb3 libmysqlclient21 \
  2>/dev/null || true

sudo apt autoremove -y
sudo rm -rf /var/lib/mysql /etc/mysql
```

**Verify everything is gone:**

```bash
dpkg -l | grep -E "mysql|mariadb"
# Should return nothing (or only harmless library packages like libdbd-mysql-perl)
```

> **Why this matters:** DevStack installs MySQL 8.0 itself during `stack.sh`. If MariaDB or a previous MySQL install is present, DevStack's configuration scripts write `mysqlx-bind-address=127.0.0.1` into the MySQL config — a MySQL X Plugin option that is not supported in MariaDB, causing the database to abort on startup and taking down Glance, Nova, and all other services with it.

### Step 3 — Install git

```bash
sudo apt install -y git
```

### Step 4 — Create the stack user

DevStack must not run as root. Create a dedicated `stack` user:

```bash
sudo useradd -s /bin/bash -d /opt/stack -m stack
sudo chmod +x /opt/stack
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
```

Switch to the stack user:

```bash
sudo -u stack -i
```

All remaining steps are run as the `stack` user.

### Step 5 — Clone DevStack

```bash
git clone https://opendev.org/openstack/devstack
cd devstack
```

### Step 6 — Create local.conf

Create the configuration file at `~/devstack/local.conf`:

```bash
cat > ~/devstack/local.conf << 'EOF'
[[local|localrc]]

# Credentials
ADMIN_PASSWORD=secret
DATABASE_PASSWORD=secret
RABBIT_PASSWORD=secret
SERVICE_PASSWORD=secret

# Core services
enable_service n-api n-cpu n-cond n-sch n-novnc
enable_service placement

# Networking (OVN)
disable_service q-agt q-l3 q-dhcp q-meta
enable_service ovn

# Orchestration (Heat)
enable_plugin heat https://opendev.org/openstack/heat
enable_service h-eng h-api h-api-cfn h-api-cw

# Dashboard
enable_service horizon

# Clone python-heatclient from source for development
LIBS_FROM_GIT=python-heatclient
EOF
```

> **Note:** `LIBS_FROM_GIT=python-heatclient` tells DevStack to clone the Heat client from source into `/opt/stack/python-heatclient`, which is needed for the contribution exercises later.

### Step 7 — Run stack.sh

```bash
cd ~/devstack
./stack.sh 2>&1 | tee /tmp/stack.log
```

The `tee` command writes output to both the terminal and `/tmp/stack.log`. To watch the log from a second terminal while it runs:

```bash
# In a second terminal (multipass shell devstack, then sudo -u stack -i)
tail -f /tmp/stack.log
```

To monitor MySQL startup during the run:

```bash
# In a third terminal
watch -n 2 sudo systemctl status mysql
```

Installation takes approximately **20–40 minutes** depending on network speed and hardware.

### Step 8 — Verify the installation

When `stack.sh` completes successfully you will see a summary like:

```
This is your host IP address: 10.x.x.x
Horizon is now available at http://10.x.x.x/dashboard
Keystone is serving at http://10.x.x.x/identity/
The default users are: admin and demo
The password: secret
```

Verify all services are running:

```bash
sudo systemctl list-units "devstack@*" --no-pager
```

All services should show `active (running)`. Key services to verify:

```
devstack@keystone.service        active (running)
devstack@n-api.service           active (running)
devstack@n-cpu.service           active (running)
devstack@g-api.service           active (running)
devstack@neutron-api.service     active (running)
devstack@h-api.service           active (running)
devstack@h-eng.service           active (running)
devstack@placement-api.service   active (running)
```

---

## Part 4: Verify OpenStack Services

```bash
# Source credentials
source /opt/stack/devstack/openrc admin admin

# Keystone
openstack service list
openstack token issue

# Nova
openstack compute service list
openstack flavor list

# Glance
openstack image list

# Neutron
openstack network list
openstack network agent list

# Heat
openstack orchestration service list
```

---

## Part 5: Re-running DevStack

If you need to re-run (e.g. after changing `local.conf`):

```bash
cd ~/devstack
./unstack.sh       # stops all services
./clean.sh         # removes all DevStack-installed packages including MySQL
./stack.sh 2>&1 | tee /tmp/stack.log
```

> **Note:** `clean.sh` removes MySQL completely. This is intentional — `stack.sh` will reinstall it fresh. This guarantees a clean slate and is recommended especially when students re-run from a broken state.

---

## Troubleshooting

### MySQL fails to start

Check the logs:

```bash
sudo journalctl -u mysql -n 50 --no-pager
```

The most common cause is a conflicting MariaDB or MySQL installation from before DevStack ran. Re-do Step 2 (the purge), then rerun `./clean.sh && ./stack.sh`.

### A service shows as failed

```bash
# Check which services failed
sudo systemctl list-units "devstack@*" | grep failed

# Check a specific service log
sudo journalctl -u devstack@n-api -n 50 --no-pager

# Or use the DevStack log files directly
ls /opt/stack/logs/
tail -100 /opt/stack/logs/n-api.log
```

### Heat router1 error during stack.sh

If you see `No Router found for router1` near the end of `stack.sh`, this is a Tempest configuration issue — not a Heat service failure. Your Heat services (`h-api`, `h-eng`) will still be running correctly. Verify with:

```bash
openstack orchestration service list
```

This can be ignored for development purposes, or fixed by ensuring `NEUTRON_CREATE_INITIAL_NETWORKS` is not set to `False` in `local.conf`.

### Checking if stack.sh is still running

```bash
pgrep -a stack.sh
tail -f /tmp/stack.log
```
