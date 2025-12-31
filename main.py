import sys
import json
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QMenu, QFrame, QGridLayout, QColorDialog)
from PyQt6.QtCore import Qt, QTimer, QPoint, QTime
from PyQt6.QtGui import QColor
from weather_service import WeatherService
from style_manager import StyleManager

class DesktopWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.weather_service = WeatherService("Taipei")
        self.cities = {
            "台北": "Taipei", "新北": "New_Taipei", "桃園": "Taoyuan",
            "台中": "Taichung", "台南": "Tainan", "高雄": "Kaohsiung", "新竹": "Hsinchu"
        }
        self.current_city_name = "台北"
        
        # 預設風格數據
        self.bg_color = QColor(20, 60, 120)
        self.bg_alpha = 180
        self.text_color = QColor(255, 255, 255)
        self.text_alpha = 255
        self.current_opacity = 0.95 # 整體視窗不透明度
        
        self.init_ui()
        self.setup_timers()
        
    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 建立外殼佈局
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        
        # 建立主要視覺容器 (負責背景與圓角)
        self.main_container = QFrame()
        self.main_container.setObjectName("MainWidget")
        self.root_layout.addWidget(self.main_container)
        
        self.main_layout = QVBoxLayout(self.main_container)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)
        
        # --- Top Row (Main & Details) ---
        top_layout = QHBoxLayout()
        
        # 1. Main Info Card (左上)
        self.main_card = QFrame()
        self.main_card.setProperty("class", "Card")
        self.main_card.setFixedWidth(280)
        self.main_card.setFixedHeight(220)
        main_vbox = QVBoxLayout(self.main_card)
        
        self.day_label = QLabel("MONDAY")
        self.day_label.setObjectName("DayLabel")
        self.date_label = QLabel("APRIL 19")
        self.date_label.setObjectName("DateLabel")
        
        temp_hbox = QHBoxLayout()
        self.temp_label = QLabel("18°C")
        self.temp_label.setObjectName("TempLabel")
        temp_hbox.addWidget(self.temp_label)
        temp_hbox.addStretch()
        
        self.desc_label = QLabel("PARTLY CLOUDY")
        self.desc_label.setObjectName("DescLabel")
        
        main_vbox.addWidget(self.day_label)
        main_vbox.addWidget(self.date_label)
        main_vbox.addStretch()
        main_vbox.addLayout(temp_hbox)
        main_vbox.addWidget(self.desc_label)
        
        # 2. Detail Card (右上)
        self.detail_card = QFrame()
        self.detail_card.setProperty("class", "Card")
        self.detail_card.setFixedWidth(200)
        self.detail_card.setFixedHeight(220)
        detail_grid = QGridLayout(self.detail_card)
        
        self.detail_widgets = {}
        # 改為顯示時間、地點與日出日落
        self.time_label_big = QLabel("15:20:00")
        self.time_label_big.setObjectName("BigTimeLabel")
        self.time_label_big.setAlignment(Qt.AlignmentFlag.AlignCenter)
        detail_grid.addWidget(self.time_label_big, 0, 0, 1, 2)
        
        self.location_label = QLabel(self.current_city_name)
        self.location_label.setObjectName("LocationLabel")
        self.location_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        detail_grid.addWidget(self.location_label, 1, 0, 1, 2)
        
        detail_grid.addWidget(QLabel("Sunrise"), 2, 0)
        self.sunrise_val = QLabel("--")
        detail_grid.addWidget(self.sunrise_val, 2, 1)
        
        detail_grid.addWidget(QLabel("Sunset"), 3, 0)
        self.sunset_val = QLabel("--")
        detail_grid.addWidget(self.sunset_val, 3, 1)
        
        self.detail_widgets["sunrise"] = self.sunrise_val
        self.detail_widgets["sunset"] = self.sunset_val
            
        top_layout.addWidget(self.main_card)
        top_layout.addWidget(self.detail_card)
        
        # --- Bottom Row (Forecast) ---
        self.forecast_area = QFrame()
        self.forecast_layout = QHBoxLayout(self.forecast_area)
        self.forecast_layout.setContentsMargins(0, 0, 0, 0)
        self.forecast_widgets = []
        
        self.main_layout.addLayout(top_layout)
        self.main_layout.addWidget(self.forecast_area)
        
        self.update_styles()
        
        self.old_pos = None

    def setup_timers(self):
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time_and_date)
        self.time_timer.start(1000)
        self.update_time_and_date()
        
        self.weather_timer = QTimer(self)
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(1800000)
        self.update_weather()

    def update_time_and_date(self):
        now = datetime.now()
        self.day_label.setText(now.strftime("%A").upper())
        self.date_label.setText(now.strftime("%B %d, %Y").upper())
        self.time_label_big.setText(now.strftime("%H:%M:%S"))

    def update_weather(self):
        data = self.weather_service.fetch_weather()
        if not data: return
        
        self.temp_label.setText(f"{data['temp_C']}°C")
        self.desc_label.setText(data['desc'].upper())
        
        # 更新細項
        self.location_label.setText(self.current_city_name)
        self.detail_widgets["sunrise"].setText(data["sunrise"])
        self.detail_widgets["sunset"].setText(data["sunset"])
        
        # 更新預報
        # 先清除舊的
        for i in reversed(range(self.forecast_layout.count())): 
            self.forecast_layout.itemAt(i).widget().setParent(None)
            
        for day in data["forecast"]:
            f_card = QFrame()
            f_card.setProperty("class", "Card")
            f_vbox = QVBoxLayout(f_card)
            f_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            d_l = QLabel(day["day"].upper())
            d_l.setProperty("class", "ForecastDay")
            t_l = QLabel(f"{day['max']}° / {day['min']}°")
            t_l.setProperty("class", "ForecastTemp")
            
            f_vbox.addWidget(d_l)
            f_vbox.addWidget(t_l)
            self.forecast_layout.addWidget(f_card)

    def update_styles(self):
        bg_rgba = (self.bg_color.red(), self.bg_color.green(), self.bg_color.blue(), self.bg_alpha)
        text_rgba = (self.text_color.red(), self.text_color.green(), self.text_color.blue(), self.text_alpha)
        
        style = StyleManager.get_style(bg_rgba, text_rgba)
        self.main_container.setStyleSheet(style) # 樣式套用在容器上
        self.setWindowOpacity(self.current_opacity)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        
        city_menu = context_menu.addMenu("切換城市")
        for name, code in self.cities.items():
            action = city_menu.addAction(name)
            action.triggered.connect(lambda checked, n=name, c=code: self.change_city(n, c))

        # 風格與顏色設定
        settings_menu = context_menu.addMenu("外觀設定")
        
        # 1. 背景調整
        bg_menu = settings_menu.addMenu("背景顏色")
        bg_pick = bg_menu.addAction("選擇底色")
        bg_pick.triggered.connect(self.pick_bg_color)
        bg_alpha_menu = bg_menu.addMenu("背景透明度")
        for val in [50, 100, 150, 200, 255]:
            act = bg_alpha_menu.addAction(f"{int(val/255.0*100)}%")
            act.triggered.connect(lambda checked, v=val: self.change_bg_alpha(v))
            
        # 2. 文字調整
        text_menu = settings_menu.addMenu("文字顏色")
        text_pick = text_menu.addAction("選擇字型顏色")
        text_pick.triggered.connect(self.pick_text_color)
        text_alpha_menu = text_menu.addMenu("文字透明度")
        for val in [50, 100, 150, 200, 255]:
            act = text_alpha_menu.addAction(f"{int(val/255.0*100)}%")
            act.triggered.connect(lambda checked, v=val: self.change_text_alpha(v))

        # 3. 整體視窗透明度
        opac_menu = settings_menu.addMenu("視窗整體透明度")
        for val in [0.4, 0.6, 0.8, 1.0]:
            action = opac_menu.addAction(f"{int(val*100)}%")
            action.triggered.connect(lambda checked, v=val: self.change_opacity(v))
            
        context_menu.addSeparator()
        quit_action = context_menu.addAction("結束")
        quit_action.triggered.connect(QApplication.instance().quit)
        context_menu.exec(event.globalPos())

    def pick_bg_color(self):
        color = QColorDialog.getColor(self.bg_color, self, "選擇背景顏色")
        if color.isValid():
            self.bg_color = color
            self.update_styles()

    def pick_text_color(self):
        color = QColorDialog.getColor(self.text_color, self, "選擇文字顏色")
        if color.isValid():
            self.text_color = color
            self.update_styles()

    def change_bg_alpha(self, val):
        self.bg_alpha = val
        self.update_styles()

    def change_text_alpha(self, val):
        self.text_alpha = val
        self.update_styles()

    def change_city(self, name, code):
        self.current_city_name = name
        self.weather_service.city = code
        self.weather_service.url = f"https://wttr.in/{code}?format=j1"
        self.update_weather()

    def change_opacity(self, val):
        self.current_opacity = val
        self.update_styles()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = DesktopWidget()
    widget.show()
    sys.exit(app.exec())
