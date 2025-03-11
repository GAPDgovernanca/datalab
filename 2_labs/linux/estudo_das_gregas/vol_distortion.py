import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk, messagebox
import mplcursors

# Função para calcular volatilidade implícita
def implied_volatility(option_price, S, K, T, r, option_type='call'):
    def bs_price(sigma):
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option_type == 'call':
            return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2) - option_price
        elif option_type == 'put':
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1) - option_price
    
    try:
        iv = brentq(bs_price, 0.001, 5.0)
        return iv
    except ValueError:
        return np.nan

# Função para capturar dados de opções
def get_option_chain(ticker_symbol, risk_free_rate):
    stock = yf.Ticker(ticker_symbol)
    S = stock.history(period="1d")['Close'].iloc[-1]
    expirations = stock.options
    
    all_data = []
    for expiration in expirations[:1]:  # Apenas primeira expiração
        opt_chain = stock.option_chain(expiration)
        calls = opt_chain.calls
        puts = opt_chain.puts
        
        T = (pd.to_datetime(expiration) - pd.Timestamp.today()).days / 365
        calls['IV'] = calls.apply(
            lambda row: implied_volatility(row['lastPrice'], S, row['strike'], T, risk_free_rate, 'call'), axis=1
        )
        puts['IV'] = puts.apply(
            lambda row: implied_volatility(row['lastPrice'], S, row['strike'], T, risk_free_rate, 'put'), axis=1
        )
        
        all_data.append(calls[['strike', 'lastPrice', 'IV']])
        all_data.append(puts[['strike', 'lastPrice', 'IV']])
    
    return pd.concat(all_data), S

# Função para detectar distorções
def find_vol_distortions(df, threshold):
    df = df.sort_values('strike')
    df['IV_diff'] = df['IV'].diff().abs()
    return df[df['IV_diff'] > threshold]

# Classe da interface gráfica
class VolatilityAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisador de Distorções de Volatilidade")
        self.root.geometry("1000x700")

        # Frame de entrada
        input_frame = ttk.Frame(root, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Label(input_frame, text="Ticker:").grid(row=0, column=0, padx=5)
        self.ticker_entry = ttk.Entry(input_frame)
        self.ticker_entry.grid(row=0, column=1, padx=5)
        self.ticker_entry.insert(0, "AAPL")

        ttk.Label(input_frame, text="Taxa Livre de Risco (%):").grid(row=1, column=0, padx=5)
        self.rfr_entry = ttk.Entry(input_frame)
        self.rfr_entry.grid(row=1, column=1, padx=5)
        self.rfr_entry.insert(0, "3.0")

        ttk.Label(input_frame, text="Limite de Distorção:").grid(row=2, column=0, padx=5)
        self.threshold_entry = ttk.Entry(input_frame)
        self.threshold_entry.grid(row=2, column=1, padx=5)
        self.threshold_entry.insert(0, "0.1")

        ttk.Button(input_frame, text="Analisar", command=self.analyze).grid(row=3, column=0, columnspan=2, pady=10)

        # Frame para gráfico e resultados
        self.result_frame = ttk.Frame(root, padding="10")
        self.result_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

    def analyze(self):
        # Limpar frame anterior
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Obter entradas
        ticker = self.ticker_entry.get()
        try:
            rfr = float(self.rfr_entry.get()) / 100
            threshold = float(self.threshold_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Taxa livre de risco e limite devem ser números.")
            return

        # Obter dados e calcular
        try:
            option_data, stock_price = get_option_chain(ticker, rfr)
            option_data = option_data.sort_values('strike')
            option_data['IV_diff'] = option_data['IV'].diff().abs()
            option_data = option_data.reset_index(drop=True)
            distortions = find_vol_distortions(option_data.copy(), threshold)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao obter dados: {str(e)}")
            return

        # Exibir preço atual
        ttk.Label(self.result_frame, text=f"Preço Atual: {stock_price:.2f}").grid(row=0, column=0, pady=5)

        # Criar gráfico interativo
        fig, ax = plt.subplots(figsize=(10, 5))
        scatter = ax.scatter(option_data['strike'], option_data['IV'], c='blue', label='Volatilidade Implícita', alpha=0.6)
        if not distortions.empty:
            ax.scatter(distortions['strike'], distortions['IV'], c='red', label='Distorções', s=100, edgecolor='black')

        ax.set_xlabel('Preço de Exercício (Strike)')
        ax.set_ylabel('Volatilidade Implícita (IV)')
        ax.set_title(f'Sorriso de Volatilidade - {ticker}')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()

        # Adicionar tooltips
        cursor = mplcursors.cursor(scatter, hover=True)
        @cursor.connect("add")
        def on_add(sel):
            idx = sel.index
            row = option_data.iloc[idx]
            iv_diff = f"{row['IV_diff']:.4f}" if not pd.isna(row['IV_diff']) else "N/A"
            sel.annotation.set_text(
                f"Strike: {row['strike']:.2f}\n"
                f"IV: {row['IV']:.4f}\n"
                f"Preço: {row['lastPrice']:.2f}\n"
                f"IV Diff: {iv_diff}"
            )

        # Adicionar canvas e barra de ferramentas
        canvas = FigureCanvasTkAgg(fig, master=self.result_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))

        toolbar = NavigationToolbar2Tk(canvas, self.result_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=2, column=0, pady=5, sticky=(tk.W, tk.E))

        # Exibir distorções em texto
        if not distortions.empty:
            text = "Distorções Detectadas:\n" + distortions[['strike', 'IV', 'IV_diff']].to_string(index=False)
        else:
            text = "Nenhuma distorção significativa encontrada."
        
        ttk.Label(self.result_frame, text=text, wraplength=900).grid(row=3, column=0, pady=10)

# Inicializar aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = VolatilityAnalyzerApp(root)
    root.mainloop()