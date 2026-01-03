from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def looks_like_botcheck(html: str) -> bool:
    h = (html or "").lower()
    keywords = [
        "captcha", "enter the characters", "type the characters",
        "robot check", "sorry", "verify", "unusual traffic"
    ]
    return any(k in h for k in keywords)

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

driver.get("https://www.amazon.in")
driver.maximize_window()

# Search
wait.until(EC.visibility_of_element_located((By.ID, "twotabsearchtextbox"))).send_keys("iphones")
wait.until(EC.element_to_be_clickable((By.ID, "nav-search-submit-button"))).click()

# Wait for results area (Amazon commonly uses one of these)
wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.s-main-slot, div.s-search-results, [data-component-type='s-search-result']")
    )
)

time.sleep(2)  # allow lazy rendering

print("\n=== DEBUG ===")
print("URL  :", driver.current_url)
print("Title:", driver.title)

html = driver.page_source
if looks_like_botcheck(html):
    print("\n⚠️ Amazon likely triggered a bot-check/CAPTCHA page (sometimes subtle).")
    print("   Fix: solve any CAPTCHA in the open browser, then re-run OR use your Chrome profile (see below).")
    driver.quit()
    raise SystemExit(0)

# Scroll to trigger lazy-loaded content
driver.execute_script("window.scrollTo(0, 900);")
time.sleep(1)
driver.execute_script("window.scrollTo(0, 0);")
time.sleep(1)

# Try multiple selectors (Amazon changes markup often)
selectors = [
    (By.CSS_SELECTOR, "h2 a span"),  # common
    (By.CSS_SELECTOR, "span.a-size-medium.a-color-base.a-text-normal"),
    (By.CSS_SELECTOR, "span.a-size-base-plus.a-color-base.a-text-normal"),
    (By.XPATH, "//div[@data-component-type='s-search-result']//h2//span"),
    (By.XPATH, "//div[@data-component-type='s-search-result']//span[contains(@class,'a-text-normal')]"),
]

elements = []
for how, sel in selectors:
    found = driver.find_elements(how, sel)
    # Keep non-empty textContent only
    filtered = []
    for el in found:
        t = (el.get_attribute("textContent") or "").strip()
        if t:
            filtered.append((t, el))
    if filtered:
        elements = filtered
        print(f"\n✅ Matched using selector: {how} -> {sel}")
        break

if not elements:
    # Last resort: extract via JS from result cards
    print("\n⚠️ No titles found via Selenium locators. Trying JS extraction...")
    titles = driver.execute_script("""
        const cards = Array.from(document.querySelectorAll("[data-component-type='s-search-result']"));
        const out = [];
        for (const c of cards) {
          const t = c.querySelector("h2 span") || c.querySelector("span.a-text-normal");
          if (t && t.textContent && t.textContent.trim()) out.push(t.textContent.trim());
        }
        return out;
    """) or []
    titles = [t for t in titles if t.strip()]
    print(f"Found titles via JS: {len(titles)}\n")
    for i, t in enumerate(titles[:10], start=1):
        print(f"{i}. {t}")
    driver.quit()
    raise SystemExit(0)

print("\n📱 iPhone search results:\n")
for i, (title, _) in enumerate(elements[:10], start=1):
    print(f"{i}. {title}")

driver.quit()
