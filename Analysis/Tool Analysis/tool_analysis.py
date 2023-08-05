import tkinter as tk
from tkinter import ttk
import csv
from tkinter import messagebox


class WrapCellRenderer(ttk.Treeview):
    def __init__(self, master=None, **kw):
        ttk.Treeview.__init__(self, master, **kw)

        # Configure cell renderer to wrap text
        self.column("#0", stretch=tk.YES)
        self.column("#0", anchor="w")

        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event):
        self.update()


def search_domains():
    tool = entry.get().lower().replace("_", " ")

    with open(
            'C:/Users/Vishwas/Desktop/Thesis/tool_fetch_dbpedia/Second Revison/dbpedia_tools_with_translations_alt_labels_FINAL.csv',
            'r') as file:
        csv_reader = csv.DictReader(file)

        match_rows = []
        for row in csv_reader:
            parent_url = row['Parent_Url']
            tool_url = row['Tool_Url']
            translated_parent_url = row['Translated Parent_Url']
            translated_tool_url = row['Translated Tool_Url']
            parent_url_alt_labels = row['Parent URL Alternate Labels']
            tool_url_alt_labels = row['Tool Url Alternate Labels']

            parent_url_modified = parent_url.split("http://dbpedia.org/resource/")[1].lower().replace("_", " ")
            tool_url_modified = tool_url.split("http://dbpedia.org/resource/")[1].lower().replace("_", " ")
            translated_parent_url_modified = translated_parent_url.lower().replace("_", " ")
            translated_tool_url_modified = translated_tool_url.lower().replace("_", " ")

            if tool == parent_url_modified or tool == tool_url_modified or tool == translated_parent_url_modified or tool == translated_tool_url_modified:
                match_rows.append([
                    parent_url_modified,
                    translated_parent_url,
                    tool_url_modified,
                    translated_tool_url,
                    tool_url_alt_labels,
                    parent_url_alt_labels
                ])

        if len(match_rows) > 0:
            display_match_rows(match_rows)
        else:

            with open(
                    'C:/Users/Vishwas/Desktop/Thesis/tool_fetch_dbpedia/Second Revison/Concept Analysis/dbpedia_concepts.csv',
                    'r') as concept_file:
                concept_reader = csv.DictReader(concept_file)

                for row in concept_reader:
                    parent_url = row['\ufeffConcept_Parent_Url']
                    tool_url = row['Concept_Url']

                    parent_url_modified = parent_url.split("http://dbpedia.org/resource/")[1].lower().replace("_", " ")
                    tool_url_modified = tool_url.split("http://dbpedia.org/resource/")[1].lower().replace("_", " ")

                    if tool == parent_url_modified or tool == tool_url_modified:
                        messagebox.showinfo("Concept Found", f"The tool '{tool}' is a concept.")
                        break

                messagebox.showinfo("Match Not Found", "Tool not found in any column.")


def display_match_rows(match_rows):
    match_window = tk.Toplevel()
    match_window.title("Match Results")

    tree = WrapCellRenderer(match_window)
    tree.pack(fill=tk.BOTH, expand=True)

    tree["columns"] = (
    "Parent_URL", "Translated_Parent_URL", "Tool_url", "Translated_Tool_URL", "Tool_URL_Alternate_Labels",
    "Parent_URL_Alternate_Labels")

    tree.heading("Parent_URL", text="Parent URL")
    tree.heading("Translated_Parent_URL", text="Translated Parent URL")
    tree.heading("Tool_url", text="Tool URL")
    tree.heading("Translated_Tool_URL", text="Translated Tool URL")
    tree.heading("Tool_URL_Alternate_Labels", text="Tool URL Alternate Labels")
    tree.heading("Parent_URL_Alternate_Labels", text="Parent URL Alternate Labels")

    for row in match_rows:
        tree.insert("", "end", values=row)


window = tk.Tk()

window.title("Tool Domain App")

label = tk.Label(window, text="Please enter your tool:")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Search Domains", command=search_domains)
button.pack()

window.mainloop()
