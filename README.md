# Discord Server/Group Leaver 

A Python script that helps you quickly leave multiple Discord servers and group DMs at once, with the option to keep specific ones.

## Features 

- **Bulk Leave Servers** - Leave all Discord servers you're in with one command
- **Bulk Leave Groups** - Exit all group DMs automatically
- **Selective Keeping** - Specify server/group IDs you want to keep
- **Smart Rate Limiting** - Built-in delays and rate limit handling to avoid Discord API restrictions
- **Owner Protection** - Automatically skips servers you own (can't leave those!)
- **Progress Tracking** - Visual progress bar and detailed status updates
- **Error Handling** - Comprehensive error messages and retry logic

## Prerequisites 📋

- Python 3.6 or higher
- `colorama` library
- `requests` library

## Installation 

1. Clone this repository:
```bash
git clone https://github.com/fastmodue/group-server-leaver.git
cd group-server-leaver
```

2. Install required dependencies:
```bash
pip install colorama
pip install requests
```

## Usage 💻

1. Run the script:
```bash
python main.py
```

2. Choose what you want to leave:
   - `1` - Discord Groups (DMs)
   - `2` - Discord Servers
   - `3` - Both

3. Enter your Discord token when prompted

4. (Optional) Enter server/group IDs to keep, separated by commas
   - Example: `123456789,987654321`
   - Press Enter to leave ALL

5. Confirm and let the script do its work!

## Getting Your Discord Token 

> ⚠️ **Warning**: Never share your Discord token with anyone! It gives full access to your account.

### Method 1: Browser Console (Recommended)
1. Open Discord in your web browser
2. Press `Ctrl + Shift + I` (or `Cmd + Option + I` on Mac)
3. Go to the "Console" tab
4. Paste this code and press Enter:
```javascript
let token;
window.webpackChunkdiscord_app.push([[Symbol()], {}, o => {
  for (let e of Object.values(o.c)) {
    try {
      if (!e.exports || e.exports === window) continue;
      if (e.exports?.getToken) {
        token = e.exports.getToken();
        console.log("Token:", token);
      }
      for (let o in e.exports) {
        if (e.exports?.[o]?.getToken && "IntlMessagesProxy" !== e.exports[o][Symbol.toStringTag]) {
          token = e.exports[o].getToken();
          console.log("Token:", token);
        }
      }
    } catch {}
  }
}]);
window.webpackChunkdiscord_app.pop();
```
5. Copy the token that appears (without quotes)

### Method 2: Network Tab
1. Open Discord in your web browser
2. Press `Ctrl + Shift + I` (or `Cmd + Option + I` on Mac)
3. Go to the "Network" tab
4. Press `Ctrl + R` to reload
5. Type "api" in the filter box
6. Click on any request and look for "Authorization" in the headers

## Example Output 📊

```
╔═══════════════════════════════════════════════════════╗
║            DISCORD SERVER/GROUP LEAVER                ║
║                  AGENT SOLUTION                       ║
╚═══════════════════════════════════════════════════════╝

[Found 15 servers]
[Leaving servers...]

[LEFT] Random Server 1
[LEFT] Gaming Community
[KEPT] My Favorite Server (ID: 123456789)
[SKIPPED] Can't leave owned server: My Own Server
[Progress] ████████████████████████████████████████ 15/15

╔═══════════════════════════════════════╗
║          OPERATION COMPLETE!          ║
╠═══════════════════════════════════════╣
║  Left:   12                           ║
║  Kept:   1                            ║
║  Owned:  1  (skipped)                 ║
║  Failed: 1                            ║
╚═══════════════════════════════════════╝
```

## Safety Features 🛡️

- **Rate Limit Handling**: Automatically waits when rate limited
- **Smart Delays**: Random delays between requests (0.5-0.8s for servers, 0.3-0.5s for groups)
- **Retry Logic**: Attempts failed requests up to 3 times
- **Owner Protection**: Cannot leave servers you own
- **Confirmation Prompts**: Asks for confirmation before proceeding
- **Keep List Preview**: Shows what will be kept before starting

## Disclaimer ⚠️

This script is for educational purposes only. Use at your own risk. I am not responsible for any Discord account restrictions or bans that may result from using this tool. Using automation tools may violate Discord's Terms of Service.

**Important Notes:**
- This uses your personal Discord token - keep it private!
- Excessive API usage may result in rate limiting or temporary restrictions
- Always keep backups of important server invite links before leaving

## Troubleshooting 💢

**"Invalid token" error:**
- Make sure you copied the entire token correctly
- Try getting a fresh token
- Ensure you're logged into Discord

**Rate limiting issues:**
- The script automatically handles this with delays
- If it persists, wait a few minutes and try again

**"Can't leave owned server":**
- You cannot leave servers you own
- Transfer ownership or delete the server instead

## License 📄

This project is open source and available under the [GNU GPL v3.0](LICENSE) License.

## Contact me 💌
- Add my discord: fastmodue 
- Or join my server: https://discord.gg/Ju4xe6gYJ4

## Author 

Made by fastmodue

---

**⭐ If you found this helpful, consider giving it a star!**
