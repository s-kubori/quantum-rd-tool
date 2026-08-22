# Ansible deployment

Brings up the app, Prometheus, and Grafana on an Ubuntu host. The app image
comes from GHCR rather than a local build, so nothing is compiled on the
target.

## Usage

    cd ansible
    ansible-playbook site.yml -K

The stack runs under the compose project name `quantum-rd-tool-deploy`,
separate from the development stack in the repository root. Both bind the
same ports, so stop one before starting the other:

    cd .. && docker compose down

## Variables

| Variable | Default | Notes |
|---|---|---|
| `deploy_dir` | `/opt/quantum-rd-tool` | Where the stack lives on the target |
| `image_tag` | `latest` | Use `sha-<commit>` for a reproducible deploy |
| `anthropic_api_key` | from `$ANTHROPIC_API_KEY` | Optional; the VQE page works without one |

Override any of them at run time:

    ansible-playbook site.yml -K -e image_tag=sha-71aec645d80df28ba594994ecb4f357f79b89702

## Ubuntu 25.10 and later

25.10 ships `sudo-rs` as `/usr/bin/sudo`. It wraps the `-p` prompt string in
its own decoration, which defeats the prompt matching Ansible relies on to
know when to send the become password; the run times out before any task
executes. Point Ansible at the traditional sudo, which is still installed as
`/usr/bin/sudo.ws`:

    export ANSIBLE_BECOME_EXE=/usr/bin/sudo.ws

Not needed on 24.04, where `/usr/bin/sudo` is the traditional implementation.
