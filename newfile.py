import os
import re

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# Simulated apps
APPS = ["Facebook", "Instagram", "WhatsApp"]

PASSWORD_FILE = "password.txt"

# ===== PASSWORD SYSTEM =====
def load_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as f:
            return f.read().strip()
    return None

def save_password(password):
    with open(PASSWORD_FILE, "w") as f:
        f.write(password)

# ===== SCAM LINK DETECTOR =====
def is_scam_link(url):
    suspicious_keywords = [
        "free", "login", "verify", "account", "update",
        "secure", "bank", "bonus", "win", "claim"
    ]

    ip_pattern = r"http[s]?://\d+\.\d+\.\d+\.\d+"
    if re.search(ip_pattern, url):
        return True

    for word in suspicious_keywords:
        if word in url.lower():
            return True

    return False

# ===== FAKE MESSAGE DETECTOR =====
def is_fake_message(message):
    message = message.lower()

    scam_phrases = [
        "urgent action required",
        "your account will be suspended",
        "click the link below",
        "verify your account",
        "you have won",
        "claim your reward",
        "send money",
        "limited time offer",
        "reset your password now"
    ]

    for phrase in scam_phrases:
        if phrase in message:
            return True

    return False


# ===== MAIN UI =====
class SecurityLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.password = load_password()
        self.app_states = {app: False for app in APPS}

        # TITLE
        self.add_widget(Label(
            text="🔐 META SECURITY APP",
            color=(0,1,0,1),
            font_size=24
        ))

        # ===== PASSWORD INPUT =====
        self.pwd_input = TextInput(
            hint_text="Enter or Set Password",
            password=True,
            font_size=22,
            size_hint_y=None,
            height=60
        )
        self.add_widget(self.pwd_input)

        self.pwd_btn = Button(
            text="SUBMIT PASSWORD",
            background_color=(0,1,0,1),
            font_size=20,
            size_hint_y=None,
            height=60
        )
        self.pwd_btn.bind(on_press=self.check_password)
        self.add_widget(self.pwd_btn)

        self.status = Label(text="", font_size=18)
        self.add_widget(self.status)

        # ===== TOOL AREA =====
        self.tools = BoxLayout(orientation='vertical', spacing=10)
        self.tools.opacity = 0
        self.add_widget(self.tools)

        # ===== LINK CHECK (BIG UI) =====
        self.tools.add_widget(Label(text="🔗 Link Checker", color=(0,1,0,1), font_size=20))

        self.link_input = TextInput(
            hint_text="Paste link here",
            font_size=22,
            size_hint_y=None,
            height=70
        )
        self.tools.add_widget(self.link_input)

        self.link_btn = Button(
            text="🔍 CHECK LINK",
            background_color=(0,1,0,1),
            font_size=20,
            size_hint_y=None,
            height=60
        )
        self.link_btn.bind(on_press=self.check_link)
        self.tools.add_widget(self.link_btn)

        self.link_result = Label(text="", font_size=18)
        self.tools.add_widget(self.link_result)

        # ===== MESSAGE CHECK (BIG UI) =====
        self.tools.add_widget(Label(text="📩 Message Checker", color=(0,1,0,1), font_size=20))

        self.msg_input = TextInput(
            hint_text="Paste message here",
            font_size=22,
            size_hint_y=None,
            height=120
        )
        self.tools.add_widget(self.msg_input)

        self.msg_btn = Button(
            text="🔍 CHECK MESSAGE",
            background_color=(0,1,0,1),
            font_size=20,
            size_hint_y=None,
            height=60
        )
        self.msg_btn.bind(on_press=self.check_message)
        self.tools.add_widget(self.msg_btn)

        self.msg_result = Label(text="", font_size=18)
        self.tools.add_widget(self.msg_result)

        # ===== APP LOCK SIMULATION =====
        self.tools.add_widget(Label(text="📱 App Lock Simulation", color=(0,1,0,1), font_size=20))

        self.app_buttons = {}
        for app in APPS:
            btn = Button(
                text=f"🔓 {app} (Unlocked)",
                background_color=(0,1,0,1),
                font_size=18,
                size_hint_y=None,
                height=60
            )
            btn.bind(on_press=lambda instance, a=app: self.toggle_app(a))
            self.tools.add_widget(btn)
            self.app_buttons[app] = btn

    # ===== PASSWORD CHECK =====
    def check_password(self, instance):
        entered = self.pwd_input.text

        if self.password is None:
            save_password(entered)
            self.password = entered
            self.status.text = "✅ Password Set Successfully"
            self.unlock()

        elif entered == self.password:
            self.status.text = "✅ Access Granted"
            self.unlock()
        else:
            self.status.text = "❌ Wrong Password"

    def unlock(self):
        self.tools.opacity = 1

    # ===== LINK CHECK =====
    def check_link(self, instance):
        url = self.link_input.text

        if is_scam_link(url):
            self.link_result.text = "⚠️ Scam Link Detected!"
        else:
            self.link_result.text = "✅ Safe Link"

    # ===== MESSAGE CHECK =====
    def check_message(self, instance):
        msg = self.msg_input.text

        if is_fake_message(msg):
            self.msg_result.text = "⚠️ Fake Message!"
        else:
            self.msg_result.text = "✅ Message Safe"

    # ===== APP LOCK SIMULATION =====
    def toggle_app(self, app_name):
        self.app_states[app_name] = not self.app_states[app_name]

        if self.app_states[app_name]:
            self.app_buttons[app_name].text = f"🔒 {app_name} (Locked)"
            self.app_buttons[app_name].background_color = (1, 0, 0, 1)
        else:
            self.app_buttons[app_name].text = f"🔓 {app_name} (Unlocked)"
            self.app_buttons[app_name].background_color = (0, 1, 0, 1)


# ===== APP CLASS =====
class SecurityApp(App):
    def build(self):
        return SecurityLayout()


if __name__ == "__main__":
    SecurityApp().run()