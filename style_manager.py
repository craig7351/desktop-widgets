class StyleManager:
    @staticmethod
    def get_style(mode="glass", opacity=0.8):
        # 基礎容器樣式
        base_container = f"""
            #MainWidget {{
                background-color: rgba(255, 255, 255, {opacity});
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            QLabel {{
                color: #2c3e50;
                font-family: "Microsoft JhengHei", "Segoe UI", sans-serif;
            }}
            #TimeLabel {{
                font-size: 48px;
                font-weight: bold;
            }}
            #WeatherLabel {{
                font-size: 18px;
            }}
        """
        
        if mode == "dark":
            base_container = base_container.replace("rgba(255, 255, 255,", f"rgba(30, 30, 30,")
            base_container = base_container.replace("color: #2c3e50;", "color: #ecf0f1;")
            base_container = base_container.replace("border: 1px solid rgba(255, 255, 255, 0.2);", "border: 1px solid rgba(0, 0, 0, 0.3);")
            
        elif mode == "glass":
            # 毛玻璃質感透過視窗屬性實現，這裡主要是字體與基礎背景
            base_container = f"""
                #MainWidget {{
                    background-color: rgba(255, 255, 255, {opacity * 0.4});
                    border-radius: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.5);
                }}
                QLabel {{
                    color: white;
                    font-family: "Microsoft JhengHei", "Segoe UI", sans-serif;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
                }}
                #TimeLabel {{
                    font-size: 52px;
                    font-weight: 800;
                }}
                #WeatherLabel {{
                    font-size: 20px;
                    font-weight: 400;
                }}
            """
            
        return base_container
