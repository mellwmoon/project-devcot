import flet as ft

class LayoutBox(ft.Container):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create_invisible_container(cls) -> "LayoutBox":
        """
        Creates an invisible placeholder container that expands 
        to fill available flex space.
        """
        return cls(expand=True)

    @classmethod
    def create_bordered_container(cls, inner_content: ft.Control = None, **kwargs) -> "LayoutBox":
        """
        Creates a standard white-bordered testing box.
        """
        return cls(
            border=ft.Border.all(1, ft.Colors.WHITE),
            border_radius=2,
            content=inner_content,
            expand=kwargs.pop("expand", False),
            **kwargs
        )