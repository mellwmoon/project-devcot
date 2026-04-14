import flet as ft
from Pages import web_scenes as ws

def web_manager(page: ft.Page):
    page.fonts = {
        "JetBrains Mono" : "/fonts/JetBrainsMono[wght].ttf"
    }

    # Settings and such
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.GREEN_ACCENT,
        text_theme=ft.TextTheme(
            display_large=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
            display_medium=ft.TextStyle(size=24, color=ft.Colors.GREEN_200),
            display_small=ft.TextStyle(color=ft.Colors.WHITE),

            body_large=ft.TextStyle(color=ft.Colors.GREEN_ACCENT),
            body_medium=ft.TextStyle(color=ft.Colors.GREEN_400),
            body_small=ft.TextStyle(color=ft.Colors.WHITE),

            label_large=ft.TextStyle(color=ft.Colors.WHITE),
            label_medium=ft.TextStyle(color=ft.Colors.WHITE),
            label_small=ft.TextStyle(color=ft.Colors.WHITE),

            headline_large=ft.TextStyle(color=ft.Colors.WHITE),
            headline_medium=ft.TextStyle(color=ft.Colors.WHITE),
            headline_small=ft.TextStyle(color=ft.Colors.WHITE),

            title_large=ft.TextStyle(color=ft.Colors.GREEN_300),
            title_medium=ft.TextStyle(color=ft.Colors.GREEN_100),
            title_small=ft.TextStyle(color=ft.Colors.WHITE),
        )
    )
    

    page.theme_mode = ft.ThemeMode.DARK

    # Scenes Manager
    def change_route():
        page.views.clear()
        match page.route:
            case "/":
                page.views.append(ws.home())
            case "/login":
                page.views.append(ws.login())
            case _:
                page.views.append(ws.home())
        print(f""" =======================
routed to: "{page.route}" 
current views: {len(page.views)}
        """)
        
    # page.route = "/login"
    page.on_route_change = change_route

    change_route()

if __name__ == "__main__":
    ft.run(main=web_manager)