# Quick Fix: Configure ngrok with Your Authtoken

## Your Authtoken
```
34paTIAbxk3cY8WYfm6I1mriIsx_2JTgxHuNkqwLaHGAADTTA
```

## Option 1: Download and Configure (Easiest)

### Step 1: Download ngrok
1. Go to: https://ngrok.com/download
2. Download for Windows
3. Extract `ngrok.exe` to `C:\`

### Step 2: Configure ngrok
Open PowerShell and run:
```powershell
C:\ngrok.exe config add-authtoken 34paTIAbxk3cY8WYfm6I1mriIsx_2JTgxHuNkqwLaHGAADTTA
```

### Step 3: Test ngrok
```powershell
C:\ngrok.exe http 5000
```

**Copy the HTTPS URL** and update `config/settings.yaml`

## Option 2: Use Full Path in Scripts

If ngrok is elsewhere (e.g., Downloads), use full path:

**To configure:**
```powershell
"C:\Users\jerry\Downloads\ngrok.exe" config add-authtoken 34paTIAbxk3cY8WYfm6I1mriIsx_2JTgxHuNkqwLaHGAADTTA
```

**To run:**
```powershell
"C:\Users\jerry\Downloads\ngrok.exe" http 5000
```

## Option 3: Add ngrok to PATH

1. Place `ngrok.exe` in a folder (e.g., `C:\Tools\`)
2. Add to PATH:
   - Press Win+X → System
   - Advanced system settings
   - Environment Variables
   - Edit Path → Add `C:\Tools\`
3. Restart PowerShell
4. Run: `ngrok config add-authtoken 34paTIAbxk3cY8WYfm6I1mriIsx_2JTgxHuNkqwLaHGAADTTA`

## Quick Command (Copy & Paste)

If ngrok is at `C:\ngrok.exe`:
```powershell
C:\ngrok.exe config add-authtoken 34paTIAbxk3cY8WYfm6I1mriIsx_2JTgxHuNkqwLaHGAADTTA
```

Then test:
```powershell
C:\ngrok.exe http 5000
```

## What's Next?

After ngrok is configured:

1. **Start webhook server** (Terminal 1):
   ```powershell
   python src/webhook_server.py
   ```

2. **Start ngrok** (Terminal 2):
   ```powershell
   C:\ngrok.exe http 5000
   ```

3. **Update settings.yaml** with the ngrok URL

4. **Run the app** - interactive confirmation will work!

