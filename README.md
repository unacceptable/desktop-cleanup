# Desktop Cleanup Script

A Python daemon that automatically moves screenshot files from your Desktop to a temporary folder and archives old screenshots to keep your desktop organized.

## What it does

This script monitors your Desktop for screenshot files (files matching the pattern `Screen*.png`) and automatically:
1. Moves screenshot files from Desktop to `~/Pictures/Temp/`
2. Keeps only the 5 most recent screenshots in the temp folder
3. Archives older screenshots to `~/Pictures/` organized by date
4. Runs continuously as a background daemon

## Setup Instructions

### 1. Create the LaunchAgent

First, create a launchd configuration file to run the script automatically:

```bash
cat > ~/Library/LaunchAgents/com.scriptmyjob.desktop_cleanup.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">

<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.scriptmyjob.desktop_cleanup</string>
        <key>Program</key>
        <string>$HOME/Scripts/.bin/desktop_cleanup.py</string>
        <key>RunAtLoad</key>
        <true/>
    </dict>
</plist>
EOF
```

### 2. Set Execute Permissions

Make the script executable (after saving it to the location specified in the plist file):

```bash
chmod u+x ~/Scripts/.bin/desktop_cleanup.py
```

### 3. Start the Daemon

Start the LaunchAgent:

```bash
launchctl start com.scriptmyjob.desktop_cleanup
```

## Requirements

- Python 3.x
- macOS (uses LaunchAgent for daemon functionality)
- Write permissions to `~/Pictures/` directory

## How it works

1. **Monitoring**: The script continuously monitors your Desktop folder every second
2. **Detection**: Looks for files matching the pattern `Screen*.png` (typical macOS screenshot naming)
3. **Moving**: Moves found screenshots to `~/Pictures/Temp/`
4. **Archiving**: Keeps only the 5 most recent screenshots in the temp folder
5. **Organization**: Archives older screenshots to `~/Pictures/` with date-based organization

## Directory Structure

```
~/Desktop/              # Monitored for screenshots
~/Pictures/Temp/        # Temporary storage for recent screenshots (max 5)
~/Pictures/             # Archive location for older screenshots
```

## Running Manually

You can also run the script manually for testing:

```bash
python3 desktop_cleanup.py
```

Press `Ctrl+C` to stop the script when running manually.

## Logging

The script logs all operations to stdout, including:
- Files found and moved
- Directory creation
- Archive operations
- Start/stop messages

## Notes

- The script is designed specifically for macOS screenshot files
- It preserves the 5 most recent screenshots for quick access
- Older screenshots are organized by date for long-term storage
- The daemon runs continuously in the background once started
