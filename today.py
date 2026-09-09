import json
import os
import time
import urllib.request
import urllib.error

try:
    from lxml import etree
    USE_LXML = True
except ImportError:
    import xml.etree.ElementTree as ET
    USE_LXML = False

try:
    import requests
except ImportError:
    requests = None

USER_NAME = os.environ.get("USER_NAME", "Rahulchaube1")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")


def github_request(url):
    headers = {"User-Agent": "Rahulchaube1-profile-stats"}
    if ACCESS_TOKEN:
        headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"

    if requests:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.json()

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_public_metrics(username):
    """Return live public profile metrics without fabricated fallback values."""
    user = github_request(f"https://api.github.com/users/{username}")
    repos = github_request(
        f"https://api.github.com/users/{username}/repos?per_page=100&type=owner&sort=updated"
    )

    if not isinstance(repos, list):
        repos = []

    return (
        int(user.get("public_repos", 0)),
        sum(int(repo.get("stargazers_count", 0)) for repo in repos),
        int(user.get("followers", 0)),
    )


def find_and_replace(root, element_id, new_text):
    if USE_LXML:
        elem = root.find(f".//*[@id='{element_id}']")
        if elem is not None:
            elem.text = new_text
            return True
        return False

    for elem in root.iter():
        if elem.attrib.get("id") == element_id:
            elem.text = new_text
            return True
    return False


def svg_overwrite(filename, repo_data, star_data, follower_data):
    if not os.path.exists(filename):
        raise FileNotFoundError(filename)

    if USE_LXML:
        tree = etree.parse(filename)
        root = tree.getroot()
    else:
        tree = ET.parse(filename)
        root = tree.getroot()

    find_and_replace(root, "stats_repos", f"{repo_data:,}")
    find_and_replace(root, "stats_stars", f"{star_data:,}")
    find_and_replace(root, "stats_followers", f"{follower_data:,}")

    tree.write(filename, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    start_time = time.perf_counter()

    try:
        repo_data, star_data, follower_data = fetch_public_metrics(USER_NAME)
        svg_overwrite("dark_mode.svg", repo_data, star_data, follower_data)
        svg_overwrite("light_mode.svg", repo_data, star_data, follower_data)
        elapsed = time.perf_counter() - start_time
        print(
            f"Profile stats updated successfully in {elapsed:.3f}s: "
            f"repos={repo_data}, stars={star_data}, followers={follower_data}"
        )
    except (OSError, ValueError, urllib.error.URLError) as exc:
        print(f"Profile stats update failed: {exc}")
        raise SystemExit(1)
