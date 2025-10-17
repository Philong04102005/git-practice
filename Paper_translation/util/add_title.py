import pandas as pd
news_sites = [
    "TechCrunch (Startups)",
    "VentureBeat",
    "Inc.",
    "World Bank",
    "Techstars",
    "Crunchbase News",
    "Forbes (Entrepreneurs)",
    "CB Insights (Research)",
    "Reuters (Technology)",
    "Bloomberg (Technology)",
    "Glossy",
    "Business of Fashion",
    "Fashionista",
    "WWD",
    "TechCrunch",
    "The Fintech Times",
    "Fintech Global",
    "Fintech News Singapore",
    "CNBC (Fintech)",
    "Fintech Magazine",
    "Fintech Futures",
    "Global Influences",
    "Reuters (Lifestyle)",
    "New York Times (Lifestyle Spotlight)",
    "Vogue UK (Arts & Lifestyle)",
    "GQ (Lifestyle)",
    "Bloomberg Pursuits (Style)",
    "W Magazine (Life)",
    "Harper's Bazaar UK (Guide)",
    "Robb Report (Lifestyle)",
    "Elle",
    "New York Times (International Style)",
    "TechCrunch (Lifestyle)"
]
url_list = pd.read_csv("data/tech_sources.csv")
url_list = pd.DataFrame({
    "URL":url_list.iloc[:,1],
    "Web name": news_sites,
    "Tag name": 0,
    "Tag time": 0,
})
url_list.to_csv('data/link_tag1.csv', index=False)