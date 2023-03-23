import requests
import os

def update():
    # Set the repository URL and the current version of the script
    repo_url = 'https://api.github.com/repos/IanDalton/PdfSlideShow/releases/latest'
    current_version = 'v0.0.0'

    # Get the latest release information from GitHub
    response = requests.get(repo_url)
    data = response.json()
    latest_version = data['tag_name']

    # Compare the current and latest versions
    if current_version != latest_version:
        print(f'New version available: {latest_version}')
        print('Updating...')

        # Download and replace the script with the latest version
        download_url = data['assets'][0]['browser_download_url']
        filename = os.path.basename(__file__)
        response = requests.get(download_url)
        with open(filename, 'wb') as f:
            f.write(response.content)

        print('Update complete!')
    else:
        print('No updates available.')

update()