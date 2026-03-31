# Adding a New CLI Flag to python-heatclient
## A Step-by-Step Contribution Example: `--meta`

> **Prerequisites:** DevStack is running and python-heatclient is installed in editable mode into the DevStack venv per the previous guide.

---

## Overview

This guide walks through adding a new `--meta` flag to the `openstack stack create` command in python-heatclient. This is a realistic, end-to-end contribution example covering:

1. Understanding the codebase
2. Adding the argument to the CLI parser
3. Passing it through to the API
4. Writing a unit test
5. Running tox (pep8 + unit tests)
6. Testing live in DevStack
7. Adding a release note

> **Why `--meta` and not `--tags`?** The `--tags` flag already exists in python-heatclient. Adding `--meta` as an additional way to pass tags demonstrates how to extend existing CLI commands and handle flag interactions — a common real-world contribution scenario.

---

## Step 1 — Understand the Codebase

The `openstack stack create` command lives in:

```
/opt/stack/python-heatclient/heatclient/osc/v1/stack.py
```

Find the `CreateStack` class and its two key methods:

```bash
# Find the class and its methods
grep -n "class CreateStack\|def get_parser\|def take_action" \
  /opt/stack/python-heatclient/heatclient/osc/v1/stack.py
```

- **`get_parser`** — registers all CLI flags with argparse. This is what populates `--help`.
- **`take_action`** — executes when the command runs. Reads `parsed_args` and calls the Heat API.

Look at how an existing flag like `--tags` is implemented end-to-end:

```bash
# See how --tags is defined in get_parser
grep -n "tags" /opt/stack/python-heatclient/heatclient/osc/v1/stack.py
```

Your `--meta` flag will follow the exact same pattern.

---

## Step 2 — Add the `--meta` Argument to `get_parser`

Open the file:

```bash
vim /opt/stack/python-heatclient/heatclient/osc/v1/stack.py
```

Inside the `CreateStack` class, find `get_parser`. Add the `--meta` argument **before** the `return parser` line, alongside the other arguments. A good place is right before or after the existing `--tags` argument:

```python
parser.add_argument(
    '--meta',
    metavar='<tag1,tag2,...>',
    help='Additional comma-separated tags to associate with the stack'
)
```

**Important:** Make sure the indentation matches the surrounding `parser.add_argument(...)` calls exactly. Python is whitespace-sensitive.

Verify the argument was added correctly:

```bash
grep -n "meta\|tags" /opt/stack/python-heatclient/heatclient/osc/v1/stack.py
```

---

## Step 3 — Pass `--meta` Through to the API in `take_action`

Still in `stack.py`, find the `take_action` method inside `CreateStack`. Look for the block where `parsed_args.tags` is handled — your `--meta` logic goes in the same area:

```bash
grep -n "parsed_args.tags\|fields\[.tags" \
  /opt/stack/python-heatclient/heatclient/osc/v1/stack.py
```

The Heat API uses a single `tags` field. To avoid overwriting an existing `--tags` value, merge `--meta` into it:

```python
if parsed_args.meta:
    existing_tags = fields.get('tags', '')
    if existing_tags:
        fields['tags'] = existing_tags + ',' + parsed_args.meta
    else:
        fields['tags'] = parsed_args.meta
```

Add this block **after** the existing `if parsed_args.tags:` block in `take_action`.

The relevant section of `take_action` should now look like:

```python
if parsed_args.tags:
    fields['tags'] = parsed_args.tags

# Your new block below
if parsed_args.meta:
    existing_tags = fields.get('tags', '')
    if existing_tags:
        fields['tags'] = existing_tags + ',' + parsed_args.meta
    else:
        fields['tags'] = parsed_args.meta

if parsed_args.timeout:
    fields['timeout_mins'] = parsed_args.timeout
```

---

## Step 4 — Check for Syntax Errors

Before running anything, verify there are no Python syntax errors:

```bash
source /opt/stack/data/venv/bin/activate
python3 -c "from heatclient.osc.v1 import stack; print('OK')"
deactivate
```

If this prints `OK`, your syntax is clean. If it throws an error, fix it before continuing.

---

## Step 5 — Verify the Flag Appears in Help

```bash
source ~/devstack/openrc admin admin
openstack stack create --help | grep -A3 "\-\-meta"
```

Expected output:

```
  --meta <tag1,tag2,...>
                        Additional comma-separated tags to associate with the
                        stack
```

If the flag does not appear, refer to the troubleshooting section in the previous guide (heatclient dev setup).

---

## Step 6 — Write a Unit Test

The unit tests live here:

```
/opt/stack/python-heatclient/heatclient/tests/unit/osc/v1/test_stacks.py
```

Find the existing `TestStackCreate` class:

```bash
grep -n "class TestStackCreate" \
  /opt/stack/python-heatclient/heatclient/tests/unit/osc/v1/test_stacks.py
```

Open the test file and add two new test methods inside `TestStackCreate` — one for `--meta` alone, one for `--meta` combined with `--tags`:

```bash
vim /opt/stack/python-heatclient/heatclient/tests/unit/osc/v1/test_stacks.py
```

Look at an existing test like `test_stack_create_with_tags` for the exact pattern to follow. Your new tests should look like this:

```python
def test_stack_create_with_meta(self):
    """Test --meta flag sets tags field"""
    arglist = ['my-stack',
               '--template', '/tmp/test.yaml',
               '--meta', 'env=dev,team=backend']
    parsed_args = self.check_parser(self.cmd, arglist, [])
    self.cmd.take_action(parsed_args)

    self.stack_client.create.assert_called_once()
    call_kwargs = self.stack_client.create.call_args[1]
    self.assertEqual('env=dev,team=backend', call_kwargs.get('tags'))

def test_stack_create_with_meta_and_tags(self):
    """Test --meta merges with existing --tags"""
    arglist = ['my-stack',
               '--template', '/tmp/test.yaml',
               '--tags', 'existing-tag',
               '--meta', 'env=dev']
    parsed_args = self.check_parser(self.cmd, arglist, [])
    self.cmd.take_action(parsed_args)

    self.stack_client.create.assert_called_once()
    call_kwargs = self.stack_client.create.call_args[1]
    tags = call_kwargs.get('tags', '')
    self.assertIn('existing-tag', tags)
    self.assertIn('env=dev', tags)
```

> **Tip:** Look at the existing tests in the file carefully before writing yours. The test class setup (mock clients, fixtures) is already handled — you just need to add new `def test_*` methods following the same pattern.

---

## Step 7 — Run the Tests with tox

### Run pep8 (code style check)

```bash
cd /opt/stack/python-heatclient
tox -e pep8
```

Common pep8 issues to watch for:
- Lines over 79 characters
- Missing blank lines between methods
- Trailing whitespace
- Wrong import order

Fix any issues reported and re-run until it passes cleanly.

### Run unit tests

```bash
tox -e py3
```

This runs the full unit test suite. Output will show how many tests passed/failed. Look for your new tests in the output:

```
heatclient.tests.unit.osc.v1.test_stacks.TestStackCreate.test_stack_create_with_meta ... ok
heatclient.tests.unit.osc.v1.test_stacks.TestStackCreate.test_stack_create_with_meta_and_tags ... ok
```

### Run only your specific tests (faster during development)

```bash
tox -e py3 -- heatclient.tests.unit.osc.v1.test_stacks.TestStackCreate.test_stack_create_with_meta
```

### Run both checks together

```bash
tox -e pep8 && tox -e py3
```

Both must pass before submitting a patch.

---

## Step 8 — Test Live in DevStack

With the unit tests passing, test the flag against your running DevStack:

### Create a simple test template

```bash
cat > /tmp/test-stack.yaml << 'EOF'
heat_template_version: 2021-04-16
description: Test stack

resources:
  my_random:
    type: OS::Heat::RandomString
    properties:
      length: 16

outputs:
  random_value:
    value: { get_attr: [my_random, value] }
EOF
```

### Test `--meta` alone

```bash
source ~/devstack/openrc admin admin

openstack stack create \
  --template /tmp/test-stack.yaml \
  --meta "env=dev,team=backend" \
  meta-test-stack

# Wait for it to complete
watch -n 2 openstack stack list
```

### Verify tags were applied

```bash
openstack stack show meta-test-stack | grep tags
```

Expected output:

```
| tags                | env=dev,team=backend
```

### Test `--meta` combined with `--tags`

```bash
openstack stack create \
  --template /tmp/test-stack.yaml \
  --tags "existing-tag" \
  --meta "env=prod" \
  combined-test-stack

openstack stack show combined-test-stack | grep tags
# Expected: existing-tag,env=prod
```

### Clean up test stacks

```bash
openstack stack delete meta-test-stack --yes
openstack stack delete combined-test-stack --yes
```

---

## Step 9 — Add a Release Note

OpenStack requires a release note for any user-visible change. Release notes are managed with the `reno` tool.

```bash
cd /opt/stack/python-heatclient

# Install reno if not present
pip install reno --break-system-packages

# Create a new release note
reno new add-meta-flag-to-stack-create
```

This creates a new YAML file under `releasenotes/notes/`. Open it:

```bash
ls releasenotes/notes/add-meta-flag-to-stack-create-*.yaml
vim releasenotes/notes/add-meta-flag-to-stack-create-*.yaml
```

Replace the generated content with:

```yaml
---
features:
  - |
    Added ``--meta`` flag to the ``openstack stack create`` command.
    Users can now provide additional comma-separated tags using
    ``--meta tag1,tag2``. If ``--tags`` is also provided, the values
    from both flags are merged together.
```

---

## Step 10 — Summary of All Files Changed

| File | Change |
|------|--------|
| `heatclient/osc/v1/stack.py` | Added `--meta` argument to `get_parser`; added merge logic in `take_action` |
| `heatclient/tests/unit/osc/v1/test_stacks.py` | Added `test_stack_create_with_meta` and `test_stack_create_with_meta_and_tags` |
| `releasenotes/notes/add-meta-flag-to-stack-create-*.yaml` | Release note describing the new feature |

---

## Step 11 — What Comes Next (Contributing Upstream)

If this were a real contribution to OpenStack:

```bash
cd /opt/stack/python-heatclient

# Set up git-review (first time only)
pip install git-review --break-system-packages
git review -s

# Create a branch
git checkout -b feature/add-meta-flag

# Stage your changes
git add heatclient/osc/v1/stack.py
git add heatclient/tests/unit/osc/v1/test_stacks.py
git add releasenotes/notes/add-meta-flag-to-stack-create-*.yaml

# Commit with a meaningful message
git commit -m "Add --meta flag to stack create command

Adds a new --meta CLI flag to openstack stack create that
allows users to specify additional tags. If --tags is also
provided, both values are merged before being sent to the
Heat API.

Change-Id: I0000000000000000000000000000000000000000"

# Submit for review
git review
```

This creates a Gerrit review at `review.opendev.org` where core reviewers can comment, vote, and eventually merge the patch.

---

## Complete Workflow Summary

```
Edit stack.py          →  Add --meta to get_parser + take_action
         ↓
Syntax check           →  python3 -c "from heatclient.osc.v1 import stack; print('OK')"
         ↓
Verify --help          →  openstack stack create --help | grep meta
         ↓
Write unit tests       →  test_stacks.py: test_stack_create_with_meta
         ↓
tox -e pep8            →  Code style must pass
         ↓
tox -e py3             →  All unit tests must pass
         ↓
Live test              →  openstack stack create --meta "env=dev" my-stack
         ↓
Verify in DevStack     →  openstack stack show my-stack | grep tags
         ↓
Add release note       →  reno new add-meta-flag-to-stack-create
         ↓
(Upstream) git review  →  Submit to Gerrit for core reviewer approval
```
