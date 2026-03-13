#!/usr/bin/env python3
"""
Bot 1 - Claim Page Generator
Customizes the claim.html landing page for each prospect with their business data.
The landing page wraps the demo in a blue/teal wrapper with portfolio section.
"""

import os
import re
from pathlib import Path

class ClaimPageGenerator:
    def __init__(self):
        self.template_path = "/Users/adayliakrispli/webreach/four-seasons-roofing-v2/claim.html"

    def generate(self, business_name, demo_url, output_path):
        """
        Generate a customized claim.html for a prospect.

        Args:
            business_name: Name of the business
            demo_url: URL to the index.html demo (for iframe src)
            output_path: Where to save the customized claim.html

        Returns:
            Path to generated file
        """
        # Read template
        with open(self.template_path, 'r') as f:
            content = f.read()

        # Customize for this prospect
        # 1. Update the 48hr reservation banner
        content = content.replace(
            '<span>This preview is reserved for <strong>Four Seasons Roofing</strong>',
            f'<span>This preview is reserved for <strong>{business_name}</strong>'
        )

        # 2. Update header label
        content = content.replace(
            '<span class="header-label">Live Preview &mdash; <span>Four Seasons Roofing</span></span>',
            f'<span class="header-label">Live Preview &mdash; <span>{business_name}</span></span>'
        )

        # 3. Update intro headline
        content = content.replace(
            '<h1 class="intro-headline">\n            A preview website was created<br>for <em>Four Seasons Roofing</em>\n        </h1>',
            f'<h1 class="intro-headline">\n            A preview website was created<br>for <em>{business_name}</em>\n        </h1>'
        )

        # 4. Update iframe src
        content = content.replace(
            'src="http://localhost:9999/demos/bot1/four-seasons-roofing-v2/index.html"',
            f'src="{demo_url}"'
        )

        # 5. Update iframe title
        content = content.replace(
            'title="Four Seasons Roofing Demo Website"',
            f'title="{business_name} Demo Website"'
        )

        # 6. Update trust strip
        content = content.replace(
            'This website was built using information already available about Four Seasons Roofing.',
            f'This website was built using information already available about {business_name}.'
        )

        # 7. Update CTA headline (optional, keep it generic for roofing)
        # Don't change this - it's generic enough

        # Write to output
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(content)

        return output_path

if __name__ == "__main__":
    # Test usage
    generator = ClaimPageGenerator()

    # Test: Generate for Dwell Roofing
    claim_path = generator.generate(
        business_name="Dwell Roofing",
        demo_url="https://adayliak1-pixel.github.io/webreach/demo/dwell-roofing/index.html",
        output_path="/Users/adayliakrispli/webreach/demo/dwell-roofing/claim.html"
    )
    print(f"✓ Generated claim page: {claim_path}")

    # Test: Generate for Monarch Roofing
    claim_path = generator.generate(
        business_name="Monarch Roofing",
        demo_url="https://adayliak1-pixel.github.io/webreach/demo/monarch-roofing/index.html",
        output_path="/Users/adayliakrispli/webreach/demo/monarch-roofing/claim.html"
    )
    print(f"✓ Generated claim page: {claim_path}")
