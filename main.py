import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMenu, QSlider
from PyQt6.QtCore import Qt, QTimer, QPoint, QTime
from PyQt6.QtGui import QAction, QCursor
from weather_service import WeatherService
from style_manager import StyleManager

class DesktopWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.weather_service = WeatherService("Taipei")
        self.cities = {
            "台北": "Taipei",
            "新北": "New_Taipei",
            "桃園": "Taoyuan",
            "台中": "Taichung",
            "台南": "Tainan",
            "高雄": "Kaohsiung",
            "新竹": "Hsinchu"
        }
        self.current_city_name = "台北"
        self.current_mode = "glass"
        self.current_opacity = 0.8
        
        self.init_ui()
        self.setup_timers()
        
    def init_ui(self):
        # 視窗屬性設定：無邊框、置頂、背景透明
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout()
        self.setObjectName("MainWidget")
        
        # 時間標籤
        self.time_label = QLabel()
        self.time_label.setObjectName("TimeLabel")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.time_label)
        
        # 天氣標籤
        self.weather_label = QLabel("讀取天氣中...")
        self.weather_label.setObjectName("WeatherLabel")
        self.weather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.weather_label)
        
        self.setLayout(self.layout)
        self.update_styles()
        
        # 拖曳功能相關變數
        self.old_pos = None

    def setup_timers(self):
        # 時間更新定時器 (每秒)
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        self.update_time()
        
        # 天氣更新定時器 (每 30 分鐘)
        self.weather_timer = QTimer(self)
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(1800000)
        self.update_weather()

    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.time_label.setText(current_time)

    def update_weather(self):
        weather_info = self.weather_service.fetch_weather()
        self.weather_label.setText(f"{self.current_city_name}: {weather_info}")

    def update_styles(self):
        style = StyleManager.get_style(self.current_mode, self.current_opacity)
        self.setStyleSheet(style)
        # 強制套用窗口整體透明度 (修復透明度沒反應問題)
        self.setWindowOpacity(self.current_opacity)

    # --- 鼠標事件處理 (實現拖曳) ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    # --- 右鍵選單 ---
    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        
        # 風格切換
        style_menu = context_menu.addMenu("切換風格")
        glass_action = style_menu.addAction("玻璃擬態")
        dark_action = style_menu.addAction("暗色模式")
        light_action = style_menu.addAction("亮色模式")
        
        glass_action.triggered.connect(lambda: self.change_mode("glass"))
        dark_action.triggered.connect(lambda: self.change_mode("dark"))
        light_action.triggered.connect(lambda: self.change_mode("light"))
        
        # 城市切換
        city_menu = context_menu.addMenu("切換城市")
        for name, code in self.cities.items():
            action = city_menu.addAction(name)
            # 使用 closure 捕捉變數
            action.triggered.connect(lambda checked, n=name, c=code: self.change_city(n, c))

        # 透明度調整
        opac_menu = context_menu.addMenu("透明度")
        for val in [0.2, 0.4, 0.6, 0.8, 1.0]:
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
        self.weather_label.setText(f"{name}: 獲取中...")
        self.update_weather()

    def change_mode(self, mode):
        self.current_mode = mode
        self.update_styles()

    def change_opacity(self, val):
        self.current_opacity = val
        self.update_styles()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = DesktopWidget()
    widget.show()
    sys.exit(app.exec())
