# Reddit Scraper

A Python-based Reddit scraper for fetching posts from a specified subreddit. This tool can scrape posts based on various criteria and supports proxy usage for improved performance and anonymity.

## Features

- **Fetch Posts**: Retrieve posts from a subreddit with options for different types of fetching.
  - **`all`**: Fetch all posts from the subreddit.
  - **`random_n`**: Fetch a specified number of random posts.
  - **`first_n`**: Fetch the first `n` posts.
  - **`date_range`**: Fetch posts within a specified date range.

- **Proxy Support**: Optionally use a list of proxies to make requests to Reddit.
  - Supports testing proxies to ensure they are working.
  - Automatically switches proxies on failure.
  - Handle proxy file input and retry mechanisms.

- **Error Handling**: Robust error handling for network issues, proxy failures, and API errors.

- **Multithreading Option**: Option to use multiple threads for fetching posts (can be disabled for single-threaded requests).

- **Output**: Save scraped post data to a text file with details such as title, content, upvotes, comments, date, and time.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Devn913/subreddit_post_scrapping.git
   cd subreddit_post_scrapping
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Requirements

The following packages are required to run this script:

- `requests`: For making HTTP requests to Reddit.

You can install these packages using the `requirements.txt` file.

## Usage

To run the scraper, execute the following command in your terminal:

```bash
python3 scrape.py
```

### User Inputs

You will be prompted for the following inputs:

1. **Subreddit Name**: The name of the subreddit to scrape (e.g., `idm`).
2. **Fetch Type**: The type of fetching operation:
   - `all` for all posts
   - `random_n` for a random number of posts
   - `first_n` for the first `n` posts
   - `date_range` for posts within a specific date range

3. **Number of Posts**: For `random_n` and `first_n` fetch types, specify the number of posts to fetch.
4. **Date Range**: For `date_range`, provide start and end dates in the format `yyyy/mm/dd`.
5. **Use Proxy**: Choose whether to use a proxy list. If `yes`, provide the name of the proxy file.
6. **Proxy File**: Specify the file name containing the list of proxies (one per line).
7. **Output File Name**: The name of the file where scraped data will be saved (default is `reddit_posts.txt`).
8. **Multithreading**: Choose whether to enable multithreading and specify the number of threads if enabled.

### Example

```bash
python3 scrape.py
```

Follow the prompts to enter the subreddit name, fetch type, number of posts, and other options.

### Sample Output

The output file will contain information about each post in the following format:

```
Title: Post Title
Content: Post Content
Upvotes: 123
Comments: 45
Date: 2024-07-13
Time: 14:32:10
--------------------------------------------------------------------------------
```

## Error Handling

The scraper includes error handling for:
- Network issues and API errors
- Proxy failures and invalid proxies
- Incorrect or missing user inputs

If all proxies are dead or invalid, the scraper will prompt for a new proxy file.

## License

This project is licensed under the [GPL License](https://opensource.org/licenses/GPL-3.0).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

## Contact

For questions or feedback, feel free to open an issue on the [GitHub repository](https://github.com/Devn913/subreddit_post_scrapping).

Happy scraping!


