# Installation Notes

## Windows pip Command Issue

On Windows, if you get `'pip' is not recognized as an internal or external command`, use:

```bash
python -m pip install -r requirements.txt
```

instead of:

```bash
pip install -r requirements.txt
```

## Why This Happens

On some Windows installations, `pip` is not added to the system PATH, but Python is. Using `python -m pip` ensures Python runs pip from the correct installation.

## Quick Reference

**Use this on Windows:**
```bash
python -m pip install -r requirements.txt
```

**All documentation has been updated** to use this command format for Windows compatibility.

## Verify Installation

After installing, verify everything works:

```bash
python -c "from src import config_loader, logger, data_processor, scheduler, caller; print('SUCCESS!')"
```

You should see: `SUCCESS!`

## Alternative: Add pip to PATH

If you prefer using `pip` directly:

1. Find your Python Scripts directory (usually `C:\Users\YourName\AppData\Local\Programs\Python\Python313\Scripts`)
2. Add it to your system PATH
3. Restart terminal
4. Then you can use `pip` directly

However, `python -m pip` works on all systems without any PATH configuration!

