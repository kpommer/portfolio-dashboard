# HOW TO UPDATE YOUR DASHBOARD DAILY

## Automatic Update Script

I've created a script that will:
1. Fetch latest portfolio prices
2. Generate updated dashboard
3. You just need to upload the new files

## Quick Update Steps:

### Step 1: Run Update Script (Daily at 3:05 PM CDT)
```
cd C:\Users\kevin\.openclaw\workspace\scripts
python automated_portfolio_tracker.py
```

### Step 2: New Files Generated
The script creates:
- Updated `portfolio_data/portfolio_YYYY-MM-DD.json`
- Updated `portfolio_website/index.html`
- Updated `portfolio_website/data.json`

### Step 3: Upload to GitHub
1. Go to: https://github.com/kpommer/portfolio-dashboard
2. Click "Add file" → "Upload files"
3. Upload the NEW `index.html` and `data.json`
4. Click "Commit changes"

## Scheduled Task (Already Set Up):

A Windows Task Scheduler job runs daily at 3:05 PM CDT:
- Task Name: `PanPortfolioTracker`
- Runs: `C:\Users\kevin\.openclaw\workspace\scripts\run_daily.bat`

## Manual Update Process:

If you want to update manually:
1. Open Command Prompt as Administrator
2. Run: `python C:\Users\kevin\.openclaw\workspace\scripts\automated_portfolio_tracker.py`
3. Upload the new files to GitHub

## GitHub Pages Note:

GitHub Pages automatically deploys when you push new files. No need to re-enable pages.

## View Your Dashboard:

Always available at: **https://kpommer.github.io/portfolio-dashboard/**

## Need Help?

The AI companion "Pan" can help with:
- Setting up complete automation
- Troubleshooting updates
- Adding new features
- Customizing the dashboard