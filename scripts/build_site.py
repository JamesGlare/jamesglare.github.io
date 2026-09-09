#!/usr/bin/env python3
from __future__ import annotations

import hashlib
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
    version = hashlib.sha256(CSS.read_bytes()).hexdigest()[:10]
    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>{h(title)}</title>
    <meta name=\"description\" content=\"{h(description)}\" />
    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />
    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />
    <link href=\"https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap\" rel=\"stylesheet\" />
    <link rel=\"stylesheet\" href=\"/assets/site.css?v={version}\" />
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
    {body}
  </body>
</html>
"""


def header(name, home=False):
    prefix = "" if home else "/"
    return f"""<header class="site-header">
      <a class="wordmark" href="/">{h(name)}</a>
      <nav aria-label="Main navigation">
        <a href="{prefix}#projects">Work</a>
        <a href="/publications/">Publications</a>
        <a href="/cv/">CV</a>
        <a href="mailto:jannesgla@gmail.com">Contact <span aria-hidden="true">↗</span></a>
      </nav>
    </header>"""


def footer(data):
    links = "".join(f'<a href="{h(x["url"])}">{h(x["label"])} <span aria-hidden="true">↗</span></a>' for x in data['person']['links'] if x['label'] not in ('CV', 'Email'))
    return f'<footer class="site-footer"><span>{h(data["person"]["name"])} · London</span><div class="footer-links">{links}</div></footer>'


def render_featured(projects):
    categories = ["Optical computing", "Language models", "Stochastic physics"]
    blocks = []
    for i, project in enumerate(projects):
        links = "".join(f'<a href="{h(x["url"])}">{h(x["label"])} <span aria-hidden="true">↗</span></a>' for x in project['links'])
        blocks.append(f"""<article class="featured-project">
          <div class="project-index" aria-hidden="true">0{i+1}</div>
          <div class="project-copy"><p class="eyebrow">{categories[i]}</p>
          <h3>{h(project['title'])}</h3><p>{h(project['summary'])}</p>
          <div class="card-links">{links}</div></div>
        </article>""")
    return "".join(blocks)


def build_index(data):
    person = data['person']
    home = data['home']
    featured = [data['projects'][i] for i in home['featured_projects']]
    other = [p for i,p in enumerate(data['projects']) if i not in home['featured_projects']]
    selected = [data['publications'][i] for i in home['selected_publications']]
    body = f"""<div class="shell">
    {header(person['name'], home=True)}
    <main id="main">
      <section class="hero" aria-labelledby="intro-title">
        <div class="hero-copy">
          <p class="eyebrow">AI research & engineering <span class="eyebrow-divider">/</span> London</p>
          <h1 id="intro-title">Jannes<br>Gladrow<span class="name-period">.</span></h1>
          <p class="headline">{h(home['intro'])}</p>
          <div class="hero-links"><a class="primary-link" href="#projects">Explore my work <span aria-hidden="true">↓</span></a><a href="mailto:jannesgla@gmail.com">Get in touch <span aria-hidden="true">↗</span></a></div>
        </div>
        <figure class="hero-visual">
          <img src="/assets/negative-prism.svg" width="440" height="320" alt="Ray paths through a negative-index prism" />
          <figcaption>Negative refraction <span aria-hidden="true">/</span> n &lt; 0</figcaption>
        </figure>
      </section>
      <div class="career-strip"><span>Currently <strong>Meta AI</strong></span><span>Previously <strong>Microsoft Research</strong></span></div>
      <section id="projects" class="section editorial-section" aria-labelledby="work-title">
        <div class="section-heading"><p class="eyebrow">01 / Research</p><h2 id="work-title">Selected <br>work</h2><p>From learning algorithms to the physical systems that run them.</p></div>
        <div class="section-content">{render_featured(featured)}
          <details class="more-work"><summary>More projects <span aria-hidden="true">+</span></summary><div class="card-grid">{render_project_cards(other)}</div></details>
        </div>
      </section>
      <section id="publications" class="section editorial-section" aria-labelledby="papers-title">
        <div class="section-heading"><p class="eyebrow">02 / Writing</p><h2 id="papers-title">Selected <br>papers</h2><p><a class="text-link" href="/publications/">All publications <span aria-hidden="true">↗</span></a></p></div>
        <div class="publication-list section-content">{render_publications(selected)}</div>
      </section>
      <section id="experience" class="section editorial-section" aria-labelledby="about-title">
        <div class="section-heading"><p class="eyebrow">03 / Background</p><h2 id="about-title">Context</h2></div>
        <div class="about-copy section-content">
          <p>At Meta, I work on post-training, agentic harnesses, and systems for frontier models. Before that, I spent six years at Microsoft Research Cambridge, working across machine learning and optical computing.</p>
          <p>My PhD at Cambridge explored stochastic thermodynamics, optical tweezers, and machine learning, focusing on how to understand and control systems shaped by fluctuations.</p>
          <a class="text-link" href="/cv/">Full experience & education <span aria-hidden="true">↗</span></a>
          <span id="education" class="anchor-target" aria-hidden="true"></span>
        </div>
      </section>
      <section class="contact-section" aria-labelledby="contact-title"><p class="eyebrow">Say hello</p><h2 id="contact-title">Let’s compare notes.</h2><a class="contact-link" href="mailto:jannesgla@gmail.com">Email me <span aria-hidden="true">↗</span></a></section>
    </main>{footer(data)}</div>"""
    return page(person['name'], body, home['intro'])


def build_publications(data):
    body = f"""<div class="shell shell-narrow">{header(data['person']['name'])}
      <main id="main" class="archive"><section class="archive-hero"><p class="eyebrow">Research archive</p><h1>Publications</h1><p class="headline">Papers across machine learning, optical computing, and stochastic physics.</p><a class="text-link" href="https://scholar.google.de/citations?user=Kvy6GHYAAAAJ">Google Scholar <span aria-hidden="true">↗</span></a></section>
      <div class="publication-list">{render_publications(data['publications'])}</div></main>{footer(data)}</div>"""
    return page('Jannes Gladrow | Publications',body,'Publications by Jannes Gladrow.')


def build_cv(data):
    person = data["person"]
    body = f"""
    <div class=\"shell shell-narrow\">
      {header(person['name'])}

      <main id=\"main\" class=\"cv\">
        <section class=\"section cv-hero\">
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
            <h2>Publications</h2>
          </div>
          <div class=\"publication-list\">{render_publications(data['publications'])}</div>
        </section>
      </main>
    </div>
    """
    return page(f"{person['name']} | CV", body, f"CV of {person['name']}")


def clean_page(markup):
    return "\n".join(line.rstrip() for line in markup.splitlines()) + "\n"


def main():
    data = json.loads(CONTENT.read_text())
    CSS.parent.mkdir(parents=True, exist_ok=True)
    CV_DIR.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(clean_page(build_index(data)))
    CV_INDEX.write_text(clean_page(build_cv(data)))
    (ROOT / "publications").mkdir(exist_ok=True)
    (ROOT / "publications" / "index.html").write_text(clean_page(build_publications(data)))
    NOJEKYLL.write_text("")


if __name__ == "__main__":
    main()
