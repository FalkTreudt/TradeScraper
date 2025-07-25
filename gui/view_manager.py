# gui/view_manager.py
import tkinter as tk

class ViewManager:
    def __init__(self, root):
        self.root = root
        self.current_view = None

    def show_view(self, view_class, *args, **kwargs):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = view_class(self.root, self, *args, **kwargs)
        self.current_view.pack(fill="both", expand=True)
