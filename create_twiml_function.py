"""
Create a Twilio Function that can handle appointment reminder messages.
This outputs JavaScript code you can paste into a Twilio Function.
"""

print("=" * 60)
print("TWILIO FUNCTION CODE FOR APPOINTMENT REMINDERS")
print("=" * 60)
print()
print("Instructions:")
print("1. Go to: https://www.twilio.com/console/functions")
print("2. Click 'Create Function'")
print("3. Choose 'Blank'")
print("4. Name it: 'Appointment Reminder'")
print("5. Paste this code:")
print()
print("-" * 60)
print()
print("""exports.handler = function(context, event, callback) {
    const twiml = new Twilio.twiml.VoiceResponse();
    
    // Get the message from query parameter
    const message = event.message || 'This is your appointment reminder.';
    
    // Speak the appointment message
    twiml.say({
        voice: 'alice',
        language: 'en-US'
    }, message);
    
    // Pause briefly
    twiml.pause({length: 2});
    
    // Say goodbye
    twiml.say({
        voice: 'alice',
        language: 'en-US'
    }, 'Thank you for your time. Goodbye.');
    
    // Return TwiML
    callback(null, twiml);
};""")
print()
print("-" * 60)
print()
print("6. Click 'Deploy'")
print("7. Copy the function URL (it will look like: https://xxxx-xxxx.twilio.run)")
print("8. Tell me the URL and I'll update the app to use it!")
print()
print("=" * 60)

