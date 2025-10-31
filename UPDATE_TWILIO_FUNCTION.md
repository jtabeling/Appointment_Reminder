# Update Twilio Function for Interactive Confirmation

## Current Issue

Your Twilio Function at `https://appointmentreminder-1291.twil.io/path_1` doesn't include the interactive Gather prompt. 

## Solution: Update Twilio Function Code

### Step 1: Go to Twilio Console

1. Log in: https://www.twilio.com/console
2. Go to **Functions** → **Services**
3. Find your function service (should be related to "appointmentreminder-1291")
4. Click on it to edit

### Step 2: Update the Function Code

Replace the existing code with this:

```javascript
exports.handler = function(context, event, callback) {
    const twiml = new Twilio.twiml.VoiceResponse();
    
    // Get the message from the call
    const message = event.message || 'This is your appointment reminder. If you need to reschedule, please contact us.';
    
    // Say the appointment reminder message
    twiml.say({
        voice: 'alice',
        language: 'en-US'
    }, message);
    
    // Pause briefly
    twiml.pause({length: 1});
    
    // Gather user input (Press 1 to confirm, 2 to cancel)
    const gather = twiml.gather({
        numDigits: 1,
        timeout: 10,
        action: '/path_1',  // Post back to same endpoint
        method: 'POST'
    });
    
    gather.say({
        voice: 'alice',
        language: 'en-US'
    }, 'Press 1 to confirm your appointment, or press 2 to cancel or reschedule.');
    
    // Handle user input (when they press a key)
    if (event.Digits) {
        const choice = event.Digits;
        
        if (choice === '1') {
            // User confirmed
            twiml.say({
                voice: 'alice',
                language: 'en-US'
            }, 'Thank you. Your appointment is confirmed. We look forward to seeing you. Goodbye.');
        } else if (choice === '2') {
            // User cancelled
            twiml.say({
                voice: 'alice',
                language: 'en-US'
            }, 'Your appointment has been cancelled. Please contact us to reschedule if needed. Thank you. Goodbye.');
        } else {
            // Invalid input - reprompt
            twiml.say({
                voice: 'alice',
                language: 'en-US'
            }, 'Sorry, I didn\'t understand that choice.');
            
            const gatherRetry = twiml.gather({
                numDigits: 1,
                timeout: 10,
                action: '/path_1',
                method: 'POST'
            });
            
            gatherRetry.say({
                voice: 'alice',
                language: 'en-US'
            }, 'Press 1 to confirm your appointment, or press 2 to cancel or reschedule.');
        }
    }
    
    // Fallback if no input received
    twiml.say({
        voice: 'alice',
        language: 'en-US'
    }, 'We didn\'t receive a response. Please contact us if you need to confirm or reschedule your appointment. Goodbye.');
    
    callback(null, twiml);
};
```

### Step 3: Deploy

1. Click **Deploy**
2. The function URL stays the same: `https://appointmentreminder-1291.twil.io/path_1`
3. No need to update `config/settings.yaml` - it will automatically use the updated function

### Step 4: Test

Run the app:
```bash
python src/app.py data/ready_to_test.xlsx
```

Now when you answer the call, you should hear:
1. ✅ Appointment reminder message
2. ✅ "Press 1 to confirm your appointment, or press 2 to cancel or reschedule"
3. ✅ Press 1 or 2
4. ✅ Confirmation or cancellation message

## Note on Response Tracking

⚠️ **Important**: The Twilio Function approach will enable the interactive prompts, but the `user_response` column in CSV won't be populated because we can't easily track responses from Twilio Functions.

For full response tracking in CSV, use the Flask webhook server approach (requires ngrok).

