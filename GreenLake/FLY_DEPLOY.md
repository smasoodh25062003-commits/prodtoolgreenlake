# Deploy GreenLake to Fly.io

This folder is ready to deploy. Follow these steps.

## 1. Install Fly CLI

**Windows (PowerShell):**
```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

Or install from: https://fly.io/docs/hands-on/install-flyctl/

## 2. Log in

```bash
fly auth login
```

Sign in in the browser when prompted.

## 3. Deploy from this folder

Open a terminal in the **GreenLake** app folder (the one that contains `main.py`, `Dockerfile`, and `fly.toml`):

```bash
cd c:\Users\hussasye\Downloads\GreenLake\GreenLake
fly launch --no-deploy
```

- When asked for an app name, use `greenlake` or any name you like.
- Choose a region (e.g. nearest to you).
- Say **no** to adding a database or Redis.

Then deploy:

```bash
fly deploy
```

## 4. Open your app

When deploy finishes, you’ll get a URL like:

**https://greenlake.fly.dev**

- Home / Tools: https://greenlake.fly.dev/
- Device Management: https://greenlake.fly.dev/DeviceManagement.html
- Subscription Management: https://greenlake.fly.dev/Subscriptionmanagement.html
- User Management: https://greenlake.fly.dev/UserManagement.html

## 5. Later: redeploy after changes

From the same folder:

```bash
fly deploy
```

## Optional: change app name or region

Edit `fly.toml` and change the `app = "greenlake"` line, then run `fly deploy` again.

---

## Deploy from GitHub (auto-deploy on push)

You can have Fly.io deploy automatically whenever you push to GitHub.

### One-time setup

1. **Create the Fly app** (if you haven’t already). From this folder:
   ```bash
   fly launch --no-deploy
   ```
   Use app name `greenlake`, pick a region, say no to DB/Redis.

2. **Create a deploy token.** In a terminal:
   ```bash
   fly tokens create deploy -x 999999h
   ```
   Copy the whole token (starts with `FlyV1`).

3. **Add the token to GitHub.** On GitHub:
   - Open your repo → **Settings** → **Secrets and variables** → **Actions**
   - **New repository secret**
   - Name: `FLY_API_TOKEN`
   - Value: paste the token → **Add secret**

4. **Push the workflow.** The repo already has `.github/workflows/fly.yml`. Commit and push:
   ```bash
   git add .github/workflows/fly.yml
   git commit -m "Add Fly.io deploy from GitHub"
   git push
   ```

### After setup

Every push to the **master** or **main** branch will trigger a deploy. Check the **Actions** tab on GitHub for status. No need to run `fly deploy` locally.
