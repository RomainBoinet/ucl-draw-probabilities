import tkinter as tk
from tkinter import ttk, simpledialog, filedialog
import threading
import csv
import numpy as np
from ucl_draw_probabilities.logic import Equipe, TableauProbas2023


def create_app():
    """
    Create and configure the Tkinter GUI for computing UCL draw probabilities

    Returns
    -------
    tk.Tk
        The main Tkinter window ready to be launched with mainloop()
    """

    fenetre = tk.Tk()
    fenetre.title("UCL Round of 16 Draw Probabilities Calculator")
    fenetre.columnconfigure(0, weight=1)

    try:
        fenetre.iconbitmap("logoLDC.ico")
    except tk.TclError:
        print("⚠️ Icon not found, using default icon")

    # ================================
    # SECTION: TEAM AND COUNTRY TABLES
    # ================================
    label_equipes = tk.Label(fenetre, text="Teams")
    label_equipes.grid(row=0, column=0, sticky="nsew")

    tree_equipes = ttk.Treeview(
        fenetre,
        columns=("Group", "First", "Second"),
        show="headings",
        height=8
    )
    tree_equipes.heading("Group", text="Group")
    tree_equipes.heading("First", text="First")
    tree_equipes.heading("Second", text="Second")

    groupes = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for g in groupes:
        tree_equipes.insert("", "end", values=(g, f"Team{g}1", f"Team{g}2"))
    tree_equipes.grid(row=1, column=0)
    tree_equipes.column("Group", width=50)

    label_pays = tk.Label(fenetre, text="Countries")
    label_pays.grid(row=0, column=1)

    tree_pays = ttk.Treeview(
        fenetre,
        columns=("Group", "First", "Second"),
        show="headings",
        height=8
    )
    tree_pays.heading("Group", text="Group")
    tree_pays.heading("First", text="First")
    tree_pays.heading("Second", text="Second")

    for g in groupes:
        tree_pays.insert("", "end", values=(g, f"Country{g}1", f"Country{g}2"))
    tree_pays.grid(row=1, column=1)
    tree_pays.column("Group", width=50)

    # =====================
    # SECTION: PROBABILITY TABLE
    # =====================
    label_proba = tk.Label(fenetre, text="Match Probabilities")
    label_proba.grid(row=3, columnspan=2)

    tree_proba = ttk.Treeview(
        fenetre,
        columns=["empty"] + groupes,
        show="headings",
        height=8
    )
    tree_proba.heading("empty", text="")
    tree_proba.column("empty", width=100)

    for i in range(8):
        tree_proba.heading(f"#{i+2}", text=f"Team{groupes[i]}2")
        tree_proba.column(f"#{i+2}", anchor="center", width=100)

    for i in range(8):
        tree_proba.insert("", "end", values=(f"Team{groupes[i]}1",) + ("0%",) * 8)

    tree_proba.grid(row=4, columnspan=2)

    # =========================================
    # SECTION: EDITION FUNCTIONS (TEAMS + COUNTRIES)
    # =========================================
    def edit_cell_equipes(event):
        """
        Handle double-click events on the team table to edit team names

        Parameters
        ----------
        event : tk.Event
            The Tkinter event triggered by double-clicking on a table cell
        """
        region = tree_equipes.identify("region", event.x, event.y)
        if region == "cell":
            rowid = tree_equipes.identify_row(event.y)
            column = tree_equipes.identify_column(event.x)
            item = tree_equipes.item(rowid)
            values = list(item["values"])
            new_value = simpledialog.askstring("Edit Team", "Enter the new team name")
            if new_value:
                if column == "#2":
                    values[1] = new_value
                    tree_equipes.item(rowid, values=values)
                    tree_proba.set(rowid, "#1", new_value)
                elif column == "#3":
                    values[2] = new_value
                    tree_equipes.item(rowid, values=values)
                    index = groupes.index(values[0])
                    tree_proba.heading(f"#{index+2}", text=new_value)

    def edit_cell_pays(event):
        """
        Handle double-click events on the country table to edit country names

        Parameters
        ----------
        event : tk.Event
            The Tkinter event triggered by double-clicking on a table cell
        """
        region = tree_pays.identify("region", event.x, event.y)
        if region == "cell":
            rowid = tree_pays.identify_row(event.y)
            column = tree_pays.identify_column(event.x)
            item = tree_pays.item(rowid)
            values = list(item["values"])
            new_value = simpledialog.askstring("Edit Country", "Enter the new country")
            if new_value:
                if column == "#2":
                    values[1] = new_value
                elif column == "#3":
                    values[2] = new_value
                tree_pays.item(rowid, values=values)

    tree_equipes.bind("<Double-1>", edit_cell_equipes)
    tree_pays.bind("<Double-1>", edit_cell_pays)

    # ====================================
    # SECTION: UPDATE PROBABILITIES BUTTON
    # ====================================
    def update_probabilities():
        """
        Compute and update the probability table based on current teams and countries
        """
        listeChapeau12023, listeChapeau22023 = [], []
        label_proba.config(text="Computing probabilities... ⏳")
        fenetre.update_idletasks()

        equipes, pays = [], []
        for row in tree_equipes.get_children():
            v = tree_equipes.item(row)["values"]
            equipes.append(v[1])
            equipes.append(v[2])
        for row in tree_pays.get_children():
            v = tree_pays.item(row)["values"]
            pays.append(v[1])
            pays.append(v[2])

        for i in range(0, len(equipes), 2):
            eq1 = Equipe(equipes[i], 1, pays[i], groupes[i // 2])
            eq2 = Equipe(equipes[i + 1], 2, pays[i + 1], groupes[i // 2])
            listeChapeau12023.append(eq1)
            listeChapeau22023.append(eq2)

        proba_table = TableauProbas2023(listeChapeau12023, listeChapeau22023)
        rows = tree_proba.get_children()
        for i in range(8):
            for j in range(8):
                tree_proba.set(rows[i], f"#{j + 2}", f"{proba_table[i, j] * 100:.2f}%")

        label_proba.config(text="Match Probabilities ✅")

    def update_probabilities_threaded():
        """
        Run the probability computation in a separate thread to keep the GUI responsive
        """
        threading.Thread(target=update_probabilities, daemon=True).start()

    tk.Button(
        fenetre,
        text="Compute Probabilities",
        command=update_probabilities_threaded
    ).grid(row=5, columnspan=2)

    # =========================
    # SECTION: EXPORT TO CSV
    # =========================
    def export_csv():
        """
        Export the probability table to a CSV file
        """
        data = []
        columns = [tree_proba.heading(f"#{i}", "text") for i in range(1, 10)]
        data.append(columns)
        for row in tree_proba.get_children():
            data.append(tree_proba.item(row)["values"])
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if filename:
            with open(filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)

    tk.Button(fenetre, text="Export CSV", command=export_csv).grid(row=5, column=0, sticky="w")

    return fenetre