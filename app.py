import streamlit as st
import pandas as pd
from scrape import FashionTrendAnalyzer
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Fashion Trend Analysis", layout="wide")

st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .trend-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("Fashion Trend Analysis Dashboard")
st.subheader("Intelligent Decision Support System")

with st.sidebar:
    st.header("Your Preferences")

    style = st.multiselect(
        "Style Preferences",
        [
            "Minimal",
            "Editorial",
            "Casual",
            "Streetwear",
            "Luxury",
            "Vintage",
            "Bohemian",
        ],
        default=["Minimal", "Casual"],
    )

    budget = st.select_slider(
        "Budget Range",
        options=["< $100", "$100 - $300", "$300 - $500", "$500 - $1000", "Luxury"],
        value="$100 - $300",
    )

    preferred_brands = st.multiselect(
        "Preferred Brands",
        ["Nike", "Zara", "H&M", "Gucci", "Prada", "Balenciaga", "Adidas", "Uniqlo"],
        default=[],
    )

    current_season = st.selectbox(
        "Season", ["Spring 2024", "Summer 2024", "Fall 2024", "Winter 2024"], index=1
    )

analyzer = FashionTrendAnalyzer()

if st.button("Analyze Fashion Trends"):
    with st.spinner("Analyzing fashion trends..."):
        from scrape import main

        analyzer = main()

        st.header("Personalized Recommendations")

        rec_col1, rec_col2 = st.columns(2)

        with rec_col1:
            st.subheader("Top Trends for Your Style")
            filtered_trends = analyzer.get_trend_rankings()
            filtered_trends = {
                k: v
                for k, v in filtered_trends.items()
                if any(s.lower() in k.lower() for s in style)
            }

            for trend, metrics in list(filtered_trends.items())[:5]:
                with st.container():
                    st.markdown(
                        f"""
                    <div class="trend-card">
                        <h3>{trend}</h3>
                        <p>Trend Strength: {metrics['trend_strength']:.2f}</p>
                        <p>Confidence Score: {metrics['average_sentiment']:.2f}</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

        with rec_col2:
            st.subheader("Brand Recommendations")
            # Filter brands based on budget and preferences
            brand_recs = analyzer.brands.most_common(10)
            brand_recs = [
                b
                for b in brand_recs
                if b[0].lower() in [p.lower() for p in preferred_brands]
            ]

            for brand, count in brand_recs[:5]:
                with st.container():
                    st.markdown(
                        f"""
                    <div class="trend-card">
                        <h3>{brand}</h3>
                        <p>Mentions: {count}</p>
                        <p>Trend Relevance: {count/len(analyzer.brands):.2%}</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

        st.header("Trend Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top Brands")
            brands_df = pd.DataFrame(
                analyzer.brands.most_common(10), columns=["Brand", "Mentions"]
            )
            fig_brands = px.bar(
                brands_df, x="Brand", y="Mentions", title="Top 10 Brands"
            )
            st.plotly_chart(fig_brands)

            st.subheader("Popular Garment Types")
            garments_df = pd.DataFrame(
                analyzer.garments.most_common(10), columns=["Garment", "Mentions"]
            )
            fig_garments = px.bar(
                garments_df, x="Garment", y="Mentions", title="Top 10 Garment Types"
            )
            st.plotly_chart(fig_garments)

        with col2:
            st.subheader("Top Designers")
            designers_df = pd.DataFrame(
                analyzer.designers.most_common(10), columns=["Designer", "Mentions"]
            )
            fig_designers = px.bar(
                designers_df, x="Designer", y="Mentions", title="Top 10 Designers"
            )
            st.plotly_chart(fig_designers)

            st.subheader("Trending Themes")
            themes_df = pd.DataFrame(
                analyzer.themes.most_common(10), columns=["Theme", "Mentions"]
            )
            fig_themes = px.bar(
                themes_df, x="Theme", y="Mentions", title="Top 10 Trending Themes"
            )
            st.plotly_chart(fig_themes)

        st.header("Trend Evolution")
        rankings = analyzer.get_trend_rankings()
        rankings_df = pd.DataFrame(
            [
                {
                    "Trend": trend,
                    "Trend Strength": metrics["trend_strength"],
                    "Frequency": metrics["frequency"],
                    "Average Sentiment": metrics["average_sentiment"],
                }
                for trend, metrics in rankings.items()
            ]
        )

        rankings_df = rankings_df.sort_values("Trend Strength", ascending=False)

        fig_heatmap = go.Figure(
            data=go.Heatmap(
                z=rankings_df[
                    ["Trend Strength", "Frequency", "Average Sentiment"]
                ].values,
                x=["Trend Strength", "Frequency", "Average Sentiment"],
                y=rankings_df["Trend"],
                colorscale="Viridis",
            )
        )
        fig_heatmap.update_layout(title="Trend Analysis Heatmap")
        st.plotly_chart(fig_heatmap)

        st.subheader("Detailed Trend Data")
        st.dataframe(rankings_df)

        csv = rankings_df.to_csv(index=False)
        st.download_button(
            label="Download Trend Data",
            data=csv,
            file_name="fashion_trends.csv",
            mime="text/csv",
        )
