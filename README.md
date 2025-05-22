# Fashion Trend Analysis

Analyzes fashion trends from Vogue articles using natural language processing and sentiment analysis. The application provides insights into trending brands, designers, garment types, and themes in the fashion industry.

## Features

- Automatically scrapes fashion articles from Vogue's website
- NLP: spaCy and NLTK for entity recognition and text analysis
- Analyzes the sentiment of fashion-related content
-  Tracks and ranks fashion trends based on:
  - Brand mentions
  - Designer mentions
  - Garment types
  - Seasonal themes
- Streamlit-based interface for visualizing:
  - Top brands and designers
  - Popular garment types
  - Trending themes
  - Trend strength heatmaps
  - Detailed trend metrics

## Running App

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)


## Project Structure

- `scrape.py`: Core functionality for web scraping and trend analysis
- `app.py`: Streamlit web application interface
- `requirements.txt`: Project dependencies
- `README.md`: Project documentation

## Dependencies

- requests: Web scraping
- beautifulsoup4: HTML parsing
- spacy: Natural language processing
- nltk: Text analysis and sentiment analysis
- streamlit: Web application interface
- pandas: Data manipulation
- plotly: Interactive visualizations
