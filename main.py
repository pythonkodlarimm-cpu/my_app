from pathlib import Path
import json
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivy.core.text import LabelBase
from kivy.clock import Clock


# ==================================================
# BASE / FONT
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
FONT_PATH = BASE_DIR / "fonts" / "RobotoMono-Regular.ttf"

USE_MONO = False
if FONT_PATH.exists():
    LabelBase.register(name="Mono", fn_regular=str(FONT_PATH))
    USE_MONO = True


def mono(**kw):
    if USE_MONO:
        kw["font_name"] = "Mono"
    return kw


# ==================================================
# THEME
# ==================================================

BG_PANEL = (0.12, 0.12, 0.12, 1)
BG_INPUT = (0.14, 0.14, 0.14, 1)
TEXT_COL = (1, 1, 1, 1)

GREEN = (0.15, 0.15, 0.15, 1)
BACK = (0.1, 0.1, 0.1, 1)

EXCLUDE = {".git", "__pycache__", ".idea", ".vscode", ".DS_Store"}


# ==================================================
# INFO POPUP (3 SN)
# ==================================================

def show_info(message: str):
    popup = Popup(
        title="Bilgi",
        content=Label(text=message, color=TEXT_COL),
        size_hint=(None, None),
        size=(dp(420), dp(160)),
    )
    popup.open()
    Clock.schedule_once(lambda *_: popup.dismiss(), 3)


# ==================================================
# FILES
# ==================================================

TAHTA_FILE = BASE_DIR / ".tahta.txt"
NOTES_FILE = BASE_DIR / ".notes.json"


# ==================================================
# STORAGE
# ==================================================

def load_notes():
    if NOTES_FILE.exists():
        return json.loads(NOTES_FILE.read_text(encoding="utf-8"))
    return []


def save_notes(notes):
    NOTES_FILE.write_text(
        json.dumps(notes, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


# ==================================================
# TAHTA
# ==================================================

class TahtaView(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation="vertical", spacing=dp(6), padding=dp(6), **kw)

        self.text = TextInput(
            text=TAHTA_FILE.read_text(encoding="utf-8") if TAHTA_FILE.exists() else "",
            multiline=True,
            **mono(font_size=dp(14)),
            background_color=BG_INPUT,
            foreground_color=TEXT_COL,
        )
        self.text.bind(text=self._save)

        scroll = ScrollView()
        scroll.add_widget(self.text)
        self.add_widget(scroll)

    def _save(self, *_):
        TAHTA_FILE.write_text(self.text.text, encoding="utf-8")


# ==================================================
# NOT DEFTERİ
# ==================================================

class NotesView(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation="vertical", spacing=dp(6), padding=dp(6), **kw)

        self.notes = load_notes()

        self.title_input = TextInput(
            hint_text="Başlık",
            size_hint_y=None,
            height=dp(40),
            **mono(font_size=dp(14)),
            background_color=BG_INPUT,
            foreground_color=TEXT_COL,
        )

        self.body_input = TextInput(
            hint_text="Not içeriği",
            multiline=True,
            **mono(font_size=dp(14)),
            background_color=BG_INPUT,
            foreground_color=TEXT_COL,
        )

        add_btn = Button(
            text="➕ NOT EKLE",
            size_hint_y=None,
            height=dp(44),
            background_color=GREEN,
        )
        add_btn.bind(on_release=self.add_note)

        self.list_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(4),
        )
        self.list_box.bind(minimum_height=self.list_box.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.list_box)

        self.add_widget(self.title_input)
        self.add_widget(self.body_input)
        self.add_widget(add_btn)
        self.add_widget(scroll)

        self.refresh()

    def add_note(self, *_):
        if not self.title_input.text.strip() or not self.body_input.text.strip():
            return

        self.notes.insert(0, {
            "id": datetime.utcnow().isoformat(),
            "title": self.title_input.text,
            "body": self.body_input.text,
        })

        save_notes(self.notes)
        self.title_input.text = ""
        self.body_input.text = ""
        self.refresh()

    def refresh(self):
        self.list_box.clear_widgets()
        for note in self.notes:
            btn = Button(
                text=f"📝 {note['title']}",
                size_hint_y=None,
                height=dp(42),
                background_color=BG_PANEL,
                color=TEXT_COL,
                halign="left",
            )
            btn.bind(on_release=lambda _, n=note: self.open_note(n))
            self.list_box.add_widget(btn)

    def copy_all(self):
        Clipboard.copy(
            "\n\n".join(f"{n['title']}\n{n['body']}" for n in self.notes)
        )
        show_info("✅ Tüm notlar kopyalandı")

    # 🔴 ÖNEMLİ: METOT SINIFIN İÇİNDE
    def open_note(self, note):
        popup = Popup(size_hint=(0.95, 0.95), auto_dismiss=False)

        title = TextInput(
            text=note["title"],
            size_hint_y=None,
            height=dp(44),
            **mono(font_size=dp(16)),
            background_color=BG_INPUT,
            foreground_color=TEXT_COL,
        )

        body = TextInput(
            text=note["body"],
            multiline=True,
            **mono(font_size=dp(14)),
            background_color=BG_INPUT,
            foreground_color=TEXT_COL,
        )

        body.size_hint_y = None
        body.bind(minimum_height=body.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(body)

        bar = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))

        back = Button(text="⬅️ Geri", background_color=BACK)
        delete = Button(text="🗑️ Sil", background_color=BACK)
        save = Button(text="💾 Kaydet", background_color=GREEN)

        back.bind(on_release=lambda *_: popup.dismiss())
        save.bind(on_release=lambda *_: self._save_note(note, title, body, popup))
        delete.bind(on_release=lambda *_: self._delete_note(note, popup))

        bar.add_widget(back)
        bar.add_widget(delete)
        bar.add_widget(save)

        root = BoxLayout(orientation="vertical", spacing=dp(6), padding=dp(6))
        root.add_widget(title)
        root.add_widget(scroll)
        root.add_widget(bar)

        popup.content = root
        popup.open()

    def _save_note(self, note, title, body, popup):
        note["title"] = title.text
        note["body"] = body.text
        save_notes(self.notes)
        self.refresh()
        popup.dismiss()

    def _delete_note(self, note, popup):
        self.notes.remove(note)
        save_notes(self.notes)
        self.refresh()
        popup.dismiss()


# ==================================================
# TREE + CONTRACT
# ==================================================

def visible(p: Path):
    return p.name not in EXCLUDE


def build_tree(folder: Path, prefix=""):
    lines = []
    items = [p for p in sorted(folder.iterdir()) if visible(p)]
    for i, p in enumerate(items):
        last = i == len(items) - 1
        lines.append(prefix + ("└── " if last else "├── ") + p.name)
        if p.is_dir():
            lines.extend(build_tree(p, prefix + ("    " if last else "│   ")))
    return lines


def build_architecture_contract(folder: Path, tree_text: str) -> str:
    return (
        "# 📐 ARCHITECTURE CONTRACT\n\n"
        "## 📅 Generated At\n"
        f"{datetime.utcnow().isoformat()} UTC\n\n"
        "## 📁 Root Folder\n"
        f"{folder.name}/\n\n"
        "## 🌳 Folder Tree\n"
        "```text\n"
        f"{tree_text}\n"
        "```\n\n"
        "## 🔒 Rules\n"
        "- Bu dosya mimari sözleşmedir\n"
        "- Manuel düzenlenmez\n"
        "- Guard / Tooling referans alır\n"
    )


def write_architecture_contract(folder: Path, content: str):
    (folder / "ARCHITECTURE_CONTRACT.md").write_text(content, encoding="utf-8")


class TreeView(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation="vertical", spacing=dp(6), padding=dp(6), **kw)

        self.selected_folder = None

        self.folder_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(4),
        )
        self.folder_box.bind(minimum_height=self.folder_box.setter("height"))

        folder_scroll = ScrollView(size_hint_y=0.35)
        folder_scroll.add_widget(self.folder_box)

        self.tree_text = TextInput(
            readonly=True,
            multiline=True,
            size_hint_y=None,
            **mono(font_size=dp(13)),
            background_color=BG_INPUT,
            foreground_color=TEXT_COL,
        )
        self.tree_text.bind(minimum_height=self.tree_text.setter("height"))

        tree_scroll = ScrollView()
        tree_scroll.add_widget(self.tree_text)

        self.add_widget(folder_scroll)
        self.add_widget(tree_scroll)

        self._load_folders()

    def _load_folders(self):
        self.folder_box.clear_widgets()
        for p in sorted(BASE_DIR.iterdir()):
            if p.is_dir() and visible(p):
                btn = Button(
                    text=f"📁 {p.name}",
                    size_hint_y=None,
                    height=dp(42),
                    background_color=BG_PANEL,
                    color=TEXT_COL,
                )
                btn.bind(on_release=lambda _, f=p: self.show_tree(f))
                self.folder_box.add_widget(btn)

    def show_tree(self, folder: Path):
        self.selected_folder = folder
        lines = [f"{folder.name}/"] + build_tree(folder)
        self.tree_text.text = "\n".join(lines)
        self.tree_text.cursor = (0, 0)

    def generate_contract(self):
        if not self.selected_folder:
            show_info("❗ Önce bir klasör seçmelisin")
            return

        content = build_architecture_contract(
            self.selected_folder,
            self.tree_text.text
        )
        write_architecture_contract(self.selected_folder, content)
        show_info("✅ ARCHITECTURE_CONTRACT.md oluşturuldu")


# ==================================================
# MAIN UI
# ==================================================

class MainUI(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation="vertical", **kw)

        top = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(6),
            padding=dp(6),
        )

        self.btn_tahta = Button(text="🧾 TAHTA", background_color=BACK)
        self.btn_notes = Button(text="📝 NOTLAR", background_color=BACK)
        self.btn_tree = Button(text="🌳 AĞAÇ", background_color=BACK)

        top.add_widget(self.btn_tahta)
        top.add_widget(self.btn_notes)
        top.add_widget(self.btn_tree)

        self.container = BoxLayout()
        self.action_bar = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            padding=dp(6),
            spacing=dp(6),
        )

        self.tahta = TahtaView()
        self.notes = NotesView()
        self.tree = TreeView()

        self.btn_tahta.bind(on_release=lambda *_: self.show(self.tahta))
        self.btn_notes.bind(on_release=lambda *_: self.show(self.notes))
        self.btn_tree.bind(on_release=lambda *_: self.show(self.tree))

        self.add_widget(top)
        self.add_widget(self.container)
        self.add_widget(self.action_bar)

        self.show(self.tahta)

    def show(self, widget):
        self.container.clear_widgets()
        self.action_bar.clear_widgets()
        self.container.add_widget(widget)

        if widget is self.tahta:
            btn = Button(text="📋 KOPYALA", background_color=GREEN)
            btn.bind(on_release=lambda *_: (
                Clipboard.copy(self.tahta.text.text),
                show_info("✅ Tahta kopyalandı")
            ))
            self.action_bar.add_widget(btn)

        elif widget is self.notes:
            btn = Button(text="📋 KOPYALA", background_color=GREEN)
            btn.bind(on_release=lambda *_: self.notes.copy_all())
            self.action_bar.add_widget(btn)

        elif widget is self.tree:
            copy_btn = Button(text="📋 KOPYALA", background_color=GREEN)
            copy_btn.bind(on_release=lambda *_: (
                Clipboard.copy(self.tree.tree_text.text),
                show_info("✅ Ağaç kopyalandı")
            ))

            contract_btn = Button(
                text="📜 ARCHITECTURE_CONTRACT.md",
                background_color=GREEN,
            )
            contract_btn.bind(on_release=lambda *_: self.tree.generate_contract())

            self.action_bar.add_widget(copy_btn)
            self.action_bar.add_widget(contract_btn)


# ==================================================
# APP
# ==================================================

class ArchitectureToolApp(App):
    def build(self):
        self.title = "Architecture Tool"
        return MainUI()


if __name__ == "__main__":
    ArchitectureToolApp().run()