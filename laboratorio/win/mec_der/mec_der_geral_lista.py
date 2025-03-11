import pyodbc
from pyvis.network import Network
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

class WorkbenchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Diagram Workbench")
        self.setup_ui()
        self.conn = None

    def setup_ui(self):
        self.create_connection_frame()
        self.create_diagram_frame()

    def create_connection_frame(self):
        frame = ttk.LabelFrame(self.root, text="Conexão ao Banco de Dados")
        frame.pack(padx=10, pady=10, fill="x")

        fields = [
            ("Servidor:", "server_entry", "RONI\\SQLEXPRESS"),
            ("Banco de Dados:", "database_entry", "GATEC_MEC")
        ]

        for i, (label, attr, default) in enumerate(fields):
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, default)
            setattr(self, attr, entry)

        ttk.Button(frame, text="Conectar", command=self.connect_to_database).grid(
            row=len(fields), column=0, columnspan=2, pady=10)

    def create_diagram_frame(self):
        frame = ttk.LabelFrame(self.root, text="Gerar Diagrama")
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ttk.Button(frame, text="Gerar Diagrama", command=self.generate_diagram).pack(pady=10)
        self.status_label = ttk.Label(frame, text="Status: Aguardando conexão...", foreground="blue")
        self.status_label.pack(pady=10)

    def connect_to_database(self):
        try:
            self.conn = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={self.server_entry.get()};'
                f'DATABASE={self.database_entry.get()};Trusted_Connection=yes;'
            )
            self.status_label.config(text="Status: Conectado ao banco de dados.", foreground="green")
            messagebox.showinfo("Conexão", "Conectado ao banco de dados com sucesso!")
        except Exception as e:
            self.status_label.config(text="Status: Erro na conexão.", foreground="red")
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar: {e}")

    def get_database_info(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                c.TABLE_NAME, c.COLUMN_NAME, c.DATA_TYPE,
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
                    fkc.TABLE_NAME, fkc.COLUMN_NAME,
                    rc.TABLE_NAME AS REFERENCED_TABLE_NAME,
                    rc.COLUMN_NAME AS REFERENCED_COLUMN_NAME
                FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS r
                JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE fkc
                    ON r.CONSTRAINT_NAME = fkc.CONSTRAINT_NAME
                JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE rc
                    ON r.UNIQUE_CONSTRAINT_NAME = rc.CONSTRAINT_NAME
            ) fk ON c.TABLE_NAME = fk.TABLE_NAME AND c.COLUMN_NAME = fk.COLUMN_NAME
            ORDER BY c.TABLE_NAME, COLUMN_TYPE DESC;
        """)
        return cursor.fetchall()

    def generate_diagram(self):
        if not self.conn:
            messagebox.showerror("Erro", "Conecte-se ao banco de dados primeiro!")
            return

        net = Network(notebook=False, directed=True, height='800px', width='100%', bgcolor='#ffffff')
        net.barnes_hut(gravity=-5000, central_gravity=0.5, spring_length=150)

        table_columns = {}
        relationships = []

        for row in self.get_database_info():
            table_name, column_name, data_type, column_type, ref_table, ref_column = row
            table_columns.setdefault(table_name, []).append(
                f"{column_name} ({data_type}) [{column_type}]")
            if ref_table:
                relationships.append((table_name, ref_table, column_name))

        all_tables = set(table_columns.keys()) | {rel[1] for rel in relationships}
        
        for table in all_tables:
            net.add_node(table, label=table, title="\n".join(table_columns.get(table, [])),
                        shape="box", color="#1f78b4")

        for parent, child, column in relationships:
            net.add_edge(parent, child, label=f"{column} (1:N)")

        html_content = net.generate_html()
        with open("der_geral_lista.html", "w", encoding='utf-8') as f:
            script_position = html_content.find('</body>')
            if script_position != -1:
                html_content = html_content[:script_position] + """
                <div style="position: fixed; top: 10px; left: 10px; z-index: 1000; background: white; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                    <input list="tables" id="tableSearch" placeholder="Buscar tabela..." style="padding: 5px; margin-right: 5px; width: 200px;">
                    <datalist id="tables">
                    </datalist>
                    <button onclick="searchTable()" style="padding: 5px 10px;">Buscar</button>
                </div>

                <script>
                document.addEventListener("DOMContentLoaded", function() {
                if (typeof network === 'undefined') return;
                
                const networkCache = {
                    nodes: new Map(),
                    edges: new Map(),
                    highlighted: false,
                    updates: []
                };

                // Cria um map global para busca rápida das tabelas
                window.tableMap = new Map();
                
                // Flag para indicar se uma busca está ativa, de modo a inibir atualizações de cliques
                let searchActive = false;

                function throttle(func, limit) {
                    let inThrottle;
                    return function(...args) {
                    if (!inThrottle) {
                        func.apply(this, args);
                        inThrottle = true;
                        setTimeout(() => inThrottle = false, limit);
                    }
                    }
                }

                function batchUpdate(updates) {
                    if (updates.length === 0) return;
                    network.body.data.nodes.update(updates);
                    networkCache.updates = [];
                }

                function scheduleUpdate(nodeId, color) {
                    networkCache.updates.push({ id: nodeId, color: color });
                    if (networkCache.updates.length > 50) {
                    batchUpdate(networkCache.updates);
                    }
                }

                function updateColors(params) {
                    if (searchActive) return;  // Ignora atualizações se uma busca estiver ativa
                    if (!params.nodes && !params.edges) return;
                    networkCache.updates = [];
                    if (!networkCache.highlighted) {
                    networkCache.nodes.forEach((data, id) => {
                        scheduleUpdate(id, '#d3d3d3');
                    });
                    const highlightNodes = new Set(params.nodes || []);
                    (params.edges || []).forEach(edgeId => {
                        const edge = networkCache.edges.get(edgeId);
                        if (edge) {
                        highlightNodes.add(edge.from).add(edge.to);
                        }
                    });
                    highlightNodes.forEach(nodeId => {
                        scheduleUpdate(nodeId, 'red');
                    });
                    } else {
                    networkCache.nodes.forEach((data, id) => {
                        scheduleUpdate(id, data.originalColor);
                    });
                    }
                    batchUpdate(networkCache.updates);
                    networkCache.highlighted = !networkCache.highlighted;
                }

                // Função throttled para updateColors
                const throttledUpdateColors = throttle(updateColors, 150);

                function initializeCache() {
                    // Cache dos nós
                    const nodes = network.body.data.nodes.get();
                    nodes.forEach(node => {
                    networkCache.nodes.set(node.id, {
                        originalColor: node.color || '#1f78b4'
                    });
                    });
                    // Cache das arestas
                    network.body.data.edges.get().forEach(edge => {
                    networkCache.edges.set(edge.id, {
                        from: edge.from,
                        to: edge.to
                    });
                    });
                    // Popula a datalist com os nomes das tabelas ordenados alfabeticamente
                    const tablesList = document.getElementById('tables');
                    const sortedNodes = nodes.slice().sort((a, b) => a.label.localeCompare(b.label));
                    sortedNodes.forEach(node => {
                    const option = document.createElement('option');
                    option.value = node.label;
                    tablesList.appendChild(option);
                    window.tableMap.set(node.label, node);
                    });
                }

                function searchTable() {
                    const searchTerm = document.getElementById('tableSearch').value;
                    const foundNode = window.tableMap.get(searchTerm);
                    if (foundNode) {
                    searchActive = true;
                    network.focus(foundNode.id, {
                        scale: 1.5,
                        animation: {
                        duration: 1000,
                        easingFunction: 'easeInOutQuad'
                        }
                    });
                    networkCache.updates = [];
                    networkCache.nodes.forEach((data, id) => {
                        scheduleUpdate(id, '#d3d3d3');
                    });
                    scheduleUpdate(foundNode.id, 'red');
                    batchUpdate(networkCache.updates);
                    networkCache.highlighted = true;
                    // Aumenta o tempo de desativação para 5000ms (5 segundos)
                    setTimeout(() => {
                        searchActive = false;
                    }, 5000);
                    }
                }

                // Expondo a função searchTable para o escopo global
                window.searchTable = searchTable;

                document.getElementById('tableSearch').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                    searchTable();
                    }
                });

                // Aguarda a estabilização da rede antes de inicializar o cache
                network.once("stabilizationIterationsDone", function() {
                    initializeCache();
                });

                network.on("click", throttledUpdateColors);
                });
                </script>


                """ + html_content[script_position:]
            
            f.write(html_content)

        webbrowser.open("der_geral_lista.html")
        messagebox.showinfo("Diagrama Gerado", "Diagrama interativo salvo como 'der_geral_lista.html'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkbenchApp(root)
    root.mainloop()