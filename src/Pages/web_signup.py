import flet as ft
import datetime
from Utilities import effect_util as efutil


class Signup(ft.View):

  INPUT_CONTAINER_WIDTH = 500
  INPUT_ROUNDED_BORDER_RAD = 5

  def __init__(self):
       
    
    m_anim_title = efutil.Fun("> Sign_up", theme_styling=ft.TextThemeStyle.TITLE_MEDIUM)

    def date_changed(e) -> None:
        field_date.value = e.control.value.astimezone().strftime("%B %d, %Y")

    input_date = ft.DatePicker(
        on_change=date_changed,
        first_date=datetime.datetime(1950, 1, 1),
        last_date=datetime.datetime(2023, 12, 31),
    )

    field_date = self.create_field(
      "Birthdate",
      on_click=lambda _:self.page.show_dialog(input_date),
      is_readonly=True
    )

    input_fields_container = ft.Container(
        width=self.INPUT_CONTAINER_WIDTH,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    margin=10,
                    controls=[
                        ft.Divider(),
                        ft.Text(
                          "First Name", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        self.create_field("Username"),
                        ft.Text(
                          "Last Name", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        self.create_field("Username"),
                        ft.Text(
                          "Birthday", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        field_date, # This is the only exception lol
                        ft.Divider(),
                        ft.Text(
                          "Phone Number", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        self.create_field("+63", is_numerical=True),
                        ft.Text(
                          "Email", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        self.create_field("Email"),
                        ft.Text(
                          "University Email (Optional)", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        self.create_field("reichard@univeristy.org"),
                        ft.Text(
                          "Password ", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        self.create_field("Password", True),
                    ]
                )
            ]
        )
    )

    button_submit = ft.FilledButton(
       height=40,
       width=200,
        content=ft.Text(
            value="Continue ->",
            font_family="JetBrains Mono",
            weight=ft.FontWeight.W_800
        )
    )

    button_back_login = ft.FilledButton(
      height=40,
        content=ft.Text(
            value="Back to login",
            font_family="JetBrains Mono",
            weight=ft.FontWeight.W_800
        ),
      color=ft.Colors.GREEN_900,
      bgcolor=ft.Colors.GREEN_300,
      on_click=self.push_login
    )

    main_layout = ft.Column(
      margin=10,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        m_anim_title,
        ft.Container(
          alignment=ft.Alignment.CENTER,
          height=500,
          width=500,
          margin=15,
          border=ft.Border.all(2, ft.Colors.WHITE_38),
          border_radius=5,
          padding=10,
          content=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=ft.Container(
              content=input_fields_container,
              padding=ft.Padding.only(right=12)
            )
          )
        ),
        ft.Row(
          spacing=40,
          alignment=ft.MainAxisAlignment.CENTER,
          vertical_alignment=ft.CrossAxisAlignment.CENTER,
          controls=[
            button_back_login,
            button_submit,
          ]
        )
      ],
    )

    super().__init__(
      route="/signup",
      vertical_alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        main_layout
      ]
    )

  async def push_login(self, e):
    await self.page.push_route("/login")

  def create_field(self, hint_text, is_password=False, is_numerical=False, on_click=None, label=None, is_readonly=False) -> ft.TextField:
      return ft.TextField(
          read_only=is_readonly,
          value=label if label!=None else None,
          on_click=on_click,
          input_filter=ft.NumbersOnlyInputFilter() if is_numerical else None,
          password=is_password,
          autofill_hints=True,
          can_reveal_password=True,
          multiline=False,
          expand=True,
          hint_text=hint_text,
          border=ft.RoundedRectangleBorder(radius=self.INPUT_ROUNDED_BORDER_RAD),
          content_padding=0,
          border_color=ft.Colors.WHITE,
          height=50,
          text_vertical_align=ft.VerticalAlignment.CENTER,
          hint_style=ft.TextStyle(
                  color="#363636",
                  font_family="JetBrains Mono",
                  size=14,
          ),
          text_style=ft.TextStyle(
                  color="#FFFFFF",
                  font_family="JetBrains Mono",
                  size=14,
          ),
      )
