# Bot 1 - Quick Start Guide (Claim Pages Version)

## 5-Minute Setup

### What You Get

Recipients receive emails pointing to a **blue landing page** that:
1. Shows your prospect's business name
2. Displays a **portfolio section** with 6 recent projects & reviews
3. Contains an **embedded Maine roofing template demo**
4. Matches professional agency branding

### Email Flow

```
Prospect receives Email 1
    ↓
Clicks "claim page" link
    ↓
Sees portfolio section with 6 projects
    ↓
Clicks through to demo inside landing page
    ↓
Impressed by Maine roofing template design
    ↓
Replies to claim available page or DM
```

## Step-by-Step Setup

### Step 1: Prepare Your Prospect List

Create `prospects.csv` (pipe-delimited):

```
email|business_name|owner_name|website_url|sender_account
roofing.owner@example.com|Dwell Roofing|John Smith|https://dwellroofing.com|Your Name
roofing2@example.com|Monarch Roofing|Jane Doe|https://monarchroofing.com|Your Name
```

**Field Explanations:**
- `email`: Where to send the campaign
- `business_name`: Displayed in claim page (e.g., "Dwell Roofing")
- `owner_name`: Used in email greeting (e.g., "John Smith")
- `website_url`: Their existing website (for scraping data)
- `sender_account`: Name shown in email signature

### Step 2: Run the Pipeline

```bash
cd /Users/adayliakrispli/webreach
python3 BOT1_MASTER_PIPELINE.py prospects.csv
```

### Step 3: Check Results

The system generates:
- `campaign_results_TIMESTAMP.json` with all details

Example output:
```json
{
  "business_name": "Dwell Roofing",
  "claim_url": "https://adayliak1-pixel.github.io/webreach/demo/dwell-roofing/claim.html",
  "demo_url": "https://adayliak1-pixel.github.io/webreach/demo/dwell-roofing/index.html",
  "email_campaign": [
    {
      "order": 1,
      "delay_days": 0,
      "subject": "Dwell Roofing",
      "body": "Hi John Smith,\n\nI've been reviewing Dwell Roofing..."
    },
    ...
  ]
}
```

### Step 4: Send via Instantly.ai (or Manual)

Copy email content from JSON and schedule via your email tool.

**Key URLs to use:**
- **In emails:** `https://...demo.../claim.html` (the blue landing page)
- **Not:** `https://...demo.../index.html` (raw demo)

## File Structure

```
webreach/
├── bot1_claim_generator.py          ← Generates claim pages
├── BOT1_MASTER_PIPELINE.py          ← Main orchestrator
├── bot1_website_scraper.py          ← Scrapes prospect websites
├── bot1_maine_template_injector.py  ← Creates Maine template demos
├── demo/
│   ├── dwell-roofing/
│   │   ├── index.html               ← Maine roofing template
│   │   └── claim.html               ← Blue landing page with portfolio
│   ├── monarch-roofing/
│   │   ├── index.html
│   │   └── claim.html
│   └── [future-prospects]/
└── campaign_results_*.json          ← Generated after each run
```

## What the Claim Page Shows

### Header
- Teal/dark blue theme
- Business name in "reserved for" banner
- "Claim This Site" button

### Intro Section
- Explanation of the preview
- Link to open demo full-screen

### Portfolio Section (NEW!)
- **"Recent Projects & Reviews"**
- 6 project cards:
  - Residential Roofing
  - Commercial Project
  - Roof Repair & Maintenance
  - Storm Damage Restoration
  - Metal Roofing Installation
  - Customer Testimonials
- Hover shows ★★★★★ ratings

### Embedded Demo
- Full Maine roofing template
- Desktop/mobile toggle
- Browser chrome frame

### CTA Section
- Pricing ($800 + $249/mo)
- Trust badges
- Setup timeline

## Email Templates (Automatically Generated)

### Email 1 (Day 0)
```
Subject: Dwell Roofing

Hi John Smith,

I've been reviewing Dwell Roofing and noticed something — most roofing
websites are pretty dated. They don't really sell well.

I actually rebuilt a cleaner version of Dwell Roofing's website quickly
to see how it could look with a simpler layout and a clearer contact
section to generate more leads.

[CLAIM PAGE LINK HERE]

I'm not selling anything — this is just a concept to see if a fresh
design could help you get more calls.

Let me know if you'd like me to send over some other ideas.
```

### Email 2 (Day 2)
```
Subject: re: Dwell Roofing

Hi John Smith,

Did you get a chance to check out the preview I sent?

A lot of roofing companies are starting to realize that their websites
aren't doing the heavy lifting they should be...

[CLAIM PAGE LINK HERE]
```

### Email 3 (Day 7)
```
Subject: re: Dwell Roofing

Hi John Smith,

Final thought — I think Dwell Roofing could really benefit from a
design update...

[CLAIM PAGE LINK HERE]
```

## Customizations Per Prospect

Each prospect gets:
1. **Custom business name** in claim page (5 places)
2. **Custom demo** with their website data scraped
3. **Custom claim page** wrapping their demo
4. **Custom emails** with personalized greeting
5. **Unique URL** for tracking

## Email Features

✓ No hyphens or dashes
✓ Simple subject lines
✓ "to generate more leads" phrase in Email 1
✓ Professional, conversational tone
✓ Clear, single CTA (the claim page link)
✓ Randomized send times (8 AM - 4 PM)

## Deployment Locations

### Demo Files
- Deployed to: `https://adayliak1-pixel.github.io/webreach/demo/[slug]/`
- Example: `https://adayliak1-pixel.github.io/webreach/demo/dwell-roofing/`

### What Gets Deployed
- `index.html` - Maine roofing template demo (56KB)
- `claim.html` - Blue landing page with portfolio (25KB)

### GitHub Pages Settings
- Repo: adayliak1-pixel/webreach
- Branch: main
- Public URL: https://adayliak1-pixel.github.io/webreach/

## Testing Before Campaign

### Test 1: Verify Claim Page Loads
```bash
# Should show portfolio + embedded demo
https://adayliak1-pixel.github.io/webreach/demo/dwell-roofing/claim.html
```

### Test 2: Check Demo Loads in iframe
- The claim page should show Maine template inside

### Test 3: Verify Business Name
- Should see "Dwell Roofing" in:
  - 48hr banner
  - Header label
  - Intro headline
  - Trust strip

### Test 4: Portfolio Section
- Should show 6 project cards
- Hover should show ratings

## Advanced Usage

### Batch Processing
Multiple prospects at once:

```python
pipeline = BotMasterPipeline()
results = pipeline.run("prospects.csv")

for result in results:
    print(f"{result['business_name']}: {result['claim_url']}")
```

### Custom Email Templates
Edit `EMAIL_BODIES` in `BOT1_MASTER_PIPELINE.py` before running.

### Custom Claim Pages
Use `bot1_claim_generator.py` directly:

```python
generator = ClaimPageGenerator()
generator.generate(
    business_name="Custom Business",
    demo_url="https://your-demo-url/",
    output_path="/path/to/claim.html"
)
```

## Troubleshooting

**Q: Claim page loads but demo iframe is blank**
- Check that `index.html` is deployed to GitHub
- Verify iframe src URL is correct
- Give GitHub 2-3 minutes for deployment

**Q: Business name not showing in claim page**
- Re-run `bot1_claim_generator.py`
- Ensure business name matches exactly

**Q: Portfolio images not showing**
- They're using gradient backgrounds (not images)
- No image files needed for portfolio section
- Hover to see stars appear

## Next Steps

1. ✓ Create `prospects.csv`
2. ✓ Run `BOT1_MASTER_PIPELINE.py`
3. ✓ Test claim page URLs
4. ✓ Copy emails from JSON to Instantly.ai
5. ✓ Set schedule (Day 0, Day 2, Day 7)
6. ✓ Launch campaign!

---

**Current Demo Examples:**
- Dwell Roofing: https://adayliak1-pixel.github.io/webreach/demo/dwell-roofing/claim.html
- Monarch Roofing: https://adayliak1-pixel.github.io/webreach/demo/monarch-roofing/claim.html

**System Version:** Bot 1 - Claim Pages Edition v2.0
