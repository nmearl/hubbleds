import hashlib
import os
from warnings import filterwarnings

import solara
from cosmicds.app import Application
from solara.alias import rv
from solara.server import settings
from solara_enterprise import auth

filterwarnings(action="ignore", category=UserWarning)

if 'AWS_EBS_URL' in os.environ:
    settings.main.base_url = os.environ['AWS_EBS_URL']

active = solara.reactive(False)
user_info = solara.reactive({})
class_code = solara.reactive("")
update_db = solara.reactive(False)
debug_mode = solara.reactive(False)


def get_session_id() -> str:
    """Returns the session id, which is stored using a browser cookie."""
    import solara.server.kernel_context

    context = solara.server.kernel_context.get_current_context()
    return context.session_id


def _load_from_cache():
    cache = solara.cache.storage.get(f"cds-login-options-{get_session_id()}")

    if cache is not None:
        for key, state in [('class_code', class_code),
                           ('update_db', update_db),
                           ('debug_mode', debug_mode)]:
            if key in cache:
                state.set(cache[key])


def _save_to_cache():
    solara.cache.storage[f"cds-login-options-{get_session_id()}"] = {
        'class_code': class_code.value,
        'update_db': update_db.value,
        'debug_mode': debug_mode.value
    }


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

                    solara.InputText(label="Class Code",
                                     value=class_code,
                                     continuous_update=True)

                    # TODO: hide these in production
                    with solara.Row():
                        solara.Checkbox(label="Update DB", value=update_db)
                        solara.Checkbox(label="Debug Mode", value=debug_mode)

                    solara.Button(
                        "Sign in",
                        href=auth.get_login_url(),
                        disabled=not class_code.value,
                        outlined=False,
                        large=True,
                        color='success',
                        on_click=_save_to_cache
                    )

    return login


@solara.component
def Page():
    _load_from_cache()

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
                                      update_db=update_db.value,
                                      show_team_interface=debug_mode.value,
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
