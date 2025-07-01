import asyncio
from pyppeteer import launch


async def main():
    # Starte den Headless-Browser
    browser = await launch(headless=True)
    page = await browser.newPage()

    # Besuche die Website
    await page.goto('https://www.example.com')

    # Extrahiere alle Links von der Seite
    links = await page.evaluate('''() => {
        const links = Array.from(document.querySelectorAll('a'));
        return links.map(link => link.href);
    }''')

    # Gebe alle Links aus
    for link in links:
        print(link)

    # Schließe den Browser
    await browser.close()


# Starte das Skript
asyncio.get_event_loop().run_until_complete(main())
