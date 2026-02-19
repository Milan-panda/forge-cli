# Deployment Steps

Here is the step-by-step guide to deploying your binary for the public:

## Step 1: Host the Binary
You need to put the `dist/forge` file somewhere public where `curl` can download it.

1.  Go to your GitHub repo: [https://github.com/Milan-panda/forge-cli](https://github.com/Milan-panda/forge-cli)
2.  Click **"Releases"** (on the right sidebar) -> **"Draft a new release"**.
3.  Tag version: `v1.0.0`.
4.  Title: `Initial Release`.
5.  **Upload the binary**: Drag and drop the `dist/forge` file into the release.
6.  Click **"Publish release"**.
7.  **Right-click** the uploaded asset link and "Copy Link Address". 
    It will look like: 
    `https://github.com/Milan-panda/forge-cli/releases/download/v1.0.0/forge`

## Step 2: Update the Installer Script
Now tell your installer where to find that file.

1.  Edit `scripts/install.sh`:
    Change the `DOWNLOAD_URL_BASE` line:
    ```bash
    # LINE 6
    DOWNLOAD_URL_BASE="https://github.com/Milan-panda/forge-cli/releases/download/v1.0.0" 
    # Ensure this matches your actual release URL structure!
    ```
2.  Commit and push this change:
    ```bash
    git add scripts/install.sh
    git commit -m "Update installer URL"
    git push
    ```

## Step 3: Host the Installer
Users need a URL to the raw script content.

1.  In your GitHub repo file list, click on `scripts/install.sh`.
2.  Click the **"Raw"** button.
3.  Copy that URL. It will look like:
    `https://raw.githubusercontent.com/Milan-panda/forge-cli/main/scripts/install.sh`

## Step 4: The Magic Command
Combine it all. Tell your users to run:

```bash
curl -fsSL https://raw.githubusercontent.com/Milan-panda/forge-cli/main/scripts/install.sh | sh
```

This will:
1.  Download your script.
2.  The script downloads the binary from the Release URL.
3.  It installs `forge` to their system!
