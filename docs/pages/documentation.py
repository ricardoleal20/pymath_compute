"""
Page for the documentation
"""
import reflex as rx
# Local imports


def documentation() -> rx.Component:
    """Page for the documentation of the package
    
    Returns:
        - The UI for the documentation page
    """
    return rx.box(
        rx.text("hola xd")
    )
