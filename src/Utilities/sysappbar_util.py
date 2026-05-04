import flet as ft
import asyncio
import datetime
from Utilities import database_util as dubil

class SysAppBar(ft.AppBar):
    def __init__(self, page:ft.Page, topic_selected: str = "", is_appbar_only: bool = False, db:dubil.DatabaseManager=None):
        self.db = db
        self.current_user_data = None

        # ---------------------------------------------------
        # SETTINGS DIALOG UI SETUP
        # ---------------------------------------------------
        self.settings_date_picker = ft.DatePicker(
            on_change=self.handle_date_change,
            first_date=datetime.datetime(1950, 1, 1),
            last_date=datetime.datetime(2026, 12, 31),
        )

        self.settings_content_area = ft.Container(expand=True)

        self.sidebar_buttons = [
            ft.TextButton("Account Info", data="account", on_click=self.handle_sidebar_click, style=self.get_sidebar_style(True)),
            ft.TextButton("Details & Scores", data="scores", on_click=self.handle_sidebar_click, style=self.get_sidebar_style(False)),
            ft.TextButton("Topics", data="topics", on_click=self.handle_sidebar_click, style=self.get_sidebar_style(False)),
        ]

        self.settings_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("User Settings", font_family="JetBrains Mono"),
            content_padding=0,
            content=ft.Container(
                width=700,
                height=350,
                padding=ft.padding.only(left=20, top=20, right=20, bottom=10),
                content=ft.Row(
                    expand=True,
                    spacing=20,
                    controls=[
                        ft.Column(
                            width=160,
                            controls=self.sidebar_buttons
                        ),
                        ft.VerticalDivider(width=1, color=ft.Colors.WHITE24),
                        self.settings_content_area
                    ]
                )
            ),
        )

        # The Delete Account Confirmation Dialog
        self.delete_confirm_dialog = ft.AlertDialog(
            modal=True,
            
            title=ft.Text("Delete Account?", font_family="JetBrains Mono", color=ft.Colors.RED_400, text_align=ft.TextAlign.CENTER),
            content=ft.Text("Are you absolutely sure \nyou want to delete your account?\n\nThis action cannot be undone.", font_family="JetBrains Mono", size=14, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
            actions=[
                ft.FilledButton("Yes, Delete Everything", style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700), on_click=self.execute_delete_account, color=ft.Colors.WHITE),
                ft.FilledButton("No, It was a missclick", on_click=self.close_delete_confirm),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # ---------------------------------------------------
        # ORIGINAL APPBAR SETUP
        # ---------------------------------------------------
        self.extramenu = [
            ft.PopupMenuItem(
                on_click=self.open_settings_dialog,
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
                            ft.Text("General Settings", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_SMALL)
                        ]
                    ),
                    width=200, opacity=0.4,
                ), disabled=True
            ),
            ft.PopupMenuItem(content=ft.Divider(), height=1, disabled=True),
            ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Row(
                        spacing=20,
                        controls=[
                            ft.Icon(ft.Icons.BOOK),
                            ft.Text("References", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_SMALL)
                        ]
                    ),
                    width=200, opacity=0.4,
                ), disabled=True
            ),
            ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Row(
                        spacing=20,
                        controls=[
                            ft.Icon(ft.Icons.QUIZ),
                            ft.Text("Excercises", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_SMALL)
                        ]
                    ),
                    width=200, opacity=0.4,
                ), disabled=True
            ),
            ft.PopupMenuItem(content=ft.Divider(), height=1, disabled=True),
            ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Row(
                        spacing=20,
                        controls=[
                            ft.Icon(ft.Icons.QUESTION_ANSWER),
                            ft.Text("Help & Support", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_SMALL)
                        ]
                    ),
                    width=170, opacity=0.4,
                ), disabled=True
            ),
            ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Row(
                        spacing=20,
                        controls=[
                            ft.Icon(ft.Icons.PERSON),
                            ft.Text("About us", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_SMALL)
                        ]
                    ),
                    width=170, opacity=0.4,
                ), disabled=True
            ),
            ft.PopupMenuItem(content=ft.Divider(), height=1),
            ft.PopupMenuItem(
                on_click=self.handle_sign_out,
                content=ft.Container(
                    content=ft.Row(
                        spacing=20,
                        controls=[
                            ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED_400),
                            ft.Text("Sign Out", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_SMALL, color=ft.Colors.RED_400)
                        ]
                    ),
                    width=170
                )
            ),
        ]
        
        page.update()
        title_text = f"> DevCot: {topic_selected}" if not is_appbar_only else "> DevCot"
        
        super().__init__(
            title=ft.Text(value=title_text, font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
            leading_width=20, elevation=0, elevation_on_scroll=0,
            bgcolor=ft.Colors.BLACK_45, color=ft.Colors.GREEN_300,
            actions=[
                item_menus:=ft.PopupMenuButton(
                    margin=ft.Margin.only(right=20), menu_padding=8,
                    menu_position=ft.PopupMenuPosition.UNDER, items=self.extramenu
                )
            ]
        )
        self.item_menus = item_menus
        page.run_task(self._spot_instructor)

    # ---------------------------------------------------
    # INSTRUCTOR LOGIC
    # ---------------------------------------------------
    async def _spot_instructor(self) -> bool:
      r = await self.page.shared_preferences.get("current_user_type") == "instructor"
      await asyncio.sleep(0.1)
      if not r: return
      
      self.item_menus.items.append(ft.PopupMenuItem(content=ft.Divider(), height=1, disabled=True),)
      self.item_menus.items.append(
          ft.PopupMenuItem(content=ft.Container(content=ft.Row(spacing=20, controls=[ft.Icon(ft.Icons.HANDYMAN), ft.Text("Create a Lesson", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_SMALL)]), width=170, on_click=self.push_creator))
      )
      self.item_menus.items.append(
          ft.PopupMenuItem(content=ft.Container(content=ft.Row(spacing=20, controls=[ft.Icon(ft.Icons.EDIT_SQUARE), ft.Text("Go to Library", font_family="JetBrains Mono", theme_style=ft.TextThemeStyle.LABEL_SMALL)]), width=170, on_click=self.push_library))
      )
      self.update()
    
    async def push_creator(self, e):
      if self.page.route == "/creator":
        self.page.show_dialog(ft.SnackBar(ft.Text("You are Already there!", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        return
      elif self.page.route in ["/lecture", "/discussion"]:
        self.page.show_dialog(ft.SnackBar(ft.Text("Exit out of Lecture first.", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        return
      await self.page.push_route("/creator")

    async def push_library(self, e):
      if self.page.route == "/library":
        self.page.show_dialog(ft.SnackBar(ft.Text("You are Already there!", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        return
      elif self.page.route in ["/lecture", "/discussion"]:
        self.page.show_dialog(ft.SnackBar(ft.Text("Exit out of Lecture first.", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        return
      await self.page.push_route("/library")

    # ---------------------------------------------------
    # DIALOG HANDLERS & ROUTING
    # ---------------------------------------------------
    async def handle_sign_out(self, e):
        await asyncio.sleep(0.5)

        if len(self.page.session.store.get_keys()) > 0:
            self.page.session.store.clear()
        if self.page.shared_preferences is not None:
            await self.page.shared_preferences.clear()
        
        await asyncio.sleep(0.5)


        await self.page.push_route("/login")

        self.page.show_dialog(ft.SnackBar(ft.Text("Logged Out", color=ft.Colors.WHITE), bgcolor=ft.Colors.BLACK_26))
        self.update()

    async def open_settings_dialog(self, e):
        await self.load_account_view()
        self.page.show_dialog(self.settings_dialog)
        self.page.update()

    async def close_settings_dialog(self, e):
        self.settings_dialog.open = False
        self.page.update()

    async def open_delete_confirm(self, e):
        self.page.show_dialog(self.delete_confirm_dialog)
        self.page.update()

    async def close_delete_confirm(self, e):
        self.delete_confirm_dialog.open = False
        self.page.update()

    async def execute_delete_account(self, e):
        if not self.current_user_data or not self.db:
            return
        
        self.delete_confirm_dialog.open = False
        self.settings_dialog.open = False

        self.page.pop_dialog()
        self.page.pop_dialog()
            
        u_id = self.current_user_data[0]
        
        self.db.connect()
        self.db.delete_user(u_id)
        self.db.close()
        
        
        if len(self.page.session.store.get_keys()) > 0:
            self.page.session.store.clear()
        if self.page.shared_preferences is not None:
            await self.page.shared_preferences.clear()
        
        await asyncio.sleep(0.5)

        self.page.show_dialog(ft.SnackBar(ft.Text("Account deleted forever.", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_800))
        await self.page.push_route("/")
        self.page.update()

    def get_sidebar_style(self, is_selected: bool):
        return ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
            color=ft.Colors.GREEN_300 if is_selected else ft.Colors.WHITE54,
            bgcolor=ft.Colors.WHITE10 if is_selected else ft.Colors.TRANSPARENT,
            padding=ft.Padding.symmetric(horizontal=15, vertical=15),
            alignment=ft.Alignment.CENTER_LEFT
        )

    async def handle_sidebar_click(self, e):
        for btn in self.sidebar_buttons:
            btn.style = self.get_sidebar_style(btn.data == e.control.data)
        
        if e.control.data == "account":
            await self.load_account_view() 
        elif e.control.data == "scores":
            self.load_placeholder_view("Details & Scores", "Score history will appear here.")
        elif e.control.data == "topics":
            self.load_placeholder_view("Topics", "Topic preferences will appear here.")
            
        self.page.update()

    # ---------------------------------------------------
    # VIEW LOADERS (The Right Side Content)
    # ---------------------------------------------------
    def load_placeholder_view(self, title, description):
        self.settings_content_area.content = ft.Column(
            expand=True,
            controls=[
                ft.Text(title, theme_style=ft.TextThemeStyle.TITLE_SMALL, font_family="JetBrains Mono", color=ft.Colors.GREEN_300),
                ft.Divider(color=ft.Colors.WHITE24),
                ft.Text(description, font_family="JetBrains Mono", color=ft.Colors.WHITE54)
            ]
        )

    async def load_account_view(self):
        """Fetches data from DB and builds the Account Information form."""
        if not self.db:
            print("DB not provided to SysAppBar!")
            return

        current_identifier = await self.page.shared_preferences.get("current_user")
        
        self.db.connect()
        self.current_user_data = self.db.get_user_info(username=current_identifier)
        self.db.close()

        if not self.current_user_data:
            print("Failed to find user in DB.")
            return

        user_id, username, birthdate, email, email_univ, acc_type = self.current_user_data
        name_parts = username.split(" ", 1)
        f_name = name_parts[0]
        l_name = name_parts[1] if len(name_parts) > 1 else ""
        
        self.field_fname = ft.TextField(label="First Name", value=f_name, expand=True, text_style=ft.TextStyle(font_family="JetBrains Mono", size=14), border_color=ft.Colors.WHITE24)
        self.field_lname = ft.TextField(label="Last Name", value=l_name, expand=True, text_style=ft.TextStyle(font_family="JetBrains Mono", size=14), border_color=ft.Colors.WHITE24)
        
        self.field_email = ft.TextField(expand=True, label="Personal Email", value=email, read_only=True, text_style=ft.TextStyle(font_family="JetBrains Mono", size=14, color=ft.Colors.WHITE54), border_color=ft.Colors.WHITE24)
        self.field_univ_email = ft.TextField(expand=True, label="University Email", value=email_univ if email_univ else "N/A", read_only=True, text_style=ft.TextStyle(font_family="JetBrains Mono", size=14, color=ft.Colors.WHITE54), border_color=ft.Colors.WHITE24)

        self.field_pass = ft.TextField(expand=True, label="New Password (Leave blank to keep)", password=True, can_reveal_password=True, text_style=ft.TextStyle(font_family="JetBrains Mono", size=14), border_color=ft.Colors.WHITE24)
        self.field_bdate = ft.TextField(
            expand=True,
            label="Birthdate", 
            value=birthdate,
            read_only=True, 
            on_click=lambda _: self.page.show_dialog(self.settings_date_picker),
            text_style=ft.TextStyle(font_family="JetBrains Mono", size=14),
            border_color=ft.Colors.WHITE24
        )


        self.settings_content_area.content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            controls=[
                ft.Text("Personal Information", theme_style=ft.TextThemeStyle.TITLE_SMALL, font_family="JetBrains Mono", color=ft.Colors.GREEN_300),
                ft.Divider(color=ft.Colors.WHITE24),
                
                ft.Row([self.field_fname, self.field_lname]),
                self.field_email,
                self.field_univ_email,
                self.field_bdate,
                
                ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
                ft.Text("Security", theme_style=ft.TextThemeStyle.TITLE_SMALL, font_family="JetBrains Mono", color=ft.Colors.GREEN_300),
                ft.Divider(color=ft.Colors.WHITE24),
                self.field_pass,
                
                ft.Container(expand=True, margin=0, padding=0),

                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.OutlinedButton("Delete Account", icon=ft.Icons.WARNING_ROUNDED, icon_color=ft.Colors.RED_400, style=ft.ButtonStyle(color=ft.Colors.RED_400), on_click=self.open_delete_confirm),
                        ft.Row(
                            controls=[
                                ft.TextButton("Discard", on_click=self.close_settings_dialog),
                                ft.FilledButton("Save Changes", on_click=self.save_account_changes, style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_400))
                            ]
                        )
                    ]
                )

            ]
        )

    # ---------------------------------------------------
    # DATA HANDLING
    # ---------------------------------------------------
    def handle_date_change(self, e):
        if self.settings_date_picker.value:
            self.field_bdate.value = self.settings_date_picker.value.astimezone().strftime("%B %d, %Y")
            self.page.update()

    async def save_account_changes(self, e):
        if not self.current_user_data or not self.db:
            return
        
        u_id = self.current_user_data[0]
        new_username = f"{self.field_fname.value} {self.field_lname.value}".strip()
        new_bdate = self.field_bdate.value
        new_password = self.field_pass.value


        self.db.connect()
        self.db.update_username(u_id, new_username)
        self.db.update_birthdate(u_id, new_bdate)
        
        if new_password:
            self.db.update_password(u_id, new_password)
            
        self.db.close()

        await self.page.shared_preferences.set("current_user", new_username)

        self.page.show_dialog(ft.SnackBar(ft.Text("Settings saved successfully!", color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN_800))
        await self.close_settings_dialog(e)