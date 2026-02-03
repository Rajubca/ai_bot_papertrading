from playwright.sync_api import sync_playwright
import time

def verify_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to dashboard
        try:
            page.goto("http://localhost:3000")
            # Wait for content
            page.wait_for_selector("h1", timeout=10000)

            # Take screenshot of dashboard
            page.screenshot(path="verification/dashboard.png")
            print("Dashboard screenshot taken.")

            # Navigate to trade page
            page.goto("http://localhost:3000/trade")
            page.wait_for_selector("input", timeout=10000)
            page.screenshot(path="verification/trade.png")
            print("Trade screenshot taken.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_dashboard()
