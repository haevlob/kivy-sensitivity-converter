from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from functools import partial
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
import webbrowser

class Blocker(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.touch_start_x = None
        self.touch_start_y = None
        self.is_swiping = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch_start_x = touch.x
            self.touch_start_y = touch.y
            touch.grab(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            delta_x = touch.x - self.touch_start_x
            delta_y = touch.y - self.touch_start_y
            if abs(delta_x) > abs(delta_y) and abs(delta_x) > dp(10):
                self.is_swiping = True
                new_x = min(0, max(-self.app.menu.width, delta_x))
                self.app.menu.x = new_x
                return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
            if self.is_swiping:
                self.is_swiping = False
                if self.app.menu.x < -self.app.menu.width / 2:
                    anim = Animation(x=-self.app.menu.width, d=0.2)
                    anim.start(self.app.menu)
                    self.app.root.remove_widget(self)
                    del self.app.blocker
                    self.app.menu_btn.text = '☰'
                else:
                    anim = Animation(x=0, d=0.2)
                    anim.start(self.app.menu)
                return True
            else:
                anim = Animation(x=-self.app.menu.width, d=0.2)
                anim.start(self.app.menu)
                self.app.root.remove_widget(self)
                del self.app.blocker
                self.app.menu_btn.text = '☰'
                return True
        return super().on_touch_up(touch)

class Menu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            for child in reversed(self.children):
                if child.dispatch('on_touch_down', touch):
                    return True
            return True
        return super(Menu, self).on_touch_down(touch)

class SensitivityConverter(BoxLayout):
    orientation = 'vertical'
    left_game = StringProperty('standoff')
    right_game = StringProperty('cod')
    conversion_mode = StringProperty('auto')
    sensor_type = StringProperty('sensitivity')
    pubg_accel = BooleanProperty(False)
    standoff_accel = NumericProperty(0.0)
    cod_accel = NumericProperty(0)
    language = StringProperty('ru')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.translations = {
            'from_game': {
                'ru': 'Из игры',
                'en': 'From game',
                'es': 'De juego',
                'pt': 'Do jogo'
            },
            'to_game': {
                'ru': 'В игру',
                'en': 'To game',
                'es': 'A juego',
                'pt': 'Para jogo'
            },
            'accel_title': {
                'ru': 'Ускорение',
                'en': 'Acceleration',
                'es': 'Aceleración',
                'pt': 'Aceleração'
            },
            'mode': {
                'ru': 'Режим:',
                'en': 'Mode:',
                'es': 'Modo:',
                'pt': 'Modo:'
            },
            'auto': {
                'ru': 'Автоматически',
                'en': 'Automatically',
                'es': 'Automáticamente',
                'pt': 'Automaticamente'
            },
            'manual': {
                'ru': 'Вручную',
                'en': 'Manually',
                'es': 'Manualmente',
                'pt': 'Manualmente'
            },
            'type': {
                'ru': 'Тип:',
                'en': 'Type:',
                'es': 'Tipo:',
                'pt': 'Tipo:'
            },
            'sens': {
                'ru': 'Сенса',
                'en': 'Sens',
                'es': 'Sens',
                'pt': 'Sens'
            },
            'gyro': {
                'ru': 'Гироскоп',
                'en': 'Gyroscope',
                'es': 'Giroscopio',
                'pt': 'Giroscópio'
            },
            'same_games': {
                'ru': 'Выберите разные игры для конвертации',
                'en': 'Select different games for conversion',
                'es': 'Seleccione juegos diferentes para la conversión',
                'pt': 'Selecione jogos diferentes para conversão'
            },
            'general_sens': {
                'ru': 'Чувствит',
                'en': 'Sensitivity',
                'es': 'Sensibilidad',
                'pt': 'Sensibilidade'
            },
            '3person': {
                'ru': '3-е лицо',
                'en': 'TPP No Scope',
                'es': 'PTP sin visor',
                'pt': '3ª Pessoa'
            },
            '1person': {
                'ru': '1-е лицо',
                'en': 'FPP No Scope',
                'es': 'PPP sin visor',
                'pt': '1ª Pessoa'
            },
            'col_holo_iron_side': {
                'ru': 'Кол., голо.,\nмушка, боковой',
                'en': 'Red Dot,Holo,...',
                'es': 'Punto Rojo,Holo,...',
                'pt': 'Ponto Verm., Holo,...'
            },
            'in_scope': {
                'ru': 'С прицелом',
                'en': 'Scope sensitivity',
                'es': 'Sens.de la mirilla',
                'pt': 'Telescópica'
            },
            '3person_dot': {
                'ru': '3-е лицо',
                'en': 'Third person',
                'es': 'Tercera persona',
                'pt': 'Terceira pessoa'
            },
            'standard': {
                'ru': 'Стандарт (руль)',
                'en': 'Steering',
                'es': 'Dirección',
                'pt': 'Condução'
            },
            'col_holo_aim': {
                'ru': 'Кол., голо.,\nв реж. прицел.',
                'en': 'Red dot,holo,ADS',
                'es': 'Punto rojo/ holo.,apuntado',
                'pt': 'Ponto verm./ holo.,mira'
            },
            'tactical': {
                'ru': 'Тактический',
                'en': 'Tactical',
                'es': 'Mira táctica',
                'pt': 'Escopo táctico'
            },
            'sniper': {
                'ru': 'Снайперский',
                'en': 'Sniper',
                'es': 'Mira de précision',
                'pt': 'Escopo do fuzil'
            },
            'settings': {
                'ru': 'Настройки',
                'en': 'Settings',
                'es': 'Ajustes',
                'pt': 'Configurações'
            },
            'language': {
                'ru': 'Язык',
                'en': 'Language',
                'es': 'Idioma',
                'pt': 'Idioma'
            },
            'menu': {
                'ru': 'Меню',
                'en': 'Menu',
                'es': 'Menú',
                'pt': 'Menu'
            },
            'about_title': {
                'ru': 'О приложении',
                'en': 'About the App',
                'es': 'Acerca de la aplicación',
                'pt': 'Sobre o aplicativo'
            },
            'about_text': {
                'ru': """Mobile Games Sens Converter
Версия: 1.2
Автор: Taysin Dim
Удобный конвертер чувствительности и гироскопа
для Standoff 2, PUBG Mobile и Call of Duty Mobile.
• Точная конвертация сенсы и гироскопа
• Автоматический и ручной режим
• Поддержка ускорения (PUBG)
• Работает полностью оффлайн
• Без рекламы и платных функций
© 2026 Taysin Dim. Все права защищены.""",
                'en': """Mobile Games Sens Converter
Version: 1.2
Author: Taysin Dim
Convenient sensitivity and gyroscope converter
for Standoff 2, PUBG Mobile and Call of Duty Mobile.
• Accurate sensitivity and gyroscope conversion
• Automatic and manual mode
• Acceleration support (PUBG)
• Works completely offline
• No ads or paid features
© 2026 Taysin Dim. All rights reserved.""",
                'es': """Mobile Games Sens Converter
Versión: 1.2
Autor: Taysin Dim
Convertidor práctico de sensibilidad y giroscopio
para Standoff 2, PUBG Mobile y Call of Duty Mobile.
• Conversión precisa de sensibilidad y giroscopio
• Modo automático y manual
• Soporte de aceleración (PUBG)
• Funciona completamente sin conexión
• Sin anuncios ni funciones de pago
© 2026 Taysin Dim. Todos los derechos reservados.""",
                'pt': """Mobile Games Sens Converter
Versão: 1.2
Autor: Taysin Dim
Conversor conveniente de sensibilidade e giroscópio
para Standoff 2, PUBG Mobile e Call of Duty Mobile.
• Conversão precisa de sensibilidade e giroscópio
• Modo automático e manual
• Suporte à aceleração (PUBG)
• Funciona completamente offline
• Sem anúncios ou recursos pagos
© 2026 Taysin Dim. Todos os direitos reservados."""
            },
            'donate_button': {
                'ru': 'Политика конфиденциальности',
                'en': 'Privacy Policy',
                'es': 'Política de privacidad',
                'pt': 'Política de privacidade'
            }
        }
        self.langs = {
            'ru': 'Русский',
            'en': 'English',
            'es': 'Español',
            'pt': 'Português (BR)'
        }
        self.setup_conversion_data()
        self.entry_widgets = []
        self.left_widgets = []
        self.create_widgets()

    def get_text(self, key):
        return self.translations.get(key, {}).get(self.language, key)

    def setup_conversion_data(self):
        self.standoff_pubg_sens = {
            "general_3p": {0.0: 0, 1.0: 12, 2.0: 50, 3.0: 75, 4.0: 100, 6.0: 150, 10.0: 250, 96.0: 2343},
            "general_1p": {0.0: 0, 1.0: 12, 2.0: 50, 3.0: 75, 4.0: 100, 6.0: 150, 10.0: 250, 96.0: 2343},
            "col": {0.0: 0, 1.0: 16, 2.0: 32, 3.0: 48, 4.0: 64, 6.0: 96, 10.0: 153, 96.0: 1537},
            "2x": {0.0: 0, 1.0: 13, 2.0: 26, 3.0: 39, 4.0: 52, 6.0: 77, 10.0: 123, 96.0: 1218},
            "3x": {0.0: 0, 1.0: 8, 2.0: 15, 3.0: 23, 4.0: 31, 6.0: 46, 10.0: 74, 96.0: 731},
            "4x": {0.0: 0, 1.0: 6, 2.0: 12, 3.0: 18, 4.0: 24, 6.0: 34, 10.0: 55, 96.0: 543},
            "6x": {0.0: 0, 1.0: 4, 2.0: 7, 3.0: 11, 4.0: 15, 6.0: 23, 10.0: 37, 96.0: 356},
            "8x": {0.0: 0, 1.0: 3, 2.0: 6, 3.0: 10, 4.0: 13, 6.0: 19, 10.0: 31, 96.0: 300}
        }
        self.standoff_pubg_gyro = {
            "general_3p": {0.0: 0, 0.5: 83, 1.0: 167, 1.5: 248, 2.0: 330, 7.77: 1287, 32.7: 5456},
            "general_1p": {0.0: 0, 0.5: 83, 1.0: 167, 1.5: 248, 2.0: 330, 7.77: 1287, 32.7: 5456},
            "col": {0.0: 0, 0.5: 128, 1.0: 250, 1.5: 380, 2.0: 400, 7.77: 1973, 32.7: 8347},
            "2x": {0.0: 0, 0.5: 103, 1.0: 205, 1.5: 305, 2.0: 400, 7.77: 1579, 32.7: 6683},
            "3x": {0.0: 0, 0.5: 60, 1.0: 125, 1.5: 185, 2.0: 247, 7.77: 963, 32.7: 4446},
            "4x": {0.0: 0, 0.5: 45, 1.0: 94, 1.5: 140, 2.0: 185, 7.77: 721, 32.7: 3342},
            "6x": {0.0: 0, 0.5: 30, 1.0: 63, 1.5: 93, 2.0: 124, 7.77: 481, 32.7: 2224},
            "8x": {0.0: 0, 0.5: 25, 1.0: 51, 1.5: 77, 2.0: 103, 7.77: 400, 32.7: 2550}
        }
        self.standoff_cod_sens = {
            "general_3p": {0.0: 0, 1.0: 39, 2.0: 79, 3.0: 117, 4.0: 156, 6.0: 232, 10.0: 384, 96.0: 3652},
            "general_1p": {0.0: 0, 1.0: 39, 2.0: 79, 3.0: 117, 4.0: 156, 6.0: 232, 10.0: 384, 96.0: 3652},
            "col": {0.0: 0, 1.0: 97, 2.0: 193, 3.0: 293, 4.0: 397, 6.0: 617, 10.0: 1105, 96.0: 11596},
            "2x": {0.0: 0, 1.0: 132, 2.0: 263, 3.0: 394, 4.0: 525, 6.0: 787, 10.0: 1311, 96.0: 12577},
            "3x": {0.0: 0, 1.0: 76, 2.0: 153, 3.0: 233, 4.0: 316, 6.0: 491, 10.0: 877, 96.0: 9176},
            "4x": {0.0: 0, 1.0: 43, 2.0: 86, 3.0: 131, 4.0: 173, 6.0: 256, 10.0: 392, 96.0: 3316},
            "6x": {0.0: 0, 1.0: 36, 2.0: 72, 3.0: 111, 4.0: 146, 6.0: 216, 10.0: 323, 96.0: 2624},
            "6x_sniper": {0.0: 0, 1.0: 41, 2.0: 83, 3.0: 126, 4.0: 167, 6.0: 247, 10.0: 380, 96.0: 3240},
            "8x": {0.0: 0, 1.0: 29, 2.0: 58, 3.0: 91, 4.0: 119, 6.0: 176, 10.0: 254, 96.0: 1931}
        }
        self.standoff_cod_gyro = {
            "general_3p": {0.0: 0, 0.6: 31, 2.4: 126, 32.7: 1917},
            "general_1p": {0.0: 0, 0.6: 31, 2.4: 126, 32.7: 1917},
            "col": {0.0: 0, 0.6: 31, 2.4: 126, 32.7: 1917},
            "2x": {0.0: 0, 0.6: 25, 2.4: 108, 32.7: 1473},
            "3x": {0.0: 0, 0.6: 13, 2.4: 58, 32.7: 791},
            "4x": {0.0: 0, 0.6: 10, 2.4: 45, 32.7: 614},
            "6x": {0.0: 0, 0.6: 7, 2.4: 31, 32.7: 423},
            "6x_sniper": {0.0: 0, 0.6: 8, 2.4: 34, 32.7: 464},
            "8x": {0.0: 0, 0.6: 5, 2.4: 22, 32.7: 300}
        }
        self.pubg_cod_sens = {
            "general_3p": {0: 0, 12: 39, 50: 79, 75: 117, 100: 156, 150: 232, 250: 384, 2343: 3652},
            "general_1p": {0: 0, 12: 39, 50: 79, 75: 117, 100: 156, 150: 232, 250: 384, 2343: 3652},
            "col": {0: 0, 16: 97, 32: 193, 48: 293, 64: 397, 96: 617, 153: 1105, 1537: 11596},
            "2x": {0: 0, 13: 132, 26: 263, 39: 394, 52: 525, 77: 787, 123: 1311, 1218: 12577},
            "3x": {0: 0, 8: 76, 15: 153, 23: 233, 31: 316, 46: 491, 74: 877, 731: 9176},
            "4x": {0: 0, 6: 43, 12: 86, 18: 131, 24: 173, 34: 256, 55: 392, 543: 3316},
            "6x": {0: 0, 4: 36, 7: 72, 11: 111, 15: 146, 23: 216, 37: 323, 356: 2624},
            "8x": {0: 0, 3: 29, 6: 58, 10: 91, 13: 119, 19: 176, 31: 254, 300: 1931},
            "6x_sniper": {0: 0, 4: 41, 7: 83, 11: 126, 15: 167, 23: 247, 37: 380, 356: 3240}
        }
        self.pubg_cod_gyro = {
            "general_3p": {0: 0, 400: 126, 5456: 1719},
            "general_1p": {0: 0, 400: 126, 5456: 1719},
            "col": {0: 0, 612: 126, 8347: 1719},
            "2x": {0: 0, 490: 108, 6683: 1473},
            "3x": {0: 0, 326: 58, 4446: 791},
            "4x": {0: 0, 245: 45, 3342: 614},
            "6x": {0: 0, 163: 31, 2224: 423},
            "8x": {0: 0, 122: 22, 1664: 300},
            "6x_sniper": {0: 0, 163: 34, 2224: 464}
        }
        self.standoff_cod_accel = {
            0: 0,
            0.25: 300
        }

    def create_widgets(self):
        top_frame = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(120))
        self.add_widget(top_frame)
        left_game_frame = BoxLayout(orientation='vertical')
        top_frame.add_widget(left_game_frame)
        self.left_title = Label(text=self.get_text("from_game"), size_hint_y=None, height=dp(30), halign='center', valign='middle')
        self.left_title.bind(size=self.left_title.setter('text_size'))
        left_game_frame.add_widget(self.left_title)
        games = {'Standoff 2': 'standoff', 'PUBG Mobile': 'pubg', 'CoD Mobile': 'cod'}
        self.left_spinner = Spinner(
            text='Standoff 2',
            values=list(games.keys()),
            size_hint_y=None,
            height=dp(44)
        )
        self.left_spinner.bind(text=lambda instance, value: self.on_left_game_change(value))
        left_game_frame.add_widget(self.left_spinner)
        right_game_frame = BoxLayout(orientation='vertical')
        top_frame.add_widget(right_game_frame)
        self.right_title = Label(text=self.get_text("to_game"), size_hint_y=None, height=dp(30), halign='center', valign='middle')
        self.right_title.bind(size=self.right_title.setter('text_size'))
        right_game_frame.add_widget(self.right_title)
        self.right_spinner = Spinner(
            text='CoD Mobile',
            values=list(games.keys()),
            size_hint_y=None,
            height=dp(44)
        )
        self.right_spinner.bind(text=lambda instance, value: self.on_right_game_change(value))
        right_game_frame.add_widget(self.right_spinner)
        self.accel_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(60))
        self.add_widget(self.accel_frame)
        self.accel_title = Label(text=self.get_text("accel_title"), size_hint_y=None, height=dp(30))
        self.accel_frame.add_widget(self.accel_title)
        self.accel_inner_frame = BoxLayout(orientation='horizontal')
        self.accel_frame.add_widget(self.accel_inner_frame)
        settings_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120))
        self.add_widget(settings_frame)
        mode_frame = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        settings_frame.add_widget(mode_frame)
        self.mode_label = Label(text=self.get_text("mode"), size_hint_x=None, width=dp(60))
        mode_frame.add_widget(self.mode_label)
        self.mode_buttons = {}
        for mode, text_key in [('auto', 'auto'), ('manual', 'manual')]:
            btn = ToggleButton(text=self.get_text(text_key), group='mode', state='down' if mode == 'auto' else 'normal')
            btn.mode_id = mode
            btn.bind(state=self.on_mode_change)
            mode_frame.add_widget(btn)
            self.mode_buttons[mode] = btn
        sensor_frame = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        settings_frame.add_widget(sensor_frame)
        self.type_label = Label(text=self.get_text("type"), size_hint_x=None, width=dp(60))
        sensor_frame.add_widget(self.type_label)
        self.sensor_buttons = {}
        for sensor, text_key in [('sensitivity', 'sens'), ('gyroscope', 'gyro')]:
            btn = ToggleButton(text=self.get_text(text_key), group='sensor', state='down' if sensor == 'sensitivity' else 'normal')
            btn.sensor_id = sensor
            btn.bind(state=self.on_sensor_change)
            sensor_frame.add_widget(btn)
            self.sensor_buttons[sensor] = btn
        self.table_scroll = ScrollView()
        self.add_widget(self.table_scroll)
        self.table_frame = GridLayout(cols=4, spacing=dp(5), size_hint_y=None, row_force_default=True, row_default_height=dp(40))
        self.table_frame.bind(minimum_height=self.table_frame.setter('height'))
        self.table_scroll.add_widget(self.table_frame)

        self.footer = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), padding=[dp(10), dp(5), dp(10), dp(5)])
        self.add_widget(self.footer)   
        self.footer.add_widget(Widget())

        self.update_ui()

    def on_lang_change(self, instance, value):
        for code, name in self.langs.items():
            if name == value:
                self.language = code
                break
        self.update_texts()
        App.get_running_app().update_menu_texts()

    def update_texts(self):
        self.left_title.text = self.get_text('from_game')
        self.right_title.text = self.get_text('to_game')
        self.accel_title.text = self.get_text('accel_title')
        self.mode_label.text = self.get_text('mode')
        self.type_label.text = self.get_text('type')
        for mode, btn in self.mode_buttons.items():
            btn.text = self.get_text(mode)
        for sensor, btn in self.sensor_buttons.items():
            btn.text = self.get_text('sens' if sensor == 'sensitivity' else 'gyro') 
        self.update_ui()

    def on_left_game_change(self, value):
        games = {'Standoff 2': 'standoff', 'PUBG Mobile': 'pubg', 'CoD Mobile': 'cod'}
        self.left_game = games[value]
        self.update_ui()

    def on_right_game_change(self, value):
        games = {'Standoff 2': 'standoff', 'PUBG Mobile': 'pubg', 'CoD Mobile': 'cod'}
        self.right_game = games[value]
        self.update_ui()

    def on_mode_change(self, instance, state):
        if state == 'down':
            self.conversion_mode = instance.mode_id
            self.update_ui()

    def on_sensor_change(self, instance, state):
        if state == 'down':
            self.sensor_type = instance.sensor_id
            self.update_ui()

    def update_ui(self):
        self.accel_inner_frame.clear_widgets()
        self.table_frame.clear_widgets()
        self.entry_widgets = []
        self.left_widgets = []
        if self.left_game == self.right_game:
            self.accel_frame.height = 0
        else:
            self.accel_frame.height = dp(60)
            self.setup_acceleration_ui()
        self.setup_conversion_table()

    def setup_acceleration_ui(self):
        left_game = self.left_game
        right_game = self.right_game
        if left_game == right_game:
            return
        if 'pubg' in [left_game, right_game]:
            pubg_side = 'left' if left_game == 'pubg' else 'right'
            other_game = left_game if pubg_side == 'right' else right_game
            readonly = pubg_side == 'left'

            cb = CheckBox(active=self.pubg_accel)
            cb.bind(active=self.update_acceleration)
            self.bind(pubg_accel=cb.setter('active'))
            self.pubg_checkbox = cb

            if other_game == 'standoff':
                input_widget = TextInput(text='', multiline=False, input_filter='float', height=dp(40), size_hint_y=None, padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14))
                input_widget.readonly = readonly
                if readonly:
                    input_widget.background_color = [0.8, 0.8, 0.8, 1]
                    input_widget.foreground_color = [0, 0, 0, 1]
                    input_widget.text = f"{self.standoff_accel:.2f}" if self.standoff_accel != 0.0 else ''
                if not readonly:
                    input_widget.bind(text=self.on_standoff_accel_text)
                self.standoff_accel_input = input_widget
                other_label = "Standoff"
            elif other_game == 'cod':
                input_widget = TextInput(text='', multiline=False, input_filter='int', height=dp(40), size_hint_y=None, padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14))
                input_widget.readonly = readonly
                if readonly:
                    input_widget.background_color = [0.8, 0.8, 0.8, 1]
                    input_widget.foreground_color = [0, 0, 0, 1]
                    input_widget.text = str(self.cod_accel) if self.cod_accel != 0 else ''
                if not readonly:
                    input_widget.bind(text=self.on_cod_accel_text)
                self.cod_accel_input = input_widget
                other_label = "CoD"

            if pubg_side == 'right':
                self.other_accel_input = input_widget
                self.bind(pubg_accel=self.update_other_input_state)
                self.update_other_input_state(None, self.pubg_accel)

            if pubg_side == 'left':
                self.accel_inner_frame.add_widget(Label(text="PUBG", size_hint_x=None, width=dp(100)))
                self.accel_inner_frame.add_widget(cb)
                self.accel_inner_frame.add_widget(Label(text=other_label, size_hint_x=None, width=dp(100)))
                self.accel_inner_frame.add_widget(input_widget)
            else:
                self.accel_inner_frame.add_widget(Label(text=other_label, size_hint_x=None, width=dp(100)))
                self.accel_inner_frame.add_widget(input_widget)
                self.accel_inner_frame.add_widget(Label(text="PUBG", size_hint_x=None, width=dp(100)))
                self.accel_inner_frame.add_widget(cb)
        elif left_game == 'standoff' and right_game == 'cod':
            self.accel_inner_frame.add_widget(Label(text="Standoff", size_hint_x=None, width=dp(100)))
            self.standoff_accel_input = TextInput(text='', multiline=False, input_filter='float', height=dp(40), size_hint_y=None, padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14))
            self.accel_inner_frame.add_widget(self.standoff_accel_input)
            self.standoff_accel_input.bind(text=self.on_standoff_accel_text)
            self.accel_inner_frame.add_widget(Label(text="CoD", size_hint_x=None, width=dp(100)))
            self.cod_accel_input = TextInput(text='', multiline=False, readonly=True, input_filter='int', height=dp(40), size_hint_y=None, padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14), background_color=[0.8, 0.8, 0.8, 1], foreground_color=[0, 0, 0, 1])
            self.accel_inner_frame.add_widget(self.cod_accel_input)
            self.cod_accel_input.text = str(self.cod_accel) if self.cod_accel != 0 else ''
        elif left_game == 'cod' and right_game == 'standoff':
            self.accel_inner_frame.add_widget(Label(text="CoD", size_hint_x=None, width=dp(100)))
            self.cod_accel_input = TextInput(text='', multiline=False, input_filter='int', height=dp(40), size_hint_y=None, padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14))
            self.accel_inner_frame.add_widget(self.cod_accel_input)
            self.cod_accel_input.bind(text=self.on_cod_accel_text)
            self.accel_inner_frame.add_widget(Label(text="Standoff", size_hint_x=None, width=dp(100)))
            self.standoff_accel_input = TextInput(text='', multiline=False, readonly=True, input_filter='float', height=dp(40), size_hint_y=None, padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14), background_color=[0.8, 0.8, 0.8, 1], foreground_color=[0, 0, 0, 1])
            self.accel_inner_frame.add_widget(self.standoff_accel_input)
            self.standoff_accel_input.text = f"{self.standoff_accel:.2f}" if self.standoff_accel != 0.0 else ''

    def update_other_input_state(self, instance, value):
        self.other_accel_input.readonly = value
        self.other_accel_input.background_color = [0.8, 0.8, 0.8, 1] if value else [1, 1, 1, 1]
        self.other_accel_input.foreground_color = [0, 0, 0, 1]
        self.update_accel_inputs()

    def on_standoff_accel_text(self, instance, value):
        if value == '':
            self.standoff_accel = 0.0
        else:
            try:
                val = float(value)
                self.standoff_accel = max(0.0, val)
            except ValueError:
                self.standoff_accel = 0.0
                instance.text = ''
        if hasattr(self, 'pubg_checkbox'):
            self.pubg_checkbox.unbind(active=self.update_acceleration)
            self.pubg_accel = abs(self.standoff_accel - 0.42) <= 0.01
            self.pubg_checkbox.bind(active=self.update_acceleration)
        self.update_standoff_cod_accel()
        self.update_accel_inputs()

    def on_cod_accel_text(self, instance, value):
        if value == '':
            self.cod_accel = 0
        else:
            try:
                val = int(value)
                self.cod_accel = max(0, val)
            except ValueError:
                self.cod_accel = 0
                instance.text = ''
        if hasattr(self, 'pubg_checkbox'):
            self.pubg_checkbox.unbind(active=self.update_acceleration)
            self.pubg_accel = abs(self.cod_accel - 300) <= 1
            self.pubg_checkbox.bind(active=self.update_acceleration)
        self.update_standoff_cod_accel()
        self.update_accel_inputs()

    def update_accel_inputs(self):
        if hasattr(self, 'standoff_accel_input') and self.standoff_accel_input.readonly:
            self.standoff_accel_input.text = f"{self.standoff_accel:.2f}" if self.standoff_accel != 0.0 else ''
        if hasattr(self, 'cod_accel_input') and self.cod_accel_input.readonly:
            self.cod_accel_input.text = str(self.cod_accel) if self.cod_accel != 0 else ''

    def update_acceleration(self, instance, active):
        # ====================================================
        # ИСПРАВЛЕНИЕ БАГА: убраны строки, которые очищали
        # поля таблицы конвертации при снятии галочки.
        # Теперь значения сенсы/гироскопа сохраняются.
        # ====================================================
        self.pubg_accel = active
        if active:
            left_game = self.left_game
            right_game = self.right_game
            if left_game == 'pubg' and right_game == 'standoff':
                self.standoff_accel = 0.42
            elif left_game == 'standoff' and right_game == 'pubg':
                self.standoff_accel = 0.42
            elif left_game == 'pubg' and right_game == 'cod':
                self.cod_accel = 300
            elif left_game == 'cod' and right_game == 'pubg':
                self.cod_accel = 300
        else:
            self.standoff_accel = 0.0
            self.cod_accel = 0
        self.update_accel_inputs()

    def update_standoff_cod_accel(self):
        if self.left_game == 'standoff' and self.right_game == 'cod':
            standoff_val = self.standoff_accel
            keys = sorted(self.standoff_cod_accel.keys())
            if standoff_val <= keys[0]:
                self.cod_accel = self.standoff_cod_accel[keys[0]]
            elif standoff_val >= keys[-1]:
                self.cod_accel = self.standoff_cod_accel[keys[-1]]
            else:
                for i in range(len(keys)-1):
                    if keys[i] <= standoff_val <= keys[i+1]:
                        ratio = (standoff_val - keys[i]) / (keys[i+1] - keys[i])
                        cod_value = self.standoff_cod_accel[keys[i]] + ratio * (self.standoff_cod_accel[keys[i+1]] - self.standoff_cod_accel[keys[i]])
                        self.cod_accel = int(round(cod_value))
                        break
        elif self.left_game == 'cod' and self.right_game == 'standoff':
            cod_val = self.cod_accel
            values = sorted(self.standoff_cod_accel.items(), key=lambda x: x[1])
            if cod_val <= values[0][1]:
                self.standoff_accel = values[0][0]
            elif cod_val >= values[-1][1]:
                self.standoff_accel = values[-1][0]
            else:
                for i in range(len(values)-1):
                    if values[i][1] <= cod_val <= values[i+1][1]:
                        ratio = (cod_val - values[i][1]) / (values[i+1][1] - values[i][1])
                        standoff_value = values[i][0] + ratio * (values[i+1][0] - values[i][0])
                        self.standoff_accel = round(standoff_value, 2)
                        break
        self.update_accel_inputs()

    def setup_conversion_table(self):
        left_game = self.left_game
        right_game = self.right_game
        mode = self.conversion_mode
        sensor = self.sensor_type
        if left_game == right_game:
            self.table_frame.add_widget(Label(text=self.get_text("same_games")))
            return
        rows = [
            (self.get_text("general_sens"), self.get_text("3person"), self.get_text("3person_dot"), "general_3p"),
            ("", self.get_text("1person"), self.get_text("standard"), "general_1p"),
            ("", self.get_text("col_holo_iron_side"), self.get_text("col_holo_aim"), "col"),
            ("", "2x", self.get_text("tactical"), "2x"),
            (self.get_text("in_scope"), "3x", "3x", "3x"),
            ("", "4x", "4x", "4x"),
            ("", "6x", "6x", "6x"),
            ("", "8x", "8x", "8x"),
            ("", "", self.get_text("sniper"), "6x_sniper")
        ]
        for standoff_label, pubg_label, cod_label, key in rows:
            left_label_text = standoff_label if left_game == "standoff" else pubg_label if left_game == "pubg" else cod_label
            right_label_text = standoff_label if right_game == "standoff" else pubg_label if right_game == "pubg" else cod_label
            font_size = dp(10) if 'кол' in left_label_text.lower() else dp(12)
            add_left = left_label_text or left_game == "standoff" or (left_game == "pubg" and key == "6x_sniper")
            if add_left:
                left_label = Label(text=left_label_text, font_size=font_size, size_hint_y=None, height=dp(40), halign='right', valign='middle')
                left_label.bind(size=left_label.setter('text_size'))
                self.table_frame.add_widget(left_label)
                state = True
                if left_game == "standoff":
                    if mode == "auto" and key == "general_3p" and left_label_text:
                        state = False
                    elif mode == "manual" and key in ["general_3p", "3x"] and left_label_text:
                        state = False
                elif left_game == "pubg" and right_game == "standoff":
                    if mode == "auto" and key == "general_3p" and left_label_text == self.get_text("3person"):
                        state = False
                    elif mode == "manual" and key in ["general_3p", "3x"] and left_label_text in [self.get_text("3person"), "3x"]:
                        state = False
                elif left_game == "pubg" and right_game == "cod":
                    if mode == "auto" and key == "general_3p" and left_label_text == self.get_text("3person"):
                        state = False
                    elif mode == "manual" and key in ["general_3p", "general_1p", "col", "2x", "3x", "4x", "6x", "8x"] and left_label_text:
                        state = False
                elif left_game == "cod" and right_game == "standoff":
                    if mode == "auto" and key == "general_3p" and left_label_text == self.get_text("3person_dot"):
                        state = False
                    elif mode == "manual" and key in ["general_3p", "3x"] and left_label_text in [self.get_text("3person_dot"), "3x"]:
                        state = False
                elif left_game == "cod" and right_game == "pubg":
                    if mode == "auto" and key == "general_3p" and left_label_text == self.get_text("3person_dot"):
                        state = False
                    elif mode == "manual" and key in ["general_3p", "general_1p", "col", "2x", "3x", "4x", "6x", "8x"] and left_label_text:
                        state = False
                if left_game == "pubg" and key == "6x_sniper":
                    state = True
                left_input = TextInput(text='', multiline=False, readonly=state, input_filter='float', size_hint_y=None, height=dp(40), padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14))
                if state:
                    left_input.background_color = [0.8, 0.8, 0.8, 1]
                    left_input.foreground_color = [0, 0, 0, 1]
                self.table_frame.add_widget(left_input)
                self.left_widgets.append((left_input, key, left_label_text))
            else:
                self.table_frame.add_widget(Label(text='', size_hint_y=None, height=dp(40)))
                left_input = TextInput(text='', multiline=False, readonly=True, size_hint_y=None, height=dp(40), padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14), background_color=[0.8, 0.8, 0.8, 1], foreground_color=[0, 0, 0, 1])
                self.table_frame.add_widget(left_input)
            right_label = Label(text=right_label_text, font_size=font_size, size_hint_y=None, height=dp(40), halign='right', valign='middle')
            right_label.bind(size=right_label.setter('text_size'))
            self.table_frame.add_widget(right_label)
            right_input = TextInput(text='', multiline=False, readonly=True, input_filter='float', size_hint_y=None, height=dp(40), padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14), background_color=[0.8, 0.8, 0.8, 1], foreground_color=[0, 0, 0, 1])
            self.table_frame.add_widget(right_input)
            self.entry_widgets.append((left_input, right_input, key, left_label_text, right_label_text))
            if mode == "auto":
                left_input.bind(text=partial(self.on_auto_text_change, key, right_input, left_input))
            else:
                left_input.bind(text=partial(self.on_manual_text_change, key, right_input, left_input, left_label_text))

    def on_auto_text_change(self, key, right_input, left_input, instance, value):
        if value:
            try:
                val = float(value)
                if val < 0:
                    instance.text = ''
                    return
            except ValueError:
                instance.text = ''
                return
        Clock.schedule_once(partial(self.update_auto_conversion, key, right_input, left_input, value), 0)

    def on_manual_text_change(self, key, right_input, left_input, left_label, instance, value):
        if value:
            try:
                val = float(value)
                if val < 0:
                    instance.text = ''
                    return
            except ValueError:
                instance.text = ''
                return
        Clock.schedule_once(partial(self.update_manual_conversion, key, right_input, left_input, left_label, value), 0)

    def update_auto_conversion(self, key, right_input, left_input, value, *args):
        if value == "":
            for lw, _, _ in self.left_widgets:
                lw.text = ""
            for li, ri, k, _, _ in self.entry_widgets:
                li.text = ""
                ri.text = ""
            return
        try:
            left_value = float(value)
        except ValueError:
            for lw, _, _ in self.left_widgets:
                lw.text = ""
            for li, ri, k, _, _ in self.entry_widgets:
                li.text = ""
                ri.text = ""
            return
        left_game = self.left_game
        right_game = self.right_game
        sensor = self.sensor_type
        if left_game == "pubg" and right_game == "cod" and key == "general_3p":
            pubg_keys = {"general_1p", "col", "2x", "3x", "4x", "6x", "8x"}
            cod_keys = {"general_3p", "general_1p", "col", "2x", "3x", "4x", "6x", "8x", "6x_sniper"}
            source_data = self.pubg_cod_sens if sensor == "sensitivity" else self.pubg_cod_gyro
            values = list(source_data["general_3p"].keys())
            if left_value <= values[0]:
                row_index = 0
                ratio = 0
            elif left_value >= values[-1]:
                row_index = len(values) - 2
                ratio = 1
            else:
                for j in range(len(values) - 1):
                    if values[j] <= left_value <= values[j+1]:
                        row_index = j
                        ratio = (left_value - values[j]) / (values[j+1] - values[j])
                        break
            for lw, k, _ in self.left_widgets:
                if k in pubg_keys:
                    lower = list(source_data[k].keys())[row_index]
                    upper = list(source_data[k].keys())[row_index + 1]
                    val = lower + ratio * (upper - lower)
                    lw.text = str(int(round(val)))
            for _, ri, k, _, _ in self.entry_widgets:
                if k in cod_keys:
                    lower = source_data[k][list(source_data[k].keys())[row_index]]
                    upper = source_data[k][list(source_data[k].keys())[row_index + 1]]
                    val = lower + ratio * (upper - lower)
                    ri.text = str(int(round(val)))
        elif left_game == "cod" and right_game == "pubg" and key == "general_3p":
            pubg_keys = {"general_3p", "general_1p", "col", "2x", "3x", "4x", "6x", "8x"}
            cod_keys = {"general_1p", "col", "2x", "3x", "4x", "6x", "8x", "6x_sniper"}
            source_data = self.pubg_cod_sens if sensor == "sensitivity" else self.pubg_cod_gyro
            values = list(source_data["general_3p"].values())
            if left_value <= values[0]:
                row_index = 0
                ratio = 0
            elif left_value >= values[-1]:
                row_index = len(values) - 2
                ratio = 1
            else:
                for j in range(len(values) - 1):
                    if values[j] <= left_value <= values[j+1]:
                        row_index = j
                        ratio = (left_value - values[j]) / (values[j+1] - values[j])
                        break
            for lw, k, _ in self.left_widgets:
                if k in cod_keys:
                    lower = list(source_data[k].values())[row_index]
                    upper = list(source_data[k].values())[row_index + 1]
                    val = lower + ratio * (upper - lower)
                    lw.text = str(int(round(val)))
            for _, ri, k, _, _ in self.entry_widgets:
                if k in pubg_keys:
                    lower = list(source_data[k].keys())[row_index]
                    upper = list(source_data[k].keys())[row_index + 1]
                    val = lower + ratio * (upper - lower)
                    ri.text = str(int(round(val)))
        elif left_game == "standoff" and right_game == "pubg":
            source_data = self.standoff_pubg_sens if sensor == "sensitivity" else self.standoff_pubg_gyro
            if key == "general_3p":
                for li, ri, k, _, _ in self.entry_widgets:
                    calculated_value = self.interpolate_value(left_value, source_data, k)
                    ri.text = str(int(round(calculated_value)))
                    if k == "3x" and li != left_input:
                        li.text = str(left_value)
        elif left_game == "pubg" and right_game == "standoff":
            source_data = self.standoff_pubg_sens if sensor == "sensitivity" else self.standoff_pubg_gyro
            if key == "general_3p":
                general_standoff = self.invert_interpolate(left_value, source_data, "general_3p", is_standoff_output=True)
                for lw, k, lbl in self.left_widgets:
                    if lw != left_input and k in ["general_1p", "col", "2x", "3x", "4x", "6x", "8x"]:
                        pubg_value = self.interpolate_value(general_standoff, source_data, k)
                        lw.text = str(int(round(pubg_value)))
                for _, ri, k, _, _ in self.entry_widgets:
                    if k in ["general_3p", "3x"]:
                        ri.text = f"{general_standoff:.2f}"
        elif left_game == "standoff" and right_game == "cod":
            source_data = self.standoff_cod_sens if sensor == "sensitivity" else self.standoff_cod_gyro
            if key == "general_3p":
                for li, ri, k, _, _ in self.entry_widgets:
                    calculated_value = self.interpolate_value(left_value, source_data, k)
                    ri.text = str(int(round(calculated_value)))
                    if k == "3x" and li != left_input:
                        li.text = str(left_value)
        elif left_game == "cod" and right_game == "standoff":
            source_data = self.standoff_cod_sens if sensor == "sensitivity" else self.standoff_cod_gyro
            if key == "general_3p":
                general_standoff = self.invert_interpolate(left_value, source_data, "general_3p", is_standoff_output=True)
                for lw, k, lbl in self.left_widgets:
                    if lw != left_input and k in ["general_1p", "col", "2x", "3x", "4x", "6x", "8x", "6x_sniper"]:
                        cod_value = self.interpolate_value(general_standoff, source_data, k)
                        lw.text = str(int(round(cod_value)))
                for _, ri, k, _, _ in self.entry_widgets:
                    if k in ["general_3p", "3x"]:
                        ri.text = f"{general_standoff:.2f}"

    def update_manual_conversion(self, key, right_input, left_input, left_label, value, *args):
        left_game = self.left_game
        right_game = self.right_game
        sensor = self.sensor_type
        if value == "":
            if left_game == "standoff" and right_game == "pubg":
                if key == "general_3p":
                    for _, ri, k, _, _ in self.entry_widgets:
                        if k in ["general_3p", "general_1p", "col", "2x"]:
                            ri.text = ""
                elif key == "3x":
                    for _, ri, k, _, _ in self.entry_widgets:
                        if k in ["3x", "4x", "6x", "8x"]:
                            ri.text = ""
            elif left_game == "pubg" and right_game == "standoff":
                if key == "general_3p":
                    for lw, k, lbl in self.left_widgets:
                        if k in ["general_1p", "col", "2x"]:
                            lw.text = ""
                    for _, ri, k, _, _ in self.entry_widgets:
                        if k in ["general_3p", "general_1p", "col", "2x"]:
                            ri.text = ""
                elif key == "3x":
                    for lw, k, lbl in self.left_widgets:
                        if k in ["4x", "6x", "8x"]:
                            lw.text = ""
                    for _, ri, k, _, _ in self.entry_widgets:
                        if k in ["3x", "4x", "6x", "8x"]:
                            ri.text = ""
            elif left_game == "pubg" and right_game == "cod":
                for _, ri, k, _, _ in self.entry_widgets:
                    if k == key:
                        ri.text = ""
                    if key == "6x" and k == "6x_sniper":
                        ri.text = ""
            elif left_game == "cod" and right_game == "pubg":
                for _, ri, k, _, _ in self.entry_widgets:
                    if k == key:
                        ri.text = ""
                    if key == "6x_sniper" and k == "6x":
                        ri.text = ""
                if key == "6x":
                    for lw, k2, lbl in self.left_widgets:
                        if k2 == "6x_sniper":
                            lw.text = ""
            elif left_game == "standoff" and right_game == "cod":
                if key == "general_3p":
                    for _, ri, k, _, _ in self.entry_widgets:
                        if k in ["general_3p", "general_1p", "col", "2x"]:
                            ri.text = ""
                elif key == "3x":
                    for _, ri, k, _, _ in self.entry_widgets:
                        if k in ["3x", "4x", "6x", "8x", "6x_sniper"]:
                            ri.text = ""
            elif left_game == "cod" and right_game == "standoff":
                if key == "general_3p":
                    for lw, k, lbl in self.left_widgets:
                        if k in ["general_1p", "col", "2x"]:
                            lw.text = ""
                    for _, ri, k, _, _ in self.entry_widgets:
                        if k in ["general_3p", "general_1p", "col", "2x"]:
                            ri.text = ""
                elif key == "3x":
                    for lw, k, lbl in self.left_widgets:
                        if k in ["4x", "6x", "8x", "6x_sniper"]:
                            lw.text = ""
                    for _, ri, k, _, _ in self.entry_widgets:
                        if k in ["3x", "4x", "6x", "8x"]:
                            ri.text = ""
            return
        try:
            left_value = float(value)
        except ValueError:
            left_input.text = ""
            return
        if left_game == "standoff" and right_game == "pubg":
            source_data = self.standoff_pubg_sens if sensor == "sensitivity" else self.standoff_pubg_gyro
            if key == "general_3p":
                for li, ri, k, _, _ in self.entry_widgets:
                    if k in ["general_3p", "general_1p", "col", "2x"]:
                        calculated_value = self.interpolate_value(left_value, source_data, k)
                        ri.text = str(int(round(calculated_value)))
            elif key == "3x":
                for li, ri, k, _, _ in self.entry_widgets:
                    if k in ["3x", "4x", "6x", "8x"]:
                        calculated_value = self.interpolate_value(left_value, source_data, k)
                        ri.text = str(int(round(calculated_value)))
        elif left_game == "pubg" and right_game == "standoff":
            source_data = self.standoff_pubg_sens if sensor == "sensitivity" else self.standoff_pubg_gyro
            if key == "general_3p":
                general_standoff = self.invert_interpolate(left_value, source_data, "general_3p", is_standoff_output=True)
                for lw, k, lbl in self.left_widgets:
                    if k in ["general_1p", "col", "2x"] and lw != left_input:
                        pubg_value = self.interpolate_value(general_standoff, source_data, k)
                        lw.text = str(int(round(pubg_value)))
                for _, ri, k, _, _ in self.entry_widgets:
                    if k == "general_3p":
                        ri.text = f"{general_standoff:.2f}"
            elif key == "3x":
                ads_standoff = self.invert_interpolate(left_value, source_data, "3x", is_standoff_output=True)
                for lw, k, lbl in self.left_widgets:
                    if k in ["4x", "6x", "8x"] and lw != left_input:
                        pubg_value = self.interpolate_value(ads_standoff, source_data, k)
                        lw.text = str(int(round(pubg_value)))
                for _, ri, k, _, _ in self.entry_widgets:
                    if k == "3x":
                        ri.text = f"{ads_standoff:.2f}"
        elif left_game == "pubg" and right_game == "cod":
            source_data = self.pubg_cod_sens if sensor == "sensitivity" else self.pubg_cod_gyro
            calculated_value = self.interpolate_value(left_value, source_data, key)
            right_input.text = str(int(round(calculated_value)))
            if key == "6x":
                calculated_value = self.interpolate_value(left_value, source_data, "6x_sniper")
                for _, ri, k, _, _ in self.entry_widgets:
                    if k == "6x_sniper":
                        ri.text = str(int(round(calculated_value)))
        elif left_game == "cod" and right_game == "pubg":
            source_data = self.pubg_cod_sens if sensor == "sensitivity" else self.pubg_cod_gyro
            if key == "6x":
                pubg_value = self.invert_interpolate(left_value, source_data, "6x")
                right_input.text = str(int(round(pubg_value)))
                sniper_value = self.interpolate_value(pubg_value, source_data, "6x_sniper")
                for lw, k, lbl in self.left_widgets:
                    if k == "6x_sniper":
                        lw.text = str(int(round(sniper_value)))
            elif key == "6x_sniper":
                pubg_value = self.invert_interpolate(left_value, source_data, "6x_sniper")
                for _, ri, k, _, _ in self.entry_widgets:
                    if k == "6x":
                        ri.text = str(int(round(pubg_value)))
            else:
                calculated_value = self.invert_interpolate(left_value, source_data, key)
                right_input.text = str(int(round(calculated_value)))
        elif left_game == "standoff" and right_game == "cod":
            source_data = self.standoff_cod_sens if sensor == "sensitivity" else self.standoff_cod_gyro
            if key == "general_3p":
                for li, ri, k, _, _ in self.entry_widgets:
                    if k in ["general_3p", "general_1p", "col", "2x"]:
                        calculated_value = self.interpolate_value(left_value, source_data, k)
                        ri.text = str(int(round(calculated_value)))
            elif key == "3x":
                for li, ri, k, _, _ in self.entry_widgets:
                    if k in ["3x", "4x", "6x", "8x", "6x_sniper"]:
                        calculated_value = self.interpolate_value(left_value, source_data, k)
                        ri.text = str(int(round(calculated_value)))
        elif left_game == "cod" and right_game == "standoff":
            source_data = self.standoff_cod_sens if sensor == "sensitivity" else self.standoff_cod_gyro
            if key == "general_3p":
                general_standoff = self.invert_interpolate(left_value, source_data, "general_3p", is_standoff_output=True)
                for lw, k, lbl in self.left_widgets:
                    if k in ["general_1p", "col", "2x"] and lw != left_input:
                        cod_value = self.interpolate_value(general_standoff, source_data, k)
                        lw.text = str(int(round(cod_value)))
                for _, ri, k, _, _ in self.entry_widgets:
                    if k == "general_3p":
                        ri.text = f"{general_standoff:.2f}"
            elif key == "3x":
                ads_standoff = self.invert_interpolate(left_value, source_data, "3x", is_standoff_output=True)
                for lw, k, lbl in self.left_widgets:
                    if k in ["4x", "6x", "8x", "6x_sniper"] and lw != left_input:
                        cod_value = self.interpolate_value(ads_standoff, source_data, k)
                        lw.text = str(int(round(cod_value)))
                for _, ri, k, _, _ in self.entry_widgets:
                    if k == "3x":
                        ri.text = f"{ads_standoff:.2f}"

    def interpolate_value(self, input_val, data, key, is_standoff_output=False):
        table = data.get(key, {})
        keys = sorted(table.keys())
        if not keys:
            return 0
        min_val, max_val = keys[0], keys[-1]
        input_val = max(min_val, min(input_val, max_val))
        if input_val <= keys[0]:
            return table[keys[0]]
        if input_val >= keys[-1]:
            return table[keys[-1]]
        for i in range(len(keys)-1):
            if keys[i] <= input_val <= keys[i+1]:
                ratio = (input_val - keys[i]) / (keys[i+1] - keys[i])
                value = table[keys[i]] + ratio * (table[keys[i+1]] - table[keys[i]])
                return round(value, 2) if is_standoff_output else int(round(value))
        return 0

    def invert_interpolate(self, input_val, data, key, is_standoff_output=False):
        table = data.get(key, {})
        if not table:
            return 0
        items = sorted(table.items())
        inputs = [k for k, v in items]
        outputs = [v for k, v in items]
        min_val, max_val = outputs[0], outputs[-1]
        input_val = max(min_val, min(input_val, max_val))
        if input_val <= outputs[0]:
            return inputs[0]
        if input_val >= outputs[-1]:
            return inputs[-1]
        for i in range(len(outputs) - 1):
            low_out, high_out = outputs[i], outputs[i + 1]
            if low_out <= input_val <= high_out:
                if high_out == low_out:
                    return inputs[i]
                ratio = (input_val - low_out) / (high_out - low_out)
                value = inputs[i] + ratio * (inputs[i + 1] - inputs[i])
                return round(value, 2) if is_standoff_output else int(round(value))
        return inputs[-1]

class RootLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.touch_start_x = None
        self.touch_start_y = None
        self.is_swiping = False

    def on_touch_down(self, touch):
        if self.app.menu.x < 0:
            if touch.x < dp(30):
                self.touch_start_x = touch.x
                self.touch_start_y = touch.y
                touch.grab(self)
                return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            delta_x = touch.x - self.touch_start_x
            delta_y = touch.y - self.touch_start_y
            if abs(delta_x) > abs(delta_y) and abs(delta_x) > dp(10):
                self.is_swiping = True
                new_x = max(-self.app.menu.width, min(0, delta_x))
                self.app.menu.x = new_x
                return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
            if self.is_swiping:
                self.is_swiping = False
                if self.app.menu.x > -self.app.menu.width / 2:
                    anim = Animation(x=0, d=0.2)
                    anim.start(self.app.menu)
                    self.app.blocker = Blocker(pos=(self.app.menu.width, 0), size=(Window.width - self.app.menu.width, Window.height))
                    self.add_widget(self.app.blocker, index=1)
                    self.app.menu_btn.text = 'X'
                else:
                    anim = Animation(x=-self.app.menu.width, d=0.2)
                    anim.start(self.app.menu)
                    self.app.menu_btn.text = '☰'
                return True
        return super().on_touch_up(touch)

class ConverterApp(App):
    def build(self):
        Window.fullscreen = 'auto'
        root = RootLayout()
        self.converter = SensitivityConverter(size_hint=(1, 1), pos=(0, 0))
        root.add_widget(self.converter)
        self.menu = Menu(orientation='vertical', size_hint=(None, None), size=(dp(250), Window.height), pos=(-dp(250), 0))
        root.add_widget(self.menu)
        self.menu_btn = Button(text='☰', font_size=dp(24), size_hint=(None, None), size=(dp(40), dp(40)), pos=(dp(10), Window.height - dp(50)))
        self.menu_btn.bind(on_press=self.toggle_menu)
        root.add_widget(self.menu_btn)
        self.build_menu()
        Window.bind(size=self.on_window_resize)
        
        self.store = JsonStore('privacy.json')
        if not self.store.exists('accepted'):
            Clock.schedule_once(lambda dt: self.show_privacy_dialog(), 0.5)

        return root
    
    def show_privacy_dialog(self):
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))

        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)  
        
        label = Label(
            text = """Политика конфиденциальности\n\nПриложение Mobile Games Sens Converter\nНЕ собирает, НЕ хранит и НЕ передаёт\nваши персональные данные.\n\nПриложение работает полностью офлайн.\nКнопка "Страница автора" открывает внешний сайт\nboosty.to — переход происходит только\nпо вашему желанию.\n\nНажав «Принять» вы соглашаетесь\nс политикой конфиденциальности.""",
            halign='center',
            valign='top',
            text_size=(dp(260), None),
            size_hint_y=None,            
        )
        label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        scroll.add_widget(label)
        content.add_widget(scroll)

        btn_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )

        decline_btn = Button(text='Отклонить')
        accept_btn = Button(text='Принять')

        btn_layout.add_widget(decline_btn)
        btn_layout.add_widget(accept_btn)
        content.add_widget(btn_layout)

        self.privacy_popup = Popup(
            title='Соглашение',
            content=content,
            size_hint=(0.9, None),
            height=dp(420),
            auto_dismiss=False  # Нельзя закрыть кликом вне окна
         )

        def on_accept(instance):
            self.store.put('accepted', value=True)  # Запоминаем согласие
            self.privacy_popup.dismiss()

        def on_decline(instance):
            self.stop()  # Закрывает приложение

        accept_btn.bind(on_press=on_accept)
        decline_btn.bind(on_press=on_decline)
        self.privacy_popup.open()

    def on_window_resize(self, instance, value):
        self.menu.height = Window.height
        self.menu.pos = (0 if self.menu.x >= 0 else -self.menu.width, 0)
        self.menu_btn.pos = (dp(10), Window.height - dp(50))
        if hasattr(self, 'blocker'):
            self.blocker.pos = (self.menu.width, 0)
            self.blocker.size = (Window.width - self.menu.width, Window.height)

    def build_menu(self):
        self.menu.clear_widgets()
        self.menu_header = Label(text=self.converter.get_text('menu'), size_hint_y=None, height=dp(40))
        self.menu.add_widget(self.menu_header)
        self.acc = Accordion(orientation='vertical')
        self.menu.add_widget(self.acc)
        self.settings_item = AccordionItem(title=self.converter.get_text('settings'))
        self.acc.add_widget(self.settings_item)
        inner = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.settings_item.add_widget(inner)
        self.lang_label = Label(text=self.converter.get_text('language'), size_hint_y=None, height=dp(30))
        inner.add_widget(self.lang_label)
        self.lang_spinner = Spinner(
            text=self.converter.langs[self.converter.language],
            values=list(self.converter.langs.values()),
            size_hint_y=None,
            height=dp(44)
        )
        self.lang_spinner.bind(text=self.converter.on_lang_change)
        inner.add_widget(self.lang_spinner)

        self.about_item = AccordionItem(title=self.converter.get_text('about_title'))
        self.acc.add_widget(self.about_item)
        about_inner = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        self.about_item.add_widget(about_inner)

        self.about_label = Label(
            text=self.converter.get_text('about_text'),
            size_hint_y=None,
            height=dp(280),
            halign='left',
            valign='top',
            text_size=(dp(230), None),
            font_size=dp(13),
            markup=True,
            color=(0.2, 0.4, 0.9, 1)  # ← синий цвет (R, G, B, прозрачность)
        )
        about_inner.add_widget(self.about_label)

        self.donate_label = Label(
            text=f'[u][color=3366cc]{self.converter.get_text("donate_button")}[/color][/u]',
            size_hint_y=None,
            height=dp(40),
            markup=True,
            font_size=dp(14),
            halign='left',
            valign='middle'
        )
        self.donate_label.bind(on_touch_down=self.on_donate_click)
        about_inner.add_widget(self.donate_label)

    def update_menu_texts(self):
        self.menu_header.text = self.converter.get_text('menu')
        self.settings_item.title = self.converter.get_text('settings')
        self.lang_label.text = self.converter.get_text('language')
        self.about_item.title = self.converter.get_text('about_title')
        self.about_label.text = self.converter.get_text('about_text')
        self.donate_label.text = f'[u][color=3366cc]{self.converter.get_text("donate_button")}[/color][/u]'

    def on_donate_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            webbrowser.open('https://haevlob.github.io/privacy-policy/')
            return True
        return False

    def toggle_menu(self, *args):
        if self.menu.x < 0:
            anim = Animation(x=0, d=0.2)
            anim.start(self.menu)
            self.blocker = Blocker(pos=(dp(250), 0), size=(Window.width - dp(250), Window.height))
            self.root.add_widget(self.blocker, index=1)
            self.menu_btn.text = 'X'
        else:
            anim = Animation(x=-dp(250), d=0.2)
            anim.start(self.menu)
            self.root.remove_widget(self.blocker)
            del self.blocker
            self.menu_btn.text = '☰'

if __name__ == '__main__':
    ConverterApp().run()
