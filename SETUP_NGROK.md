# Setting Up ngrok Authentication

## Quick Setup (2 Minutes)

### Step 1: Sign Up for Free ngrok Account

1. Go to: https://dashboard.ngrok.com/signup
2. Sign up with email (free account is fine)
3. Verify your email

### Step 2: Get Your Authtoken

1. After signing in, go to: https://dashboard.ngrok.com/get-started/your-authtoken
2. **Copy your authtoken** (looks like: `2abc123def456ghi789jkl012mno345pq_678RSTUVWXYZ`)

### Step 3: Configure ngrok

In PowerShell, run:
```bash
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

Replace `YOUR_AUTHTOKEN_HERE` with the token you copied.

Example:
```bash
ngrok config add-authtoken 2abc123def456ghi789jkl012mno345pq_678RSTUVWXYZ
```

You should see:
```
Authtoken saved to configuration file: C:\Users\YourName\AppData\Local\ngrok\ngrok.yml
```

### Step 4: Test ngrok

Now try again:
```bash
ngrok http 5000
```

You should see the forwarding URL without errors!

## Alternative: Use LocalTunnel (No Account Needed)

If you don't want to sign up for ngrok, you can use **localtunnel** instead:

### Install LocalTunnel
```bash
npm install -g localtunnel
```

If you don't have Node.js/npm:
- Download Node.js from: https://nodejs.org/
- Install it
- Then run the install command above

### Use LocalTunnel
```bash
lt --port 5000
```

This will give you a URL like: `https://random-name.loca.lt`

Then update `config/settings.yaml`:
```yaml
webhook_url: "https://random-name.loca.lt"
```

**Note:** LocalTunnel URLs change each time, so you'll need to update settings.yaml each time you restart it.

## Alternative: Use Cloudflare Tunnel (Free, No Account Limits)

### Install Cloudflare Tunnel
1. Download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
2. Extract and run:
```bash
cloudflared tunnel --url http://localhost:5000
```

This gives you a URL like: `https://random-name.trycloudflare.com`

Update `config/settings.yaml`:
```yaml
webhook_url: "https://random-name.trycloudflare.com"
```

## Which Should I Use?

| Service | Account Needed? | Free? | Setup Time |
|---------|----------------|-------|------------|
| **ngrok** | ✅ Yes (free) | ✅ Yes | 2 min |
| **LocalTunnel** | ❌ No | ✅ Yes | 5 min (if Node.js installed) |
| **Cloudflare Tunnel** | ❌ No | ✅ Yes | 5 min |

**Recommendation:** Use ngrok - it's the most reliable and only takes 2 minutes to set up.

## Quick ngrok Setup Script

I can create a script to help set up ngrok. Just let me know your authtoken and I'll create it!

