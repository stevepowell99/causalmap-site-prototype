from pathlib import Path

from livereload import Server

from build import build

# Project root and built output folder.
ROOT = Path(__file__).parent
DIST_DIR = ROOT / "dist"


def rebuild():
    # Rebuild the static site after any source change.
    print("\nRebuilding...")
    build()


if __name__ == "__main__":
    # Build once on startup so the preview always has fresh files.
    rebuild()

    server = Server()

    # Watch all content plus the generator and config.
    server.watch(str(ROOT / "content"), rebuild)
    server.watch(str(ROOT / "build.py"), rebuild)
    server.watch(str(ROOT / "config.yml"), rebuild)

    # Serve the generated site locally with live reload in the browser.
    server.serve(root=str(DIST_DIR), host="127.0.0.1", port=5500, open_url_delay=1)
