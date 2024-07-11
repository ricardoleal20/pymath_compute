"""
Index for my FrontEnd application
"""

import reflex as rx
# Import all the pages.
from docs.pages import index, documentation


# ========================================== #
#                    APP                     #
# ========================================== #


# Create the app.
app = rx.App(  # pylint: disable=E1102
    theme=rx.theme(
        appearance="dark",
        has_background=True
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap",
        "/styles.css"
    ],
    style={
        "font_family": "Montserrat, sans-serif",
        "font_size": "13px"
    }
)

# Add the pages
app.add_page(index, title="PyMath Compute", route="/")
app.add_page(documentation, title="PyMath :: Introduction", route="/docs")
