# Quick TwiML Setup - Appointment Message

Your calls are working but using a generic message. Here's the **easiest** way to fix it:

## Option 1: Twilio Functions (Recommended - 2 minutes)

1. Log into Twilio Console: https://www.twilio.com/console
2. Go to **Functions → Create Function**
3. Choose **Blank** template
4. Name it: "Appointment Reminder"
5. Copy/paste this code:

```javascript
exports.handler = function(context, event, callback) {
    const twiml = new Twilio.twiml.VoiceResponse();
    
    // Get the message from the call
    const message = event.message || 'This is your appointment reminder. If you need to reschedule, please contact us.';
    
    twiml.say({voice: 'alice', language: 'en-US'}, message);
    twiml.pause({length: 2});
    twiml.say({voice: 'alice', language: 'en-US'}, 'Thank you, goodbye.');
    
    callback(null, twiml);
};
```

6. Click **Deploy**
7. Copy the function URL (looks like: `https://xxx-xxxx.twilio.run/app`)
8. Send that URL to me and I'll update the app

## Option 2: Ngrok (For local testing)

If you want to test locally:

1. Download ngrok: https://ngrok.com/download
2. In Terminal 1, run: `python src/twiml_server.py`
3. In Terminal 2, run: `ngrok http 8000`
4. Copy the ngrok URL (like: `https://abc123.ngrok.io`)
5. Send that URL to me

## Current Status

✅ Calls are being placed to your number  
⚠️ Using generic demo message  
✅ Ready to add custom message  

**Next:** Send me your Twilio Function URL or ngrok URL and I'll update the app!

