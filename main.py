import requests
import os
import re
from jinja2 import Environment, FileSystemLoader


def get_nasa_image():
    resp = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={os.getenv('NASA_API_KEY')}")
    resp.raise_for_status()

    data = {}
    body = resp.json()
    data["nasa_img"] = body["url"]
    data["img_explanation"] = body["explanation"]
    data["img_title"] = body["title"]
    data["is_video"] = body["media_type"] == "video"
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


if __name__ == "__main__":
    apod = get_nasa_image()
    generate_readme(apod)
