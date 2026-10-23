from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

PAGES = {
    "/": {
        "title": "CBK Pension Towers",
        "heading": "CBK Pension Towers",
        "content": """
            <p>An independent information page about CBK and Pension Towers.
            This site is not operated by or affiliated with the Central Bank
            of Kenya.</p>
            <p>For verified CBK information and current contact details, use
            the <a href="https://www.centralbank.go.ke/">official CBK website</a>.</p>
        """,
    },
    "/about": {
        "title": "About",
        "heading": "About the property",
        "content": """
            <h2>About the Central Bank of Kenya</h2>
            <p>The Central Bank of Kenya (CBK) is Kenya's central bank. Its
            principal objective is to formulate and implement monetary policy
            directed at achieving and maintaining price stability, supporting
            the stability of the Kenya shilling.</p>
            <p>CBK describes monetary policy and its objectives on its
            <a href="https://www.centralbank.go.ke/monetary-policy/">official
            Monetary Policy page</a>.</p>
            <h2>About Pension Towers</h2>
            <p>Building-specific details, services, and visitor arrangements
            have not been verified for this sample. Confirm these with CBK
            before relying on or publishing them.</p>
        """,
    },
    "/facilities": {
        "title": "Facilities",
        "heading": "Facilities and services",
        "content": """
            <p>No Pension Towers-specific facilities or visitor services are
            listed here because they have not been confirmed by an official
            source. Contact CBK to verify current arrangements.</p>
        """,
    },
    "/contact": {
        "title": "Contact",
        "heading": "Contact and visitor information",
        "content": """
            <h2>Central Bank of Kenya — head-office contacts</h2>
            <address>
                Haile Selassie Avenue<br>
                P.O. Box 60000–00200<br>
                Nairobi, Kenya
            </address>
            <p>Telephone:
            <a href="tel:+254202860000">+254 20 286 0000</a>,
            <a href="tel:+254202861000">+254 20 286 1000</a>,
            <a href="tel:+254202863000">+254 20 286 3000</a><br>
            Mobile:
            <a href="tel:+254709081000">+254 709 081 000</a>,
            <a href="tel:+254709083000">+254 709 083 000</a></p>
            <p>These are CBK head-office contacts, not a separately verified
            Pension Towers reception number. For current details, see CBK's
            <a href="https://www.centralbank.go.ke/contact-us/">official
            Contact Us page</a>. Confirm building access and visitor
            arrangements directly with CBK.</p>
        """,
    },
}


def make_page(title: str, content: str) -> bytes:
    links = "".join(
        f'<a href="{path}">{page["title"]}</a>'
        for path, page in PAGES.items()
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | CBK Pension Towers</title>
  <style>
    :root {{ color-scheme: light; font-family: Arial, sans-serif; }}
    body {{ margin: 0; color: #1f2937; background: #f3f6f8; line-height: 1.6; }}
    header {{ padding: 1rem max(1rem, calc((100% - 960px) / 2)); background: #123b5d; color: white; }}
    nav {{ display: flex; flex-wrap: wrap; gap: 1rem; margin-top: .5rem; }}
    nav a {{ color: white; }}
    main {{ box-sizing: border-box; max-width: 960px; margin: 2rem auto; padding: 2rem; background: white; border-radius: 10px; }}
    footer {{ max-width: 960px; margin: 1rem auto; padding: 1rem; color: #4b5563; font-size: .9rem; }}
  </style>
</head>
<body>
  <header>
    <strong>CBK Pension Towers</strong>
    <nav>{links}</nav>
  </header>
  <main>
    <h1>{title}</h1>
    {content}
  </main>
  <footer>
    Unofficial sample website. Confirm all information with an authoritative
    source before publishing.
  </footer>
</body>
</html>"""
    return html.encode("utf-8")


class WebsiteHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlparse(self.path).path
        page = PAGES.get(path)

        if page is None:
            body = make_page(
                "Page not found",
                "<p>That page does not exist. Use the navigation to continue.</p>",
            )
            self.send_response(404)
        else:
            body = make_page(page["heading"], page["content"])
            self.send_response(200)

        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), WebsiteHandler)
    print("Open http://127.0.0.1:8000 in your browser. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
