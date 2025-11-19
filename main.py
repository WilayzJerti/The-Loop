import flet as ft
import json
import time
from datetime import datetime, timedelta
import os

class PomodoroTimer:
    def __init__(self):
        # Основные настройки таймера по умолчанию
        self.work_time = 25 * 60  # 25 минут в секундах
        self.break_time = 5 * 60  # 5 минут в секундах
        self.long_break_time = 15 * 60  # 15 минут длинного перерыва
        self.sessions_before_long_break = 4
        
        # Текущее состояние
        self.current_time = self.work_time
        self.is_running = False
        self.is_work_time = True
        self.session_count = 0
        self.total_pomodoros = 0
        
        # Статистика
        self.daily_stats = {"work": 0, "break": 0, "pomodoros": 0}
        self.weekly_stats = {"work": 0, "break": 0, "pomodoros": 0}
        self.monthly_stats = {"work": 0, "break": 0, "pomodoros": 0}
        
        # Пользовательские данные
        self.tags = [
            {"name": "Работа", "color": ft.Colors.RED},
            {"name": "Учеба", "color": ft.Colors.BLUE},
            {"name": "Личное", "color": ft.Colors.GREEN}
        ]
        self.current_tag = "Работа"
        self.points = 0
        self.shop_items = [
            {"name": "1 час игры", "cost": 100, "description": "1 час игры на ПК"},
            {"name": "Кофе-брейк", "cost": 50, "description": "15 минут перерыва с кофе"},
            {"name": "Вечер кино", "cost": 200, "description": "Вечер просмотра фильма"}
        ]
        
        # Настройки темы
        self.themes = {
            "light": {
                "primary": ft.Colors.BLUE,
                "background": ft.Colors.WHITE,
                "surface": ft.Colors.GREY_100,
                "on_primary": ft.Colors.WHITE,
                "on_background": ft.Colors.BLACK,
                "on_surface": ft.Colors.BLACK
            },
            "dark": {
                "primary": ft.Colors.BLUE_700,
                "background": ft.Colors.BLACK,
                "surface": ft.Colors.GREY_900,
                "on_primary": ft.Colors.WHITE,
                "on_background": ft.Colors.WHITE,
                "on_surface": ft.Colors.WHITE
            },
            "purple": {
                "primary": ft.Colors.PURPLE,
                "background": ft.Colors.PURPLE_50,
                "surface": ft.Colors.PURPLE_100,
                "on_primary": ft.Colors.WHITE,
                "on_background": ft.Colors.BLACK,
                "on_surface": ft.Colors.BLACK
            },
            "blue": {
                "primary": ft.Colors.BLUE,
                "background": ft.Colors.BLUE_50,
                "surface": ft.Colors.BLUE_100,
                "on_primary": ft.Colors.WHITE,
                "on_background": ft.Colors.BLACK,
                "on_surface": ft.Colors.BLACK
            },
            "green": {
                "primary": ft.Colors.GREEN,
                "background": ft.Colors.GREEN_50,
                "surface": ft.Colors.GREEN_100,
                "on_primary": ft.Colors.WHITE,
                "on_background": ft.Colors.BLACK,
                "on_surface": ft.Colors.BLACK
            }
        }
        self.current_theme = "light"
        
        # Загрузка данных
        self.load_data()

    def format_time(self, seconds):
        """Форматирование времени в MM:SS"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def start_timer(self):
        """Запуск таймера"""
        self.is_running = True

    def pause_timer(self):
        """Пауза таймера"""
        self.is_running = False

    def reset_timer(self):
        """Сброс таймера"""
        self.is_running = False
        if self.is_work_time:
            self.current_time = self.work_time
        else:
            self.current_time = self.break_time

    def toggle_timer(self):
        """Переключение состояния таймера"""
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()

    def update_timer(self):
        """Обновление таймера"""
        if self.is_running:
            self.current_time -= 1
            if self.current_time <= 0:
                self.complete_session()

    def complete_session(self):
        """Завершение сессии"""
        if self.is_work_time:
            # Завершение рабочей сессии
            self.total_pomodoros += 1
            self.session_count += 1
            self.daily_stats["pomodoros"] += 1
            self.daily_stats["work"] += self.work_time
            self.points += 10  # Начисление очков за завершенный помодоро
            
            # Определение типа перерыва
            if self.session_count % self.sessions_before_long_break == 0:
                self.current_time = self.long_break_time
            else:
                self.current_time = self.break_time
                
            self.is_work_time = False
        else:
            # Завершение перерыва
            self.daily_stats["break"] += self.break_time
            self.current_time = self.work_time
            self.is_work_time = True
            
        self.is_running = False

    def add_tag(self, name, color):
        """Добавление нового тега"""
        self.tags.append({"name": name, "color": color})

    def add_shop_item(self, name, cost, description):
        """Добавление нового товара в магазин"""
        self.shop_items.append({"name": name, "cost": cost, "description": description})

    def buy_item(self, item_index):
        """Покупка товара из магазина"""
        item = self.shop_items[item_index]
        if self.points >= item["cost"]:
            self.points -= item["cost"]
            return True
        return False

    def set_theme(self, theme_name):
        """Установка темы"""
        self.current_theme = theme_name

    def save_data(self):
        """Сохранение данных в файл"""
        data = {
            "tags": self.tags,
            "shop_items": self.shop_items,
            "points": self.points,
            "theme": self.current_theme,
            "work_time": self.work_time,
            "break_time": self.break_time,
            "long_break_time": self.long_break_time,
            "sessions_before_long_break": self.sessions_before_long_break
        }
        with open("pomodoro_data.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        """Загрузка данных из файла"""
        try:
            if os.path.exists("pomodoro_data.json"):
                with open("pomodoro_data.json", "r") as f:
                    data = json.load(f)
                    self.tags = data.get("tags", self.tags)
                    self.shop_items = data.get("shop_items", self.shop_items)
                    self.points = data.get("points", 0)
                    self.current_theme = data.get("theme", "light")
                    self.work_time = data.get("work_time", 25 * 60)
                    self.break_time = data.get("break_time", 5 * 60)
                    self.long_break_time = data.get("long_break_time", 15 * 60)
                    self.sessions_before_long_break = data.get("sessions_before_long_break", 4)
        except:
            pass

def main(page: ft.Page):
    timer = PomodoroTimer()
    
    # Элементы интерфейса
    time_display = ft.Text(
        timer.format_time(timer.current_time),
        size=80,
        weight=ft.FontWeight.BOLD
    )
    
    status_text = ft.Text(
        "Рабочее время" if timer.is_work_time else "Перерыв",
        size=20,
        weight=ft.FontWeight.BOLD
    )
    
    tag_text = ft.Text(f"Тег: {timer.current_tag}", size=16)
    points_text = ft.Text(f"Очки: {timer.points}", size=16, weight=ft.FontWeight.BOLD)
    
    # Кнопки управления таймером
    start_pause_btn = ft.ElevatedButton("Старт", on_click=lambda _: toggle_timer())
    reset_btn = ft.ElevatedButton("Сброс", on_click=lambda _: reset_timer())
    
    # Статистика
    stats_text = ft.Column()
    
    def on_tag_change(e):
        timer.current_tag = tag_dropdown.value
        update_interface()

    # Выбор тега
    tag_dropdown = ft.Dropdown(
        label="Выберите тег",
        options=[],
        on_change=on_tag_change
    )
    
    def on_work_time_change(e):
        try:
            timer.work_time = int(work_time_field.value) * 60
            if not timer.is_running and timer.is_work_time:
                timer.current_time = timer.work_time
            update_interface()
        except:
            pass

    # Настройки времени
    work_time_field = ft.TextField(
        label="Время работы (мин)",
        value=str(timer.work_time // 60),
        on_change=on_work_time_change
    )
    
    def on_break_time_change(e):
        try:
            timer.break_time = int(break_time_field.value) * 60
            if not timer.is_running and not timer.is_work_time:
                timer.current_time = timer.break_time
            update_interface()
        except:
            pass

    break_time_field = ft.TextField(
        label="Время перерыва (мин)",
        value=str(timer.break_time // 60),
        on_change=on_break_time_change
    )
    
    # Магазин
    shop_items_column = ft.Column()
    
    # Добавление нового товара
    new_item_name = ft.TextField(label="Название товара")
    new_item_cost = ft.TextField(label="Стоимость")
    new_item_desc = ft.TextField(label="Описание")
    
    def on_theme_change(e):
        timer.set_theme(theme_radio.value)
        update_interface()

    # Темы
    theme_radio = ft.RadioGroup(
        content=ft.Column(),
        on_change=on_theme_change
    )

    def update_interface():
        """Обновление интерфейса"""
        # Обновление времени
        time_display.value = timer.format_time(timer.current_time)
        
        # Обновление статуса
        status_text.value = "Рабочее время" if timer.is_work_time else "Перерыв"
        status_text.color = ft.Colors.RED if timer.is_work_time else ft.Colors.GREEN
        
        # Обновление текста кнопки
        start_pause_btn.text = "Пауза" if timer.is_running else "Старт"
        
        # Обновление тега и очков
        tag_text.value = f"Тег: {timer.current_tag}"
        points_text.value = f"Очки: {timer.points}"
        
        # Обновление статистики
        update_stats()
        
        # Обновление темы
        apply_theme()
        
        page.update()

    def update_stats():
        """Обновление отображения статистики"""
        stats_text.controls.clear()
        stats_text.controls.extend([
            ft.Text("Статистика за день:", weight=ft.FontWeight.BOLD),
            ft.Text(f"Помодоро: {timer.daily_stats['pomodoros']}"),
            ft.Text(f"Работа: {timer.daily_stats['work'] // 60} мин"),
            ft.Text(f"Перерывы: {timer.daily_stats['break'] // 60} мин"),
            ft.Divider(),
            ft.Text("Общая статистика:", weight=ft.FontWeight.BOLD),
            ft.Text(f"Всего помодоро: {timer.total_pomodoros}"),
            ft.Text(f"Сессии: {timer.session_count}"),
        ])

    def update_tag_dropdown():
        """Обновление выпадающего списка тегов"""
        tag_dropdown.options.clear()
        for tag in timer.tags:
            tag_dropdown.options.append(
                ft.dropdown.Option(
                    text=tag["name"],
                    # Flet пока не поддерживает прямой цвет для Dropdown
                )
            )
        tag_dropdown.value = timer.current_tag

    def update_shop_items():
        """Обновление списка товаров в магазине"""
        shop_items_column.controls.clear()
        for i, item in enumerate(timer.shop_items):
            shop_items_column.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(item["name"], weight=ft.FontWeight.BOLD),
                            ft.Text(item["description"]),
                            ft.Text(f"Стоимость: {item['cost']} очков"),
                            ft.ElevatedButton(
                                "Купить",
                                on_click=lambda e, idx=i: buy_shop_item(idx)
                            )
                        ]),
                        padding=10
                    )
                )
            )

    def update_theme_selector():
        """Обновление выбора темы"""
        theme_radio.content.controls.clear()
        for theme_name in timer.themes.keys():
            theme_radio.content.controls.append(
                ft.Radio(value=theme_name, label=theme_name.capitalize())
            )
        theme_radio.value = timer.current_theme

    def apply_theme():
        """Применение выбранной темы"""
        theme = timer.themes[timer.current_theme]
        page.bgcolor = theme["background"]
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=theme["primary"],
                on_primary=theme["on_primary"],
                background=theme["background"],
                on_background=theme["on_background"],
                surface=theme["surface"],
                on_surface=theme["on_surface"]
            )
        )

    def toggle_timer():
        timer.toggle_timer()
        update_interface()

    def reset_timer():
        timer.reset_timer()
        update_interface()




    def on_break_time_change(e):
        try:
            timer.break_time = int(break_time_field.value) * 60
            if not timer.is_running and not timer.is_work_time:
                timer.current_time = timer.break_time
            update_interface()
        except:
            pass

    def on_theme_change(e):
        timer.set_theme(theme_radio.value)
        update_interface()

    def add_new_tag(e):
        """Добавление нового тега"""
        def save_tag(e):
            if new_tag_name.value and new_tag_color.value:
                timer.add_tag(new_tag_name.value, new_tag_color.value)
                update_tag_dropdown()
                timer.save_data()
                page.dialog.open = False
                update_interface()
        
        new_tag_name = ft.TextField(label="Название тега")
        new_tag_color = ft.Dropdown(
            label="Цвет",
            options=[
                ft.dropdown.Option("RED"),
                ft.dropdown.Option("BLUE"),
                ft.dropdown.Option("GREEN"),
                ft.dropdown.Option("PURPLE"),
                ft.dropdown.Option("ORANGE"),
                ft.dropdown.Option("YELLOW"),
            ]
        )
        
        page.dialog = ft.AlertDialog(
            title=ft.Text("Добавить новый тег"),
            content=ft.Column([new_tag_name, new_tag_color], tight=True),
            actions=[ft.ElevatedButton("Сохранить", on_click=save_tag)]
        )
        page.dialog.open = True
        page.update()

    def add_new_shop_item(e):
        """Добавление нового товара в магазин"""
        def save_item(e):
            if (new_item_name.value and new_item_cost.value and 
                new_item_desc.value):
                try:
                    cost = int(new_item_cost.value)
                    timer.add_shop_item(
                        new_item_name.value, 
                        cost, 
                        new_item_desc.value
                    )
                    update_shop_items()
                    timer.save_data()
                    page.dialog.open = False
                    update_interface()
                except:
                    pass
        
        new_item_name_local = ft.TextField(label="Название товара")
        new_item_cost_local = ft.TextField(label="Стоимость")
        new_item_desc_local = ft.TextField(label="Описание")
        
        page.dialog = ft.AlertDialog(
            title=ft.Text("Добавить товар в магазин"),
            content=ft.Column([
                new_item_name_local, 
                new_item_cost_local, 
                new_item_desc_local
            ], tight=True),
            actions=[ft.ElevatedButton("Сохранить", on_click=save_item)]
        )
        page.dialog.open = True
        page.update()

    def buy_shop_item(item_index):
        """Покупка товара из магазина"""
        if timer.buy_item(item_index):
            update_interface()
            timer.save_data()
            # Показать сообщение об успешной покупке
            page.show_snack_bar(ft.SnackBar(
                content=ft.Text(f"Товар '{timer.shop_items[item_index]['name']}' куплен!"),
                action="OK"
            ))
        else:
            page.show_snack_bar(ft.SnackBar(
                content=ft.Text("Недостаточно очков!"),
                action="OK"
            ))

    # Инициализация интерфейса
    page.title = "Pomodoro Timer"
    page.padding = 20
    
    # Создание вкладок
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Таймер",
                icon=ft.Icons.TIMER,
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([time_display], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([tag_text, points_text], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        ft.Row([start_pause_btn, reset_btn], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Divider(),
                        stats_text
                    ]),
                    padding=20
                )
            ),
            ft.Tab(
                text="Настройки",
                icon=ft.Icons.SETTINGS,
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Настройки времени:", weight=ft.FontWeight.BOLD),
                        work_time_field,
                        break_time_field,
                        ft.Divider(),
                        ft.Text("Управление тегами:", weight=ft.FontWeight.BOLD),
                        tag_dropdown,
                        ft.ElevatedButton("Добавить тег", on_click=add_new_tag),
                        ft.Divider(),
                        ft.Text("Тема:", weight=ft.FontWeight.BOLD),
                        theme_radio
                    ]),
                    padding=20
                )
            ),
            ft.Tab(
                text="Магазин",
                icon=ft.Icons.SHOPPING_CART,
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Магазин мотивации", size=20, weight=ft.FontWeight.BOLD),
                        points_text,
                        ft.ElevatedButton("Добавить товар", on_click=add_new_shop_item),
                        ft.Divider(),
                        shop_items_column
                    ]),
                    padding=20
                )
            )
        ]
    )
    
    page.add(tabs)
    
    # Инициализация данных
    update_tag_dropdown()
    update_shop_items()
    update_theme_selector()
    update_stats()
    apply_theme()
    
    # Главный цикл таймера
    def timer_tick():
        while True:
            timer.update_timer()
            update_interface()
            time.sleep(1)
    
    # Запуск таймера в отдельном потоке
    import threading
    timer_thread = threading.Thread(target=timer_tick, daemon=True)
    timer_thread.start()
    
    # Сохранение данных при закрытии
    def on_window_event(e):
        if e.data == "close":
            timer.save_data()
    
    page.on_window_event = on_window_event

if __name__ == "__main__":
    ft.app(target=main)
