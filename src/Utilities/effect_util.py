import flet as ft
import asyncio

# Gen #1 : Just a blinking caret.
class Fun(ft.Row):
    def __init__(self, text_value, text_size=30, text_font="JetBrains Mono", caret_type="_", is_caret_colored=False, theme_styling=ft.TextThemeStyle.TITLE_LARGE):
        super().__init__()
        self.tight = True
        self.spacing = 0
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        
        self.main_text = ft.Text(
            value=text_value,
            size=text_size,
            font_family=text_font,
            weight=ft.FontWeight.W_500,
            theme_style=theme_styling
        )
        
        self.caret = ft.Text(
            value=caret_type, 
            size=text_size,
            font_family=text_font,
            animate_opacity=100,
            theme_style=theme_styling if is_caret_colored else ft.TextThemeStyle.TITLE_SMALL
        )
        
        self.controls = [self.main_text, self.caret]

    def did_mount(self):
        self.page.run_task(self.animate_caret)

    async def animate_caret(self):
        while True:
            self.caret.opacity = 0 if self.caret.opacity == 1 else 1
            try:
                self.update()
            except Exception:
                break
            await asyncio.sleep(0.5)