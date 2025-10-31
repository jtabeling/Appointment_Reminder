# Using LocalTunnel Instead of ngrok

If you don't want to create an ngrok account, use LocalTunnel - it's free and requires no account!

## Step 1: Install Node.js (If Needed)

1. Download from: https://nodejs.org/
2. Install Node.js (includes npm)
3. Verify installation:
   ```bash
   node --version
   npm --version
   ```

## Step 2: Install LocalTunnel

```bash
npm install -g localtunnel
```

## Step 3: Start LocalTunnel

**Open Terminal 2** (keep webhook server running in Terminal 1):

```bash
lt --port 5000
```

You'll see output like:
```
your url is: https://random-name-12345.loca.lt
```

## Step 4: Update settings.yaml

Copy the URL and update `config/settings.yaml`:

```yaml
calling:
  webhook_url: "https://random-name-12345.loca.lt"
```

**Important:** The URL changes each time you restart LocalTunnel, so update settings.yaml each time.

## Step 5: Test

Run the app as normal:
```bash
python src/app.py data/ready_to_test.xlsx
```

## Pros & Cons

**Pros:**
- ✅ No account needed
- ✅ Free
- ✅ Easy to use

**Cons:**
- ⚠️ URL changes each time
- ⚠️ Requires Node.js installation
- ⚠️ Sometimes less stable than ngrok

