class StyleManager:
    @staticmethod
    def get_style(mode="glass", opacity=0.8):
        # 基礎顏色定義 (深藍色調，匹配圖片)
        bg_color = f"rgba(20, 60, 120, {opacity * 0.7})"
        card_bg = "rgba(255, 255, 255, 0.15)"
        text_white = "#FFFFFF"
        text_accent = "#FFD700" # 金黃色 (日落/UV)
        
        return f"""
            #MainWidget {{
                background-color: {bg_color};
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .Card {{
                background-color: {card_bg};
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            QLabel {{
                color: {text_white};
                font-family: "Microsoft JhengHei", "Segoe UI", sans-serif;
            }}
            #DayLabel {{
                font-size: 32px;
                font-weight: 200;
                text-transform: uppercase;
            }}
            #DateLabel {{
                font-size: 14px;
                color: rgba(255,255,255,0.7);
            }}
            #TempLabel {{
                font-size: 64px;
                font-weight: bold;
            }}
            #DescLabel {{
                font-size: 16px;
                color: rgba(255,255,255,0.8);
            }}
            .DetailLabel {{
                font-size: 12px;
                color: rgba(255,255,255,0.7);
            }}
            .DetailValue {{
                font-size: 13px;
                font-weight: bold;
            }}
            .ForecastDay {{
                font-size: 12px;
                font-weight: bold;
            }}
            .ForecastTemp {{
                font-size: 14px;
            }}
        """
