from concurrent.futures import ThreadPoolExecutor
from strategies.trend_strategy import TrendStrategy
from strategies.consistency_strategy import ConsistencyStrategy
from Day import Day
from Week import Week
from Month import Month
from Year import Year
from DBConnector import DBConnector
# weitere Strategien hier importieren...

from Calculator import Calculator

class StrategyEngine:
    def __init__(self):
        self.connector = DBConnector()
        self.connector.Startconnection()

        try:
            self.products = self.connector.GetProducts()  # Muss ein 3-Tupel sein: (IDs, names, URLs)
        except Exception as e:
            print(f"❌ Fehler beim Laden der Produkte: {e}")
            self.products = ([], [], [])

        self.strategies = [
            TrendStrategy(),
            ConsistencyStrategy(),
            # weitere Strategien
        ]
        self.maxWorkers = 10

    def evaluate_single(self, day, week, month, year):
        result = {}
        for strat in self.strategies:
            try:
                score = strat.evaluate(day, week, month, year)
                result[strat.name] = score
            except Exception as e:
                print(f"[Fehler] Strategie {strat.name} für Aktie {day.name}: {e}")
                result[strat.name] = 0
        return (day.Aktie_ID, day.name, result)

    def evaluate_all_parallel(self):
        print("🔍 Lade Daten aus Datenbank...")
        days = self.calc.GetDaysFromDB()
        weeks = self.calc.GetWeeksFromDB()
        months = self.calc.GetMonthsFromDB()
        years = self.calc.GetYearsFromDB()

        # Kombiniere alle Zeiteinheiten anhand gleicher Indexreihenfolge
        all_data = list(zip(days, weeks, months, years))

        print(f"⚙️ Starte Auswertung für {len(all_data)} Aktien mit {self.max_workers} Threads...")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.evaluate_single, day, week, month, year)
                       for (day, week, month, year) in all_data]
            results = [future.result() for future in futures]

        print("✅ Strategiebewertung abgeschlossen.")
        return results

    def analyze_by_id(self, aktie_id: int, draw=True):
        ids, names, urls = self.products
        if aktie_id not in ids:
            print(f"Aktie-ID {aktie_id} nicht gefunden.")
            return

        index = ids.index(aktie_id)
        name, url = names[index], urls[index]

        print(f"\n📊 Analyse für {name} (ID: {aktie_id})")

        # Objekte instanziieren
        day = Day(aktie_id, name, url)
        week = Week(aktie_id, name, url)
        month = Month(aktie_id, name, url)
        year = Year(aktie_id, name, url)

        # Daten aus DB holen
        day_data = self.connector.GetCurrentDays()
        week_data = self.connector.GetCurrentWeek()
        month_data = self.connector.GetCurrentMonth()
        year_data = self.connector.GetCurrentYear()

        day.GetDayFromDB(aktie_id, day_data)
        week.GetWeekFromDB(aktie_id, week_data)
        month.GetMonthFromDB(aktie_id, month_data)
        year.GetYearFromDB(aktie_id, year_data)

        # Regressionen berechnen
        print("  ➤ Regressions-Steigungen:")
        print(f"     📅 Day   : {day.GetSlope():.4f}")
        print(f"     📈 Week  : {week.GetSlope():.4f}")
        print(f"     📆 Month : {month.GetSlope():.4f}")
        print(f"     📊 Year  : {year.GetSlope():.4f}")

        # Strategien bewerten
        print("\n  ➤ Strategie-Scores:")
        for strat in self.strategies:
            score = strat.evaluate(day, week, month, year)
            print(f"     {strat.name}: {score:.4f}")

        # Optional: Graphen anzeigen
        if draw:
            day.DrawDay()
            week.DrawWeek()
            month.DrawMonth()
            year.DrawYear()