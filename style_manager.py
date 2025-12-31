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
                font-size: 56px;
                font-weight: bold;
                color: {text_css};
            }}
            #WeatherIcon {{
                font-size: 64px;
                margin-left: 5px;
            }}
            #ForecastIcon {{
                font-size: 24px;
                margin: 5px 0;
            }}
            #BigTimeLabel {{
                font-size: 48px;
                font-weight: bold;
                margin-top: 8px;
            }}
            #LocationLabel {{
                font-size: 14px;
                color: {text_css};
                opacity: 0.6;
                margin-top: 0px;
            }}
            .TimerBtn {{
                background-color: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                color: {text_css};
                font-size: 14px;
                padding: 4px;
            }}
            .TimerBtn:hover {{
                background-color: rgba(255, 255, 255, 0.4);
            }}
            .TimerInput {{
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: {text_css};
                font-size: 20px;
                font-weight: bold;
                border-radius: 5px;
            }}
            #TimerDisplay {{
                font-size: 44px;
                font-weight: bold;
                color: {text_css};
            }}
            .TodoInput {{
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: {text_css};
                font-size: 12px;
                border-radius: 5px;
                padding: 2px 5px;
            }}
            .TodoItem {{
                padding: 2px 5px;
                font-size: 11px;
                color: {text_css};
            }}
            .TodoItemDone {{
                color: rgba(255, 255, 255, 0.3);
                text-decoration: line-through;
            }}
            .TodoDelBtn {{
                background: transparent;
                border: none;
                color: rgba(255, 255, 255, 0.2);
                font-size: 13px;
                font-weight: bold;
                padding: 0 4px;
            }}
            .TodoDelBtn:hover {{
                color: #ff5555;
            }}
            #TodoTitle {{
                font-size: 13px;
                font-weight: bold;
                margin-bottom: 2px;
                opacity: 0.8;
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
            .RefreshBtn {{
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                color: {text_css};
                font-size: 14px;
                font-weight: bold;
                padding: 2px;
            }}
            .RefreshBtn:hover {{
                background-color: rgba(255, 255, 255, 0.3);
            }}
            QProgressBar {{
                background-color: rgba(255, 255, 255, 0.05);
                border: none;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                border-radius: 2px;
            }}
            /* CPU 基調色 (綠) */
            .CpuBar::chunk {{
                background-color: rgba(0, 230, 118, 0.6);
            }}
            /* RAM 基調色 (黃) */
            .RamBar::chunk {{
                background-color: rgba(255, 214, 0, 0.6);
            }}
            /* Disk 基調色 (灰銀) */
            .DiskBar::chunk {{
                background-color: rgba(180, 200, 220, 0.6);
            }}
            /* 狀態色擴充 */
            QProgressBar[status="warning"]::chunk {{
                background-color: rgba(255, 145, 0, 0.8);
            }}
            QProgressBar[status="critical"]::chunk {{
                background-color: rgba(255, 23, 68, 0.9);
            }}
            .NetDownBar::chunk {{
                background-color: rgba(0, 180, 255, 0.6);
            }}
            .NetUpBar::chunk {{
                background-color: rgba(180, 100, 255, 0.6);
            }}
        """
