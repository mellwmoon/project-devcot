import flet as ft
import asyncio

class SysAppBar(ft.AppBar):
    def __init__(self, page: ft.Page, topic_selected: str = "", is_appbar_only: bool = False):

        self.extramenu = [
            ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Row(
                        spacing=20,
                        controls=[
                            ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
                            ft.Text(
                                value="Account Settings",
                                font_family="JetBrains Mono",
                                theme_style=ft.TextThemeStyle.LABEL_SMALL
                            )
                        ]
                    ),
                    width=170
                )
            ),
            ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Row(
                        spacing=20,
                        controls=[
                            ft.Icon(ft.Icons.SETTINGS),
                            ft.Text(
                                value="General Settings",
                                font_family="JetBrains Mono",
                                theme_style=ft.TextThemeStyle.LABEL_SMALL,
                            )
                        ]
                    ),
                    width=200,
                    opacity=0.4,
                ),
                disabled=True
            ),
            ft.PopupMenuItem(content=ft.Divider(), height=1, disabled=True),
            ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Row(
                        spacing=20,
                        controls=[
                            ft.Icon(ft.Icons.BOOK),
                            ft.Text(
                                value="References",
                                font_family="JetBrains Mono",
                                theme_style=ft.TextThemeStyle.LABEL_SMALL,
                            )
                        ]
                    ),
                    width=200,
                    opacity=0.4,
                ),
                disabled=True
            ),
            ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Row(
                        spacing=20,
                        controls=[
                            ft.Icon(ft.Icons.QUIZ),
                            ft.Text(
                                value="Excercises",
                                font_family="JetBrains Mono",
                                theme_style=ft.TextThemeStyle.LABEL_SMALL,
                            )
                        ]
                    ),
                    width=200,
                    opacity=0.4,
                ),
                disabled=True
            ),
            ft.PopupMenuItem(content=ft.Divider(), height=1, disabled=True),
            ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Row(
                        spacing=20,
                        controls=[
                            ft.Icon(ft.Icons.QUESTION_ANSWER),
                            ft.Text(
                                value="Help & Support",
                                font_family="JetBrains Mono",
                                theme_style=ft.TextThemeStyle.LABEL_SMALL,
                            )
                        ]
                    ),
                    width=170,
                    opacity=0.4,
                ),
                disabled=True
            ),
            ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Row(
                        spacing=20,
                        controls=[
                            ft.Icon(ft.Icons.PERSON),
                            ft.Text(
                                value="About us",
                                font_family="JetBrains Mono",
                                theme_style=ft.TextThemeStyle.LABEL_SMALL,
                            )
                        ]
                    ),
                    width=170,
                    opacity=0.4,
                ),
                disabled=True
            ),
        ]
        page.update()
        

        title_text = f"> DevCot: {topic_selected}" if not is_appbar_only else "> DevCot"
        
        super().__init__(
            title=ft.Text(
                value=title_text,
                font_family="JetBrains Mono",
                theme_style=ft.TextThemeStyle.TITLE_MEDIUM
            ),
            leading_width=20,
            elevation=0,
            elevation_on_scroll=0,
            bgcolor=ft.Colors.BLACK_45,
            color=ft.Colors.GREEN_300,
            actions=[
                item_menus:=ft.PopupMenuButton(
                    margin=ft.Margin.only(right=20),
                    menu_padding=8,
                    menu_position=ft.PopupMenuPosition.UNDER,
                    items=self.extramenu
                )
            ]
        )
        self.item_menus = item_menus
        page.run_task(self._spot_instructor)

    async def _spot_instructor(self) -> bool:
      r = await self.page.shared_preferences.get("current_user_type") == "instructor"
      print(r)
      await asyncio.sleep(0.1)
      if not r: return
      
      self.item_menus.items.append(ft.PopupMenuItem(content=ft.Divider(), height=1, disabled=True),)
      self.item_menus.items.append(
          ft.PopupMenuItem(
          content=ft.Container(
              content=ft.Row(
                  spacing=20,
                  controls=[
                      ft.Icon(ft.Icons.HANDYMAN),
                      ft.Text(
                          value="Create a Lesson",
                          font_family="JetBrains Mono",
                          theme_style=ft.TextThemeStyle.LABEL_SMALL,
                      )
                  ]
              ),
              width=170,
              on_click=self.push_creator
          ),
        ),
      )
      self.item_menus.items.append(
          ft.PopupMenuItem(
          content=ft.Container(
              content=ft.Row(
                  spacing=20,
                  controls=[
                      ft.Icon(ft.Icons.EDIT_SQUARE),
                      ft.Text(
                          value="Go to Library",
                          font_family="JetBrains Mono",
                          theme_style=ft.TextThemeStyle.LABEL_SMALL,
                      )
                  ]
              ),
              width=170,
              on_click=self.push_library
          ),
        ),
      )
      self.update()
    
    async def push_creator(self, e):

      if self.page.route == "/creator":
        self.page.show_dialog(ft.SnackBar(ft.Text("You are Already there!", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        return
      elif self.page.route == "/lecture" or self.page.route == "/discussion":
        self.page.show_dialog(ft.SnackBar(ft.Text("Exit out of Lecture first.", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        return

      await self.page.push_route("/creator")

    async def push_library(self, e):

      if self.page.route == "/library":
        self.page.show_dialog(ft.SnackBar(ft.Text("You are Already there!", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        return
      elif self.page.route == "/lecture" or self.page.route == "/discussion":
        self.page.show_dialog(ft.SnackBar(ft.Text("Exit out of Lecture first.", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        return


      await self.page.push_route("/library")