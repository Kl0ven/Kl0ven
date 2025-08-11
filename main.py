import requests
import os
import re
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup


def get_nasa_image():
    resp = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={os.getenv('NASA_API_KEY')}")
    resp.raise_for_status()

    data = {}
    body = resp.json()
    data["nasa_img"] = body.get("url")
    data["img_explanation"] = body.get("explanation")
    data["img_title"] = body.get("title")
    data["is_video"] = body.get("media_type") == "video"
    if data["is_video"]:
        match = re.match(r"^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*", body["url"])
        data["video_id"] = match[7] if match and len(match[7]) == 11 else None

    return data


def generate_readme(data):
    env = Environment(loader=FileSystemLoader("view"))
    template = env.get_template("main.html.j2")
    readme = template.render(**data)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)


def get_gh_stars_list():
    # FML https://github.com/orgs/community/discussions/8293
    resp = requests.get("https://github.com/Kl0ven?tab=stars")
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, features="html.parser")
    stars_list = soup.find_all(id="profile-lists-container")
    assert len(stars_list) == 1, 'Could not find tag with id="profile-lists-container"'
    data = []
    for item in stars_list[0].find_all("a"):
        href = item.get_attribute_list("href")[0]
        name = item.find("h3").text
        desc_span = item.find("span")
        desc = None
        if desc_span:
            desc = desc_span.text.strip()
        data.append((name, desc, href))
    return data


if __name__ == "__main__":
    data = get_nasa_image()
    stars = get_gh_stars_list()
    data["stars"] = sorted(stars, key=lambda x: "0000" + x[0] if x[1] else x[0])
    generate_readme(data)
