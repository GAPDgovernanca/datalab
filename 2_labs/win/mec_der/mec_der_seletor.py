# DER interativo com lista das tabelas selecionadas

import pyodbc
from pyvis.network import Network
import tkinter as tk
from tkinter import ttk, messagebox, Listbox, MULTIPLE, StringVar, Text

class WorkbenchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Diagram Workbench")

        # Interface de conexão ao banco de dados
        self.connection_frame = ttk.LabelFrame(root, text="Conexão ao Banco de Dados")
        self.connection_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(self.connection_frame, text="Servidor:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.server_entry = ttk.Entry(self.connection_frame, width=30)
        self.server_entry.grid(row=0, column=1, padx=5, pady=5)
        self.server_entry.insert(0, "RONI\\SQLEXPRESS")

        ttk.Label(self.connection_frame, text="Banco de Dados:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.database_entry = ttk.Entry(self.connection_frame, width=30)
        self.database_entry.grid(row=1, column=1, padx=5, pady=5)
        self.database_entry.insert(0, "GATEC_MEC")

        self.connect_button = ttk.Button(self.connection_frame, text="Conectar", command=self.connect_to_database)
        self.connect_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame para seleção de tabelas
        self.table_frame = ttk.LabelFrame(root, text="Selecionar Tabelas")
        self.table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.filter_var = StringVar()
        ttk.Label(self.table_frame, text="Filtrar tabelas:").pack(pady=5)
        self.filter_entry = ttk.Entry(self.table_frame, textvariable=self.filter_var)
        self.filter_entry.pack(padx=10, pady=5, fill="x")
        self.filter_entry.bind("<KeyRelease>", self.filter_tables)

        self.table_listbox = Listbox(self.table_frame, selectmode=MULTIPLE, height=15)
        self.table_listbox.pack(padx=10, pady=10, fill="both", expand=True)

        self.load_tables_button = ttk.Button(self.table_frame, text="Carregar Tabelas", command=self.load_tables)
        self.load_tables_button.pack(pady=5)

        # Frame para exibição e geração de diagramas
        self.diagram_frame = ttk.LabelFrame(root, text="Gerar Diagrama")
        self.diagram_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.generate_button = ttk.Button(self.diagram_frame, text="Gerar Diagrama", command=self.generate_diagram)
        self.generate_button.pack(pady=10)

        self.status_label = ttk.Label(self.diagram_frame, text="Status: Aguardando conexão...", foreground="blue")
        self.status_label.pack(pady=10)

        # Rodapé para exibir tabelas selecionadas
        self.footer_frame = ttk.LabelFrame(root, text="Tabelas Selecionadas")
        self.footer_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.selected_tables_text = Text(self.footer_frame, height=5, wrap="word")
        self.selected_tables_text.pack(padx=10, pady=5, fill="both", expand=True)

        self.conn = None
        self.tables = []

    def connect_to_database(self):
        server = self.server_entry.get()
        database = self.database_entry.get()

        try:
            self.conn = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
            )
            messagebox.showinfo("Conexão", "Conectado ao banco de dados com sucesso!")
            self.status_label.config(text="Status: Conectado ao banco de dados.", foreground="green")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar: {e}")
            self.status_label.config(text="Status: Erro na conexão.", foreground="red")

    def load_tables(self):
        if not self.conn:
            messagebox.showerror("Erro", "Conecte-se ao banco de dados primeiro!")
            return

        query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';"
        cursor = self.conn.cursor()
        cursor.execute(query)

        self.tables = sorted([row.TABLE_NAME for row in cursor.fetchall()])
        self.update_table_listbox()
        messagebox.showinfo("Tabelas Carregadas", "As tabelas foram carregadas com sucesso. Selecione as desejadas para gerar o diagrama.")

    def update_table_listbox(self):
        filter_text = self.filter_var.get().lower()
        filtered_tables = [table for table in self.tables if filter_text in table.lower()]

        self.table_listbox.delete(0, tk.END)
        for table in filtered_tables:
            self.table_listbox.insert(tk.END, table)

    def filter_tables(self, event):
        self.update_table_listbox()

    def generate_diagram(self):
        if not self.conn:
            messagebox.showerror("Erro", "Conecte-se ao banco de dados primeiro!")
            return

        selected_tables = [self.table_listbox.get(i) for i in self.table_listbox.curselection()]
        if not selected_tables:
            messagebox.showerror("Erro", "Selecione pelo menos uma tabela para gerar o diagrama.")
            return

        # Atualizar lista de tabelas selecionadas no rodapé
        self.selected_tables_text.delete(1.0, tk.END)
        self.selected_tables_text.insert(tk.END, ", ".join(selected_tables))

        query = f"""
        SELECT 
            c.TABLE_NAME,
            c.COLUMN_NAME,
            c.DATA_TYPE,
            CASE 
                WHEN pk.COLUMN_NAME IS NOT NULL THEN 'PK'
                WHEN fk.COLUMN_NAME IS NOT NULL THEN 'FK'
                ELSE 'ATTR'
            END AS COLUMN_TYPE,
            fk.REFERENCED_TABLE_NAME,
            fk.REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS c
        LEFT JOIN (
            SELECT k.TABLE_NAME, k.COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE k
            JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS t
            ON k.CONSTRAINT_NAME = t.CONSTRAINT_NAME
            WHERE t.CONSTRAINT_TYPE = 'PRIMARY KEY'
        ) pk ON c.TABLE_NAME = pk.TABLE_NAME AND c.COLUMN_NAME = pk.COLUMN_NAME
        LEFT JOIN (
            SELECT 
                fkc.TABLE_NAME, 
                fkc.COLUMN_NAME,
                rt.TABLE_NAME AS REFERENCED_TABLE_NAME,
                rc.COLUMN_NAME AS REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS r
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE fkc
                ON r.CONSTRAINT_NAME = fkc.CONSTRAINT_NAME
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE rc
                ON r.UNIQUE_CONSTRAINT_NAME = rc.CONSTRAINT_NAME
            JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS rt
                ON rc.TABLE_NAME = rt.TABLE_NAME AND rt.CONSTRAINT_TYPE = 'PRIMARY KEY'
        ) fk ON c.TABLE_NAME = fk.TABLE_NAME AND c.COLUMN_NAME = fk.COLUMN_NAME
        WHERE c.TABLE_NAME IN ({', '.join(f"'{table}'" for table in selected_tables)})
        ORDER BY c.TABLE_NAME, COLUMN_TYPE DESC;
        """

        cursor = self.conn.cursor()
        cursor.execute(query)

        net = Network(notebook=False, directed=True, height='800px', width='100%', bgcolor='#ffffff', font_color='black')
        net.barnes_hut(gravity=-30000, central_gravity=0.3, spring_length=250, spring_strength=0.1, damping=0.9)

        table_columns = {}
        relationships = []

        for row in cursor.fetchall():
            table_name, column_name, data_type, column_type, referenced_table, referenced_column = row
            if table_name not in table_columns:
                table_columns[table_name] = []
            table_columns[table_name].append(f"{column_name} ({data_type}) [{column_type}]")

            if referenced_table:
                relationships.append((table_name, referenced_table, column_name))

        all_tables = set(table_columns.keys()).union({rel[1] for rel in relationships})

        for table in all_tables:
            tooltip = "\n".join(table_columns.get(table, []))
            net.add_node(table, label=table, title=tooltip or "No columns", shape="box", color="#1f78b4")

        for parent, child, column in relationships:
            net.add_edge(parent, child, label=f"{column} (1:N)")

        net.write_html("der_seletor.html")
        import webbrowser
        webbrowser.open("der_seletor.html")
        messagebox.showinfo("Diagrama Gerado", "Diagrama interativo salvo como 'der_seletor.html'. Abra no navegador.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkbenchApp(root)
    root.mainloop()
