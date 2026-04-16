import flet as ft
import datetime
from Utilities import effect_util as efutil
from Utilities import database_util as dabil


class Signup(ft.View):

  INPUT_CONTAINER_WIDTH = 500
  INPUT_ROUNDED_BORDER_RAD = 5

  def __init__(self):
    
    
    m_anim_title = efutil.Fun("> Sign_up basic_info", theme_styling=ft.TextThemeStyle.TITLE_MEDIUM)

    def date_changed(e) -> None:
        field_date.value = e.control.value.astimezone().strftime("%B %d, %Y")

    def _update_fields(e) -> None:
      is_complete = False
      inc = 0
      switch_label = []
      switch = [1, 1, 1, 1, 1, 1]

      for f in fields:
        cur_field : ft.TextField = f
        if (cur_field.value == None):
          cur_field.border_color=ft.Colors.RED
          labels[f].color = ft.Colors.RED

          switch_label.append(cur_field.hint_text)
          is_complete = False
          switch[inc] = 0
        
        inc += 1

      if (is_complete):
        pass # Code for next panel here
      else:
        self.page.show_dialog(
          ft.AlertDialog(
              title=ft.Text(
                value="ERROR", 
                align=ft.Alignment.CENTER, 
                font_family="JetBrains Mono",
                color=ft.Colors.RED,
                weight=ft.FontWeight.W_700,
              ),
              content=ft.Text(
                value=f"Some fields are incomplete or incorrect!",
                text_align=ft.TextAlign.CENTER,
                theme_style=ft.TextThemeStyle.LABEL_LARGE,
                font_family="JetBrains Mono",
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.W_500
              ),
              actions=[
                  ft.FilledButton(
                    content=ft.Text(
                    value=f"Back",
                    text_align=ft.TextAlign.CENTER,
                    theme_style=ft.TextThemeStyle.LABEL_LARGE,
                    font_family="JetBrains Mono",
                    color=ft.Colors.BLACK,
                    weight=ft.FontWeight.W_300,
                  ), 
                  on_click=lambda e: self.page.pop_dialog(), align=ft.Alignment.CENTER,
                  bgcolor=ft.Colors.RED_500,
                ),
              ],
            )
          )
      self.page.update()

    def detect_input_change(e):
      in_field : ft.TextField = e.control
      print(in_field.value)
      if in_field.value == None:
        in_field.border_color = ft.Colors.RED
      else:
        in_field.border_color = ft.Colors.WHITE
      self.page.update()

    def detect_input_change_user(e):
      in_field : ft.TextField = e.control
      if in_field.value == None:
        in_field.border_color = ft.Colors.RED
      elif any(char.isdigit() for char in in_field.value):
        in_field.border_color = ft.Colors.RED
      else:
        in_field.border_color = ft.Colors.WHITE
      self.page.update()

    def detect_input_change_pass(e):
      in_field : ft.TextField = e.control
      if in_field.value == None:
        in_field.border_color = ft.Colors.RED
      elif len(in_field.value) < 8:
        in_field.border_color = ft.Colors.RED
      else:
        in_field.border_color = ft.Colors.WHITE
      self.page.update()

    def detect_input_change_phone(e):
      in_field : ft.TextField = e.control
      if in_field.value == None:
        in_field.border_color = ft.Colors.RED
      elif not in_field.value.isdigit() or len(in_field.value) < 11:
        in_field.border_color = ft.Colors.RED
      else:
        in_field.border_color = ft.Colors.WHITE
      self.page.update()

    input_date = ft.DatePicker(
        on_change=date_changed,
        value=datetime.datetime(2005, 1, 1),
        first_date=datetime.datetime(1950, 1, 1),
        last_date=datetime.datetime(2023, 12, 31),
    )

    field_firstname = self.create_field("First Name", on_click_change=detect_input_change_user)
    field_lastname = self.create_field("Last Name", on_click_change=detect_input_change_user)
    field_password = self.create_field("Password", True, on_click_change=detect_input_change_pass, max_length=24)
    field_number = self.create_field("09xxxxxxxx (PH)", is_numerical=True, on_click_change=detect_input_change_phone, max_length=12)
    field_email = self.create_field("Email", on_click_change=detect_input_change)
    field_date = self.create_field(
      "Birthdate",
      on_click=lambda _:self.page.show_dialog(input_date),
      is_readonly=True,
      on_click_change=detect_input_change
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
                        ft.Text(
                          "Basic Information", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_LARGE,
                        ),
                        ft.Divider(),


                        label_first_name := ft.Text(
                          "First Name", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        field_firstname,
                        label_last_name := ft.Text(
                          "Last Name", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        field_lastname,
                        label_date := ft.Text(
                          "Birthday", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        field_date,
                        label_password := ft.Text(
                          "Password ", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        field_password,

# ============================================== Divider 

                        ft.Text(
                          "Contact and Verification", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_LARGE,
                          margin=ft.Margin.only(top=20)
                        ),
                        ft.Divider(),


                        label_phone_number := ft.Text(
                          "Phone Number", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        field_number,
                        label_personal_email := ft.Text(
                          "Personal Email", 
                          font_family="JetBrains Mono", 
                          theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
                        ),
                        field_email,
                    ]
                )
            ]
        )
    )

    fields = [
      field_firstname, 
      field_lastname,
      field_date,
      field_password,
      field_number,
      field_email
    ]

    labels = {
      field_firstname : label_first_name,
      field_lastname : label_last_name,
      field_date : label_date,
      field_password : label_password,
      field_number : label_phone_number,
      field_email : label_personal_email
    }

    button_submit = ft.FilledButton(
       height=40,
       width=200,
        content=ft.Text(
            value="Continue ->",
            font_family="JetBrains Mono",
            weight=ft.FontWeight.W_800
        ),
        on_click=_update_fields
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

  def create_field(self, hint_text, is_password=False, is_numerical=False, on_click=None, on_click_change=None, label=None, is_readonly=False, max_length=None) -> ft.TextField:
      return ft.TextField(
        max_length=max_length,
          on_blur=on_click_change,
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
