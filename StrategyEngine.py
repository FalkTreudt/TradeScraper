from Day import Day
from Week import Week
from Month import Month
from Year import Year
from DBConnector import DBConnector
from concurrent.futures import ThreadPoolExecutor

# Strategien
from strategies.trend_strategy import TrendStrategy
from strategies.consistency_strategy import ConsistencyStrategy
from strategies.momentum_strategy import MomentumStrategy
from strategies.stability_strategy import StabilityStrategy
from strategies.composite_strategy import CompositeStrategy
from strategies.final_strategy import FinalRecommendationStrategy


class StrategyEngine:
    def __init__(self):
        self.connector = DBConnector()
        self.connector.Startconnection()
        self.products = self.connector.GetProducts()
        self.strategies = [
            TrendStrategy(),
            StabilityStrategy(),
            MomentumStrategy(),
            ConsistencyStrategy(),
            CompositeStrategy(),
        ]
        self.final_strategy = FinalRecommendationStrategy()

    def fetch_all_data(self):
        ids, names, urls = self.products

        print(f"📦 Lade Aktien-Daten für {len(ids)} Produkte...")

        day_data = self.connector.GetCurrentDays()
        week_data = self.connector.GetCurrentWeek()
        month_data = self.connector.GetCurrentMonth()
        year_data = self.connector.GetCurrentYear()

        all_entries = []

        for i in range(len(ids)):
            day = Day(ids[i], names[i], urls[i])
            week = Week(ids[i], names[i], urls[i])
            month = Month(ids[i], names[i], urls[i])
            year = Year(ids[i], names[i], urls[i])

            day.GetDayFromDB(ids[i], day_data)
            week.GetWeekFromDB(ids[i], week_data)
            month.GetMonthFromDB(ids[i], month_data)
            year.GetYearFromDB(ids[i], year_data)

            all_entries.append((ids[i], names[i], day, week, month, year))

        return all_entries

    def evaluate_single(self, entry):
        aktien_id, name, day, week, month, year = entry
        scores = {}

        for strat in self.strategies:
            try:
                score = strat.evaluate(day, week, month, year)
            except Exception as e:
                score = f"Fehler: {e}"
            scores[strat.name] = score

        # final strategy
        try:
            final_score = self.final_strategy.evaluate(day, week, month, year, scores)
            scores["FinalRecommendation"] = final_score
        except Exception as e:
            scores["FinalRecommendation"] = f"Fehler: {e}"

        return {
            "id": aktien_id,
            "name": name,
            "scores": scores,
            "day": day,
            "week": week,
            "month": month,
            "year": year
        }

    def analyze_all(self, top_n=10):
        entries = self.fetch_all_data()

        print("🧠 Starte Bewertung der Strategien...")

        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.evaluate_single, entry) for entry in entries]
            for future in futures:
                result = future.result()
                results.append(result)

        print(f"\n🔝 Top {top_n} Aktien basierend auf FinalRecommendation:\n")
        sorted_results = sorted(
            results,
            key=lambda r: r['scores'].get("FinalRecommendation", 0),
            reverse=True
        )

        for res in sorted_results[:top_n]:
            score = res['scores'].get("FinalRecommendation", 0)
            level = self.classify_score(score)
            print(f"   {res['name']} (ID: {res['id']}) – {score}/100 → {level}")

    def classify_score(self, score):
        if not isinstance(score, (int, float)):
            return "❓ Unbekannt"
        if score >= 85:
            return "✅ Kaufen"
        elif score >= 60:
            return "⚠️ Beobachten"
        else:
            return "🚫 Nicht kaufen"

    def analyze_by_id(self, aktien_id):
        ids, names, urls = self.products
        try:
            i = ids.index(aktien_id)
        except ValueError:
            print(f"Aktie-ID {aktien_id} nicht gefunden.")
            return

        name = names[i]
        url = urls[i]

        day = Day(aktien_id, name, url)
        week = Week(aktien_id, name, url)
        month = Month(aktien_id, name, url)
        year = Year(aktien_id, name, url)

        day.GetDayFromDB(aktien_id, self.connector.GetCurrentDays())
        week.GetWeekFromDB(aktien_id, self.connector.GetCurrentWeek())
        month.GetMonthFromDB(aktien_id, self.connector.GetCurrentMonth())
        year.GetYearFromDB(aktien_id, self.connector.GetCurrentYear())

        print(f"\n📊 Analyse für {name} (ID: {aktien_id})")

        print("  ➤ Regressions-Steigungen:")
        print(f"     📅 Day   : {day.GetSlope():.4f}")
        print(f"     📈 Week  : {week.GetSlope():.4f}")
        print(f"     📆 Month : {month.GetSlope():.4f}")
        print(f"     📊 Year  : {year.GetSlope():.4f}")

        scores = self.evaluate_single((aktien_id, name, day, week, month, year))["scores"]

        print("\n  ➤ Strategie-Scores:")
        for strat, score in scores.items():
            if strat == "FinalRecommendation":
                continue
            print(f"     {strat}: {score:.2f}" if isinstance(score, (int, float)) else f"     {strat}: {score}")

        final_score = scores.get("FinalRecommendation", "Fehler")
        level = self.classify_score(final_score)
        print(f"\n  💡 Gesamtempfehlung: {final_score}/100 → {level}")
