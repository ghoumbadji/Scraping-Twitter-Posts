# Scraping Twitter Posts

Since scraping Twitter directly has become nearly impossible and the official Twitter API is prohibitively expensive, this project provides a reliable workaround. I have developed a Python script, located in `scraper.py`, that collects data via Lightbrd, an alternative front-end for Twitter that provides access to the same public posts and user content.

## Features

* **Bot Bypass:** Uses `undetected-chromedriver` to safely navigate past basic bot protections and verification checkboxes.
* **Pagination Handling:** Automatically loads consecutive pages until the exact requested number of tweets is reached.
* **Clean Data:** Filters out retweets to extract only the original content from the target user.
* **Structured Output:** Retrieves the text content, publication date, and the direct link for each post.

## Requirements

* Python 3.12 or higher.
* Google Chrome installed locally (the script is configured for Chrome v152).

## Installation

1. Clone this repository to your local machine.
2. Create and activate a virtual environment.
3. Install the required dependencies using the provided requirements file:

```bash
pip install -r requirements.txt
```

## Usage

The scraping logic is contained within the `scraper.py` file. Import the main function and specify the target's Twitter handle (the exact identifier that comes after the `@` symbol, not their display name) along with the number of posts you want to retrieve. 

For instance, to scrape posts from Yann LeCun, you must use his handle `ylecun` and not his display name `Yann LeCun`.

```python
from scraper import scrape_x_posts

# Extract the 10 most recent posts using the handle "ylecun"
posts = scrape_x_posts("ylecun", 10)
print(posts)
```

## Data Format

The script outputs a list of dictionaries that can easily be serialized into JSON or exported to a CSV file. Voici un exemple de structure générée :

```json
[
  {
    "link": "[https://lightbrd.com/ylecun/status/1234567890](https://lightbrd.com/ylecun/status/1234567890)",
    "publication_date": "Oct 2, 2026 2:30 PM UTC",
    "content": "This is an example of the scraped tweet content."
  }
]
```