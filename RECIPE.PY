import tkinter as tk
from tkinter import messagebox,  Listbox, Scrollbar
import requests

API_KEY = '786e666d575f490a86274f0c326db504'

class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Management System")

        self.search_label = tk.Label(root, text="Search for Recipes:")
        self.search_label.pack()

        self.search_entry = tk.Entry(root, width=50)
        self.search_entry.pack()

        self.search_button = tk.Button(root, text="Search", command=self.search_recipes)
        self.search_button.pack()

        self.recipe_listbox = Listbox(root, width=100, height=20)
        self.recipe_listbox.pack()

        self.scrollbar = Scrollbar(root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.recipe_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.recipe_listbox.yview)

        self.recipe_listbox.bind('<<ListboxSelect>>', self.show_recipe_details)

        self.recipes = []

    def search_recipes(self):
        query = self.search_entry.get()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a search term.")
            return

        url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={API_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            messagebox.showerror("API Error", "Failed to fetch recipes.")
            return

        data = response.json()
        self.recipes = data.get('results', [])
        self.update_recipe_listbox()

    def update_recipe_listbox(self):
        self.recipe_listbox.delete(0, tk.END)
        for recipe in self.recipes:
            self.recipe_listbox.insert(tk.END, recipe['title'])

    def show_recipe_details(self, event):
        selection = event.widget.curselection()
        if not selection:
            return

        index = selection[0]
        recipe_id = self.recipes[index]['id']

        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            messagebox.showerror("API Error", "Failed to fetch recipe details.")
            return

        recipe_details = response.json()
        self.display_recipe_details(recipe_details)

    def display_recipe_details(self, recipe_details):
        title = recipe_details.get('title', 'No title')
        summary = recipe_details.get('summary', 'No summary').replace('<b>', '').replace('</b>', '')

        details_window = tk.Toplevel(self.root)
        details_window.title(title)

        details_label = tk.Label(details_window, text=summary, wraplength=500, justify=tk.LEFT)
        details_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()