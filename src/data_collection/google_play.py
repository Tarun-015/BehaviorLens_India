from google_play_scraper import reviews, Sort
import pandas as pd

APP_ID = "xyz.penpencil.physicswala"


def collect_reviews(max_reviews=5000):

    all_reviews = []
    continuation_token = None

    while len(all_reviews) < max_reviews:

        result, continuation_token = reviews(
            APP_ID,
            lang="en",
            country="in",
            sort=Sort.NEWEST,
            count=100,
            continuation_token=continuation_token
        )

        if not result:
            break

        all_reviews.extend(result)

        print(f"Collected: {len(all_reviews)} reviews")

        if continuation_token is None:
            break

    df = pd.DataFrame([
        {
            "review_id": r.get("reviewId"),
            "rating": r.get("score"),
            "review_date": r.get("at"),
            "app_version": r.get("reviewCreatedVersion"),
            "likes": r.get("thumbsUpCount"),
            "review_text": r.get("content")
        }
        for r in all_reviews
    ])

    output_file = (
        "data/raw/google_play/"
        "physics_wallah/"
        "pw_reviews_5000.csv"
    )

    df.to_csv(output_file, index=False)

    print("\n====================")
    print("CSV Saved")
    print(output_file)
    print("====================")

    print("\nRating Distribution")
    print(df["rating"].value_counts().sort_index())

    print("\nDate Range")
    print("Newest:", df["review_date"].max())
    print("Oldest:", df["review_date"].min())


if __name__ == "__main__":
    collect_reviews(5000)