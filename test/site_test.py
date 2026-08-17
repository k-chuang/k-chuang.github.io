from __future__ import print_function

import os
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PRIMARY_PAGES = {
    "/": SITE / "index.html",
    "/projects/": SITE / "projects" / "index.html",
}
ABOUT_REDIRECT = SITE / "about" / "index.html"
EXPERIENCE_REDIRECT = SITE / "experience" / "index.html"
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}
IGNORED_SCHEMES = {"data", "http", "https", "javascript", "mailto", "tel"}


def normalized_text(parts):
    return " ".join("".join(parts).split())


class ParsedHtml(HTMLParser):
    def __init__(self, source):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.source = source
        self.stack = []
        self.anchors = []
        self.resources = []
        self.ids = []
        self.images = []
        self.primary_navigation = []
        self.meta = {}
        self.html_lang = None
        self.title = ""
        self.h1 = []
        self._active_anchor = None
        self._active_title = None
        self._active_h1 = None
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        context = self.stack + [(tag, attributes)]
        in_primary_navigation = (
            any(item_tag == "nav" and item_attrs.get("id") == "site-nav" for item_tag, item_attrs in context)
            and any(
                item_tag == "ul" and "visible-links" in item_attrs.get("class", "").split()
                for item_tag, item_attrs in context
            )
        )

        element_id = attributes.get("id")
        if element_id:
            self.ids.append(element_id)

        if tag == "html":
            self.html_lang = attributes.get("lang")
        elif tag == "meta" and attributes.get("name"):
            self.meta[attributes["name"].lower()] = attributes.get("content", "")
        elif tag == "title":
            self._active_title = []
        elif tag == "h1":
            self._active_h1 = []
        elif tag == "a":
            self._active_anchor = {
                "href": attributes.get("href", ""),
                "attrs": attributes,
                "text": [],
                "primary_navigation": in_primary_navigation,
            }
        elif tag == "img":
            self.images.append(attributes)

        for attribute in ("href", "src"):
            if attributes.get(attribute):
                self.resources.append((tag, attribute, attributes[attribute]))

        if tag not in VOID_ELEMENTS:
            self.stack.append((tag, attributes))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_ELEMENTS:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if self._active_anchor is not None:
            self._active_anchor["text"].append(data)
        if self._active_title is not None:
            self._active_title.append(data)
        if self._active_h1 is not None:
            self._active_h1.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._active_anchor is not None:
            self._active_anchor["text"] = normalized_text(self._active_anchor["text"])
            self.anchors.append(self._active_anchor)
            if self._active_anchor["primary_navigation"]:
                self.primary_navigation.append(
                    (self._active_anchor["text"], self._active_anchor["href"])
                )
            self._active_anchor = None
        elif tag == "title" and self._active_title is not None:
            self.title = normalized_text(self._active_title)
            self._active_title = None
        elif tag == "h1" and self._active_h1 is not None:
            self.h1.append(normalized_text(self._active_h1))
            self._active_h1 = None

        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


class PortfolioSiteTests(unittest.TestCase):
    maxDiff = None
    parsed_cache = {}

    @classmethod
    def setUpClass(cls):
        if not SITE.is_dir():
            raise AssertionError("_site is missing; build the Jekyll site before running tests")

    @classmethod
    def parse_html(cls, path):
        path = Path(path)
        if path not in cls.parsed_cache:
            cls.parsed_cache[path] = ParsedHtml(path.read_text(encoding="utf-8"))
        return cls.parsed_cache[path]

    def test_01_required_pages_assets_and_resume_exist(self):
        required = list(PRIMARY_PAGES.values()) + [
            SITE / "404.html",
            ABOUT_REDIRECT,
            EXPERIENCE_REDIRECT,
            SITE / "assets" / "css" / "main.css",
            SITE / "assets" / "js" / "main.min.js",
            SITE / "assets" / "images" / "mountains_blue_ocean.jpg",
            SITE / "feed.xml",
            SITE / "sitemap.xml",
            SITE / "resume" / "cv.pdf",
        ]
        missing = [str(path.relative_to(SITE)) for path in required if not path.is_file()]
        self.assertEqual([], missing, "Missing required generated files")

        resume = SITE / "resume" / "cv.pdf"
        self.assertGreater(resume.stat().st_size, 10_000)
        with resume.open("rb") as stream:
            resume_bytes = stream.read()
        self.assertEqual(b"%PDF", resume_bytes[:4])
        self.assertFalse(
            b"tel:" in resume_bytes.lower(),
            "The published résumé must not contain an embedded telephone link",
        )

    def test_02_primary_navigation_is_exact_and_consistent(self):
        expected = [
            ("Projects", "/projects/"),
            ("Resume", "/resume/cv.pdf"),
        ]
        for public_path, file_path in PRIMARY_PAGES.items():
            with self.subTest(page=public_path):
                self.assertEqual(expected, self.parse_html(file_path).primary_navigation)

    def test_03_homepage_is_focused_on_experience_and_about(self):
        document = self.parse_html(PRIMARY_PAGES["/"])
        source = PRIMARY_PAGES["/"].read_text(encoding="utf-8")
        self.assertEqual(["Kevin Chuang"], document.h1)
        self.assertIn("Senior Software Engineer", source)
        self.assertIn("I build resilient, production-ready systems across backend, data, and AI.", source)
        self.assertIn("portfolio-home--split", source)
        self.assertIn("portfolio-sidebar__photo", source)
        self.assertIn('id="about"', source)
        self.assertIn('id="about-title">About me</h2>', source)
        self.assertIn("Hi there! I’m Kevin, and I enjoy building things.", source)
        self.assertIn("Currently, I’m a Senior Software Engineer at <strong>Adobe</strong>", source)
        self.assertIn("Previously, I worked at <strong>Turo</strong>, <strong>HomeLight</strong>, and <strong>ViacomCBS</strong>", source)
        self.assertIn("<strong>production backend and machine-learning systems</strong>", source)
        self.assertIn("In my spare time", source)
        self.assertIn("find me running, gaming, skateboarding", source)
        self.assertIn("hiking, spending time in nature", source)
        self.assertNotIn("film photography and its slower, more intentional process", source)
        self.assertTrue(any(
            image.get("src") == "/assets/images/bio.jpg"
            and image.get("alt") == "Kevin Chuang sitting beside a waterfall"
            for image in document.images
        ))
        self.assertIn('id="experience"', source)
        self.assertIn('id="experience-title"', source)
        self.assertIn("9+ years building production systems", source)
        self.assertIn('id="projects-title">Projects</h2>', source)
        self.assertEqual(3, source.count('class="featured-project"'))

        links = {(anchor["text"], anchor["href"]) for anchor in document.anchors}
        labelled_links = {(anchor["attrs"].get("aria-label"), anchor["href"]) for anchor in document.anchors}
        self.assertIn(("Email", "mailto:kevinchuang7@gmail.com"), labelled_links)
        self.assertIn(("GitHub", "https://github.com/k-chuang"), labelled_links)
        self.assertIn(("LinkedIn", "https://www.linkedin.com/in/kevin-chuang/"), labelled_links)
        self.assertIn(("Photography on Instagram", "https://www.instagram.com/bykevinchuang/"), labelled_links)
        self.assertIn(("Résumé", "/resume/cv.pdf"), labelled_links)
        self.assertIn(("View resume", "/resume/cv.pdf"), links)
        self.assertIn(("View all projects", "/projects/"), links)
        project_navigation = [
            anchor for anchor in document.anchors
            if anchor["text"] == "Projects" and anchor["href"] == "/projects/"
        ]
        self.assertTrue(any(anchor["attrs"].get("target") == "_blank" for anchor in project_navigation))
        self.assertFalse(any(text == "About" for text, _ in document.primary_navigation))
        self.assertFalse(any(text == "Experience" for text, _ in document.primary_navigation))

        for company in ("Adobe", "Turo", "HomeLight", "ViacomCBS"):
            self.assertIn(company, source)
        self.assertIn("Knowles Intelligent Audio", source)
        for company in ("adobe", "turo", "homelight", "viacomcbs", "knowles"):
            self.assertIn(company, document.ids)
        self.assertIn('class="layout--splash portfolio-background"', source)
        self.assertNotIn("San Jose–based", source)
        self.assertNotIn("portfolio-actions", source)
        self.assertNotIn("Full experience", source)
        self.assertNotIn("experience-entry-link", source)
        self.assertNotIn("about-preview-title", source)
        self.assertNotIn("portfolio-about-preview", source)
        self.assertNotIn("More about me", source)
        self.assertNotIn("selected-projects-title", source)
        self.assertNotIn("Selected projects", source)

        redirect = self.parse_html(ABOUT_REDIRECT)
        redirect_source = ABOUT_REDIRECT.read_text(encoding="utf-8")
        redirect_links = {(anchor["text"], anchor["href"]) for anchor in redirect.anchors}
        self.assertIn(("main portfolio page", "/#about"), redirect_links)
        self.assertIn("url=/#about", redirect_source)

    def test_04_primary_pages_have_expected_content(self):
        expected_content = {
            "/projects/": (
                "Yet Another URL Shortener",
                "Text Summarizer Chrome Extension",
                "Emotional State Recognition",
                "Data Science Competitions",
            ),
        }
        for public_path, phrases in expected_content.items():
            source = PRIMARY_PAGES[public_path].read_text(encoding="utf-8")
            for phrase in phrases:
                with self.subTest(page=public_path, phrase=phrase):
                    self.assertIn(phrase, source)

    def test_04b_experience_entries_are_compact_and_complete(self):
        file_path = PRIMARY_PAGES["/"]
        document = self.parse_html(file_path)
        source = file_path.read_text(encoding="utf-8")

        self.assertNotIn("career-timeline", source)
        self.assertNotIn("data-career-navigation", source)

        for company in ("adobe", "turo", "homelight", "viacomcbs", "knowles"):
            self.assertIn(company, document.ids)

        expected_dates = (
            "Sep 2024 to Present",
            "Sep 2023 to Sep 2024",
            "Nov 2020 to Apr 2023",
            "Jun 2019 to Nov 2020",
            "Feb 2017 to May 2019",
        )
        for date_range in expected_dates:
            self.assertIn(date_range, source)

        self.assertEqual(5, source.count('class="experience-role__summary"'))
        self.assertEqual(5, source.count('class="experience-role__skills"'))
        self.assertEqual(5, source.count('class="experience-role__body"'))
        self.assertEqual(5, source.count('class="experience-role__date"'))
        company_links = {
            anchor["text"]: anchor
            for anchor in document.anchors
            if "experience-role__company-link" in anchor["attrs"].get("class", "").split()
        }
        expected_company_links = {
            "Adobe": "https://www.adobe.com/",
            "Turo": "https://turo.com/",
            "HomeLight": "https://www.homelight.com/",
            "ViacomCBS": "https://www.paramount.com/",
            "Knowles Intelligent Audio": "https://www.knowles.com/",
        }
        self.assertEqual(expected_company_links, {
            company: anchor["href"] for company, anchor in company_links.items()
        })
        for anchor in company_links.values():
            self.assertEqual("_blank", anchor["attrs"].get("target"))
            self.assertIn("noopener", anchor["attrs"].get("rel", ""))
        self.assertNotIn("experience-role__accomplishments", source)
        self.assertNotIn("experience-role__previous", source)
        self.assertIn("Joined as a Data Science Intern before building production", source)
        for skill in ("Databricks", "Airflow", "Django", "Kubernetes", "MATLAB"):
            self.assertIn("<li>{}</li>".format(skill), source)
        self.assertFalse(any(url == "/assets/js/experience.js" for _, _, url in document.resources))

        redirect = self.parse_html(EXPERIENCE_REDIRECT)
        redirect_source = EXPERIENCE_REDIRECT.read_text(encoding="utf-8")
        redirect_links = {(anchor["text"], anchor["href"]) for anchor in redirect.anchors}
        self.assertIn(("main portfolio page", "/#experience"), redirect_links)
        self.assertIn("url=/#experience", redirect_source)

    def test_05_blog_and_youtube_are_not_in_primary_ui(self):
        for public_path, file_path in PRIMARY_PAGES.items():
            document = self.parse_html(file_path)
            for anchor in document.anchors:
                with self.subTest(page=public_path, link=anchor["href"]):
                    self.assertNotEqual("blog", anchor["text"].strip().lower())
                    self.assertNotEqual("/posts/", urlsplit(anchor["href"]).path)
            for tag, attribute, url in document.resources:
                normalized = url.lower()
                with self.subTest(page=public_path, resource=url):
                    self.assertNotIn("youtube.com", normalized)
                    self.assertNotIn("youtu.be", normalized)

    def test_06_historical_blog_urls_are_preserved_but_unpromoted(self):
        historical_posts = []
        for year in ("2018", "2020"):
            year_root = SITE / year
            if year_root.is_dir():
                historical_posts.extend(year_root.rglob("index.html"))
        self.assertEqual(8, len(historical_posts))
        self.assertTrue((SITE / "posts" / "index.html").is_file())

    def test_07_every_internal_link_and_resource_resolves(self):
        broken = []
        for html_path in SITE.rglob("*.html"):
            document = self.parse_html(html_path)
            for tag, attribute, url in document.resources:
                target, fragment = self.resolve_internal_url(html_path, url)
                if target is None:
                    continue
                if not target.exists():
                    broken.append("{}: {} {}={!r}".format(
                        html_path.relative_to(SITE), tag, attribute, url
                    ))
                    continue
                if fragment and target.suffix.lower() in (".html", ".htm"):
                    target_document = self.parse_html(target)
                    if fragment not in target_document.ids:
                        broken.append("{}: missing fragment #{} in {}".format(
                            html_path.relative_to(SITE), fragment, target.relative_to(SITE)
                        ))
        self.assertEqual([], broken, "Broken internal links or resources")

    def test_08_primary_pages_have_metadata_and_accessible_images(self):
        for public_path, file_path in PRIMARY_PAGES.items():
            document = self.parse_html(file_path)
            with self.subTest(page=public_path):
                self.assertEqual("en", document.html_lang)
                self.assertTrue(document.title)
                self.assertIn("Kevin Chuang", document.title)
                self.assertGreaterEqual(len(document.meta.get("description", "").strip()), 40)
                self.assertEqual(1, len(document.h1))
                self.assertEqual(len(document.ids), len(set(document.ids)), "Duplicate HTML ids")
                for image in document.images:
                    self.assertTrue(image.get("alt", "").strip(), "Every image needs alt text")

    def test_09_generated_markup_has_no_unresolved_liquid(self):
        unresolved = []
        for html_path in SITE.rglob("*.html"):
            source = html_path.read_text(encoding="utf-8")
            if "{{" in source or "{%" in source:
                unresolved.append(str(html_path.relative_to(SITE)))
        self.assertEqual([], unresolved)

    def test_10_feed_and_sitemap_are_well_formed_xml(self):
        for filename in ("feed.xml", "sitemap.xml"):
            with self.subTest(file=filename):
                tree = ElementTree.parse(str(SITE / filename))
                self.assertIsNotNone(tree.getroot())

    def test_11_development_files_are_not_published(self):
        forbidden_suffixes = (".aux", ".log", ".synctex.gz", ".tex", ".ttf")
        forbidden_names = {"Makefile", "README.md", "site_test.py", "liquid_ruby_compat.rb"}
        leaked = []
        for path in SITE.rglob("*"):
            if not path.is_file():
                continue
            name = path.name
            if name in forbidden_names or any(name.endswith(suffix) for suffix in forbidden_suffixes):
                leaked.append(str(path.relative_to(SITE)))
        self.assertEqual([], leaked, "Development/build files leaked into the published site")

    def test_12_compiled_portfolio_css_contains_responsive_rules(self):
        css = (SITE / "assets" / "css" / "main.css").read_text(encoding="utf-8")
        self.assertGreater(len(css), 20_000)
        self.assertIn(".portfolio-hero", css)
        self.assertIn("mountains_blue_ocean.jpg", css)
        self.assertIn("body.portfolio-background::before", css)
        self.assertIn("body.portfolio-background .header-link", css)
        self.assertIn("body.portfolio-projects-page .header-link", css)
        self.assertNotIn(".career-timeline", css)
        self.assertIn(".experience-role--current", css)
        self.assertIn("@media", css)

    def test_13_pages_workflow_tests_before_deployment(self):
        workflow_path = ROOT / ".github" / "workflows" / "pages.yml"
        self.assertTrue(workflow_path.is_file())
        workflow = workflow_path.read_text(encoding="utf-8")
        build_position = workflow.index("actions/jekyll-build-pages@v1")
        test_position = workflow.index("python3 test/site_test.py -v")
        upload_position = workflow.index("actions/upload-pages-artifact@v4")
        deploy_position = workflow.index("actions/deploy-pages@v4")
        self.assertLess(build_position, test_position)
        self.assertLess(test_position, upload_position)
        self.assertLess(upload_position, deploy_position)
        self.assertIn("needs: build", workflow)

    @staticmethod
    def resolve_internal_url(source_file, url):
        parsed = urlsplit(url.strip())
        if parsed.scheme.lower() in IGNORED_SCHEMES or parsed.netloc:
            return None, None

        path = unquote(parsed.path)
        fragment = unquote(parsed.fragment)
        if path.startswith("/"):
            candidate = SITE / path.lstrip("/")
        elif path:
            candidate = source_file.parent / path
        else:
            candidate = source_file

        candidate = Path(os.path.normpath(str(candidate)))
        try:
            candidate.relative_to(SITE)
        except ValueError:
            return candidate, fragment

        if candidate.is_dir():
            candidate = candidate / "index.html"
        elif not candidate.suffix:
            directory_index = candidate / "index.html"
            html_variant = candidate.with_suffix(".html")
            if directory_index.exists():
                candidate = directory_index
            elif html_variant.exists():
                candidate = html_variant
        return candidate, fragment


if __name__ == "__main__":
    unittest.main()
