import nanopub
from nanopub import NanopubClient
import requests
import os

client = NanopubClient()

nanopub_url = "https://w3id.org/np/RAODrYRV1ZCo-sxct9JH9v44jMkCYteKw_LwFaEzQTJJY"
save_directory = r"C:\Users\alif2\PycharmProjects\NanoPub"

# Helper function to get all files within the web directory
def get_github_files_list(github_repo_url):
    try:
        api_url = github_repo_url.replace("https://github.com", "https://api.github.com/repos") + "/contents"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch repo contents. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error while fetching GitHub repo contents: {e}")
        return None

# Try to fetch the nanopub identifier
def fetch_nanopub(url):
    try:
        np = client.fetch(url)
        print(f"Successfully loaded nanopub from {url}")
        return np
    except Exception as e:
        print(f"Failed to load nanopub: {e}")
        return None

# Obtain the subject of the assertion (the dataset link)
def extract_github_link(nanopub_data):
    try:
        assertion_graph = nanopub_data.assertion
        for s, p, o in assertion_graph:
            if isinstance(s, str) and 'github.com' in s:  # Check if object is a GitHub URL
                print(f"Found GitHub repository URL: {s}")
                return s
        print("No GitHub URL found in the assertion.")
        return None
    except Exception as e:
        print(f"Failed to extract GitHub URL: {e}")
        return None

# Extract the jsonld files from the github
def scrape_jsonld_files(github_url, save_directory):
    try:
        files_list = get_github_files_list(github_url)
        if files_list:
            jsonld_files = [file['download_url'] for file in files_list if file['name'].endswith('.jsonld')]
            if jsonld_files:
                print(f"Found {len(jsonld_files)} .jsonld files.")
                for file_url in jsonld_files:
                    print(f"Downloading file: {file_url}")
                    file_response = requests.get(file_url)
                    if file_response.status_code == 200:
                        file_name = os.path.join(save_directory, file_url.split("/")[-1])
                        with open(file_name, 'wb') as f:
                            f.write(file_response.content)
                        print(f"File saved to {file_name}")
                    else:
                        print(f"Failed to download {file_url}")
            else:
                print("No .jsonld files found in the GitHub repository.")
        else:
            print("No files retrieved from the GitHub repository.")
    except Exception as e:
        print(f"Error while scraping .jsonld files: {e}")


nanopub_data = fetch_nanopub(nanopub_url)

if nanopub_data:
    github_url = extract_github_link(nanopub_data)
    if github_url:
        github_url_api = github_url.replace("https://github.com", "https://api.github.com/repos").replace("/tree/main","")
        scrape_jsonld_files(github_url_api, save_directory)
    else:
        print("No valid GitHub URL found in the nanopub.")
else:
    print("Nanopub loading failed, skipping further processing.")
