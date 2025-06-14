import tkinter as tk

from gui.app import RecipeRecommenderApp


if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeRecommenderApp(root)
    root.mainloop()
