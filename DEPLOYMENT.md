# Private Deployment Guide regarding Forge

This guide explains how to deploy and install **Forge** privately using a Git repository, ensuring your code remains secure and is not published to the public PyPI registry.

## How it Works

Python's `pip` package manager can install packages directly from a Git repository. If the repository is private, `pip` uses your local SSH keys or an HTTPS token to authenticate with GitHub/GitLab.

## Prerequisites

1.  **Private Repository**: The code must be pushed to a private repository (e.g., GitHub private repo).
2.  **Access**: The user installing the package must have read access to that repository.
3.  **SSH Keys**: The user must have their SSH keys configured and added to their GitHub/GitLab account.

## Installation Commands

### Option 1: SSH (Recommended)

Use this method if you have SSH keys set up (i.e., you can run `git clone git@github.com...` without a password).

```bash
# General syntax
pip install git+ssh://git@github.com/<username>/<repo_name>.git

# Example for Forge
pip install git+ssh://git@github.com/milan/forge.git
```

### Option 2: HTTPS with Token

Use this method for CI/CD pipelines or if you don't use SSH. You will need a Personal Access Token (PAT).

```bash
# General syntax
pip install git+https://<token>@github.com/<username>/<repo_name>.git
```

### Option 3: Install Specific Branch or Tag

To install a specific version:

```bash
# Install 'dev' branch
pip install git+ssh://git@github.com/milan/forge.git@dev

# Install 'v1.0.0' tag
pip install git+ssh://git@github.com/milan/forge.git@v1.0.0
```

## Updating

To update to the latest version of the code in the repository, add the `--upgrade` flag:

```bash
pip install --upgrade git+ssh://git@github.com/milan/forge.git
```

- **Access Control**: You control who can install it by managing repository access on GitHub/GitLab.

## Option 2: Self-Hosted Private Registry (pypiserver)

If you want a "PyPI-like" experience but on your own server.

1.  **Install pypiserver**: `pip install pypiserver passlib`
2.  **Run Server**: `pypi-server -p 8080 ~/packages`
3.  **Build Package**: `python setup.py sdist bdist_wheel`
4.  **Upload**: `twine upload --repository-url http://localhost:8080 dist/*`
5.  **Install**:
    ```bash
    pip install forge --extra-index-url http://localhost:8080/simple/ --trusted-host localhost
    ```

**Note**: This still distributes source code/bytecode unless you use obfuscation.

## Option 3: Binary Distribution (PyInstaller) - BEST FOR PRIVACY

If you want to distribute the **product** without sharing the **source code**.

1.  **Install**: `pip install pyinstaller`
2.  **Build**:
    ```bash
    pyinstaller --onefile --name forge src/forge/main.py
    ```
3.  **Distribute**:
    - The executable will be in `dist/forge` (Mac/Linux) or `dist/forge.exe` (Windows).
    - Send this single file to your users.
    - **No Python or pip required** for them!
    - **Source code is hidden** (compiled into the binary).

### End-User Installation (Binary)

For your users to run `forge` like a normal command:

1.  **Download** the `forge` file you sent them.
2.  **Make Executable** (Mac/Linux):
    ```bash
    chmod +x forge
    ```
3.  **Move to Path**:
    ```bash
    sudo mv forge /usr/local/bin/
    ```
4.  **Run**:
### One-Line Installer (The "Cool" Way)

To provide an experience like `curl ... | sh`:

1.  **Host the Binary**:
    - Compile your binary (see above).
    - Host it publicly (e.g., GitHub Releases, S3, Dropbox public link).
    - Name them `forge-linux` and `forge-mac`.

2.  **Host the Installer Script**:
    - I have created a template script in `scripts/install.sh`.
    - **Edit lines 5-7** of `scripts/install.sh` to point to your actual binary URL.
    - Upload `scripts/install.sh` to a public URL (e.g., GitHub Gist, or your website).

3.  **The Command**:
    Your users simply run:
    ```bash
    curl -fsSL https://your-website.com/install.sh | sh
    ```

