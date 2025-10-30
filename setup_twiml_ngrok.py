"""
Quick setup script to help configure TwiML endpoint with ngrok.
Run this after you've started ngrok.
"""

import re
import sys

def main():
    print("=" * 60)
    print("Twilio TwiML Endpoint Setup Helper")
    print("=" * 60)
    print()
    
    print("STEP 1: Start ngrok")
    print("Download from: https://ngrok.com/download")
    print("Then run: ngrok http 8000")
    print()
    
    print("STEP 2: Start the TwiML server")
    print("In another terminal, run: python src/twiml_server.py")
    print()
    
    print("STEP 3: Enter your ngrok URL")
    print("Example: https://abc123def456.ngrok.io")
    print()
    
    ngrok_url = input("Enter your ngrok URL: ").strip()
    
    if not ngrok_url:
        print("Error: No URL provided")
        sys.exit(1)
    
    # Clean up URL
    ngrok_url = ngrok_url.replace('https://', '').replace('http://', '')
    twiml_url = f"http://{ngrok_url}/twiml"
    
    print()
    print("Your TwiML URL will be:", twiml_url)
    print()
    
    # Update the caller.py file
    try:
        with open('src/caller.py', 'r') as f:
            content = f.read()
        
        # Replace the TwiML URL
        old_url = 'return "http://demo.twilio.com/docs/voice.xml"'
        new_url = f'return "{twiml_url}"'
        
        if old_url in content:
            content = content.replace(old_url, new_url)
            
            with open('src/caller.py', 'w') as f:
                f.write(content)
            
            print("✅ Successfully updated src/caller.py")
            print()
            print("Next steps:")
            print("1. Make sure both terminals are running (ngrok and twiml_server)")
            print("2. Test the application:")
            print("   python src/app.py data/sample_appointments.xlsx")
        else:
            print("Could not find placeholder URL in src/caller.py")
            print("Please manually update line 222 with:", twiml_url)
    
    except Exception as e:
        print(f"Error updating file: {e}")
        print()
        print("Please manually update src/caller.py line 222 with:")
        print(f'return "{twiml_url}"')

if __name__ == '__main__':
    main()

