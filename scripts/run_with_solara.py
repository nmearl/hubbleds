import os
from warnings import filterwarnings

filterwarnings(action="ignore", category=UserWarning)

from cosmicds.app import Application
import solara

import solara
from solara.alias import rv
# from ..server import manager
import hashlib

from solara_enterprise import auth

active = solara.reactive(False)
user_info = solara.reactive({})
class_code = solara.reactive("")


@solara.component
def Login(**btn_kwargs):
    with rv.Dialog(
            v_model=active.value,
            on_v_model=active.set,
            max_width=600,
            # fullscreen=True,
            persistent=True,
            overlay_color="grey darken-2"
    ) as login:
        with rv.Card():
            with rv.CardText():
                with rv.Container(
                        class_="d-flex align-center flex-column justify-center"):
                    solara.Image(
                        "/static/public/cosmicds_logo_transparent_for_dark_backgrounds.png")
                    solara.Text("Hubble's Law Data Story",
                                classes=["display-1", "py-12"])

                    solara.InputText(label="Class Code", value=class_code)

                    solara.Button(
                        "Sign in",
                        href=auth.get_login_url(),
                        disabled=not class_code.value,
                        outlined=False,
                        large=True,
                        color='success'
                    )
                    rv.Spacer()

    return login


@solara.component
def Page():
    with solara.VBox() as main:
        login_dialog = Login()

        if not auth.user.value:
            active.set(True)
        else:
            userinfo = auth.user.value['userinfo']

            if 'email' in userinfo or 'name' in userinfo:
                user_ref = userinfo.get('email', userinfo['name'])
            else:
                # TODO: should be hidden on production
                solara.Markdown(f"Failed to hash \n\n{userinfo}")
                return main

            username = hashlib.sha1(
                (user_ref + os.environ['SOLARA_SESSION_SECRET_KEY']
                 ).encode()).hexdigest()

            app = Application.element(story='hubbles_law',
                                      update_db=True,
                                      show_team_interface=True,
                                      allow_advancing=True,
                                      create_new_student=False,
                                      user_info={'name': username,
                                                 'class_code': class_code.value})

            solara.Button("", icon_name="mdi-logout", fab=True,
                          absolute=True, bottom=True, right=True,
                          text=False,
                          tag="Logout",
                          href=auth.get_logout_url(), style_="z-index:100")

        solara.Title(title="Hubble's Law Data Story")

    return main
