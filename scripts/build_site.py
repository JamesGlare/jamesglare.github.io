#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "site.json"
CSS = ROOT / "assets" / "site.css"
INDEX = ROOT / "index.html"
CV_DIR = ROOT / "cv"
CV_INDEX = CV_DIR / "index.html"
NOJEKYLL = ROOT / ".nojekyll"


def h(text: str) -> str:
    return html.escape(text, quote=True)


def render_links(links):
    return "".join(
        f'<a class="button" href="{h(item["url"])}">{h(item["label"])}{"</a>"}' for item in links
    )


def render_project_cards(projects):
    cards = []
    for project in projects:
        links = " ".join(
            f'<a href="{h(link["url"])}">{h(link["label"])}{"</a>"}' for link in project.get("links", [])
        )
        cards.append(
            f"""
            <article class=\"card\">
              <h3>{h(project['title'])}</h3>
              <p>{h(project['summary'])}</p>
              <div class=\"card-links\">{links}</div>
            </article>
            """
        )
    return "\n".join(cards)


def render_publications(items):
    blocks = []
    for item in items:
        blocks.append(
            f"""
            <article class=\"publication\">
              <h3><a href=\"{h(item['url'])}\">{h(item['title'])}</a></h3>
              <p class=\"publication-meta\">{h(item['meta'])}</p>
            </article>
            """
        )
    return "\n".join(blocks)


def render_link_cards(items):
    blocks = []
    for item in items:
        blocks.append(
            f"""
            <article class=\"card compact-card\">
              <h3><a href=\"{h(item['url'])}\">{h(item['title'])}</a></h3>
              <p>{h(item['description'])}</p>
            </article>
            """
        )
    return "\n".join(blocks)


def render_timeline(items):
    blocks = []
    for item in items:
        blocks.append(
            f"""
            <article class=\"timeline-item\">
              <div class=\"timeline-meta\">{h(item['date'])}</div>
              <div>
                <h3>{h(item['role'])}</h3>
                <div class=\"timeline-org\">{h(item['org'])}</div>
                <p>{h(item['summary'])}</p>
              </div>
            </article>
            """
        )
    return "\n".join(blocks)


def page(title: str, body: str, description: str) -> str:
    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>{h(title)}</title>
    <meta name=\"description\" content=\"{h(description)}\" />
    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />
    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />
    <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap\" rel=\"stylesheet\" />
    <link rel=\"stylesheet\" href=\"/assets/site.css\" />
  </head>
  <body>
    {body}
  </body>
</html>
"""


def build_index(data):
    person = data["person"]
    intro = "".join(f"<p>{h(paragraph)}</p>" for paragraph in person["intro"])
    body = f"""
    <div class=\"shell\">
      <header class=\"site-header\">
        <a class=\"wordmark\" href=\"/\">{h(person['name'])}</a>
        <nav>
          <a href=\"#projects\">Projects</a>
          <a href=\"#publications\">Publications</a>
          <a href=\"#experience\">Experience</a>
          <a href=\"/cv/\">CV</a>
        </nav>
      </header>

      <main>
        <section class=\"hero\">
          <p class=\"eyebrow\">{h(person['location'])}</p>
          <h1>{h(person['name'])}</h1>
          <p class=\"headline\">{h(person['headline'])}</p>
          <div class=\"intro\">{intro}</div>
          <div class=\"button-row\">{render_links(person['links'])}</div>
        </section>

        <section id=\"projects\" class=\"section\">
          <div class=\"section-heading\">
            <p class=\"eyebrow\">Selected work</p>
            <h2>Projects</h2>
          </div>
          <div class=\"card-grid\">
            {render_project_cards(data['projects'])}
          </div>
        </section>

        <section id=\"publications\" class=\"section\">
          <div class=\"section-heading\">
            <p class=\"eyebrow\">Papers</p>
            <h2>Selected publications</h2>
          </div>
          <div class=\"publication-list\">
            {render_publications(data['publications'])}
          </div>
        </section>

        <section id=\"experience\" class=\"section\">
          <div class=\"section-heading\">
            <p class=\"eyebrow\">Career</p>
            <h2>Experience</h2>
          </div>
          <div class=\"timeline\">
            {render_timeline(data['experience'])}
          </div>
        </section>

        <section class=\"section\">
          <div class=\"section-heading\">
            <p class=\"eyebrow\">Elsewhere</p>
            <h2>Links</h2>
          </div>
          <div class=\"card-grid card-grid-links\">
            {render_link_cards(data['links'])}
          </div>
        </section>
      </main>
    </div>
    """
    return page(person["name"], body, person["headline"])


def build_cv(data):
    person = data["person"]
    body = f"""
    <div class=\"shell shell-narrow\">
      <header class=\"site-header\">
        <a class=\"wordmark\" href=\"/\">{h(person['name'])}</a>
        <nav>
          <a href=\"/\">Home</a>
          <a href=\"#experience\">Experience</a>
          <a href=\"#education\">Education</a>
        </nav>
      </header>

      <main class=\"cv\">
        <section class=\"section\">
          <p class=\"eyebrow\">Curriculum vitae</p>
          <h1>{h(person['name'])}</h1>
          <p class=\"headline\">{h(person['headline'])}</p>
          <div class=\"button-row\">{render_links(person['links'][:-1])}</div>
        </section>

        <section id=\"experience\" class=\"section\">
          <div class=\"section-heading\">
            <h2>Experience</h2>
          </div>
          <div class=\"timeline\">{render_timeline(data['experience'])}</div>
        </section>

        <section id=\"education\" class=\"section\">
          <div class=\"section-heading\">
            <h2>Education</h2>
          </div>
          <div class=\"timeline\">{render_timeline(data['education'])}</div>
        </section>

        <section class=\"section\">
          <div class=\"section-heading\">
            <h2>Selected publications</h2>
          </div>
          <div class=\"publication-list\">{render_publications(data['publications'])}</div>
        </section>
      </main>
    </div>
    """
    return page(f"{person['name']} — CV", body, f"CV of {person['name']}")


def main():
    data = json.loads(CONTENT.read_text())
    CSS.parent.mkdir(parents=True, exist_ok=True)
    CV_DIR.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(build_index(data))
    CV_INDEX.write_text(build_cv(data))
    NOJEKYLL.write_text("")


if __name__ == "__main__":
    main()
