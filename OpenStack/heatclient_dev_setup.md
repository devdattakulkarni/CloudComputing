# Setting Up python-heatclient for Development
## Installing, Modifying, and Testing the Heat CLI

> **Prerequisites:** DevStack must be fully installed and running per the DevStack Setup Guide. All commands are run as the `stack` user unless noted otherwise.

---

## Overview

DevStack runs all OpenStack services inside a Python virtualenv at `/opt/stack/data/venv`. This is a critical detail — any changes you make to a client library must be installed into **that virtualenv** for the `openstack` CLI to pick them up. Installing system-wide or into your user's Python environment (`~/.local`) will have no effect.

This guide covers:
1. Locating the cloned python-heatclient repo
2. Understanding the DevStack virtualenv
3. Installing heatclient into the venv in editable mode
4. Verifying the setup is correct

---

## Step 1 — Locate the Repository

If you used `LIBS_FROM_GIT=python-heatclient` in your `local.conf` (recommended), DevStack cloned the repo during `stack.sh`:

```bash
ls /opt/stack/python-heatclient
```

If the directory does not exist (i.e. `LIBS_FROM_GIT` was not set), clone it manually:

```bash
cd /opt/stack
git clone https://opendev.org/openstack/python-heatclient
```

Verify the repo contents:

```bash
ls /opt/stack/python-heatclient
# You should see: heatclient/  setup.cfg  setup.py  tox.ini  requirements.txt ...
```

---

## Step 2 — Understand the DevStack Virtualenv

DevStack creates a dedicated Python virtualenv for all OpenStack services:

```
/opt/stack/data/venv/
```

The `openstack` CLI that you use to run commands lives inside this venv:

```bash
which openstack
# /opt/stack/data/venv/bin/openstack
```

This means:
- Installing packages with `pip install` outside the venv has **no effect** on the CLI
- Installing into `~/.local` (user-level) has **no effect** on the CLI
- You must install into `/opt/stack/data/venv` for changes to be visible

You can verify which heatclient the venv is currently using:

```bash
/opt/stack/data/venv/bin/pip show python-heatclient | grep -E "Location|Editable"
```

---

## Step 3 — Install heatclient into the DevStack Venv

Activate the DevStack virtualenv and install your local heatclient in **editable mode** (`-e`). Editable mode means Python loads the code directly from `/opt/stack/python-heatclient` — any file you edit is immediately live with no reinstall needed.

```bash
# Activate the DevStack virtualenv
source /opt/stack/data/venv/bin/activate

# Install your local heatclient in editable mode
pip install -e /opt/stack/python-heatclient

# Deactivate when done
deactivate
```

---

## Step 4 — Verify the Installation

Check that the venv is now pointing to your local repo:

```bash
/opt/stack/data/venv/bin/pip show python-heatclient
```

Expected output:

```
Name: python-heatclient
Version: 5.2.0.dev1
...
Location: /home/stack/.local/lib/python3.12/site-packages
Editable project location: /opt/stack/python-heatclient
```

> **Note:** The `Location` field showing `~/.local/...` is normal for editable installs — it is just where pip stores a small `.pth` pointer file. What matters is that `Editable project location` points to `/opt/stack/python-heatclient`. The version number `5.x.x.dev1` also confirms you are running the development version from source, not a released package.

Verify Python is actually loading code from your local repo:

```bash
/opt/stack/data/venv/bin/python3 -c "import heatclient; print(heatclient.__file__)"
# Expected: /opt/stack/python-heatclient/heatclient/__init__.py
```

Confirm there is no other copy of heatclient shadowing yours:

```bash
find /opt/stack/data/venv -name "stack.py" -path "*/osc/v1/*" 2>/dev/null
```

If you see a file inside `/opt/stack/data/venv/lib/python3.12/site-packages/heatclient/`, that is a non-editable install shadowing your local repo. Remove it:

```bash
source /opt/stack/data/venv/bin/activate
pip uninstall python-heatclient -y
pip install -e /opt/stack/python-heatclient
deactivate
```

---

## Step 5 — Verify the CLI Picks Up Your Changes

Test that the CLI is loading from your local file:

```bash
source ~/devstack/openrc admin admin
openstack stack create --help | head -5
```

If the help output appears without errors, the CLI is loading your local file correctly.

---

## Step 6 — Set Up for Local Testing (Recommended)

Install tox and test dependencies so you can run tests before submitting patches:

```bash
cd /opt/stack/python-heatclient

# Install tox
pip install tox --break-system-packages

# Verify tox environments available
tox -l
# Should list: py3, pep8, functional, etc.
```

---

## Key Concept: The Two Python Environments

| Environment | Path | Used by |
|-------------|------|---------|
| System Python | `/usr/bin/python3` | System tools, apt packages |
| DevStack venv | `/opt/stack/data/venv/bin/python3` | `openstack` CLI, all OpenStack services |

When you run `openstack stack create`, it always uses the **DevStack venv**. The correct development workflow is:

```bash
# 1. Edit your file
vim /opt/stack/python-heatclient/heatclient/osc/v1/stack.py

# 2. No reinstall needed — editable mode means changes are live immediately

# 3. Test via the CLI
source ~/devstack/openrc admin admin
openstack stack create --help
```

---

## Troubleshooting

### New flag does not show in `openstack stack create --help`

Check for a non-editable copy shadowing your repo:
```bash
find /opt/stack/data/venv -name "stack.py" -path "*/osc/v1/*"
```
If a file appears inside `site-packages`, reinstall as shown in Step 4.

Check for Python syntax errors:
```bash
source /opt/stack/data/venv/bin/activate
python3 -c "from heatclient.osc.v1 import stack; print('OK')"
```

Clear bytecode cache:
```bash
find /opt/stack/python-heatclient -name "*.pyc" -delete
find /opt/stack/python-heatclient -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
```

### `ModuleNotFoundError: No module named 'openstackclient'`

```bash
source /opt/stack/data/venv/bin/activate
pip install python-openstackclient
deactivate
```

### Wrong `openstack` binary being used

```bash
which openstack
# Must be: /opt/stack/data/venv/bin/openstack
# If not, source credentials first:
source ~/devstack/openrc admin admin
```
