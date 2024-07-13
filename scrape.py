import requests
import random
import time
import re
from datetime import datetime, timedelta
import os

class RedditScraper:
    def __init__(self):
        self.base_url = 'https://www.reddit.com/r/{}/new.json'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.proxies = []
        self.proxy_file = None
        self.use_proxy = False
        self.output_file = 'reddit_posts.txt'
        self.fetch_type = 'all'
        self.subreddit = ''
        self.num_posts = 0
        self.start_date = None
        self.end_date = None
        self.network_speed = 0.5  # Average time per request in seconds

    def load_proxies(self, file_path):
        """Load proxies from the specified file."""
        with open(file_path, 'r') as f:
            self.proxies = [line.strip() for line in f if line.strip()]

    def test_proxy(self, proxy, retries=2):
        """Test if a proxy is working."""
        test_url = 'https://www.reddit.com/r/test/new.json'
        for _ in range(retries):
            try:
                response = requests.get(test_url, proxies={'http': proxy, 'https': proxy}, headers=self.headers, timeout=5)
                if response.status_code == 200:
                    return True
            except requests.RequestException:
                continue
        return False

    def get_working_proxy(self):
        """Get a working proxy from the list."""
        random.shuffle(self.proxies)
        for proxy in self.proxies:
            if self.test_proxy(proxy):
                return proxy
        raise Exception('No working proxies available.')

    def random_mac_address(self):
        """Generate a random MAC address."""
        return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])

    def get_post_data(self, post):
        """Extract relevant data from a post."""
        title = post.get('title', 'No Title')
        content = post.get('selftext', 'No Content')
        upvotes = post.get('ups', 0)
        comments = post.get('num_comments', 0)
        date = datetime.utcfromtimestamp(post['created_utc']).strftime('%Y-%m-%d')
        time_posted = datetime.utcfromtimestamp(post['created_utc']).strftime('%H:%M:%S')
        return {
            'title': title,
            'content': content,
            'upvotes': upvotes,
            'comments': comments,
            'date': date,
            'time_posted': time_posted
        }

    def fetch_posts(self, after, all_posts):
        """Fetch posts from Reddit with error handling and proxy management."""
        url = self.base_url.format(self.subreddit)
        params = {'limit': 100}
        if after:
            params['after'] = after

        while True:
            try:
                # Set headers with a random MAC address for each request
                self.headers['User-Agent'] = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 (MAC={self.random_mac_address()})'
                proxies = {'http': self.proxy, 'https': self.proxy} if self.use_proxy else None
                response = requests.get(url, headers=self.headers, params=params, proxies=proxies, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    posts = data['data']['children']
                    after = data['data']['after']

                    for post in posts:
                        all_posts.append(self.get_post_data(post['data']))
                        if len(all_posts) >= self.num_posts:
                            return after

                    if after is None:
                        break
                else:
                    raise Exception(f"Error: Received status code {response.status_code}")
            except requests.RequestException as e:
                if self.use_proxy:
                    print(f"Request failed: {e}. Retrying with a new proxy...")
                    self.proxy = self.get_working_proxy()
                    time.sleep(2)
                else:
                    print(f"Request failed: {e}. Retrying...")
                    time.sleep(2)
            except Exception as e:
                print(f"An error occurred: {e}. Retrying...")
                if self.use_proxy:
                    self.proxy = self.get_working_proxy()
                time.sleep(2)

    def scrape_reddit(self):
        """Handle the scraping process including proxy management and error handling."""
        all_posts = []
        after = None

        if self.use_proxy:
            self.proxy = self.get_working_proxy()
        else:
            self.proxy = None

        while True:
            try:
                self.fetch_posts(after, all_posts)
                if len(all_posts) >= self.num_posts:
                    break
            except Exception as e:
                print(f"An error occurred during scraping: {e}. Retrying with a new proxy...")
                if self.use_proxy:
                    self.proxy = self.get_working_proxy()
                time.sleep(2)

        return all_posts

    def save_to_file(self, posts):
        """Save post data to the specified output file."""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for post in posts:
                f.write(f"Title: {post['title']}\n")
                f.write(f"Content: {post['content']}\n")
                f.write(f"Upvotes: {post['upvotes']}\n")
                f.write(f"Comments: {post['comments']}\n")
                f.write(f"Date: {post['date']}\n")
                f.write(f"Time: {post['time_posted']}\n")
                f.write("\n" + "-"*80 + "\n\n")

    def estimate_time(self):
        """Estimate the time required for scraping."""
        num_requests = (self.num_posts // 100) + 1
        return num_requests * self.network_speed

    def get_user_input(self):
        """Collect and validate user inputs."""
        while True:
            try:
                self.subreddit = input("Enter subreddit name: ").strip()
                if not self.subreddit:
                    raise ValueError("Subreddit name cannot be empty.")

                self.fetch_type = input("Fetch type (all/random_n/first_n/date_range): ").strip().lower()
                if self.fetch_type not in ['all', 'random_n', 'first_n', 'date_range']:
                    raise ValueError("Invalid fetch type. Choose from 'all', 'random_n', 'first_n', 'date_range'.")

                if self.fetch_type in ['random_n', 'first_n']:
                    self.num_posts = int(input("Enter number of posts to fetch: "))
                    if self.num_posts <= 0:
                        raise ValueError("Number of posts must be a positive integer.")

                if self.fetch_type == 'date_range':
                    self.start_date = input("Enter start date (yyyy/mm/dd): ")
                    self.end_date = input("Enter end date (yyyy/mm/dd): ")
                    datetime.strptime(self.start_date, '%Y/%m/%d')
                    datetime.strptime(self.end_date, '%Y/%m/%d')
                    if self.start_date >= self.end_date:
                        raise ValueError("Start date must be before end date.")

                self.use_proxy = input("Do you want to use a proxy? (yes/no): ").strip().lower()
                if self.use_proxy == 'yes':
                    self.proxy_file = input("Enter the proxy file name: ").strip()
                    self.load_proxies(self.proxy_file)
                elif self.use_proxy == 'no':
                    self.use_proxy = False
                else:
                    raise ValueError("Please answer 'yes' or 'no' for using proxy.")

                if self.use_proxy and not self.proxies:
                    raise ValueError("Proxy file is empty or not found.")
                    self.use_proxy = False

                self.output_file = input("Enter the output file name (default 'reddit_posts.txt'): ").strip()
                if not self.output_file:
                    self.output_file = 'reddit_posts.txt'

                break

            except ValueError as e:
                print(f"Error: {e}. Please try again.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")

    def run(self):
        """Main function to run the scraper."""
        self.get_user_input()

        if self.fetch_type == 'all':
            estimated_time = self.estimate_time()
            print(f"Estimated time for fetching all posts: {estimated_time:.2f} seconds")
            proceed = input("Do you want to proceed? (yes/no): ").strip().lower()
            if proceed != 'yes':
                print("Scraping cancelled.")
                return

        print("Starting the scraping process...")
        posts = self.scrape_reddit()
        self.save_to_file(posts)
        print(f"Saved {len(posts)} posts to {self.output_file}")

if __name__ == "__main__":
    scraper = RedditScraper()
    scraper.run()
