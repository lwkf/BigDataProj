import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# --- First Section: Trend Comparison Across Monthly Counts ---
df1 = pd.read_csv("analysis_output/user_join_trends.csv")
df2 = pd.read_csv("analysis_output/monthly_review_counts.csv")
df3 = pd.read_csv("analysis_output/tip_monthly_trends.csv")
df4 = pd.read_csv("analysis_output/checkin_monthly_trends.csv")

df1_name, df2_name, df3_name, df4_name = "Registration Count", "Review Count", "Tip Count", "Checkin Count"

for df in [df1, df2, df3, df4]:
    df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))

df1 = df1[["date", "count"]].rename(columns={"count": df1_name})
df2 = df2[["date", "count"]].rename(columns={"count": df2_name})
df3 = df3[["date", "count"]].rename(columns={"count": df3_name})
df4 = df4[["date", "count"]].rename(columns={"count": df4_name})

df_merged = df1.merge(df2, on="date", how="outer").merge(df3, on="date", how="outer").merge(df4, on="date", how="outer")

df_merged = df_merged.sort_values("date")

df_long = df_merged.melt(id_vars="date", var_name="Dataset", value_name="Count")

trend_fig = px.line(df_long, x="date", y="Count", color="Dataset", markers=True,
                    title="Trend Comparison Across Monthly Counts")

# --- Second Section: Business Rank and Density by State ---
yelp_df = pd.read_csv("analysis_output/rankedBusiness.csv")

rank_counts = yelp_df.groupby(["state", "rank"]).size().reset_index(name="count")

rank_counts["rank"] = rank_counts["rank"].astype(int)
rank_counts = rank_counts.sort_values(by=["state", "rank"])

rank_fig = px.bar(
    rank_counts,
    x="state",
    y="count",
    color="rank",
    barmode="group",
    title="Business Rank Distribution by State",
    labels={"count": "Number of Businesses", "state": "US State", "rank": "Rank"}
)

rank1_df = yelp_df[yelp_df["rank"] == 1]

rank1_counts = rank1_df.groupby("state").size().reset_index(name="count")

choropleth_fig = px.choropleth(
    rank1_counts,
    locations="state",
    locationmode="USA-states",
    color="count",
    scope="usa",
    color_continuous_scale="Blues",
    title="Number of Rank 1 Businesses by US State"
)

state_counts_df = pd.read_csv("analysis_output/geo_business_density_state_only.csv") 

density_fig = px.choropleth(
    state_counts_df,
    locations="state",
    locationmode="USA-states",
    color="business_count",
    scope="usa",
    color_continuous_scale="YlOrRd",
    title="Business Density by US State",
    labels={"business_count": "Number of Businesses", "state": "US State"}
)

# --- Third Section: Word Clouds and Sentiment Analysis ---
positive_df = pd.read_csv("analysis_output/top_words_positive.csv")
negative_df = pd.read_csv("analysis_output/top_words_negative.csv")

def create_wordcloud_image(df, title):
    word_freq = dict(zip(df["word"], df["count"]))
    wc = WordCloud(width=400, height=300, background_color="white").generate_from_frequencies(word_freq)

    buf = BytesIO()
    plt.figure(figsize=(5, 4))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

good_wc = create_wordcloud_image(positive_df, "Positive Reviews")
bad_wc = create_wordcloud_image(negative_df, "Negative Reviews")
sentiment_df = pd.read_csv("analysis_output/review_sentimentCounts.csv")

pie_fig = px.pie(
    sentiment_df,
    names="sentiment",
    values="count",
    title="Review Sentiment Distribution",
    color_discrete_sequence=px.colors.qualitative.Set3
)



# --- Dash App ---
app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.H1("Big Data Project Visualization"),
        html.H2("By: Group 3"),
        html.H3("Yelp Dataset Analysis"),
        html.H3("This visualization provides insights into the Yelp dataset, focusing on trends in user registrations, "
               "business rankings, and sentiment analysis of reviews.")
    ], style={"textAlign": "center", "marginBottom": "20px"}),
    

    # First Section
    html.Div([
        html.H2("Trend Comparison Across Monthly Counts", style={"textAlign": "center", "marginBottom": "20px"}),

        dcc.Graph(figure=trend_fig),

        html.Div([
            html.P("The trend of the number of check-ins is to be expected since the number of registrations is consistent. "
                "As more users are registering, more check-ins are expected."),

            html.P("We can also see when COVID hit the US, around March 2020, that is when the lockdown in the US started. "
                "However, we saw that the number of reviews surpassed the number of check-ins. "
                "This is because the reliance on Food Delivery Companies had increased and so did their review count.")
        ], style={"width": "80%", "margin": "0 auto", "marginTop": "20px", "lineHeight": "1.6", "fontSize": "20px"})
    ], style={"backgroundColor": "#f9f9f9", "padding": "30px", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"}),

    # Second Section
    html.Div([
        html.H2("Business Rank and Density by State", style={"textAlign": "center", "marginBottom": "20px"}),

        html.Div([
            html.P("The bar chart above shows the distribution of businesses by rank across different states.",
                style={"fontWeight": "bold", "marginBottom": "20px"}),

            html.Div([
                html.Div([
                    dcc.Graph(figure=choropleth_fig)
                ], style={"width": "49%", "display": "inline-block", "paddingRight": "1%"}),

                html.Div([
                    dcc.Graph(figure=density_fig)
                ], style={"width": "49%", "display": "inline-block", "paddingLeft": "1%"})
            ], style={"display": "flex", "justifyContent": "space-between"}),

            html.P("As the Yelp dataset mainly features 11 metropolitan areas, we expected to see that there are not a lot of "
                "businesses in the other states aside from these 14 states. With the choropleth map, we can see that the number "
                "of rank 1 businesses is concentrated in the states of Pennsylvania (PA), Florida (FL), California (CA), and "
                "Nevada (NV). This is rather peculiar for California. Although it has a higher number of rank 1 businesses "
                "compared to Arizona (AZ) or Nevada (NV), it has a lower density of businesses overall."), 

            html.Div([
                dcc.Graph(figure=rank_fig)
            ], style={"marginBottom": "30px"}),
            html.P("The bar chart above shows the distribution of businesses by rank across different states. Since the dataset "
            "does not cover all states, we can see that the number of the other top ranked businesses are also concentrated in "
            "the same states. This further proves that though having more businesses in a state does not mean that the state has "
            "more ranked businesses.")
        ], style={"width": "85%", "margin": "0 auto", "lineHeight": "1.6", "marginTop": "20px", "fontSize": "20px"})
    ], style={"backgroundColor": "#fdf5e2", "padding": "30px", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"}),

    # Third Section
    html.Div([
        html.H2("Word Clouds and Sentiment Analysis", style={"textAlign": "center", "marginBottom": "20px"}),

        html.Div([
            html.Div([
                html.Img(src=f"data:image/png;base64,{good_wc}", style={"width": "100%"})
            ], style={"width": "30%", "display": "inline-block", "textAlign": "center"}),

            html.Div([
                html.Img(src=f"data:image/png;base64,{bad_wc}", style={"width": "100%"})
            ], style={"width": "30%", "display": "inline-block", "textAlign": "center"}),

            html.Div([
                dcc.Graph(figure=pie_fig)
            ], style={"width": "38%", "display": "inline-block", "verticalAlign": "top", "paddingLeft": "2%"})
        ], style={"marginBottom": "30px"}),

        html.Div([
            html.P("The word clouds above show the most common words in the positive and negative reviews found in the dataset. "
                "The pie chart shows the distribution of review sentiments that reveals a majority of reviews left behind is "
                "positive. This also helps explain why the words in the positive word cloud appear larger than those in the "
                "negative word cloud. This would show that customers are also much more likely to leave a review in positive light "
                "than in negative light."),
        ], style={"width": "80%", "margin": "0 auto", "lineHeight": "1.6", "fontSize": "20px"})
    ], style={"backgroundColor": "#f9f9f9", "padding": "30px", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"})
])

if __name__ == "__main__":
    app.run(debug=True)
