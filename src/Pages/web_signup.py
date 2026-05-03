import flet as ft
import datetime
import asyncio
from Utilities import effect_util as efutil
from Utilities import database_util as dabil


class Signup(ft.View):

  INPUT_CONTAINER_WIDTH = 500
  INPUT_ROUNDED_BORDER_RAD = 5

  ANIMATE_OPACITY_SWAP_DURATION = 300
  ANIMATE_GENERAL_CONTAINER_DURATION = 500

  trigger_swaps = 0

  def __init__(self, db:dabil.DatabaseManager):
    
    self.account_type = "user"
    m_anim_title1 = efutil.Fun("> Sign_up --stage 1 basic_info", theme_styling=ft.TextThemeStyle.TITLE_MEDIUM)
    m_anim_title2 = efutil.Fun("> Sign_up --stage 2 basic_info", theme_styling=ft.TextThemeStyle.TITLE_MEDIUM)
    m_anim_title3 = efutil.Fun("> Sign_up --stage 3 basic_info", theme_styling=ft.TextThemeStyle.TITLE_MEDIUM)

    def date_changed(e) -> None:
      field_date.value = e.control.value.astimezone().strftime("%B %d, %Y")

    async def _change_to_type(e): #'student','instructor','general'
      self.account_type = e.control.data
      print("Processed type to be:", e.control.data, "\nswapping...")
      await _swap_to_final_signup(e)
      
    async def continue_button(e) -> None:
      if self.trigger_swaps == 0:
        await _update_fields(e)
      elif self.trigger_swaps == 2:
        # TO BE REFACTORED IN THE FUTURE:
        # The inputs are stored in 'fields'
        #     fields = [
        #   field_firstname,    0
        #   field_lastname,     1
        #   field_date,         2
        #   field_password,     3
        #   field_number,       4
        #   field_email,        5
        #   field_school_email, 6
        #   field_year_level    7
        # ]
        print("** Trigger Account creation")
        print("Trying an account with type: ", self.account_type)
        db.connect()
        db.create_user(
          username=" ".join([fields[0].value, fields[1].value]),
          birthdate=fields[2].value,
          password=fields[3].value,
          phone_number=fields[4].value,
          email=fields[5].value,
          email_univ=fields[6].value,
          account_type=self.account_type,
        )
        db.close()

        print("User Tried. Check DB.")

        for f in fields:
          if f.value != None:
            f.value = None
        main_layout.opacity = 0.7
        button_submit.disabled = True
        button_back_login.disabled = True
        self.page.update()
        await asyncio.sleep(2)
        await self.push_login(e)

    async def _swap_to_final_signup(e = None) -> None:
      self.trigger_swaps += 1
      input_ask_type.disabled = True
      input_ask_type.opacity = 0.0
      input_ask_type.update()
      input_student_type.update()

      await asyncio.sleep(1)

      main_layout.controls[0] = m_anim_title3

      input_ask_type.visble = False

      button_back_login.disabled = False
      button_submit.disabled = False

      input_student_type.visible = True
      input_student_type.opacity = 1.0
      input_student_type.disabled = False

      base_container.height = 270

      input_student_type.update()
      button_back_login.update()
      input_ask_type.update()
      button_submit.update()
      base_container.update()
      self.page.update()

    async def _swap_container_type(e = None) -> None:
      if self.trigger_swaps != 0: return
      else: self.trigger_swaps = 1

      button_back_login.disabled = True
      button_submit.disabled = True

      input_fields_container.opacity = 0.8
      input_fields_container.animate_opacity = None
      input_fields_container.disabled = True

      input_student_type.opacity = 0.0
      input_student_type.disabled = True
      input_student_type.update()

      input_fields_container.update()
      button_back_login.update()
      button_submit.update()

      await scroll_container.scroll_to(offset=0, duration=500)
      scroll_container.scroll = None
      
      await asyncio.sleep(1)

      scroll_container.update()
      input_fields_container.animate_opacity = self.ANIMATE_OPACITY_SWAP_DURATION
      input_fields_container.opacity = 0.8
      input_fields_container.update()

      await asyncio.sleep(0.1)

      input_fields_container.opacity = 0.0
      input_fields_container.update()

      await asyncio.sleep(0.5)

      main_layout.controls[0] = m_anim_title2

      input_fields_container.visible = False
      input_student_type.visible = False
      input_ask_type.visible = True
      base_container.height = 370
      input_ask_type.opacity = 1.0
      input_ask_type.disabled = False
      input_ask_type.update()
      base_container.update()
      input_student_type.update()
      input_fields_container.update()
      self.page.update()



    async def _update_fields(e) -> None:
      is_complete = True
      inc = 0
      switch_label = []
      switch = [1, 1, 1, 1, 1, 1]

      print("===========")

      for f in fields:
        if (inc >= len(switch)): break # halting in detecting the rest of fields

        cur_field : ft.TextField = f
        if (cur_field.value == None):
          print(f"Failed {cur_field.hint_text}")
          cur_field.border_color=ft.Colors.RED
          labels[f].color = ft.Colors.RED
          is_complete = False
          switch[inc] = 0
        else:
          cur_field.border_color=ft.Colors.WHITE
          labels[f].color = ft.Colors.WHITE
          switch_label.append(cur_field.hint_text)
        
        inc += 1

      if (is_complete):
        await _swap_container_type(e)
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
      if in_field.disabled: return

      if in_field.value == None:
        in_field.border_color = ft.Colors.RED
        labels[in_field].color = ft.Colors.RED
      else:
        in_field.border_color = ft.Colors.WHITE
        labels[in_field].color = ft.Colors.WHITE
      self.page.update()

    def detect_input_change_user(e):
      in_field : ft.TextField = e.control
      labels[in_field].color = ft.Colors.RED
      if in_field.value == None:
        in_field.border_color = ft.Colors.RED
      elif any(char.isdigit() for char in in_field.value):
        in_field.border_color = ft.Colors.RED
      else:
        in_field.border_color = ft.Colors.WHITE
        labels[in_field].color = ft.Colors.WHITE
      self.page.update()

    def detect_input_change_pass(e):
      in_field : ft.TextField = e.control
      labels[in_field].color = ft.Colors.RED
      if in_field.value == None:
        in_field.border_color = ft.Colors.RED
      elif len(in_field.value) < 8:
        in_field.border_color = ft.Colors.RED
      else:
        in_field.border_color = ft.Colors.WHITE
        labels[in_field].color = ft.Colors.WHITE
      self.page.update()

    def detect_input_change_phone(e):
      in_field : ft.TextField = e.control
      labels[in_field].color = ft.Colors.RED
      if in_field.value == None:
        in_field.border_color = ft.Colors.RED
      elif not in_field.value.isdigit() or len(in_field.value) < 11:
        in_field.border_color = ft.Colors.RED
      else:
        in_field.border_color = ft.Colors.WHITE
        labels[in_field].color = ft.Colors.WHITE
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

    input_student_type = ft.Container(
      visible=False,
      disabled=True,
      opacity=0.0,
      alignment=ft.Alignment.CENTER,
      animate_opacity=self.ANIMATE_OPACITY_SWAP_DURATION,
      content=ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
          ft.Text(
            "School Information", 
            font_family="JetBrains Mono", 
            theme_style=ft.TextThemeStyle.LABEL_LARGE,
            margin=ft.Margin.only(top=20)
          ),
          ft.Divider(),

          label_school_email := ft.Text(
            "University Email", 
            font_family="JetBrains Mono", 
            theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
          ),
          field_school_email := self.create_field("Email", on_click_change=detect_input_change),
          label_year_level := ft.Text(
            "Year Level", 
            font_family="JetBrains Mono", 
            theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
          ),
          field_year_level := self.create_field("1, 2, 3, etc...", on_click_change=detect_input_change, is_numerical=True, max_length=2)
        ]
      )
    )

    input_ask_type = ft.Container(
      visible=False,
      alignment=ft.Alignment.CENTER,
      animate_opacity=self.ANIMATE_OPACITY_SWAP_DURATION,
      opacity=0.0,
      disabled=True,
      expand=True,
      expand_loose=True,
      content=ft.Column(
        margin=30,
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
          ft.Text(
            value="What kind of Role do you have?", 
            size=22,
            text_align=ft.TextAlign.CENTER,
            font_family="JetBrains Mono", 
            theme_style=ft.TextThemeStyle.LABEL_LARGE,
            margin=10,
          ),
          ft.ElevatedButton(
            width=320,
            height=50,
            content=ft.Text(
              value="A General User"
            ),
            disabled=True,
          ),
          ft.ElevatedButton(
            width=320,
            height=50,
            content=ft.Text(
              value="A Student"
            ),
            on_click=_change_to_type,
            data="student"
          ),
          ft.ElevatedButton(
            width=320,
            height=50,
            content=ft.Text(
              value="An Educator",
            ),
            on_click=_change_to_type,
            data="instructor"
          ),
        ]
      )
    )

    input_fields_container = ft.Container(
        width=self.INPUT_CONTAINER_WIDTH,
        animate_opacity=self.ANIMATE_OPACITY_SWAP_DURATION,
        opacity=1.0,
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
      field_email,
      field_school_email,
      field_year_level
    ]

    labels = {
      field_firstname : label_first_name,
      field_lastname : label_last_name,
      field_date : label_date,
      field_password : label_password,
      field_number : label_phone_number,
      field_email : label_personal_email,
      field_school_email : label_school_email,
      field_year_level : label_year_level
    }

    button_submit = ft.FilledButton(
       height=40,
       width=200,
       animate_opacity=self.ANIMATE_OPACITY_SWAP_DURATION,
        content=ft.Text(
            value="Continue ->",
            font_family="JetBrains Mono",
            weight=ft.FontWeight.W_800
        ),
        on_click=continue_button
    )

    button_back_login = ft.FilledButton(
      height=40,
        content=ft.Text(
            value="Back to login",
            font_family="JetBrains Mono",
            weight=ft.FontWeight.W_800
        ),
      animate_opacity=self.ANIMATE_OPACITY_SWAP_DURATION,
      on_click=self.push_login
    )

    main_layout = ft.Column(
      margin=10,
      alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
      controls=[
        m_anim_title1,
        base_container := ft.Container(
          alignment=ft.Alignment.CENTER,
          animate=ft.Animation(self.ANIMATE_GENERAL_CONTAINER_DURATION, ft.AnimationCurve.EASE_IN_OUT_SINE),
          height=500,
          width=500,
          margin=15,
          border=ft.Border.all(2, ft.Colors.WHITE_38),
          border_radius=5,
          padding=10,
          content= (scroll_container:=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=ft.Container(
              content= ft.Stack(
                controls=[
                  input_fields_container,
                  input_ask_type,
                  input_student_type,
                ],
              ),
              padding=ft.Padding.only(right=12)
              ),
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
            # ft.ElevatedButton(
            #   content=ft.Text("Force Submit"),
            #   on_click=_swap_container_type
            # )
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
