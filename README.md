<div align="right">
  <a href="#-file-sorter-ru">🇷🇺 Русский</a> | <a href="#-file-sorter-en">🇺🇸 English</a>
</div>

<a id="-file-sorter-ru"></a>

# 📂 File Sorter (RU)

![Windows](https://img.shields.io/badge/OS-Windows-blue?style=flat-square&logo=windows)
![Python](https://img.shields.io/badge/Python-3.10+-yellow?style=flat-square&logo=python)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-indigo?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

<p align="center">
<a href="https://pay.cloudtips.ru/p/6f09c8e2">
<img src="assets/qerwr.png" width="200" alt="cloudtips">
</a>
&nbsp;&nbsp;&nbsp;&nbsp;
<img src="assets/qrCode.png" width="200" alt="cloudtipsQR">
</p>

**File Sorter** — это удобная утилита с современным графическим интерфейсом для автоматического наведения порядка в папках (например, в «Загрузках» или на «Рабочем столе»). 

Программа сканирует выбранную директорию, распределяет файлы по логичным категориям, находит дубликаты и удаляет мусор. Всё это — с максимальным контролем со стороны пользователя и надежной защитой от случайного удаления важных данных.

<!-- 📸 СЮДА ПОТОМ МОЖНО ВСТАВИТЬ СКРИНШОТ ПРОГРАММЫ (например: ![Screenshot](link)) -->

## ✨ Ключевые возможности

* 🧹 **Умная сортировка:** Автоматическое распределение файлов по категориям (Видео, Музыка, Документы, Изображения, Архивы и т.д.) или по вашим ключевым словам.
* 🛡️ **Абсолютная безопасность (Undo):** Программа не удаляет файлы безвозвратно в процессе работы. Весь мусор и дубликаты отправляются в скрытую папку-карантин. Если вам не понравился результат сортировки, достаточно нажать **«Вернуть всё как было»** — и файлы моментально вернутся на свои исходные места.
* 🔍 **Точный поиск дубликатов:** Используется двухэтапный алгоритм. Сначала файлы сверяются по размеру, затем по быстрому хэшу (первые 64 КБ), и только при совпадении вычисляется полный MD5. Это бережет жесткий диск и работает очень быстро.
* 🗑️ **Гибкая очистка:** Автоматическое удаление пустых папок, фильтрация недавних файлов (чтобы не трогать свежие скачивания) и удаление тяжелых файлов по заданному размеру.

---

## 🚀 Установка и запуск

### Вариант 1: Не требует установки Python
Самый простой способ — скачать уже скомпилированную версию программы.

1. Перейдите в раздел **[Releases](../../releases)** на GitHub.
2. Скачайте последний `.zip` архив с программой.
3. Распакуйте архив в любую удобную папку.
4. Запустите файл `File_Sorter.exe` (установка не требуется, утилита портативная).

### Вариант 2: Запуск из исходного кода
Если вы хотите запустить проект напрямую через Python или внести изменения в код.

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/AISofter-st/FileSorter.git
   cd File_Sorter
   pip install customtkinter tkinterdnd2 pillow
   python File_Sorter.py

## 💡 Как это работает

* **Выберите папку:** Перетащите нужную папку в окно программы (Drag & Drop) или выберите её через кнопку «Обзор».
* **Настройте фильтры:**  Выберите категории для сортировки, настройте удаление дубликатов или тяжелых файлов.
* **Нажмите «Навести порядок»:** Программа отсортирует файлы и покажет статистику.
* **Проверьте результат: Файлы хранятся на диске пока открыто окно с результатами работы программы**. Откройте вашу папку. Если всё устраивает — просто закройте программу, карантин очистится навсегда. Если что-то не так — нажмите кнопку отмены.

<div align="right">
  <a href="#-file-sorter-ru">🇷🇺 Русский</a> | <a href="#-file-sorter-en">🇺🇸 English</a>
</div>

<a id="-file-sorter-en"></a>

# 📂 File Sorter (EN)
![Image](https://img.shields.io/badge/OS-Windows-blue?style=flat-square&logo=windows)
![Image](https://img.shields.io/badge/Python-3.10+-yellow?style=flat-square&logo=python)
![Image](https://img.shields.io/badge/UI-CustomTkinter-indigo?style=flat-square)
![Image](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**File Sorter**  is a handy utility with a modern graphical interface designed to automatically organize messy folders (such as "Downloads" or "Desktop").

The application scans the selected directory, categorizes files into logical folders, detects exact duplicates, and removes unused empty folders. All of this is done with maximum user control and reliable protection against accidental deletion of important data.

## ✨ Key Features

* 🧹 **Smart Categorization:**  Automatically distributes files into folders (Video, Music, Documents, Images, Archives, etc.) or by your custom keywords.
* 🛡️ **Absolute Safety (1-click Undo):**  The program never deletes files permanently during operation. All duplicates and heavy files are temporarily sent to a hidden quarantine folder. If you don't like the result, simply click "Revert everything" — and all files will instantly return to their original locations.
* 🔍 **Precise Duplicate Finder:** Uses a two-step algorithm. First, files are compared by size, then by a fast hash (first 64 KB), and only if there's a match, the full MD5 hash is calculated. This saves disk resources and works blazingly fast.
* 🗑️ **Flexible Cleanup:** Automatically deletes empty folders, filters out recent files (so fresh downloads remain untouched), and removes heavy files over a specified size.

## 🚀 Installation & Usage

### Option 1: No Python Required

The easiest way is to download the compiled ready-to-use application.
1. Go to the **[Releases](../../releases)** section on GitHub.
2. Download the latest `.zip` archive.
3. Extract the archive into any folder.
4. Run `File_Sorter.exe` (no installation required, the app is fully portable).

### Option 2: Run from Source

If you want to run the project via Python or modify the code.
1. Clone the repository:
    code
    ~~~Bash
    git clone https://github.com/AISofter-st/FileSorter.git
    cd File_Sorter
    pip install customtkinter tkinterdnd2 pillow
    python File_Sorter.py

# 💡 How It Works

* **Select a Folder:** Drag and drop the desired folder into the app window or select it via the "Browse" button.
* **Configure Filters:** Choose categories for sorting and configure duplicate/heavy file removal settings.
* **Click "Organize Files":** The application will sort your files and display the statistics.
* **Check the Result: Your original files are kept safe on the disk as long as the result window remains open**. Open your sorted folder. If everything looks good — simply close the program, and the quarantine folder will be permanently deleted. If something went wrong — hit the Undo button.
&nbsp;&nbsp;&nbsp;&nbsp;
![Скачивания/Download](https://img.shields.io/github/downloads/AISofter-st/FileSorter/total?color=blue&label=Скачиваний/Download)

