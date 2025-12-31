import sys
import json
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QMenu, QFrame, QGridLayout)
from PyQt6.QtCore import Qt, QTimer, QPoint, QTime
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
        self.current_mode = "glass"
        self.current_opacity = 0.85
        
        self.init_ui()
        self.setup_timers()
        
    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setObjectName("MainWidget")
        
        self.main_layout = QVBoxLayout()
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
        items = [("UV Index", "uv"), ("Wind", "wind"), ("Humidity", "humidity"), 
                 ("Sunrise", "sunrise"), ("Sunset", "sunset"), ("Pressure", "pressure")]
        
        for i, (label, key) in enumerate(items):
            l = QLabel(label)
            l.setProperty("class", "DetailLabel")
            v = QLabel("--")
            v.setProperty("class", "DetailValue")
            detail_grid.addWidget(l, i, 0)
            detail_grid.addWidget(v, i, 1)
            self.detail_widgets[key] = v
            
        top_layout.addWidget(self.main_card)
        top_layout.addWidget(self.detail_card)
        
        # --- Bottom Row (Forecast) ---
        self.forecast_area = QFrame()
        self.forecast_layout = QHBoxLayout(self.forecast_area)
        self.forecast_layout.setContentsMargins(0, 0, 0, 0)
        self.forecast_widgets = []
        
        self.main_layout.addLayout(top_layout)
        self.main_layout.addWidget(self.forecast_area)
        
        self.setLayout(self.main_layout)
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

    def update_weather(self):
        data = self.weather_service.fetch_weather()
        if not data: return
        
        self.temp_label.setText(f"{data['temp_C']}°C")
        self.desc_label.setText(data['desc'].upper())
        
        # 更新細項
        self.detail_widgets["uv"].setText(str(data["uv"]))
        self.detail_widgets["wind"].setText(data["wind"])
        self.detail_widgets["humidity"].setText(f"{data['humidity']}%")
        self.detail_widgets["pressure"].setText(f"{data['pressure']} mb")
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
        style = StyleManager.get_style(self.current_mode, self.current_opacity)
        self.setStyleSheet(style)
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

        opac_menu = context_menu.addMenu("透明度")
        for val in [0.4, 0.6, 0.8, 1.0]:
            action = opac_menu.addAction(f"{int(val*100)}%")
            action.triggered.connect(lambda checked, v=val: self.change_opacity(v))
            
        context_menu.addSeparator()
        quit_action = context_menu.addAction("結束")
        quit_action.triggered.connect(QApplication.instance().quit)
        context_menu.exec(event.globalPos())

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
