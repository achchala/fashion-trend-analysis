import requests
from bs4 import BeautifulSoup
import time
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter, defaultdict
import re

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("vader_lexicon")

nlp = spacy.load("en_core_web_sm")

sia = SentimentIntensityAnalyzer()

# Custom fashion-related entity patterns
fashion_patterns = [
    r"\b(?:dress|gown|suit|jacket|coat|skirt|pants|jeans|shirt|blouse|sweater|accessory)\b",
    r"\b(?:spring|summer|fall|winter|seasonal|trend)\b",
    r"\b(?:luxury|high-end|affordable|sustainable|ethical)\b",
]


class FashionTrendAnalyzer:
    def __init__(self):
        self.brands = Counter()
        self.designers = Counter()
        self.garments = Counter()
        self.themes = Counter()
        self.trend_scores = defaultdict(list)

    def extract_entities(self, text):
        doc = nlp(text)

        for ent in doc.ents:
            if ent.label_ == "ORG":
                self.brands[ent.text.lower()] += 1
            elif ent.label_ == "PERSON":
                self.designers[ent.text.lower()] += 1

        for pattern in fashion_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                if "dress" in pattern or "gown" in pattern:
                    self.garments[match.group()] += 1
                elif "spring" in pattern or "summer" in pattern:
                    self.themes[match.group()] += 1

    def analyze_sentiment(self, text):
        return sia.polarity_scores(text)

    def update_trend_scores(self, entity, sentiment_score):
        self.trend_scores[entity].append(sentiment_score["compound"])

    def get_trend_rankings(self):
        rankings = {}
        for entity, scores in self.trend_scores.items():
            avg_score = sum(scores) / len(scores)
            frequency = len(scores)
            rankings[entity] = {
                "average_sentiment": avg_score,
                "frequency": frequency,
                "trend_strength": avg_score * frequency,
            }
        return rankings


def main():
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://www.vogue.com/fashion"

    analyzer = FashionTrendAnalyzer()

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("a", href=True)

    for a in articles:
        if "/article/" in a["href"]:
            title = a.get_text(strip=True)
            link = a["href"]
            if not link.startswith("http"):
                link = f"https://www.vogue.com{link}"

            try:
                article_response = requests.get(link, headers=headers)
                article_soup = BeautifulSoup(article_response.text, "html.parser")

                article_text = article_soup.find("div", class_="article__body")
                if article_text:
                    content = article_text.get_text(strip=True)

                    analyzer.extract_entities(content)
                    sentiment = analyzer.analyze_sentiment(content)

                    for brand in analyzer.brands:
                        analyzer.update_trend_scores(brand, sentiment)
                    for designer in analyzer.designers:
                        analyzer.update_trend_scores(designer, sentiment)
                    for garment in analyzer.garments:
                        analyzer.update_trend_scores(garment, sentiment)
                    for theme in analyzer.themes:
                        analyzer.update_trend_scores(theme, sentiment)

                time.sleep(1)

            except Exception as e:
                print(f"Error processing article {link}: {str(e)}")

    return analyzer


if __name__ == "__main__":
    analyzer = main()

    print("\nFashion Trend Analysis")

    print("\nTop Brands:")
    for brand, count in analyzer.brands.most_common(10):
        print(f"{brand}: {count} mentions")

    print("\nTop Designers:")
    for designer, count in analyzer.designers.most_common(10):
        print(f"{designer}: {count} mentions")

    print("\nPopular Garment Types:")
    for garment, count in analyzer.garments.most_common(10):
        print(f"{garment}: {count} mentions")

    print("\nTrending Themes:")
    for theme, count in analyzer.themes.most_common(10):
        print(f"{theme}: {count} mentions")

    print("\nTrend Rankings (by strength):")
    rankings = analyzer.get_trend_rankings()
    sorted_trends = sorted(
        rankings.items(), key=lambda x: x[1]["trend_strength"], reverse=True
    )

    for trend, metrics in sorted_trends[:10]:
        print(f"\n{trend}:")
        print(f"  Trend Strength: {metrics['trend_strength']:.2f}")
        print(f"  Frequency: {metrics['frequency']}")
        print(f"  Average Sentiment: {metrics['average_sentiment']:.2f}")
