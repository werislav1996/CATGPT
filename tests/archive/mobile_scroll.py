"""Check reading position after real answer clicks, locally or on a deployed URL."""
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

url = sys.argv[1] if len(sys.argv) > 1 else (Path(__file__).resolve().parents[1] / 'index.html').as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH'), headless=True)
    for width, height in [(320, 640), (390, 844), (700, 900), (1440, 960)]:
        page = browser.new_page(viewport={'width': width, 'height': height}, has_touch=width <= 700, is_mobile=width <= 700)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(url, wait_until='networkidle')
        page.locator('#startButton').click()
        page.wait_for_timeout(250)
        for choice, expected in [('credit', 'c1_credit'), ('keep', 'c1_org'), ('human', 'c1_org_work')]:
            # Include a reader who has manually scrolled partway through the text.
            if choice == 'keep':
                page.locator('#storyScroll').evaluate('(el) => { el.scrollTop = 120; }')
            before = page.locator('#storyScroll').evaluate('(el) => el.scrollTop')
            page.locator(f'#choices [data-choice="{choice}"]').click()
            page.wait_for_timeout(250)
            assert page.evaluate('CatGameUI.getState().node') == expected
            after = page.locator('#storyScroll').evaluate('(el) => el.scrollTop')
            if width <= 700:
                assert abs(after - before) <= 1, f'{width}px, {choice}: reading position jumped from {before} to {after}'
            else:
                assert after > before, 'Desktop should still navigate to the new turn'
            assert page.evaluate('window.scrollY') == 0
        if width <= 700:
            page.locator('#jumpCurrent').click()
            page.wait_for_timeout(250)
            assert page.locator('#storyScroll').evaluate('(el) => el.scrollTop') > after
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert not errors, errors
        print(f'PASS {width}x{height}: answers, reading position, explicit navigation, no script errors')
        page.close()
    browser.close()
