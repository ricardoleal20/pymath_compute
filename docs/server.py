"""
Modify a path dynamically and serve it in a HTTP server
"""
# Import for reading files and receive args
import os
from argparse import ArgumentParser
# Import for the HTTP Server
import http.server
import socketserver


def replace_path_in_files(
    directory: str,
    path_var: str,
    path: str
) -> dict[str, str]:
    """Replace the PATH variable in the HTML files"""
    og_files: dict[str, str] = {}
    # Iterate over all the files inside the directory
    for filename in os.listdir(directory):
        if os.path.isdir(directory+f"/{filename}"):
            og_files.update(
                replace_path_in_files(directory+f"/{filename}", path_var, path)
            )
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                filedata = file.read()
            # Store this file as it is original
            og_files[filepath] = filedata
            # Replace all coincidences with the new text
            filedata = filedata.replace(path_var, path)
            # Write the files once again
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(filedata)
    return og_files


def restart_files(og_files: dict[str, str]) -> None:
    """Reset the files that suffer a replace in the path"""
    for filepath, filedata in og_files.items():
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(filedata)


def serve_html() -> None:
    """Create an HTTP server for the files"""
    port = 8080
    # Create the HTTP Request Handler
    handler = http.server.SimpleHTTPRequestHandler
    # And serve it
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving HTTP connection in port {port}")
        httpd.serve_forever()


def main() -> None:
    """Read the PATH variable and decide the text to replace"""
    parser = ArgumentParser(
        prog="Portfolio",
        description="Pass files to know what to do inside the server logic"
    )
    parser.add_argument("-d", "--dev", type=bool)
    args = parser.parse_args()
    # Obtain the path to set
    path = "/docs" if args.dev else "https://ricardoleal20.github.io/pymath_compute/"
    # Get the directory of where you're going to serve the files
    directory = "./docs"
    # Decide the old variable to replace
    old_text = "{PATH}"
    # Replace everything
    og_info = replace_path_in_files(directory, old_text, path)
    if args.dev is True:
        try:
            serve_html()
        except KeyboardInterrupt:
            print("Stopping the HTML server...")
            restart_files(og_info)


if __name__ == "__main__":
    main()
