# Fix: Twilio Function Looping Issue

## Problem

After pressing 1 or 2, the call loops back and repeats the message instead of giving the confirmation/cancellation response.

## Root Cause

The Twilio Function isn't properly handling the `Digits` parameter when Twilio POSTs back after the user presses a key. The function needs to check for `event.Digits` **first** before processing the initial message.

## Solution: Update Twilio Function

### Step 1: Go to Twilio Console

1. Log in: https://www.twilio.com/console
2. Go to **Functions** → **Services**
3. Find your function service (appointmentreminder-1291)
4. Click on the function to edit

### Step 2: Replace with Fixed Code

**IMPORTANT**: Replace the entire function code with this fixed version:

```javascript
exports.handler = function(context, event, callback) {
    const twiml = new Twilio.twiml.VoiceResponse();
    
    // Get the message from the call
    const message = event.message || 'This is your appointment reminder. If you need to reschedule, please contact us.';
    
    // Check if user already pressed a digit FIRST
    if (event.Digits) {
        const choice = event.Digits;
        
        if (choice === '1') {
            // User confirmed appointment
            twiml.say({
                voice: 'alice',
                language: 'en-US'
            }, 'Thank you. Your appointment is confirmed. We look forward to seeing you. Goodbye.');
            callback(null, twiml);
            return;  // IMPORTANT: Return immediately
        } else if (choice === '2') {
            // User cancelled appointment
            twiml.say({
                voice: 'alice',
                language: 'en-US'
            }, 'Your appointment has been cancelled. Please contact us to reschedule if needed. Thank you. Goodbye.');
            callback(null, twiml);
            return;  // IMPORTANT: Return immediately
        } else {
            // Invalid input - reprompt
            twiml.say({
                voice: 'alice',
                language: 'en-US'
            }, 'Sorry, I didn\'t understand that choice.');
            
            // Reprompt with Gather
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
            
            // Fallback
            twiml.say({
                voice: 'alice',
                language: 'en-US'
            }, 'We didn\'t receive a response. Please contact us if you need to confirm or reschedule your appointment. Goodbye.');
            
            callback(null, twiml);
            return;
        }
    }
    
    // Initial call - say message and gather input
    twiml.say({
        voice: 'alice',
        language: 'en-US'
    }, message);
    
    // Pause briefly
    twiml.pause({length: 1});
    
    // Gather user input
    const gather = twiml.gather({
        numDigits: 1,
        timeout: 10,
        action: '/path_1',
        method: 'POST'
    });
    
    gather.say({
        voice: 'alice',
        language: 'en-US'
    }, 'Press 1 to confirm your appointment, or press 2 to cancel or reschedule.');
    
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
2. Wait for deployment to complete

### Step 4: Test

Run the app again:
```bash
python src/app.py data/ready_to_test.xlsx
```

When you answer and press 1 or 2, you should now hear:
- ✅ Press 1: "Thank you. Your appointment is confirmed. We look forward to seeing you. Goodbye."
- ✅ Press 2: "Your appointment has been cancelled. Please contact us to reschedule if needed. Thank you. Goodbye."

## Key Fixes

1. **Check `event.Digits` FIRST** - Before processing the message
2. **Return immediately** - After handling the digit, use `return` to prevent further execution
3. **Proper flow control** - Separate handling for initial call vs. digit response

## Alternative: Use Full Code File

I've also created `FIXED_TWILIO_FUNCTION_CODE.js` in your project folder - you can copy the entire contents from that file.

