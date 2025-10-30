"""
Set up a TwiML Bin for appointment reminders.
This creates a public URL that Twilio can call.
"""

from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

# TwiML for appointment reminder
twiml_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-US">Hello, this is an automated appointment reminder.</Say>
    <Pause length="1"/>
    <Say voice="alice" language="en-US">Thank you for your time.</Say>
</Response>'''

def main():
    print("=" * 60)
    print("Setting up TwiML Bin for Appointment Reminders")
    print("=" * 60)
    print()
    
    # Get credentials
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    
    if not account_sid or not auth_token:
        print("Error: Missing Twilio credentials in .env file")
        return
    
    try:
        client = Client(account_sid, auth_token)
        
        print("Creating TwiML Bin...")
        twiml_bin = client.messaging.v1.twi_m_l.create(
            message_service_sid=None,  # Not needed for voice
            friendly_name="Appointment Reminder",
            twiml=twiml_xml
        )
        
        print(f"TwiML Bin created!")
        print(f"Bin SID: {twiml_bin.sid}")
        print()
        
        # Now create the URL
        twiml_url = f"https://handler.twilio.com/twiml/{twiml_bin.sid}"
        
        print("Your TwiML URL:")
        print(twiml_url)
        print()
        
        # Update caller.py
        print("Updating src/caller.py...")
        with open('src/caller.py', 'r') as f:
            content = f.read()
        
        old_return = 'return "http://demo.twilio.com/docs/voice.xml"'
        new_return = f'return "{twiml_url}"'
        
        if old_return in content:
            content = content.replace(old_return, new_return)
            with open('src/caller.py', 'w') as f:
                f.write(content)
            print("✅ Updated src/caller.py")
        else:
            print("Could not find line to replace. Please manually update line 222.")
            print(f"Replace with: return \"{twiml_url}\"")
        
        print()
        print("Success! Now your calls will use the TwiML Bin.")
        print("Note: To change the message, edit this script and run it again.")
        
    except Exception as e:
        print(f"Error: {e}")
        print()
        print("If you got an error about twi_m_l not existing, your Twilio")
        print("version may not support TwiML Bins. Try using Twilio Functions instead.")

if __name__ == '__main__':
    main()

