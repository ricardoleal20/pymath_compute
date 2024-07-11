"""
Include a navigation bar for the home page
"""
import reflex as rx
# Local imports
from docs.styles import border_spacer, text_could_hover, button_secondary_hover


def navbar():
    """Navigation Bar for the project"""
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.text(""),
                rx.hstack(
                    navbar_link("Docs", "/docs"),
                    justify="end",
                    spacing="5",
                    align="center"
                ),
                align_items="center",
                justify="between",
                padding_x="3em",
                padding_y="1em"
            )
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.text(""),
                rx.hstack(
                    navbar_link("Docs", "/docs"),
                    justify="end",
                    spacing="5",
                    align="center"
                ),
                # rx.menu.root(
                #     rx.menu.trigger(
                #         rx.icon("menu", size=30)
                #     ),
                #     rx.menu.content(
                #         navbar_menu_item_link("Docs", "/docs"),
                #     ),
                #     justify="end"
                # ),
                align_items="center",
                justify="between",
            ),
            padding_y="2em",
            padding_x="3em",
        ),
        border_bottom=border_spacer,
        position="sticky",
        top="0px",
        z_index="999",
        width="100%",
        background_color=rx.color_mode_cond(light="white", dark="#111113")
    )

# ======================================== #
#               NAVBAR LINK                #
# ======================================== #


def navbar_link(
    text: str,
    id_scroll: str
):
    """Include a link for the Navigation Bar"""
    return rx.link(
        rx.text(
            text,
            style=text_could_hover
        ),
        text_decoration="none",
        color=rx.color_mode_cond(light="black", dark="white"),
        on_click=rx.redirect(id_scroll),
    )
