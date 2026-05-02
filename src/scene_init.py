import flet as ft
from Pages import web_scenes as ws

def web_manager(page: ft.Page):
	page.fonts = {
		"JetBrains Mono" : "/fonts/JetBrainsMono[wght].ttf"
	}
  
	# Settings and such
	page.theme = ft.Theme(
		color_scheme_seed=ft.Colors.GREEN_ACCENT,
		font_family="JetBrains Mono",
		text_theme=ft.TextTheme(
			display_large=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
			display_medium=ft.TextStyle(size=24, color=ft.Colors.GREEN_200),
			display_small=ft.TextStyle(color=ft.Colors.WHITE),

			body_large=ft.TextStyle(color=ft.Colors.GREEN_ACCENT),
			body_medium=ft.TextStyle(color=ft.Colors.GREEN_400),
			body_small=ft.TextStyle(color=ft.Colors.WHITE),

			label_large=ft.TextStyle(color=ft.Colors.GREEN_200),
			label_medium=ft.TextStyle(color=ft.Colors.GREEN_300, size=18),
			label_small=ft.TextStyle(color=ft.Colors.GREEN_100, size=14),

			headline_large=ft.TextStyle(color=ft.Colors.WHITE),
			headline_medium=ft.TextStyle(color=ft.Colors.WHITE),
			headline_small=ft.TextStyle(color=ft.Colors.WHITE),

			title_large=ft.TextStyle(color=ft.Colors.GREEN_ACCENT_100, size=45),
			title_medium=ft.TextStyle(color=ft.Colors.GREEN_100, size=30),
			title_small=ft.TextStyle(color=ft.Colors.WHITE, size=18),
		),
		scrollbar_theme=ft.ScrollbarTheme(
			thickness={
				ft.ControlState.HOVERED : 15,
				ft.ControlState.SELECTED : 15,
				ft.ControlState.DEFAULT : 5
			},
			radius=5,
			thumb_color={
				ft.ControlState.HOVERED : ft.Colors.GREEN_ACCENT_200,
				ft.ControlState.DEFAULT : ft.Colors.GREEN_400
			},
			track_color={
				ft.ControlState.DEFAULT : ft.Colors.GREEN_400
			},
			track_border_color=ft.Colors.GREEN_50
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
			case "/signup":
				page.views.append(ws.signup())
			case "/lecture":
				page.views.append(ws.lecture())
			case "/discuss":
				page.views.append(ws.discuss())
			case "/library":
				page.views.append(ws.library())
			case "/creator":
				page.views.append(ws.creator())
			case _:
				page.views.append(ws.home())
		print(f""" =======================
routed to: "{page.route}" 
current views: {len(page.views)}
		""")
		
	# Cores 
	# page.route = "/login" #-> Login
	# page.route = "/signup" # -> Signup
	# page.route = "/library" # -> Where we can choose what lecture we like to study
	# page.route = "/lecture" # -> Where we can choose what topic we like to read
	# page.route = "/discuss" # -> Where we actually see and read content
	page.route = "/creator"
	page.on_route_change = change_route

	change_route()

if __name__ == "__main__":
	ft.run(main=web_manager)
