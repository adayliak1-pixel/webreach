# Bot 1 - Claim Pages Deployment Update

## What Changed

The system has been updated to use **blue landing pages (claim pages)** as the primary email link, instead of pointing directly to the raw demos.

### New Architecture

```
Email Recipient
    ↓
Clicks claim URL (CLAIM.HTML - blue landing page)
    ↓
Shows portfolio with 6 pictures under "Recent Projects & Reviews"
    ↓
Embedded demo (index.html) inside an iframe
    ↓
Professional teal/dark blue theme with glassmorphism
```

## Files Updated/Created

### 1. **bot1_claim_generator.py** (NEW)
Generates customized claim pages for each prospect.

```python
generator = ClaimPageGenerator()
claim_path = generator.generate(
    business_name="Dwell Roofing",
    demo_url="https://...demo.../index.html",
    output_path="/path/to/claim.html"
)
```

**What it customizes:**
- 48hr banner business name
- Header label business name
- Intro headline business name
- iframe src (points to the demo)
- Business name in trust strip copy

### 2. **BOT1_MASTER_PIPELINE.py** (UPDATED)
Complete orchestration system with claim page workflow.

**Key change:** Email URLs now point to `claim.html` instead of `index.html`

```python
pipeline = BotMasterPipeline()
results = pipeline.run("prospects.csv")
```

**Workflow:**
1. Scrape prospect website
2. Generate Maine roofing template demo (index.html)
3. Generate claim page landing page (claim.html) - wraps the demo
4. Deploy both to GitHub Pages
5. Create 3-email campaign pointing to claim.html

## Email Campaign Flow

### Email 1 (Day 0)
```
Subject: {{BUSINESS_NAME}}

Points to: https://...demo.../claim.html  ← Blue landing page
Inside: Maine roofing template demo in iframe
Shows: Portfolio section with 6 pictures
```

### Email 2 (Day 2)
```
Subject: re: {{BUSINESS_NAME}}

Same claim URL with portfolio and embedded demo
```

### Email 3 (Day 7)
```
Subject: re: {{BUSINESS_NAME}}

Same claim URL with portfolio and embedded demo
```

## Deployed Examples

### Dwell Roofing (Dallas, TX)
- **Claim Page:** https://adayliak1-pixel.github.io/webreach/demo/dwell-roofing/claim.html
- **Demo (in iframe):** https://adayliak1-pixel.github.io/webreach/demo/dwell-roofing/index.html

### Monarch Roofing (Houston, TX)
- **Claim Page:** https://adayliak1-pixel.github.io/webreach/demo/monarch-roofing/claim.html
- **Demo (in iframe):** https://adayliak1-pixel.github.io/webreach/demo/monarch-roofing/index.html

## Claim Page Features

The blue landing page (claim.html) includes:

### Header Section
- Teal/dark blue theme with glassmorphism effects
- Business name in 48hr reservation banner
- "Claim This Site" CTA button
- Intro section explaining the preview

### Device Toggle
- Desktop/Mobile view toggle
- Browser chrome frame showing the demo

### Portfolio Section (NEW)
- **"Recent Projects & Reviews"** heading
- 6 project cards in a responsive grid
- Teal color scheme with hover effects
- Star ratings (★★★★★ 5.0) on hover
- Project types:
  1. Residential Roofing
  2. Commercial Project
  3. Roof Repair & Maintenance
  4. Storm Damage Restoration
  5. Metal Roofing Installation
  6. Customer Testimonials

### Demo Iframe
- Full Maine roofing template demo
- Fully responsive
- Mobile/desktop switching

### Improvements Section
- 4 benefit cards
- Trust metrics
- Professional messaging

### CTA Section
- Pricing block ($800 setup + $249/mo)
- "Transfer to Domain" button
- Trust badges

## How to Use

### For a Single Prospect

```bash
python3 bot1_claim_generator.py
```

### For Multiple Prospects

Create `prospects.csv`:
```
email|business_name|owner_name|website_url|sender_account
john@example.com|Dwell Roofing|John Smith|https://dwellroofing.com|John Smith
jane@example.com|Monarch Roofing|Jane Doe|https://monarchroofing.com|Jane Doe
```

Then run:
```bash
python3 BOT1_MASTER_PIPELINE.py prospects.csv
```

This will:
1. ✓ Scrape both websites
2. ✓ Generate 2 Maine template demos
3. ✓ Generate 2 claim pages
4. ✓ Deploy both to GitHub Pages
5. ✓ Create 6 personalized emails (3 per prospect)
6. ✓ Save results to `campaign_results_TIMESTAMP.json`

## Email Content (No Hyphens)

All emails are formatted without hyphens, with simple subject lines and direct claim page URLs:

```
Subject: Dwell Roofing
(or re: Dwell Roofing for follow-ups)

Email includes:
- No hyphens or dashes
- Direct call to action
- "to generate more leads" phrase in first email
- Link to claim page (with portfolio + embedded demo)
- Clean, professional formatting
```

## Customization Points

Each claim page is customized with:
- Business name (in 3 places)
- Demo iframe source URL
- Trust strip copy mentioning business name

All other content (portfolio, pricing, CTA, etc.) remains consistent for rapid deployment.

## Key Advantages

1. **Better UX:** Recipients see portfolio BEFORE deciding to view demo
2. **Lower Bounce Rate:** Landing page context + preview of what's inside
3. **Trust Building:** Portfolio section shows work quality
4. **Branding:** Each prospect sees their name throughout
5. **Professionalism:** Blue landing page looks like official agency preview
6. **Trackability:** Can track claim page clicks separately from demo engagement

## Next Steps

1. Create prospects.csv with your list
2. Run BOT1_MASTER_PIPELINE.py
3. Review generated campaign in results JSON
4. Configure Instantly.ai API credentials
5. Schedule emails through Instantly.ai or manual send

---

**Generated:** March 12, 2026
**System Version:** Bot 1 - Claim Pages Edition
