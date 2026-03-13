#!/usr/bin/env python3
"""
Bot 1 Master Pipeline - Complete Campaign Automation
Orchestrates the entire workflow from prospect list to deployed demos and email campaigns.

Workflow:
1. Read prospect CSV (email, business_name, owner_name, website_url, sender_account)
2. For each prospect:
   - Scrape their website for data
   - Generate customized Maine Roofing demo
   - Generate claim page landing page that wraps the demo
   - Deploy both to GitHub Pages
   - Create personalized 3-email sequence
3. Schedule emails via Instantly.ai API

Email points to CLAIM.HTML (the blue landing page with portfolio), not directly to demo.
"""

import csv
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os
import random
import re

# Add current directory to path for imports
sys.path.insert(0, '/Users/adayliakrispli/webreach')

from bot1_website_scraper import WebsiteScraper
from bot1_maine_template_injector import MaineTemplateInjector
from bot1_claim_generator import ClaimPageGenerator

class BotMasterPipeline:
    def __init__(self, github_repo_url="https://github.com/adayliak1-pixel/webreach.git"):
        self.scraper = WebsiteScraper()
        self.injector = MaineTemplateInjector()
        self.claim_generator = ClaimPageGenerator()
        self.github_repo_url = github_repo_url
        self.base_url = "https://adayliak1-pixel.github.io/webreach/demo"
        self.webreach_path = "/Users/adayliakrispli/webreach"

        # Email templates - Updated to point to CLAIM PAGES, not raw demos
        self.EMAIL_BODIES = {
            'email1': """Hi {{OWNER_NAME}},

I've been reviewing {{BUSINESS_NAME}} and noticed something — most roofing websites are pretty dated. They don't really sell well.

I actually rebuilt a cleaner version of {{BUSINESS_NAME}}'s website quickly to see how it could look with a simpler layout and a clearer contact section to generate more leads.

I put it together in about an hour using information I found publicly about your business. Here's the preview:

{{DEMO_URL}}

I'm not selling anything — this is just a concept to see if a fresh design could help you get more calls.

Let me know if you'd like me to send over some other ideas.

{{SENDER_NAME}}""",

            'email2': """Hi {{OWNER_NAME}},

Did you get a chance to check out the preview I sent?

A lot of roofing companies are starting to realize that their websites aren't doing the heavy lifting they should be. The ones that are getting more calls usually have better site design and a clearer path for customers to actually contact them.

Here's the preview link again if you want to take another look:

{{DEMO_URL}}

Just want to get your thoughts on it.

{{SENDER_NAME}}""",

            'email3': """Hi {{OWNER_NAME}},

Final thought — I think {{BUSINESS_NAME}} could really benefit from a design update. The preview shows what's possible without spending a lot.

Most of your competitors still have outdated sites, so refreshing yours could give you an edge.

Here's the link one more time:

{{DEMO_URL}}

If you want to talk through options, I'm here.

{{SENDER_NAME}}"""
        }

    def slugify(self, text):
        """Convert text to URL-safe slug."""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.rstrip('-')

    def process_prospect(self, prospect_data):
        """
        Process a single prospect through the entire pipeline.

        Args:
            prospect_data: Dict with keys: email, business_name, owner_name, website_url, sender_account

        Returns:
            Dict with results including demo_url, claim_url, and email_campaign
        """
        print(f"\n{'='*60}")
        print(f"Processing: {prospect_data['business_name']}")
        print(f"{'='*60}")

        # 1. SCRAPE WEBSITE
        print(f"[1/5] Scraping {prospect_data['website_url']}...")
        scraped_data = self.scraper.scrape(prospect_data['website_url'])

        if scraped_data['completion_score'] < 45:
            print(f"⚠️  Low data completion ({scraped_data['completion_score']}%). Using fallback data.")

        # Merge scraped data with prospect data
        business_data = {
            **scraped_data,
            'business_name': prospect_data['business_name'],
            'owner_name': prospect_data['owner_name'],
        }

        # 2. GENERATE DEMO
        print(f"[2/5] Generating Maine template demo...")
        demo_slug = self.slugify(prospect_data['business_name'])
        demo_dir = f"{self.webreach_path}/demo/{demo_slug}"
        os.makedirs(demo_dir, exist_ok=True)

        demo_file = self.injector.generate(
            business_data=business_data,
            output_path=f"{demo_dir}/index.html"
        )
        print(f"✓ Demo generated: {demo_file}")

        # 3. GENERATE CLAIM PAGE
        print(f"[3/5] Generating claim landing page...")
        demo_url = f"{self.base_url}/{demo_slug}/index.html"
        claim_file = self.claim_generator.generate(
            business_name=prospect_data['business_name'],
            demo_url=demo_url,
            output_path=f"{demo_dir}/claim.html"
        )
        print(f"✓ Claim page generated: {claim_file}")
        claim_url = f"{self.base_url}/{demo_slug}/claim.html"

        # 4. DEPLOY TO GITHUB
        print(f"[4/5] Deploying to GitHub Pages...")
        self._deploy_to_github(demo_slug)
        print(f"✓ Deployed to: {claim_url}")

        # 5. GENERATE EMAIL CAMPAIGN
        print(f"[5/5] Preparing email campaign...")
        email_campaign = self._generate_email_campaign(
            prospect_data=prospect_data,
            claim_url=claim_url  # Point to claim page, NOT raw demo!
        )
        print(f"✓ Email campaign prepared (3 emails)")

        return {
            'business_name': prospect_data['business_name'],
            'owner_name': prospect_data['owner_name'],
            'email': prospect_data['email'],
            'sender_account': prospect_data['sender_account'],
            'demo_url': demo_url,
            'claim_url': claim_url,  # THE MAIN URL - for emails!
            'email_campaign': email_campaign,
        }

    def _deploy_to_github(self, demo_slug):
        """Deploy the demo to GitHub Pages."""
        try:
            os.chdir(self.webreach_path)
            subprocess.run(['git', 'add', f'demo/{demo_slug}/'], check=True, capture_output=True)
            subprocess.run([
                'git', 'commit', '-m',
                f'Add {demo_slug} demo and claim page'
            ], check=True, capture_output=True)
            subprocess.run(['git', 'push', 'origin', 'main'], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git deployment had issues: {e}")

    def _generate_email_campaign(self, prospect_data, claim_url):
        """Generate personalized email campaign."""
        campaign = []

        # Email 1 - Day 0
        email1_body = self.EMAIL_BODIES['email1']
        email1_body = email1_body.replace('{{OWNER_NAME}}', prospect_data['owner_name'])
        email1_body = email1_body.replace('{{BUSINESS_NAME}}', prospect_data['business_name'])
        email1_body = email1_body.replace('{{DEMO_URL}}', claim_url)  # CLAIM URL!
        email1_body = email1_body.replace('{{SENDER_NAME}}', prospect_data['sender_account'])

        campaign.append({
            'order': 1,
            'delay_days': 0,
            'send_time': self._random_time(8, 16),
            'subject': prospect_data['business_name'],
            'body': email1_body
        })

        # Email 2 - Day 2
        email2_body = self.EMAIL_BODIES['email2']
        email2_body = email2_body.replace('{{OWNER_NAME}}', prospect_data['owner_name'])
        email2_body = email2_body.replace('{{BUSINESS_NAME}}', prospect_data['business_name'])
        email2_body = email2_body.replace('{{DEMO_URL}}', claim_url)  # CLAIM URL!
        email2_body = email2_body.replace('{{SENDER_NAME}}', prospect_data['sender_account'])

        campaign.append({
            'order': 2,
            'delay_days': 2,
            'send_time': self._random_time(8, 16),
            'subject': f're: {prospect_data["business_name"]}',
            'body': email2_body
        })

        # Email 3 - Day 7
        email3_body = self.EMAIL_BODIES['email3']
        email3_body = email3_body.replace('{{OWNER_NAME}}', prospect_data['owner_name'])
        email3_body = email3_body.replace('{{BUSINESS_NAME}}', prospect_data['business_name'])
        email3_body = email3_body.replace('{{DEMO_URL}}', claim_url)  # CLAIM URL!
        email3_body = email3_body.replace('{{SENDER_NAME}}', prospect_data['sender_account'])

        campaign.append({
            'order': 3,
            'delay_days': 7,
            'send_time': self._random_time(8, 16),
            'subject': f're: {prospect_data["business_name"]}',
            'body': email3_body
        })

        return campaign

    def _random_time(self, start_hour, end_hour):
        """Generate random time between hours for natural sending pattern."""
        hour = random.randint(start_hour, end_hour - 1)
        minute = random.randint(0, 59)
        return f"{hour:02d}:{minute:02d}"

    def run(self, csv_path):
        """
        Run the entire pipeline for all prospects in CSV.

        CSV format:
        email|business_name|owner_name|website_url|sender_account
        """
        results = []

        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f, delimiter='|')
            for row in reader:
                try:
                    result = self.process_prospect(row)
                    results.append(result)
                except Exception as e:
                    print(f"❌ Error processing {row['business_name']}: {e}")
                    import traceback
                    traceback.print_exc()

        print(f"\n{'='*60}")
        print(f"PIPELINE COMPLETE")
        print(f"{'='*60}")
        print(f"Processed: {len(results)} prospects")

        # Save results
        results_file = f"{self.webreach_path}/campaign_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {results_file}")

        # Print summary
        print(f"\n{'='*60}")
        print("CAMPAIGN SUMMARY")
        print(f"{'='*60}")
        for result in results:
            print(f"\n{result['business_name']}")
            print(f"  Email: {result['email']}")
            print(f"  Claim Page: {result['claim_url']}")
            print(f"  Demo: {result['demo_url']}")
            print(f"  Emails to send: {len(result['email_campaign'])}")

        return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 BOT1_MASTER_PIPELINE.py <prospects.csv>")
        print("\nCSV format (pipe-delimited):")
        print("email|business_name|owner_name|website_url|sender_account")
        sys.exit(1)

    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)

    pipeline = BotMasterPipeline()
    results = pipeline.run(csv_path)
