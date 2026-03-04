from google_play_scraper import reviews, Sort
import pandas as pd

app_id = "com.application.zomato"

result, _ = reviews(
    app_id,
    lang='en',
    country='in',
    count=2500,
    sort=Sort.NEWEST  # ✅ Correct way
)

df = pd.DataFrame(result)

df = df[['content', 'score', 'at', 'reviewCreatedVersion', 'thumbsUpCount']]
df.columns = ['review_text', 'rating', 'review_date', 'app_version', 'likes']

df['app_name'] = "Zomato"
df['category'] = "Food Delivery"

df.to_csv("zomato_reviews.csv", index=False)

print("Scraping Complete ✅")