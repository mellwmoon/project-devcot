import flet as ft
from Pages import web_scenes as ws

def web_manager(page: ft.Page):
    page.fonts = {
        "JetBrains Mono" : "/Assets/JetBrainsMono[wght].ttf"
    }

    # Settings and such
    ## No variables yet

    # Scenes Manager
    def change_route():
        page.views.clear()
        match page.route:
            case "/":
                page.views.append(ws.home())
            case "/page2":
                page.views.append(ws.p2())
            case _:
                page.views.append(ws.home())
        print(f""" =======================
routed to: "{page.route}" 
current views: {len(page.views)}
        """)
        
    page.on_route_change = change_route

    change_route()

if __name__ == "__main__":
    ft.run(main=web_manager)