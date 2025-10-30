"""
Quick test to verify status callback configuration.
Shows how to set up and use status callbacks.
"""

from src.caller import Caller
from src.config_loader import ConfigLoader
import os
from dotenv import load_dotenv

load_dotenv()

# Load config
config = ConfigLoader()

# Get credentials
env_config = config.get('env', {})
account_sid = env_config.get('twilio_account_sid')
auth_token = env_config.get('twilio_auth_token')
phone_number = env_config.get('twilio_phone_number')

# Get callback URL from config
status_callback_url = config.get('calling.status_callback_url')

print("=" * 60)
print("STATUS CALLBACK CONFIGURATION TEST")
print("=" * 60)
print()

# Show current configuration
print(f"Account SID: {account_sid[:15]}...")
print(f"Phone Number: {phone_number}")
print(f"Status Callback URL: {status_callback_url or 'None (polling mode)'}")
print()

# Create caller
try:
    caller = Caller(
        account_sid=account_sid,
        auth_token=auth_token,
        from_number=phone_number,
        status_callback_url=status_callback_url
    )
    
    print("[OK] Caller initialized successfully")
    print()
    
    if status_callback_url:
        print("Status callbacks are CONFIGURED:")
        print(f"  URL: {status_callback_url}")
        print("  Events: initiated, ringing, answered, completed")
        print("  Method: POST")
        print()
        print("Next steps:")
        print("  1. Make sure your callback server is running")
        print("  2. Test with: python start_with_callbacks.py data/batch_test.xlsx")
    else:
        print("Status callbacks are NOT configured:")
        print("  Using polling mode (default)")
        print()
        print("To enable callbacks:")
        print("  1. Set up ngrok: ngrok http 8080")
        print("  2. Update config/settings.yaml with ngrok URL")
        print("  3. Run callback server")
        
except Exception as e:
    print(f"[ERROR] Error: {e}")

print()
print("=" * 60)

