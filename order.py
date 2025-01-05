import colorsys, math
from pprint import pprint

COLORS = [
    "ansible-EE0000",
    "Debian-A81D33",
    "redis-D92B21",
    "Git-F05032",
    "prometheus-E6522C",
    "Ubuntu-E95420",
    "grafana-F46800",
    "Gitlab-F56A25",
    "RabbitMQ-FF6600",
    "talos-FF7300",
    "proxmox-E57000",
    "falco-00AEC7",
    "harbor-60B932",
    "MongoDB-47A248",
    "Celery-37814A",
    "Django-092E20",
    "Kustomize-35519b",
    "FluxCD-5468FF",
    "Kubernetes-316CE6",
    "PostgreSQL-336791",
    "Python-3776AB",
    "Docker-2496ED",
    "Poetry-0098f0",
    "Github Actions-2088FF",
    "VSCode-007ACC",
    "Helm-0F1689",
    "Flask-000000",
    "Heroku-430098",
    "htop-009020",
    "kaniko-FFA600",
    "keycloak-4D4D4D",
    "materialformkdocs-526CFE",
    "minio-C72E49",
    "ruff-D7FF64",
    "trivy-1904DA",
    "uptimekuma-5CDD8B",
    "zsh-F15A24",
]


def lum(r, g, b):
    return math.sqrt(0.241 * r + 0.691 * g + 0.068 * b)


def step(r, g, b, repetitions=1):
    lum = math.sqrt(0.241 * r + 0.691 * g + 0.068 * b)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)
    return (h2, lum2, v2)


working = []
for c in COLORS:
    name, html = c.split("-")
    rgb = tuple(int(html[i : i + 2], 16) / 256 for i in (0, 2, 4))

    # hsv = colorsys.rgb_to_hsv(*rgb)
    # hsv = step(*rgb, 8)

    working.append((name, rgb))


pprint(sorted(working, key=lambda x: step(*x[1], 8)))
