import os
import requests  # 确保导入 requests 模块
from github import Github

# 获取 GitHub Token（使用自定义 secret）
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")

if GITHUB_TOKEN is None:
    print("Error: MY_GITHUB_TOKEN is not set.")
    exit(1)

REPO_NAME = "jzhou9096/jilianip"
FILE_PATH = "addtro.csv"
CSV_URL = "https://addcsv.sosorg.nyc.mn/addressesapi.csv?token=ZYSS"

def fetch_webpage_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if not response.text:
            print(f"Warning: Empty content from {url}")
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching CSV: {e}")
        return None

def write_to_github(content):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    try:
        file = repo.get_contents(FILE_PATH)
        repo.update_file(FILE_PATH, "Updated CSV content", content, file.sha, branch="main")
        print("File updated successfully on GitHub.")
    except Exception as e:
        print(f"Error writing to GitHub: {e}")

def main():
    print("Fetching CSV content...")
    content = fetch_webpage_content(CSV_URL)
    if content:
        print("Writing content to GitHub...")
        write_to_github(content)

if __name__ == "__main__":
    main()
