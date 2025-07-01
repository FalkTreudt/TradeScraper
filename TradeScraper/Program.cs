using System;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;

class Program
{
    static void Main()
    {
        // WebDriver initialisieren (hier für Chrome)
        IWebDriver driver = new ChromeDriver();

        // Google öffnen
        driver.Navigate().GoToUrl("https://www.google.com");

        // Warten, bis das Suchfeld sichtbar und interagierbar ist
        WebDriverWait wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
        IWebElement searchBox = wait.Until(d => d.FindElement(By.Name("q"))); // Verwende die direkte Bedingung

        // Optional: Fokus auf das Suchfeld mit JavaScript setzen
        ((IJavaScriptExecutor)driver).ExecuteScript("arguments[0].focus();", searchBox);

        // Das Suchfeld ausfüllen und absenden
        searchBox.SendKeys("Falk Treudt");
        searchBox.Submit();

        // Warten, bis die Ergebnisseite geladen ist
        wait.Until(d => d.Title.Contains("Google Search"));

        // Extrahieren des ersten Suchergebnisses
        var firstResult = wait.Until(d => d.FindElement(By.CssSelector("h3")));

        // Den Text des ersten Ergebnisses ausgeben
        Console.WriteLine("Erstes Suchergebnis: " + firstResult.Text);

        // Den Link des ersten Ergebnisses ausgeben
        var resultLink = firstResult.FindElement(By.XPath("..")).FindElement(By.TagName("a"));
        Console.WriteLine("Link: " + resultLink.GetAttribute("href"));

        // Browser schließen
        driver.Quit();
    }
}
