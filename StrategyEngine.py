from Day import Day
from Week import Week
from Month import Month
from Year import Year
from DBConnector import DBConnector
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

class StrategyEngine:
    def __init__(self):
        self.connector = DBConnector()
        self.connector.Startconnection()
        self.products = self.connector.GetProducts()

    def fetch_all_data(self):
        ids, names, urls = self.products
        print(f"📦 Lade Aktien-Daten für {len(ids)} Produkte...")

        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                'day': executor.submit(self.connector.GetCurrentDays),
                'week': executor.submit(self.connector.GetCurrentWeek),
                'month': executor.submit(self.connector.GetCurrentMonth),
                'year': executor.submit(self.connector.GetCurrentYear),
            }
            day_data = futures['day'].result()
            week_data = futures['week'].result()
            month_data = futures['month'].result()
            year_data = futures['year'].result()

        def build_entry(i):
            day = Day(ids[i], names[i], urls[i])
            week = Week(ids[i], names[i], urls[i])
            month = Month(ids[i], names[i], urls[i])
            year = Year(ids[i], names[i], urls[i])

            day.GetDayFromDB(ids[i], day_data)
            week.GetWeekFromDB(ids[i], week_data)
            month.GetMonthFromDB(ids[i], month_data)
            year.GetYearFromDB(ids[i], year_data)

            return (ids[i], names[i], day, week, month, year)

        with ThreadPoolExecutor(max_workers=35) as executor:
            all_entries = list(executor.map(build_entry, range(len(ids))))

        return all_entries

    @staticmethod
    def evaluate_single_processsafe(entry):
        from strategies.trend_strategy import TrendStrategy
        from strategies.consistency_strategy import ConsistencyStrategy
        from strategies.momentum_strategy import MomentumStrategy
        from strategies.stability_strategy import StabilityStrategy
        from strategies.composite_strategy import CompositeStrategy
        from strategies.final_strategy import FinalRecommendationStrategy

        aktien_id, name, day, week, month, year = entry
        scores = {}

        strategies = [
            TrendStrategy(),
            StabilityStrategy(),
            MomentumStrategy(),
            ConsistencyStrategy(),
            CompositeStrategy(),
        ]
        final_strategy = FinalRecommendationStrategy()

        for strat in strategies:
            try:
                score = strat.evaluate(day, week, month, year)
            except Exception as e:
                score = f"Fehler: {e}"
            scores[strat.name] = score

        try:
            final_score = final_strategy.evaluate(day, week, month, year, scores)
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
        cpu_cores = max(2, multiprocessing.cpu_count() - 1)

        with ProcessPoolExecutor(max_workers=cpu_cores) as executor:
            futures = [executor.submit(self.evaluate_single_processsafe, entry) for entry in entries]
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                results.append(result)
                print(f"✅ Bewertet {i}/{len(entries)}: {result['name']}")

        sorted_results = sorted(
            results,
            key=lambda r: r['scores'].get("FinalRecommendation", 0),
            reverse=True
        )
        return sorted_results[:top_n]  # <<< Rückgabe der besten N Aktien

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

        scores = self.evaluate_single_processsafe((aktien_id, name, day, week, month, year))["scores"]

        print("\n  ➤ Strategie-Scores:")
        for strat, score in scores.items():
            if strat == "FinalRecommendation":
                continue
            print(f"     {strat}: {score:.2f}" if isinstance(score, (int, float)) else f"     {strat}: {score}")

        final_score = scores.get("FinalRecommendation", "Fehler")
        level = self.classify_score(final_score)
        print(f"\n  💡 Gesamtempfehlung: {final_score}/100 → {level}")
