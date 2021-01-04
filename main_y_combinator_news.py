from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/news")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")

news_items = soup.find_all(name="tr", class_="athing")

news_items_dict = {}

rank_x = None
storylink_x = None
article_link_x = None

for news_item in news_items:
    id_x = news_item.get("id")
    score_tag = soup.find(id=f"score_{id_x}")
    if score_tag is not None:
        score_x = int(score_tag.getText().replace("points", "").strip())
    else:
        score_x = 0
    for titles in news_item.find_all(name="td", class_="title"):
        for title_x in titles:
            title_type = " ".join(title_x.get("class"))
            if title_type == "rank":
                rank_x = int(title_x.getText().replace(".", ""))
            elif title_type == "storylink":
                storylink_x = title_x.getText()
                article_link_x = title_x.get("href")
            news_items_dict[rank_x] = {"storylink": storylink_x, "article_link": article_link_x, "score": score_x}

highest_upvotes = 0
highest_upvotes_key = []
for key in news_items_dict.keys():
    if news_items_dict[key]["score"] > highest_upvotes:
        highest_upvotes = news_items_dict[key]["score"]
        highest_upvotes_key = [key]
    elif news_items_dict[key]["score"] == highest_upvotes:
        highest_upvotes_key.append(key)

# Filter highest upvoted news items
highest_upvotes_news_items = {key: value for (key, value) in news_items_dict.items() if key in highest_upvotes_key}

print(highest_upvotes_news_items)