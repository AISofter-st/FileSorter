import os
import shutil
from tkinter import messagebox
import webbrowser
import time
import hashlib
import re
import uuid
import math
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageDraw, ImageFilter

# ============================================================
# КАТЕГОРИИ ФАЙЛОВ
# ============================================================

FILE_EXTENSIONS: dict[str, list[str]] = {
    "Музыка": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Видео": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
    "Изображения": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"],
    "Архивы": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
    "Документы": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv"],
    "Программы": [".exe", ".msi", ".apk", ".bat", ".cmd"],
    "Торренты": [".torrent"],
    "Разное": [".psd", ".stl", ".obj"]
}

# ============================================================
# СЛОВАРЬ ЛОКАЛИЗАЦИИ (RU / EN)
# ============================================================

LANG: dict[str, dict[str, str]] = {
    "RU": {
        "drop_text": "Перетащи сюда папку\nили нажми обзор",
        "btn_browse": "ОБЗОР",
        "btn_back": "🔙 Назад к выбору папки",
        "btn_help": "❓ Справка",
        "title_settings": "Как навести порядок в папке:",
        
        "tt_cat": "При выборе данного пункта будут перенесены файлы,\nимеющие расширение:\n{ext}",
        "tt_days": "Не трогать файлы, которые созданы\nменее указанного количества дней.",
        "tt_custom": "Сложить все файлы, содержащие указанное слово\nв названии, в отдельную папку.\n\nНапример: если ввести слово 'смета' и папку 'Работа',\nто файл 'смета_за_май.pdf' переместится в эту папку.",
        "tt_heavy": "Удалить файлы, размер которых превышает\nуказанное значение в мегабайтах (МБ).",
        
        "chk_subfolders": "Сканировать вложенные папки",
        "chk_subfolders_warn": "⚠️ Затронет файлы внутри программ\n(игры)",
        "msg_subfolders_title": "⚠️ Внимание!",
        "msg_subfolders_text": "Включен рекурсивный поиск во всех подпапках!\n\nЕсли в этой папке лежат распакованные портативные программы (например, игры), программа переместит их исполняемые файлы (.exe, .bat, .dll) по категориям.\n\nВы уверены, что хотите продолжить?",
        "chk_days": "Не трогать свежие (дней):",
        "lbl_custom_word": "Сложить файлы со словом в названии:",
        "plh_word": "Слово",
        "plh_folder": "Папка",
        "lbl_cleanup": "Очистка:",
        "chk_dups": "Удалить точные дубликаты (безопасно)",
        "chk_empty": "Удалить пустые папки",
        
        "chk_heavy": "Удалить тяжелые файлы свыше:",
        "lbl_mb": "МБ",
        
        "chk_dest": "Переместить результат в другую папку",
        "btn_choose_dest": "Выбрать папку",
        "btn_execute": "НАВЕСТИ ПОРЯДОК",
        "btn_executing": "ОБРАБОТКА...",
        "res_title": "🎉 Порядок успешно наведен!",
        "res_stats": "Перемещено файлов: {m}\nОтправлено в Карантин: {d}",
        "res_warn": "⚠️ Внимание! Не закрывайте это окно, пока не проверите папку.\n\n• Всё устраивает? Нажмите «Новая папка» или закройте программу — дубликаты и мусор удалятся навсегда.\n• Что-то пошло не так? Нажмите «Вернуть всё как было» — программа мгновенно восстановит файлы на их исходные места.",
        "btn_undo": "↩️ Вернуть всё как было",
        "btn_undoing": "ВОССТАНОВЛЕНИЕ...",
        "btn_undone": "↩️ Всё восстановлено",
        "btn_restart": "Навести порядок в другой папке",
        "btn_donate": "🐱 Поддержать автора",
        "err_title": "Ошибка",
        "err_not_folder": "Выбранный путь не является папкой.",
        "err_drop": "Перетащи именно папку.",
        "err_read": "Не удалось прочитать папку:\n",
        "msg_undo_title": "Вернуть всё как было",
        "msg_undo_text": "Программа отменит последние изменения и вернет файлы на исходные места.\nПродолжить?",
        "help_title": "Инструкция и безопасность",
        "help_text": "💡 Как безопасно навести порядок:\n\n1. Выбор папки — перетащите папку в окно или нажмите «Обзор».\n2. Портативный софт — НЕ включайте «Сканировать вложенные папки», если внутри лежат распакованные утилиты (игры), иначе их системные файлы распределятся по категориям.\n3. Карантин и отмена — после сортировки обязательно проверьте результат. Пока окно открыто, вы можете нажатием одной кнопки вернуть всё на места.\n4. Удаление дубликатов — перед удалением сверяются точные хэши файлов, поэтому важные данные не пострадают.",
        "btn_github": "🌐 Полное руководство на GitHub"
    },
    "EN": {
        "drop_text": "Drop a folder here\nor click browse",
        "btn_browse": "BROWSE",
        "btn_back": "🔙 Back to folder selection",
        "btn_help": "❓ Help",
        "title_settings": "How to organize the folder:",
        
        "tt_cat": "Selecting this will move files\nwith the following extensions:\n{ext}",
        "tt_days": "Do not touch files created\nless than the specified number of days ago.",
        "tt_custom": "Group all files containing the specified word\nin their name into a separate folder.\n\nExample: if you enter 'invoice' and folder 'Work',\nthe file 'invoice_may.pdf' will be moved there.",
        "tt_heavy": "Delete files whose size exceeds\nthe specified value in Megabytes (MB).",
        
        "chk_subfolders": "Scan subfolders",
        "chk_subfolders_warn": "⚠️ Affects files inside portable apps\n(games)",
        "msg_subfolders_title": "⚠️ Warning!",
        "msg_subfolders_text": "Recursive search in all subfolders is enabled!\n\nIf this directory contains portable apps (e.g., games), the tool will separate their executable files (.exe, .bat, .dll) into category folders.\n\nAre you sure you want to proceed?",
        "chk_days": "Keep recent files (days):",
        "lbl_custom_word": "Group files containing word:",
        "plh_word": "Word",
        "plh_folder": "Folder Name",
        "lbl_cleanup": "Cleanup:",
        "chk_dups": "Delete exact duplicates (safely)",
        "chk_empty": "Delete empty folders",
        
        "chk_heavy": "Delete heavy files over:",
        "lbl_mb": "MB",
        
        "chk_dest": "Move results to another folder",
        "btn_choose_dest": "Select Folder",
        "btn_execute": "ORGANIZE FILES",
        "btn_executing": "PROCESSING...",
        "res_title": "🎉 Successfully organized!",
        "res_stats": "Files moved: {m}\nSent to Quarantine: {d}",
        "res_warn": "⚠️ Attention! Do not close this window until you check the folder.\n\n• Everything looks good? Click 'New folder' or close the app — duplicates and trash will be deleted forever.\n• Something went wrong? Click 'Revert everything' — the app will instantly restore files to their original locations.",
        "btn_undo": "↩️ Revert everything",
        "btn_undoing": "RESTORING...",
        "btn_undone": "↩️ Everything Restored",
        "btn_restart": "Organize another folder",
        "btn_donate": "🐱 Treat the author's cat",
        "err_title": "Error",
        "err_not_folder": "Selected path is not a folder.",
        "err_drop": "Please drop a folder, not a file.",
        "err_read": "Failed to read folder:\n",
        "msg_undo_title": "Revert everything",
        "msg_undo_text": "The app will undo the latest changes and return files to their original locations.\nContinue?",
        "help_title": "Guide & Safety",
        "help_text": "💡 How to safely organize your files:\n\n1. Select Folder — Drag & drop a folder or click Browse.\n2. Portable Apps — DO NOT enable 'Scan subfolders' if the directory contains unpacked tools (games), otherwise their files will be separated.\n3. Quarantine & Undo — Check your files after organizing. As long as the window remains open, you can revert all changes with a single click.\n4. Duplicate Cleanup — Hashes are verified before deletion, ensuring your safe data is preserved.",
        "btn_github": "🌐 Full Documentation on GitHub"
    }
}


# ============================================================
# MODERN UI
# ============================================================

APP_BG = "#0B1220"
SURFACE = "#111B2E"
SURFACE_2 = "#17243A"
SURFACE_3 = "#1D2D47"
BORDER = "#294568"
TEXT = "#F4F7FB"
MUTED = "#9FB0C7"
INDIGO = "#5967F2"
INDIGO_HOVER = "#6876FF"
TURQUOISE = "#21D5D2"
GREEN = "#20C997"
GREEN_DARK = "#123A35"
WARNING = "#FFB52E"
WARNING_BG = "#2E281A"
DANGER = "#FF5B6E"
DANGER_BG = "#351C25"


class ToolTip:
    def __init__(self, widget: tk.Widget, text: str, delay: int = 450) -> None:
        self.widget = widget
        self.text = text
        self.delay = delay
        self.id: str | None = None
        self.tw: tk.Toplevel | None = None
        widget.bind("<Enter>", self.enter, add="+")
        widget.bind("<Leave>", self.leave, add="+")
        widget.bind("<ButtonPress>", self.leave, add="+")

    def enter(self, event=None) -> None:
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show)

    def leave(self, event=None) -> None:
        self.unschedule()
        self.hide()

    def unschedule(self) -> None:
        if self.id:
            try:
                self.widget.after_cancel(self.id)
            except Exception:
                pass
            self.id = None

    def show(self, event=None) -> None:
        if self.tw or not self.text:
            return
        x = self.widget.winfo_rootx() + 18
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        self.tw.attributes("-topmost", True)
        label = tk.Label(
            self.tw, text=self.text, justify="left",
            background="#18253A", foreground="#EAF2FF",
            relief="solid", borderwidth=1, highlightthickness=0,
            font=("Segoe UI", 10), padx=10, pady=7
        )
        label.pack()

    def hide(self) -> None:
        if self.tw:
            try:
                self.tw.destroy()
            except Exception:
                pass
            self.tw = None


class AppWindow(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self) -> None:
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("File Sorter")
        
        # Центрирование главного окна при старте программы
        self.update_idletasks()
        window_width = 1024
        window_height = 780
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False) 
        self.configure(fg_color=APP_BG)

        self.current_lang = "RU"
        self.source_folder = ""
        self.dest_folder = ""
        self.selected_dest_path = ""
        self.trash_dir_name = ".sort_trash"

        self.session_history: list[tuple[str, str]] = []
        self.trashed_files: list[tuple[str, str]] = []

        self._images: dict[str, ctk.CTkImage] = {}
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.build_start_screen()

    def t(self, key: str) -> str:
        return LANG[self.current_lang].get(key, key)
        
    def center_toplevel(self, win: tk.Toplevel | ctk.CTkToplevel, width: int, height: int) -> None:
        """Центрирует переданное окно относительно главного окна приложения."""
        self.update_idletasks()
        main_x = self.winfo_x()
        main_y = self.winfo_y()
        main_width = self.winfo_width()
        main_height = self.winfo_height()
        pos_x = main_x + (main_width // 2) - (width // 2)
        pos_y = main_y + (main_height // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    # ------------------------- Visual helpers -------------------------

    def make_icon(self, size: int = 96) -> ctk.CTkImage:
        """Generate a small vector-like File Sorter icon without external image files."""
        key = f"app_{size}"
        if key in self._images:
            return self._images[key]

        scale = 2
        s = size * scale
        img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)

        # Rounded gradient background
        for y in range(s):
            p = y / max(1, s - 1)
            r = int(35 + 45 * p)
            g = int(45 + 20 * p)
            b = int(115 + 85 * p)
            d.line((0, y, s, y), fill=(r, g, b, 255))
        mask = Image.new("L", (s, s), 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle((2, 2, s-2, s-2), radius=int(s * .22), fill=255)
        img.putalpha(mask)

        # soft glow
        glow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse((s*.18, s*.10, s*.82, s*.70), fill=(33, 213, 210, 75))
        glow = glow.filter(ImageFilter.GaussianBlur(s*.08))
        img = Image.alpha_composite(img, glow)
        d = ImageDraw.Draw(img)

        # folder
        folder = [
            (s*.17, s*.43), (s*.38, s*.43), (s*.45, s*.35),
            (s*.78, s*.35), (s*.87, s*.45), (s*.80, s*.78),
            (s*.20, s*.78)
        ]
        d.polygon(folder, fill=(37, 205, 221, 255))
        d.rounded_rectangle((s*.19, s*.45, s*.83, s*.79), radius=int(s*.07), fill=(48, 109, 242, 255))
        d.polygon([(s*.19, s*.50), (s*.81, s*.50), (s*.84, s*.76), (s*.21, s*.76)],
                  fill=(78, 78, 240, 255))

        # floating mini file/photo/gear/shield symbols
        cards = [
            (s*.20, s*.20, (83, 102, 244, 255), "file"),
            (s*.40, s*.12, (31, 207, 208, 255), "photo"),
            (s*.61, s*.20, (91, 84, 237, 255), "gear"),
            (s*.70, s*.39, (39, 205, 183, 255), "shield"),
        ]
        for x, y, color, typ in cards:
            rr = int(s*.07)
            d.rounded_rectangle((x, y, x+s*.18, y+s*.18), radius=rr, fill=color)
            cx, cy = x+s*.09, y+s*.09
            if typ == "file":
                d.rectangle((x+s*.055, y+s*.045, x+s*.125, y+s*.14), fill=(245,249,255,255))
                d.line((x+s*.072, y+s*.085, x+s*.112, y+s*.085), fill=color, width=max(2,int(s*.012)))
                d.line((x+s*.072, y+s*.11, x+s*.112, y+s*.11), fill=color, width=max(2,int(s*.012)))
            elif typ == "photo":
                d.rectangle((x+s*.045, y+s*.05, x+s*.135, y+s*.135), outline=(245,249,255,255), width=max(2,int(s*.012)))
                d.ellipse((x+s*.095, y+s*.06, x+s*.115, y+s*.08), fill=(245,249,255,255))
                d.polygon([(x+s*.05,y+s*.125),(x+s*.085,y+s*.09),(x+s*.105,y+s*.11),(x+s*.13,y+s*.08),
                           (x+s*.135,y+s*.13)], fill=(245,249,255,255))
            elif typ == "gear":
                d.ellipse((cx-s*.045,cy-s*.045,cx+s*.045,cy+s*.045), fill=(245,249,255,255))
                d.ellipse((cx-s*.018,cy-s*.018,cx+s*.018,cy+s*.018), fill=color)
                for a in range(0,360,45):
                    rad = math.radians(a)
                    tx = cx + math.cos(rad)*s*.055
                    ty = cy + math.sin(rad)*s*.055
                    d.rectangle((tx-s*.012,ty-s*.012,tx+s*.012,ty+s*.012), fill=(245,249,255,255))
            else:
                d.polygon([(cx, y+s*.045),(x+s*.14,y+s*.065),(x+s*.125,y+s*.125),(cx,y+s*.15),
                           (x+s*.055,y+s*.125),(x+s*.04,y+s*.065)], fill=(245,249,255,255))

        img = img.resize((size, size), Image.Resampling.LANCZOS)
        self._images[key] = ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))
        return self._images[key]

    def add_header(self, parent: ctk.CTkFrame, show_back: bool = False) -> None:
        header = ctk.CTkFrame(parent, fg_color="transparent", height=72)
        header.pack(fill="x", padx=28, pady=(20, 8))
        header.pack_propagate(False)

        if show_back:
            ctk.CTkButton(
                header, text="‹  " + self.t("btn_back"),
                width=190, height=38, corner_radius=12,
                fg_color=SURFACE_2, hover_color=SURFACE_3,
                border_width=1, border_color=BORDER,
                text_color=TEXT, font=("Segoe UI", 11),
                command=self.restart_app
            ).pack(side="left")

        brand = ctk.CTkFrame(header, fg_color="transparent")
        brand.pack(side="left", padx=(8 if show_back else 0, 0))
        ctk.CTkLabel(brand, image=self.make_icon(46), text="").pack(side="left")
        ctk.CTkLabel(
            brand, text="File Sorter", font=("Segoe UI Semibold", 19),
            text_color=TEXT
        ).pack(side="left", padx=12)

        tools = ctk.CTkFrame(header, fg_color="transparent")
        tools.pack(side="right")

        self.lang_var = ctk.StringVar(value=self.current_lang)
        ctk.CTkSegmentedButton(
            tools, values=["RU", "EN"], variable=self.lang_var,
            command=self.change_language, width=110, height=34,
            fg_color=SURFACE_2, selected_color=INDIGO,
            selected_hover_color=INDIGO_HOVER, unselected_color=SURFACE_2,
            unselected_hover_color=SURFACE_3, text_color=TEXT
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            tools, text="ⓘ  " + self.t("btn_help"), width=108, height=34,
            corner_radius=11, fg_color="transparent", hover_color=SURFACE_2,
            border_width=1, border_color=BORDER, text_color=TEXT,
            font=("Segoe UI", 10), command=self.open_help_window
        ).pack(side="left")

    def make_card(self, parent: tk.Widget, **kwargs) -> ctk.CTkFrame:
        defaults = dict(
            fg_color=SURFACE, corner_radius=18,
            border_width=1, border_color=BORDER
        )
        defaults.update(kwargs)
        return ctk.CTkFrame(parent, **defaults)

    def clear_screen(self) -> None:
        for child in self.winfo_children():
            child.destroy()

    def on_closing(self) -> None:
        self.clean_quarantine()
        self.destroy()

    def clean_quarantine(self) -> None:
        if self.dest_folder:
            trash_path = os.path.join(self.dest_folder, self.trash_dir_name)
            if os.path.exists(trash_path):
                try:
                    shutil.rmtree(trash_path, ignore_errors=True)
                except Exception:
                    pass

    # ------------------------- Custom dialogs -------------------------

    def show_dialog(self, title: str, message: str, kind: str = "info", yes_no: bool = False, yes_text: str | None = None, no_text: str | None = None) -> bool:
        result = {"value": False}
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.resizable(False, False)
        win.configure(fg_color=APP_BG)
        win.transient(self)
        
        # Центрирование окна
        width = 520
        height = 300 if yes_no else 260
        self.center_toplevel(win, width, height)
        win.grab_set()

        outer = self.make_card(win, fg_color=SURFACE, corner_radius=20, border_color=BORDER)
        outer.pack(fill="both", expand=True, padx=14, pady=14)

        colors = {"warning": WARNING, "danger": DANGER, "success": GREEN, "info": TURQUOISE}
        icons = {"warning": "!", "danger": "×", "success": "✓", "info": "i"}
        accent = colors.get(kind, TURQUOISE)

        top = ctk.CTkFrame(outer, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(22, 8))
        ctk.CTkLabel(
            top, text=icons.get(kind, "i"), width=36, height=36,
            corner_radius=18, fg_color=accent, text_color=APP_BG,
            font=("Segoe UI Semibold", 18)
        ).pack(side="left")
        ctk.CTkLabel(
            top, text=title, font=("Segoe UI Semibold", 17), text_color=TEXT
        ).pack(side="left", padx=12)

        ctk.CTkLabel(
            outer, text=message, justify="left", anchor="w",
            wraplength=450, font=("Segoe UI", 11), text_color=MUTED
        ).pack(fill="x", padx=28, pady=8)

        buttons = ctk.CTkFrame(outer, fg_color="transparent")
        buttons.pack(side="bottom", fill="x", padx=24, pady=20)

        def close(value: bool) -> None:
            result["value"] = value
            win.grab_release()
            win.destroy()

        if yes_no:
            ctk.CTkButton(
                buttons, text=no_text or ("Отмена" if self.current_lang == "RU" else "Cancel"),
                width=120, height=40, corner_radius=12,
                fg_color=SURFACE_2, hover_color=SURFACE_3,
                border_width=1, border_color=BORDER, text_color=TEXT,
                command=lambda: close(False)
            ).pack(side="right", padx=(8, 0))
            ctk.CTkButton(
                buttons, text=yes_text or ("Продолжить" if self.current_lang == "RU" else "Continue"),
                width=150, height=40, corner_radius=12,
                fg_color=accent, hover_color=INDIGO_HOVER,
                text_color=APP_BG if kind != "danger" else TEXT,
                font=("Segoe UI Semibold", 11),
                command=lambda: close(True)
            ).pack(side="right")
        else:
            ctk.CTkButton(
                buttons, text="OK", width=110, height=40, corner_radius=12,
                fg_color=INDIGO, hover_color=INDIGO_HOVER,
                text_color=TEXT, command=lambda: close(True)
            ).pack(side="right")

        win.protocol("WM_DELETE_WINDOW", lambda: close(False))
        win.wait_window()
        return result["value"]

    def open_help_window(self) -> None:
        win = ctk.CTkToplevel(self)
        win.title(self.t("help_title"))
        win.resizable(False, False)
        win.configure(fg_color=APP_BG)
        win.transient(self)
        
        # Центрирование окна справки
        self.center_toplevel(win, 700, 590)
        win.grab_set()

        header = ctk.CTkFrame(win, fg_color="transparent")
        header.pack(fill="x", padx=28, pady=(22, 10))
        ctk.CTkLabel(header, image=self.make_icon(52), text="").pack(side="left")
        ctk.CTkLabel(
            header, text=self.t("help_title"), font=("Segoe UI Semibold", 20),
            text_color=TEXT
        ).pack(side="left", padx=14)

        body = self.make_card(win, fg_color=SURFACE)
        body.pack(fill="both", expand=True, padx=28, pady=(4, 16))

        textbox = ctk.CTkTextbox(
            body, fg_color="transparent", border_width=0,
            text_color=MUTED, font=("Segoe UI", 12),
            wrap="word", activate_scrollbars=True
        )
        textbox.pack(fill="both", expand=True, padx=18, pady=18)
        textbox.insert("1.0", self.t("help_text"))
        textbox.configure(state="disabled")

        ctk.CTkButton(
            win, text=self.t("btn_github"), height=42, corner_radius=12,
            fg_color=INDIGO, hover_color=INDIGO_HOVER,
            font=("Segoe UI Semibold", 11),
            command=lambda: webbrowser.open("https://github.com/")
        ).pack(padx=28, pady=(0, 22), fill="x")

    # ------------------------- Screen 1 -------------------------

    def build_start_screen(self) -> None:
        self.clear_screen()

        root = ctk.CTkFrame(self, fg_color=APP_BG)
        root.pack(fill="both", expand=True)

        self.add_header(root)

        main = ctk.CTkFrame(root, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=28, pady=(5, 26))

        hero = self.make_card(main, fg_color=SURFACE)
        hero.pack(fill="both", expand=True)

        # Left visual block
        visual = ctk.CTkFrame(hero, fg_color="transparent", width=350)
        visual.pack(side="left", fill="y", padx=(30, 10), pady=30)
        visual.pack_propagate(False)

        ctk.CTkLabel(visual, image=self.make_icon(180), text="").pack(pady=(42, 18))
        ctk.CTkLabel(
            visual, text="File Sorter", font=("Segoe UI Semibold", 25), text_color=TEXT
        ).pack()
        ctk.CTkLabel(
            visual,
            text="Умная сортировка файлов\nбез лишних действий" if self.current_lang == "RU"
                  else "Smart file organization\nwithout unnecessary steps",
            font=("Segoe UI", 12), text_color=MUTED, justify="center"
        ).pack(pady=(8, 0))

        # Drop area
        right = ctk.CTkFrame(hero, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True, padx=(10, 30), pady=30)

        ctk.CTkLabel(
            right,
            text="Выберите папку" if self.current_lang == "RU" else "Choose a folder",
            font=("Segoe UI Semibold", 23), text_color=TEXT
        ).pack(anchor="w", pady=(42, 5))

        ctk.CTkLabel(
            right,
            text="Перетащите папку сюда, чтобы начать сортировку." if self.current_lang == "RU"
                 else "Drag a folder here to start organizing.",
            font=("Segoe UI", 12), text_color=MUTED
        ).pack(anchor="w")

        drop = ctk.CTkFrame(
            right, fg_color=SURFACE_2, corner_radius=18,
            border_width=1, border_color=BORDER, height=190
        )
        drop.pack(fill="x", pady=24)
        drop.pack_propagate(False)

        ctk.CTkLabel(drop, text="↓", font=("Segoe UI Light", 38), text_color=TURQUOISE).pack(pady=(25, 0))
        self.label_info = ctk.CTkLabel(
            drop, text=self.t("drop_text"), font=("Segoe UI Semibold", 14),
            text_color=TEXT, justify="center"
        )
        self.label_info.pack(pady=4)

        self.btn_browse = ctk.CTkButton(
            right, text=self.t("btn_browse"), height=48, corner_radius=14,
            fg_color=INDIGO, hover_color=INDIGO_HOVER,
            font=("Segoe UI Semibold", 12), command=self.browse_folder
        )
        self.btn_browse.pack(fill="x")

        note = "Файлы не удаляются без вашего подтверждения." if self.current_lang == "RU" \
               else "Files are not permanently deleted without your confirmation."
        ctk.CTkLabel(
            right, text="ⓘ  " + note, font=("Segoe UI", 12), text_color=MUTED
        ).pack(anchor="w", pady=(16, 0))

        # DnD target
        for target in (drop, right, hero):
            target.drop_target_register(DND_FILES)
            target.dnd_bind("<<Drop>>", self.drop_folder)

    def change_language(self, new_lang: str) -> None:
        self.current_lang = new_lang
        # Rebuild the current screen so every caption is translated.
        if hasattr(self, "frame_settings") and self.frame_settings.winfo_exists():
            self.build_settings_screen()
        elif hasattr(self, "frame_result") and self.frame_result.winfo_exists():
            # Result is only reached after sorting; rebuilding needs counts.
            moved = getattr(self, "_result_moved", 0)
            deleted = getattr(self, "_result_deleted", 0)
            self.build_result_screen(moved, deleted)
        else:
            self.build_start_screen()

    def browse_folder(self) -> None:
        folder_path = filedialog.askdirectory(title=self.t("btn_browse"))
        if not folder_path:
            return
        clean_path = self.normalize_path(folder_path)
        if os.path.isdir(clean_path):
            self.go_to_settings(clean_path)
        else:
            self.show_dialog(self.t("err_title"), self.t("err_not_folder"), "danger")

    def drop_folder(self, event) -> None:
        try:
            paths = self.tk.splitlist(event.data)
        except Exception:
            paths = [event.data]
        if not paths:
            return
        clean_path = self.normalize_path(paths[0])
        if os.path.isdir(clean_path):
            self.go_to_settings(clean_path)
        else:
            self.show_dialog(self.t("err_title"), self.t("err_drop"), "warning")

    def normalize_path(self, path: str) -> str:
        if not path:
            return ""
        path = path.strip()
        if len(path) >= 2 and path.startswith("{") and path.endswith("}"):
            path = path[1:-1]
        if path.startswith("\\\\?\\"):
            path = path[4:]
        return os.path.normpath(os.path.abspath(path))

    # ------------------------- Navigation -------------------------

    def go_to_settings(self, folder_path: str) -> None:
        self.source_folder = folder_path
        self.dest_folder = folder_path
        self.selected_dest_path = ""
        self.build_settings_screen()

    def go_to_result(self, moved_count: int, deleted_count: int) -> None:
        self._result_moved = moved_count
        self._result_deleted = deleted_count
        self.build_result_screen(moved_count, deleted_count)

    def restart_app(self) -> None:
        self.clean_quarantine()
        self.source_folder = ""
        self.dest_folder = ""
        self.selected_dest_path = ""
        self.session_history.clear()
        self.trashed_files.clear()
        self.build_start_screen()

    # ------------------------- Screen 2 -------------------------

    def build_settings_screen(self) -> None:
        self.clear_screen()

        self.frame_settings = ctk.CTkFrame(self, fg_color=APP_BG)
        self.frame_settings.pack(fill="both", expand=True)

        self.add_header(self.frame_settings, show_back=True)

        content = ctk.CTkFrame(self.frame_settings, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=28, pady=(0, 22))

        title_card = self.make_card(content, fg_color=SURFACE)
        title_card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            title_card,
            text=self.t("title_settings"),
            font=("Segoe UI Semibold", 19), text_color=TEXT
        ).pack(anchor="w", padx=22, pady=(16, 2))
        ctk.CTkLabel(
            title_card, text=self.source_folder,
            font=("Segoe UI", 10), text_color=MUTED,
            anchor="w", justify="left"
        ).pack(anchor="w", padx=22, pady=(0, 16))

        scroll = ctk.CTkFrame(content, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True)

        left = self.make_card(scroll)
        left.pack(side="left", fill="both", expand=True, padx=(0, 7), pady=2)

        right = self.make_card(scroll)
        right.pack(side="left", fill="both", expand=True, padx=(7, 0), pady=2)

        ctk.CTkLabel(
            left, text="Категории" if self.current_lang == "RU" else "Categories",
            font=("Segoe UI Semibold", 14), text_color=TEXT
        ).pack(anchor="w", padx=20, pady=(18, 10))

        self.cat_vars: dict[str, ctk.BooleanVar] = {}
        trans_dict = {
            "Музыка": "Music", "Видео": "Video", "Изображения": "Images",
            "Архивы": "Archives", "Документы": "Documents",
            "Программы": "Programs", "Торренты": "Torrents", "Разное": "Misc"
        }
        for category in FILE_EXTENSIONS.keys():
            var = ctk.BooleanVar(value=True)
            self.cat_vars[category] = var
            cat_display = category if self.current_lang == "RU" else trans_dict.get(category, category)
            cb = ctk.CTkCheckBox(
                left, text=cat_display, variable=var,
                height=30, corner_radius=8,
                border_width=2, fg_color=INDIGO,
                hover_color=INDIGO_HOVER, text_color=TEXT,
                font=("Segoe UI", 11)
            )
            cb.pack(pady=4, padx=20, anchor="w")
            ToolTip(cb, self.t("tt_cat").format(ext=", ".join(FILE_EXTENSIONS[category])))

        sep = ctk.CTkFrame(left, height=1, fg_color=BORDER)
        sep.pack(fill="x", padx=20, pady=14)

        self.var_subfolders = ctk.BooleanVar(value=False)
        self.chk_sub = ctk.CTkCheckBox(
            left, text=self.t("chk_subfolders"), variable=self.var_subfolders,
            text_color=WARNING, fg_color=INDIGO, hover_color=INDIGO_HOVER,
            font=("Segoe UI Semibold", 11), command=self.on_toggle_subfolders
        )
        self.chk_sub.pack(pady=(0, 4), padx=20, anchor="w")

        self.lbl_sub_warn = ctk.CTkLabel(
            left, text=self.t("chk_subfolders_warn"),
            font=("Segoe UI", 10), text_color="#FF8E9B",
            justify="left"
        )
        self.lbl_sub_warn.pack(padx=45, anchor="w", pady=(0, 18))

        ctk.CTkLabel(
            right, text="Фильтры и очистка" if self.current_lang == "RU" else "Filters & cleanup",
            font=("Segoe UI Semibold", 14), text_color=TEXT
        ).pack(anchor="w", padx=20, pady=(18, 10))

        # Recent files
        days_row = ctk.CTkFrame(right, fg_color="transparent")
        days_row.pack(fill="x", padx=20, pady=7)
        self.var_filter_days = ctk.BooleanVar(value=False)
        self.entry_days = ctk.StringVar(value="7")
        chk_days = ctk.CTkCheckBox(
            days_row, text=self.t("chk_days"), variable=self.var_filter_days,
            fg_color=INDIGO, hover_color=INDIGO_HOVER, text_color=TEXT,
            font=("Segoe UI", 11)
        )
        chk_days.pack(side="left")
        ctk.CTkEntry(
            days_row, width=62, height=34, textvariable=self.entry_days,
            corner_radius=10, fg_color=SURFACE_2, border_color=BORDER
        ).pack(side="left", padx=10)
        ToolTip(chk_days, self.t("tt_days"))

        # Custom word
        lbl_custom = ctk.CTkLabel(
            right, text=self.t("lbl_custom_word"),
            font=("Segoe UI", 11), text_color=TEXT
        )
        lbl_custom.pack(anchor="w", padx=20, pady=(12, 5))
        ToolTip(lbl_custom, self.t("tt_custom"))

        custom = ctk.CTkFrame(right, fg_color="transparent")
        custom.pack(fill="x", padx=20, pady=2)
        self.entry_custom_word = ctk.StringVar()
        self.entry_custom_folder = ctk.StringVar()
        ctk.CTkEntry(
            custom, height=34, placeholder_text=self.t("plh_word"),
            textvariable=self.entry_custom_word, corner_radius=10,
            fg_color=SURFACE_2, border_color=BORDER
        ).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(custom, text="  →  ", text_color=TURQUOISE).pack(side="left")
        ctk.CTkEntry(
            custom, height=34, placeholder_text=self.t("plh_folder"),
            textvariable=self.entry_custom_folder, corner_radius=10,
            fg_color=SURFACE_2, border_color=BORDER
        ).pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            right, text=self.t("lbl_cleanup"),
            font=("Segoe UI Semibold", 12), text_color=TEXT
        ).pack(anchor="w", padx=20, pady=(18, 5))

        self.var_duplicates = ctk.BooleanVar(value=False)
        self.var_empty_folders = ctk.BooleanVar(value=False)
        self.var_heavy = ctk.BooleanVar(value=False)
        self.entry_heavy_mb = ctk.StringVar(value="500")

        for text, var in (
            (self.t("chk_dups"), self.var_duplicates),
            (self.t("chk_empty"), self.var_empty_folders),
        ):
            ctk.CTkCheckBox(
                right, text=text, variable=var, fg_color=INDIGO,
                hover_color=INDIGO_HOVER, text_color=TEXT,
                font=("Segoe UI", 11)
            ).pack(anchor="w", padx=20, pady=5)

        heavy = ctk.CTkFrame(right, fg_color="transparent")
        heavy.pack(fill="x", padx=20, pady=5)
        chk_heavy = ctk.CTkCheckBox(
            heavy, text=self.t("chk_heavy"), variable=self.var_heavy,
            fg_color=INDIGO, hover_color=INDIGO_HOVER, text_color=TEXT,
            font=("Segoe UI", 11)
        )
        chk_heavy.pack(side="left")
        ctk.CTkEntry(
            heavy, width=70, height=34, textvariable=self.entry_heavy_mb,
            corner_radius=10, fg_color=SURFACE_2, border_color=BORDER
        ).pack(side="left", padx=10)
        ctk.CTkLabel(heavy, text=self.t("lbl_mb"), text_color=MUTED).pack(side="left")
        ToolTip(chk_heavy, self.t("tt_heavy"))

        # Destination
        ctk.CTkFrame(right, height=1, fg_color=BORDER).pack(fill="x", padx=20, pady=14)
        dest = ctk.CTkFrame(right, fg_color="transparent")
        dest.pack(fill="x", padx=20, pady=(0, 18))
        self.var_dest = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            dest, text=self.t("chk_dest"), variable=self.var_dest,
            fg_color=INDIGO, hover_color=INDIGO_HOVER, text_color=TEXT,
            font=("Segoe UI", 11), command=self.toggle_dest
        ).pack(side="left")
        self.btn_dest = ctk.CTkButton(
            dest, text=self.t("btn_choose_dest"), width=125, height=34,
            corner_radius=10, state="disabled",
            fg_color=SURFACE_2, hover_color=SURFACE_3,
            border_width=1, border_color=BORDER, text_color=TEXT,
            command=self.choose_dest
        )
        self.btn_dest.pack(side="left", padx=10)

        # Bottom action
        bottom = ctk.CTkFrame(content, fg_color="transparent", height=64)
        bottom.pack(fill="x", pady=(12, 0))
        bottom.pack_propagate(False)

        self.btn_execute = ctk.CTkButton(
            bottom, text=self.t("btn_execute"), height=52, corner_radius=15,
            fg_color=INDIGO, hover_color=INDIGO_HOVER,
            font=("Segoe UI Semibold", 13), command=self.execute_sorting
        )
        self.btn_execute.pack(fill="x")

    def on_toggle_subfolders(self) -> None:
        if self.var_subfolders.get():
            confirm = self.show_dialog(
                self.t("msg_subfolders_title"),
                self.t("msg_subfolders_text"),
                "warning", yes_no=True,
                yes_text="Продолжить" if self.current_lang == "RU" else "Continue"
            )
            if not confirm:
                self.var_subfolders.set(False)

    def toggle_dest(self) -> None:
        if self.var_dest.get():
            self.btn_dest.configure(state="normal", fg_color=SURFACE_2)
        else:
            self.btn_dest.configure(state="disabled", fg_color=SURFACE_2)
            self.selected_dest_path = ""
            self.btn_dest.configure(text=self.t("btn_choose_dest"))

    def choose_dest(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.selected_dest_path = os.path.normpath(path)
            short_name = os.path.basename(self.selected_dest_path) or self.selected_dest_path
            self.btn_dest.configure(text=short_name)

    # ========================================================
    # ЛОГИКА ФИЛЬТРАЦИИ И ХЭШЕЙ
    # ========================================================

    def get_fast_hash(self, file_path: str) -> str | None:
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(65536)
                return hashlib.md5(chunk).hexdigest()
        except: 
            return None

    def get_full_hash(self, file_path: str) -> str | None:
        md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(1024 * 1024)
                    if not chunk: break
                    md5.update(chunk)
            return md5.hexdigest()
        except: 
            return None

    def is_copy_file(self, file_name: str) -> bool:
        name = os.path.splitext(file_name)[0].lower().strip()
        patterns = [
            r"\s*-\s*копия$", r"\s*-\s*копия\s*\(\d+\)$", r"\s+копия$", r"\s+копия\s*\(\d+\)$",
            r"_копия$", r"_копия\s*\(\d+\)$", r"\s*\(копия\)$", r"\s*\(копия\s+\d+\)$", r"\s*\(\d+\)$",
            r"\s*-\s*copy$", r"\s+copy$", r"\s*copy\s*\(\d+\)$"
        ]
        for pattern in patterns:
            if re.search(pattern, name, re.IGNORECASE): 
                return True
        return False

    def get_original_score(self, file_path: str) -> tuple[int, int, float]:
        file_name = os.path.basename(file_path)
        score = 1000 if self.is_copy_file(file_name) else 0
        try: modified = os.path.getmtime(file_path)
        except: modified = time.time()
        return (score, len(file_name), modified)

    def is_inside_folder(self, file_path: str, folder_path: str) -> bool:
        try:
            file_path = os.path.normcase(os.path.realpath(file_path))
            folder_path = os.path.normcase(os.path.realpath(folder_path))
            return os.path.commonpath([file_path, folder_path]) == folder_path
        except: 
            return False

    def get_protected_folders(self) -> list[str]:
        folders = [
            os.path.normcase(os.path.abspath(os.path.join(self.dest_folder, self.trash_dir_name))),
            os.path.normcase(os.path.abspath(os.path.join(self.source_folder, self.trash_dir_name)))
        ]
        for category in FILE_EXTENSIONS.keys():
            folders.append(os.path.normcase(os.path.abspath(os.path.join(self.dest_folder, category))))
        custom_folder = self.entry_custom_folder.get().strip()
        if custom_folder:
            folders.append(os.path.normcase(os.path.abspath(os.path.join(self.dest_folder, custom_folder))))
        return folders

    def collect_files(self) -> list[str]:
        files_to_process: list[str] = []
        protected_folders = self.get_protected_folders()

        if not self.var_subfolders.get():
            try:
                for item in os.listdir(self.source_folder):
                    path = os.path.join(self.source_folder, item)
                    if os.path.isfile(path) and self.trash_dir_name not in path:
                        files_to_process.append(path)
            except Exception as e:
                messagebox.showerror(self.t("err_title"), self.t("err_read") + str(e))
                return []
        else:
            for root, dirs, files in os.walk(self.source_folder, topdown=True):
                new_dirs = []
                for directory in dirs:
                    if directory == self.trash_dir_name: continue
                    full_dir = os.path.normcase(os.path.abspath(os.path.join(root, directory)))
                    skip = any(full_dir == p or self.is_inside_folder(full_dir, p) for p in protected_folders)
                    if not skip: new_dirs.append(directory)
                dirs[:] = new_dirs

                for file_name in files:
                    path = os.path.join(root, file_name)
                    if os.path.isfile(path): files_to_process.append(path)
        return files_to_process

    def send_to_quarantine(self, file_path: str) -> bool:
        if not os.path.exists(file_path): 
            return False
        trash_dir = os.path.join(self.dest_folder, self.trash_dir_name)
        os.makedirs(trash_dir, exist_ok=True)
        safe_name = f"{uuid.uuid4().hex[:8]}_{os.path.basename(file_path)}"
        quarantine_path = os.path.join(trash_dir, safe_name)
        try:
            shutil.move(file_path, quarantine_path)
            self.trashed_files.append((quarantine_path, os.path.abspath(file_path)))
            return True
        except: 
            return False

    # ========================================================
    # СОРТИРОВКА И ОЧИСТКА
    # ========================================================

    def remove_duplicates(self, files_to_process: list[str]) -> int:
        deleted_count = 0
        size_groups: dict[int, list[str]] = {}
        for path in files_to_process:
            if not os.path.isfile(path): continue
            try:
                size = os.path.getsize(path)
                size_groups.setdefault(size, []).append(path)
            except: pass
            
        candidates_by_size = {k: v for k, v in size_groups.items() if len(v) > 1}
        fast_hash_groups: dict[tuple[int, str], list[str]] = {}
        for size, paths in candidates_by_size.items():
            for path in paths:
                try:
                    fh = self.get_fast_hash(path)
                    if fh: fast_hash_groups.setdefault((size, fh), []).append(path)
                except: pass

        candidates_by_fast_hash = {k: v for k, v in fast_hash_groups.items() if len(v) > 1}
        full_hash_groups: dict[tuple[int, str, str], list[str]] = {}
        for (size, fh), paths in candidates_by_fast_hash.items():
            for path in paths:
                try:
                    fullh = self.get_full_hash(path)
                    if fullh: full_hash_groups.setdefault((size, fh, fullh), []).append(path)
                except: pass

        final_duplicates = {k: v for k, v in full_hash_groups.items() if len(v) > 1}
        for same_files in final_duplicates.values():
            same_files.sort(key=self.get_original_score)
            for duplicate in same_files[1:]:
                if self.send_to_quarantine(duplicate):
                    deleted_count += 1
        return deleted_count

    def execute_sorting(self) -> None:
        self.btn_execute.configure(state="disabled", text=self.t("btn_executing"))
        self.update_idletasks()

        if self.var_dest.get() and self.selected_dest_path:
            self.dest_folder = self.selected_dest_path
        else:
            self.dest_folder = self.source_folder

        self.session_history.clear()
        self.trashed_files.clear()
        os.makedirs(os.path.join(self.dest_folder, self.trash_dir_name), exist_ok=True)

        moved_count = 0
        deleted_count = 0
        current_time = time.time()

        try: days = max(int(self.entry_days.get()), 0)
        except ValueError: days = 7
        seconds_limit = days * 86400

        try: heavy_mb = max(int(self.entry_heavy_mb.get()), 0)
        except ValueError: heavy_mb = 500
        heavy_limit_bytes = heavy_mb * 1024 * 1024

        custom_word = self.entry_custom_word.get().strip().lower()
        custom_folder_name = self.entry_custom_folder.get().strip()

        active_extensions = {}
        for category, variable in self.cat_vars.items():
            if variable.get():
                for extension in FILE_EXTENSIONS[category]:
                    active_extensions[extension.lower()] = category

        files_to_process = self.collect_files()

        if files_to_process and self.var_duplicates.get():
            deleted_count += self.remove_duplicates(files_to_process)
            files_to_process = [f for f in files_to_process if os.path.exists(f)]

        for item_path in files_to_process:
            if not os.path.exists(item_path): continue

            try:
                file_name = os.path.basename(item_path)
                file_size = os.path.getsize(item_path)

                if self.var_filter_days.get():
                    newest_time = max(os.path.getmtime(item_path), os.path.getctime(item_path))
                    if (current_time - newest_time) < seconds_limit: continue

                if self.var_heavy.get() and file_size > heavy_limit_bytes:
                    if self.send_to_quarantine(item_path): deleted_count += 1
                    continue

                target_dir = None
                if custom_word and custom_folder_name and custom_word in file_name.lower():
                    target_dir = os.path.join(self.dest_folder, custom_folder_name)
                else:
                    _, extension = os.path.splitext(file_name)
                    extension = extension.lower()
                    if extension in active_extensions:
                        target_dir = os.path.join(self.dest_folder, active_extensions[extension])

                if target_dir is None: continue
                target_dir = os.path.normpath(target_dir)

                if os.path.normcase(os.path.dirname(item_path)) == os.path.normcase(target_dir):
                    continue

                os.makedirs(target_dir, exist_ok=True)
                dest_path = os.path.join(target_dir, file_name)

                if os.path.exists(dest_path):
                    name, ext = os.path.splitext(file_name)
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(target_dir, f"{name} ({counter}){ext}")
                        counter += 1

                shutil.move(item_path, dest_path)
                self.session_history.append((dest_path, item_path))
                moved_count += 1
            except: pass

        if self.var_empty_folders.get():
            self.remove_empty_folders()

        self.go_to_result(moved_count, deleted_count)

    def remove_empty_folders(self) -> None:
        protected_folders = self.get_protected_folders()
        folders = []
        for root, dirs, files in os.walk(self.source_folder, topdown=False):
            if root == self.source_folder: continue
            normalized = os.path.normcase(os.path.abspath(root))
            if normalized in protected_folders or self.trash_dir_name in normalized: continue
            
            inside_protected = any(self.is_inside_folder(root, p) for p in protected_folders)
            if not inside_protected: folders.append(root)

        folders.sort(key=lambda p: p.count(os.sep), reverse=True)
        for folder in folders:
            try:
                if not os.listdir(folder): os.rmdir(folder)
            except: pass

    def clean_empty_destination_folders(self) -> None:
        if not self.dest_folder or not os.path.exists(self.dest_folder):
            return

        possible_folders = [os.path.join(self.dest_folder, cat) for cat in FILE_EXTENSIONS.keys()]
        
        custom_folder = self.entry_custom_folder.get().strip()
        if custom_folder:
            possible_folders.append(os.path.join(self.dest_folder, custom_folder))

        for folder in possible_folders:
            if os.path.exists(folder) and os.path.isdir(folder):
                try:
                    if not os.listdir(folder):
                        os.rmdir(folder)
                except Exception:
                    pass

        if self.var_dest.get() and self.selected_dest_path:
            if os.path.exists(self.selected_dest_path) and not os.listdir(self.selected_dest_path):
                try:
                    os.rmdir(self.selected_dest_path)
                except Exception:
                    pass


    # ------------------------- Screen 3 -------------------------

    def build_result_screen(self, moved_count: int, deleted_count: int) -> None:
        self._result_moved = moved_count
        self._result_deleted = deleted_count
        self.clear_screen()

        self.frame_result = ctk.CTkFrame(self, fg_color=APP_BG)
        self.frame_result.pack(fill="both", expand=True)

        self.add_header(self.frame_result)

        body = self.make_card(self.frame_result, fg_color=SURFACE)
        body.pack(fill="both", expand=True, padx=28, pady=(2, 26))

        # Оборачиваем элементы "Готово!" во фрейм, который центрируется
        hero = ctk.CTkFrame(body, fg_color="transparent")
        hero.pack(fill="x", padx=32, pady=(28, 14))

        hero_center = ctk.CTkFrame(hero, fg_color="transparent")
        hero_center.pack(anchor="center")

        ctk.CTkLabel(
            hero_center, text="✓", width=62, height=62, corner_radius=31,
            fg_color=GREEN, text_color=APP_BG,
            font=("Segoe UI Semibold", 32)
        ).pack(side="left")

        title_box = ctk.CTkFrame(hero_center, fg_color="transparent")
        title_box.pack(side="left", padx=18)
        ctk.CTkLabel(
            title_box,
            text="Готово!" if self.current_lang == "RU" else "Done!",
            font=("Segoe UI Semibold", 28), text_color=TEXT
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_box,
            text="Порядок успешно наведен." if self.current_lang == "RU"
                 else "Your folder has been organized successfully.",
            font=("Segoe UI", 12), text_color=MUTED
        ).pack(anchor="w")

        stats = ctk.CTkFrame(body, fg_color="transparent")
        stats.pack(fill="x", padx=32, pady=(2, 18))
        stats.grid_columnconfigure((0, 1), weight=1)

        moved_card = self.make_card(stats, fg_color=SURFACE_2, border_color="#2B4D77")
        moved_card.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        ctk.CTkLabel(moved_card, text="▤", font=("Segoe UI", 25), text_color=INDIGO).pack(side="left", padx=18, pady=17)
        moved_box = ctk.CTkFrame(moved_card, fg_color="transparent")
        moved_box.pack(side="left", pady=14)
        ctk.CTkLabel(moved_box, text=str(moved_count), font=("Segoe UI Semibold", 25), text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(moved_box, text="файлов перемещено" if self.current_lang == "RU" else "files moved",
                     font=("Segoe UI", 10), text_color=MUTED).pack(anchor="w")

        del_card = self.make_card(stats, fg_color=SURFACE_2, border_color="#23665F")
        del_card.grid(row=0, column=1, sticky="nsew", padx=(7, 0))
        ctk.CTkLabel(del_card, text="♢", font=("Segoe UI", 27), text_color=TURQUOISE).pack(side="left", padx=18, pady=17)
        del_box = ctk.CTkFrame(del_card, fg_color="transparent")
        del_box.pack(side="left", pady=14)
        ctk.CTkLabel(del_box, text=str(deleted_count), font=("Segoe UI Semibold", 25), text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(del_box, text="в карантине" if self.current_lang == "RU" else "in quarantine",
                     font=("Segoe UI", 10), text_color=MUTED).pack(anchor="w")

        warning = ctk.CTkFrame(
            body, fg_color=WARNING_BG, corner_radius=15,
            border_width=1, border_color="#765C25"
        )
        warning.pack(fill="x", padx=32, pady=8)
        ctk.CTkLabel(
            warning, text="!", width=36, height=36, corner_radius=18,
            fg_color=WARNING, text_color=APP_BG,
            font=("Segoe UI Semibold", 19)
        ).pack(side="left", padx=(18, 14), pady=18)
        
        # Увеличен размер текста предупреждения (12 вместо 10)
        ctk.CTkLabel(
            warning, text=self.t("res_warn"),
            font=("Segoe UI", 12), text_color="#FFD878",
            justify="left", anchor="w", wraplength=690
        ).pack(side="left", fill="x", expand=True, padx=(0, 18), pady=15)

        actions = ctk.CTkFrame(body, fg_color="transparent")
        actions.pack(fill="x", padx=32, pady=(20, 8))

        self.btn_undo = ctk.CTkButton(
            actions, text=self.t("btn_undo"), height=52, corner_radius=14,
            fg_color=INDIGO, hover_color=INDIGO_HOVER,
            font=("Segoe UI Semibold", 12), command=self.undo_sorting
        )
        self.btn_undo.pack(fill="x", pady=(0, 10))

        if not self.session_history and not self.trashed_files:
            self.btn_undo.configure(state="disabled", fg_color=SURFACE_3)

        ctk.CTkButton(
            actions, text="▣  " + self.t("btn_restart"), height=44, corner_radius=13,
            fg_color="transparent", hover_color=SURFACE_2,
            border_width=1, border_color=BORDER, text_color=TEXT,
            font=("Segoe UI", 11), command=self.restart_app
        ).pack(fill="x")

        footer = ctk.CTkFrame(body, fg_color="transparent")
        footer.pack(fill="x", padx=32, pady=(12, 18))
        ctk.CTkLabel(
            footer,
            text=("ⓘ  Файлы не удаляются окончательно, пока окно результата открыто."
                  if self.current_lang == "RU"
                  else "ⓘ  Files are not permanently removed while this result window is open."),
            font=("Segoe UI", 9), text_color=MUTED
        ).pack(side="left")
        ctk.CTkLabel(
            footer, text="v1.0.0", font=("Segoe UI", 9), text_color=MUTED
        ).pack(side="right")

        # Кнопка доната (более светлая, жирная и немного приподнятая)
        ctk.CTkButton(
            self.frame_result, text=self.t("btn_donate"),
            width=190, height=34, corner_radius=11,
            fg_color="transparent", hover_color=SURFACE_2,
            text_color=TEXT, font=("Segoe UI Semibold", 11),
            command=lambda: webbrowser.open("https://t.me/")
        ).place(relx=0.5, rely=1.0, anchor="s", y=-8)

    def undo_sorting(self) -> None:
        answer = self.show_dialog(
            self.t("msg_undo_title"),
            self.t("msg_undo_text"),
            "warning", yes_no=True,
            yes_text="Вернуть файлы" if self.current_lang == "RU" else "Restore files"
        )
        if not answer:
            return

        self.btn_undo.configure(state="disabled", text=self.t("btn_undoing"))
        self.update_idletasks()

        for dest_path, orig_path in reversed(self.session_history):
            if not os.path.exists(dest_path):
                continue
            try:
                os.makedirs(os.path.dirname(orig_path), exist_ok=True)
                if not os.path.exists(orig_path):
                    shutil.move(dest_path, orig_path)
                else:
                    name, ext = os.path.splitext(os.path.basename(orig_path))
                    counter = 1
                    alt_path = orig_path
                    while os.path.exists(alt_path):
                        alt_path = os.path.join(os.path.dirname(orig_path), f"{name} (undo {counter}){ext}")
                        counter += 1
                    shutil.move(dest_path, alt_path)
            except Exception:
                pass

        for quarantine_path, orig_path in reversed(self.trashed_files):
            if not os.path.exists(quarantine_path):
                continue
            try:
                os.makedirs(os.path.dirname(orig_path), exist_ok=True)
                if not os.path.exists(orig_path):
                    shutil.move(quarantine_path, orig_path)
                else:
                    name, ext = os.path.splitext(os.path.basename(orig_path))
                    counter = 1
                    alt_path = orig_path
                    while os.path.exists(alt_path):
                        alt_path = os.path.join(os.path.dirname(orig_path), f"{name} (undo {counter}){ext}")
                        counter += 1
                    shutil.move(quarantine_path, alt_path)
            except Exception:
                pass
        self.clean_empty_destination_folders()
        self.session_history.clear()
        self.trashed_files.clear()
        self.btn_undo.configure(
            state="disabled", fg_color=SURFACE_3, text=self.t("btn_undone")
        )


if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()