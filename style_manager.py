class StyleManager:
    @staticmethod
    def get_style(bg_rgba=(20, 60, 120, 180), text_rgba=(255, 255, 255, 255)):
        r_b, g_b, b_b, a_b = bg_rgba
        r_t, g_t, b_t, a_t = text_rgba
        
        # 轉換為 CSS RGBA 格式 (CSS Alpha 為 0-1)
        bg_css = f"rgba({r_b}, {g_b}, {b_b}, {a_b/255.0})"
        text_css = f"rgba({r_t}, {g_t}, {b_t}, {a_t/255.0})"
        # 卡片背景稍微比底色淡一點且增加一點點透明感
        card_bg = f"rgba(255, 255, 255, 0.15)"
        
        return f"""
            #MainWidget {{
                background-color: {bg_css};
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .Card {{
                background-color: {card_bg};
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            QLabel {{
                color: {text_css};
                font-family: "Microsoft JhengHei", "Segoe UI", sans-serif;
            }}
            #DayLabel {{
                font-size: 32px;
                font-weight: 200;
                text-transform: uppercase;
            }}
            #DateLabel {{
                font-size: 14px;
                color: {text_css}; /* 使用者色，透明度由傳入參數決定 */
            }}
            #TempLabel {{
                font-size: 64px;
                font-weight: bold;
            }}
            #WeatherIcon {{
                font-size: 72px;
                margin-left: 10px;
            }}
            #ForecastIcon {{
                font-size: 24px;
                margin: 5px 0;
            }}
            #BigTimeLabel {{
                font-size: 38px;
                font-weight: bold;
                margin-top: 5px;
            }}
            #LocationLabel {{
                font-size: 20px;
                color: {text_css};
                margin-bottom: 10px;
            }}
            #DescLabel {{
                font-size: 16px;
            }}
            .DetailLabel {{
                font-size: 12px;
                opacity: 0.7;
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
