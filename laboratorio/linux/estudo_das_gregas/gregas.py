#!/usr/bin/env python3
"""
Visualização Interativa Avançada das Gregas de Opções - Modelo Black-Scholes (Layout Reformulado)
Com adição de curvas de payoff no vencimento e opção de perspectiva (Comprador/Vendedor)

Requisitos:
    - Python 3.x
    - Bibliotecas: numpy, matplotlib, scipy, seaborn

Modificações:
    • Área dos gráficos (gregas, preço, payoff e painel informativo) à esquerda
    • Painel de controles (sliders, radio buttons, check buttons e botões) em uma sidebar à direita
    • Margens e espaçamentos ajustados para um layout mais limpo
    • Tipografia e cores uniformes para um visual profissional
    • Adicionada visualização de curvas de payoff no vencimento
    • Adicionada opção para alternar entre perspectiva do comprador e do vendedor
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
from scipy.stats import norm
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from matplotlib import cm
import matplotlib.gridspec as gridspec

# Configuração de estilo visual e paleta de cores
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("notebook", font_scale=1.1)
COLORS = sns.color_palette("viridis", 5)
HIGHLIGHT_COLOR = '#ff7f0e'
BG_COLOR = '#f5f5f5'
TEXT_COLOR = '#333333'

# --- Classe para cálculos com o modelo Black-Scholes ---
class OptionCalculator:
    def __init__(self, S, K, T, sigma, r, option_type='call'):
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r
        self.option_type = option_type.lower()

    def d1(self):
        return (np.log(self.S/self.K) + (self.r + 0.5*self.sigma**2)*self.T) / (self.sigma * np.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma*np.sqrt(self.T)

    def price(self):
        d1 = self.d1()
        d2 = self.d2()
        if self.option_type == 'call':
            return self.S * norm.cdf(d1) - self.K * np.exp(-self.r*self.T) * norm.cdf(d2)
        else:
            return self.K * np.exp(-self.r*self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)

    def delta(self):
        d1 = self.d1()
        if self.option_type == 'call':
            return norm.cdf(d1)
        else:
            return norm.cdf(d1) - 1

    def gamma(self):
        d1 = self.d1()
        return norm.pdf(d1) / (self.S * self.sigma * np.sqrt(self.T))

    def theta(self):
        d1 = self.d1()
        d2 = self.d2()
        term1 = -self.S * norm.pdf(d1) * self.sigma / (2*np.sqrt(self.T))
        if self.option_type == 'call':
            term2 = -self.r * self.K * np.exp(-self.r*self.T) * norm.cdf(d2)
            return term1 + term2
        else:
            term2 = self.r * self.K * np.exp(-self.r*self.T) * norm.cdf(-d2)
            return term1 + term2

    def vega(self):
        d1 = self.d1()
        return self.S * norm.pdf(d1) * np.sqrt(self.T) / 100

    def rho(self):
        d2 = self.d2()
        if self.option_type == 'call':
            return self.K * self.T * np.exp(-self.r*self.T) * norm.cdf(d2) / 100
        else:
            return -self.K * self.T * np.exp(-self.r*self.T) * norm.cdf(-d2) / 100

    def get_greek_value(self, greek_name):
        if greek_name == 'Delta':
            return self.delta()
        elif greek_name == 'Gamma':
            return self.gamma()
        elif greek_name == 'Theta':
            return self.theta()
        elif greek_name == 'Vega':
            return self.vega()
        elif greek_name == 'Rho':
            return self.rho()
        return 0
    
    def payoff_at_expiry(self, S_at_expiry):
        """Calcula o payoff no vencimento"""
        if self.option_type == 'call':
            return np.maximum(S_at_expiry - self.K, 0)
        else:
            return np.maximum(self.K - S_at_expiry, 0)
    
    def profit_at_expiry(self, S_at_expiry, is_buyer=True):
        """Calcula o lucro/prejuízo no vencimento considerando o prêmio pago/recebido"""
        # Armazena o valor atual de S
        original_S = self.S
        
        # Calcula o prêmio atual da opção
        self.S = original_S
        premium = self.price()
        
        # Calcula o payoff no vencimento
        payoff = self.payoff_at_expiry(S_at_expiry)
        
        # Retorna S ao valor original
        self.S = original_S
        
        # Retorna o lucro/prejuízo de acordo com a perspectiva
        if is_buyer:
            # Para o comprador: payoff recebido menos prêmio pago
            return payoff - premium
        else:
            # Para o vendedor: prêmio recebido menos payoff pago
            return premium - payoff
        
# --- Função para definir cor de cada grega ---
def get_greek_color(greek_name):
    greek_colors = {
        'Delta': COLORS[0],
        'Gamma': COLORS[1],
        'Theta': COLORS[2],
        'Vega': COLORS[3],
        'Rho': COLORS[4]
    }
    return greek_colors.get(greek_name, 'black')

def percent_formatter(x, pos):
    return f'{x:.1f}%' if abs(x) < 100 else f'{x:.0f}%'

# Variáveis globais para controle do modo comparativo
comparison_mode_active = False
checkbox_status = [False, False, False, False, False]
greek_options = ['Delta', 'Gamma', 'Theta', 'Vega', 'Rho']

# Variável para controlar a visibilidade do gráfico de payoff
payoff_visible = True

# Função para alternar a visibilidade do gráfico de payoff
def toggle_payoff_visibility(event):
    global payoff_visible
    payoff_visible = not payoff_visible
    ax_payoff.set_visible(payoff_visible)
    
    # Reorganiza o layout dinamicamente quando o payoff é ocultado/mostrado
    if payoff_visible:
        # Layout com payoff visível
        ax_greek.set_position([0.05, 0.68, 0.58, 0.25])
        ax_price.set_position([0.05, 0.41, 0.58, 0.22])
        ax_payoff.set_position([0.05, 0.18, 0.58, 0.18])
        ax_info.set_position([0.05, 0.01, 0.58, 0.13])
    else:
        # Layout sem payoff (expande os outros gráficos)
        ax_greek.set_position([0.05, 0.68, 0.58, 0.28])
        ax_price.set_position([0.05, 0.38, 0.58, 0.28])
        ax_info.set_position([0.05, 0.01, 0.58, 0.33])
    
    fig_main.canvas.draw_idle()

# --- Função para atualizar os gráficos ---
def update(val=None):
    S0 = slider_S.val
    K = slider_K.val
    T = slider_T.val
    sigma = slider_sigma.val
    r = slider_r.val
    opt_type = radio_option.value_selected
    greek = radio_greek.value_selected
    
    # Nova variável para perspectiva
    perspective = radio_perspective.value_selected
    is_buyer = (perspective == 'Comprador')

    # Limpa áreas de gráficos
    ax_greek.clear()
    ax_price.clear()
    ax_payoff.clear()  # Limpa o gráfico de payoff

    # Inicializa calculadora
    calc = OptionCalculator(S0, K, T, sigma, r, opt_type)
    S_vals = np.linspace(max(0.5 * S0, 1), 1.5 * S0, 200)

    # Gráfico das gregas
    ax_greek.set_title(f"{greek} vs. Preço do Ativo", fontsize=12, fontweight='bold', color=TEXT_COLOR)
    ax_greek.set_ylabel(f"Valor de {greek}", fontsize=10, color=TEXT_COLOR)
    ax_greek.grid(True, alpha=0.3)

    greeks_to_show = []
    if comparison_mode_active and len(greek_options) > 0:
        for i, g in enumerate(greek_options):
            if i < len(checkbox_status) and checkbox_status[i]:
                greeks_to_show.append(g)
    if not greeks_to_show:
        greeks_to_show = [greek]

    for g in greeks_to_show:
        greek_vals = []
        for S in S_vals:
            calc.S = S
            greek_val = calc.get_greek_value(g)
            # Inverter o sinal das gregas para o vendedor, exceto Gamma que é igual para ambos
            if not is_buyer and g != 'Gamma':
                greek_val = -greek_val
            greek_vals.append(greek_val)
            
        color = get_greek_color(g)
        ax_greek.plot(S_vals, greek_vals, lw=2.5, color=color, label=g)
        calc.S = S0
        greek_val = calc.get_greek_value(g)
        # Inverter o sinal das gregas para o vendedor, exceto Gamma
        if not is_buyer and g != 'Gamma':
            greek_val = -greek_val
            
        ax_greek.scatter(S0, greek_val, color=color, s=60, zorder=5)
        ax_greek.annotate(f'{g}: {greek_val:.4f}',
                          xy=(S0, greek_val),
                          xytext=(10, 10 if g == greeks_to_show[0] else -15 * greeks_to_show.index(g)),
                          textcoords='offset points',
                          fontsize=9,
                          bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8),
                          arrowprops=dict(arrowstyle="->", color=color))
    if len(greeks_to_show) > 1:
        ax_greek.legend(loc='best', frameon=True, fancybox=True, framealpha=0.9)
    ax_greek.axvline(x=S0, color='gray', linestyle='--', alpha=0.6)
    ax_greek.axhline(y=0, color='black', linestyle='-', alpha=0.2)

    # Gráfico de preço da opção
    ax_price.set_title(f"Preço da Opção ({opt_type.upper()})", fontsize=12, fontweight='bold', color=TEXT_COLOR)
    ax_price.set_xlabel("", fontsize=10, color=TEXT_COLOR)
    ax_price.set_ylabel("Preço da Opção", fontsize=10, color=TEXT_COLOR)
    ax_price.grid(True, alpha=0.3)

    price_vals = []
    for S in S_vals:
        calc.S = S
        price_vals.append(calc.price())
    ax_price.plot(S_vals, price_vals, lw=2.5, color=HIGHLIGHT_COLOR)

    # Sombreamento ITM/OTM
    if opt_type == 'call':
        itm_x = [S for S in S_vals if S > K]
        itm_y = [price_vals[i] for i, S in enumerate(S_vals) if S > K]
        if itm_x:
            ax_price.fill_between(itm_x, 0, itm_y, alpha=0.2, color='green', label='ITM')
            ax_price.text((min(itm_x)+max(itm_x))/2, max(itm_y)/4, 'ITM', color='darkgreen', fontsize=10, ha='center')
        if K < max(S_vals):
            ax_price.text(K * 0.75, max(price_vals)/4, 'OTM', color='darkred', fontsize=10, ha='center')
    else:
        itm_x = [S for S in S_vals if S < K]
        itm_y = [price_vals[i] for i, S in enumerate(S_vals) if S < K]
        if itm_x:
            ax_price.fill_between(itm_x, 0, itm_y, alpha=0.2, color='green', label='ITM')
            ax_price.text((min(itm_x)+max(itm_x))/2, max(itm_y)/4, 'ITM', color='darkgreen', fontsize=10, ha='center')
        if K > min(S_vals):
            ax_price.text(K * 1.25, max(price_vals)/4, 'OTM', color='darkred', fontsize=10, ha='center')
    ax_price.axvline(x=K, color='red', linestyle='--', alpha=0.6, label='Strike (K)')
    ax_price.text(K, max(price_vals)/10, f'K={K:.1f}', color='red', fontsize=9, ha='right', va='bottom')
    ax_price.axvline(x=S0, color='gray', linestyle='--', alpha=0.6)
    ax_price.text(S0, max(price_vals)/7, f'S={S0:.1f}', color='gray', fontsize=9, ha='left', va='bottom')
    calc.S = S0
    current_price = calc.price()
    ax_price.scatter(S0, current_price, color=HIGHLIGHT_COLOR, s=60, zorder=5)
    ax_price.annotate(f'Preço: {current_price:.2f}',
                      xy=(S0, current_price),
                      xytext=(10, 10),
                      textcoords='offset points',
                      fontsize=9,
                      bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8),
                      arrowprops=dict(arrowstyle="->", color=HIGHLIGHT_COLOR))
    
    # Gráfico de Payoff no Vencimento com perspectiva
    ax_payoff.set_title(f"Payoff no Vencimento ({opt_type.upper()}) - {perspective}", 
                        fontsize=12, fontweight='bold', color=TEXT_COLOR)
    ax_payoff.set_xlabel("(S)", fontsize=10, color=TEXT_COLOR)
    ax_payoff.set_ylabel("Resultado (Payoff)", fontsize=10, color=TEXT_COLOR)
    ax_payoff.grid(True, alpha=0.3)
    
    # Calcula payoff e profit para cada valor de S no vencimento
    payoff_vals = calc.payoff_at_expiry(S_vals)
    profit_vals = [calc.profit_at_expiry(S, is_buyer) for S in S_vals]
    
    # Se for o vendedor, inverte o payoff para visualização (o payoff do vendedor é o oposto do comprador)
    display_payoff = payoff_vals if is_buyer else [-p for p in payoff_vals]
    
    # Plota payoff bruto (linha tracejada)
    ax_payoff.plot(S_vals, display_payoff, lw=2, color='blue', linestyle='--', label='Payoff')
    
    # Plota lucro/prejuízo líquido (considerando o prêmio pago/recebido)
    ax_payoff.plot(S_vals, profit_vals, lw=2.5, color='green', label='Lucro/Prejuízo')
    
    # Adiciona linha horizontal no zero (break-even)
    ax_payoff.axhline(y=0, color='black', linestyle='-', alpha=0.5, label='Break-even')
    
    # Adiciona linha vertical no strike price
    ax_payoff.axvline(x=K, color='red', linestyle='--', alpha=0.6, label='Strike (K)')
    
    # Adiciona sombreamento para áreas de lucro e prejuízo
    profit_x = []
    profit_y = []
    loss_x = []
    loss_y = []
    
    for i, profit in enumerate(profit_vals):
        if profit > 0:
            profit_x.append(S_vals[i])
            profit_y.append(profit)
        else:
            loss_x.append(S_vals[i])
            loss_y.append(profit)
    
    if profit_x:
        ax_payoff.fill_between(profit_x, 0, profit_y, alpha=0.2, color='green', label='Lucro')
    if loss_x:
        ax_payoff.fill_between(loss_x, 0, loss_y, alpha=0.2, color='red', label='Prejuízo')
    
    # Calcula e marca pontos de break-even (onde o lucro = 0)
    # Para simplificar, calculamos uma aproximação linear entre pontos adjacentes
    for i in range(len(profit_vals) - 1):
        if (profit_vals[i] <= 0 and profit_vals[i+1] >= 0) or (profit_vals[i] >= 0 and profit_vals[i+1] <= 0):
            # Interpolação linear para encontrar o ponto de break-even
            ratio = abs(profit_vals[i]) / (abs(profit_vals[i]) + abs(profit_vals[i+1]))
            breakeven_x = S_vals[i] + ratio * (S_vals[i+1] - S_vals[i])
            ax_payoff.axvline(x=breakeven_x, color='black', linestyle=':', alpha=0.7)
            ax_payoff.text(breakeven_x, max(profit_vals)/10, f'BE: {breakeven_x:.2f}', 
                          color='black', fontsize=8, ha='center', va='bottom',
                          bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7))
    
    # Calcula e mostra o valor máximo de lucro ou prejuízo possível
    max_profit = max(profit_vals) if any(p > 0 for p in profit_vals) else 0
    max_loss = min(profit_vals) if any(p < 0 for p in profit_vals) else 0
    
    if max_profit > 0:
        max_profit_idx = np.argmax(profit_vals)
        ax_payoff.annotate(f'Lucro Máx: {max_profit:.2f}',
                        xy=(S_vals[max_profit_idx], max_profit),
                        xytext=(0, 15),
                        textcoords='offset points',
                        fontsize=8,
                        ha='center',
                        bbox=dict(boxstyle="round,pad=0.2", fc="green", alpha=0.7, ec="darkgreen"),
                        arrowprops=dict(arrowstyle="->", color='green'))
    
    if max_loss < 0:
        max_loss_idx = np.argmin(profit_vals)
        ax_payoff.annotate(f'Prejuízo Máx: {max_loss:.2f}',
                        xy=(S_vals[max_loss_idx], max_loss),
                        xytext=(0, -15),
                        textcoords='offset points',
                        fontsize=8,
                        ha='center',
                        bbox=dict(boxstyle="round,pad=0.2", fc="red", alpha=0.7, ec="darkred"),
                        arrowprops=dict(arrowstyle="->", color='red'))
    
    # Adiciona legenda
    ax_payoff.legend(loc='best', frameon=True, fancybox=True, framealpha=0.9, fontsize=8)
    
    # Mostra o preço atual no gráfico de payoff
    ax_payoff.axvline(x=S0, color='gray', linestyle='--', alpha=0.6)
    ax_payoff.text(S0, max(display_payoff)/2, f'S atual: {S0:.1f}', color='gray', 
                  fontsize=8, ha='left', va='bottom',
                  bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7))

    update_info_panel(S0, K, T, sigma, r, opt_type, calc, is_buyer)
    ax_greek.relim()
    ax_greek.autoscale_view()
    ax_price.relim()
    ax_price.autoscale_view()
    ax_payoff.relim()
    ax_payoff.autoscale_view()
    fig_main.canvas.draw_idle()

# --- Atualiza o painel de informações ---
def update_info_panel(S0, K, T, sigma, r, opt_type, calc, is_buyer=True):
    # Calcula alguns valores adicionais para o painel informativo
    current_price = calc.price()
    payoff_at_strike = calc.payoff_at_expiry(K)
    profit_at_strike = calc.profit_at_expiry(K, is_buyer)
    
    # Calcula o break-even aproximado
    if opt_type == 'call':
        breakeven_approx = K + current_price
    else:
        breakeven_approx = K - current_price
    
    # Texto para perspectiva
    perspective_text = "Comprador" if is_buyer else "Vendedor"
    premium_text = "pago" if is_buyer else "recebido"
    
    # Ajusta os sinais das gregas para o vendedor (exceto Gamma)
    delta = calc.delta()
    gamma = calc.gamma()
    theta = calc.theta()
    vega = calc.vega() * 100
    rho = calc.rho() * 100
    
    if not is_buyer:
        delta = -delta
        theta = -theta
        vega = -vega
        rho = -rho
        
    info_text = [
        f"Modelo: Black-Scholes",
        f"Tipo: {opt_type.upper()} | Perspectiva: {perspective_text}",
        f"S = {S0:.2f} | K = {K:.2f} | Moneyness: {S0/K:.2f}",
        f"T = {T:.2f} anos | σ = {sigma:.2%} | r = {r:.2%}",
        f"Preço: {current_price:.4f} ({premium_text})",
        f"Delta: {delta:.4f}",
        f"Gamma: {gamma:.4f}",
        f"Theta: {theta:.4f}/dia",
        f"Vega: {vega:.4f} (para 1% de Δσ)",
        f"Rho: {rho:.4f} (para 1% de Δr)",
        f"Break-even aprox.: {breakeven_approx:.2f}",
        f"Payoff no strike: {payoff_at_strike:.2f}" + (" (pago)" if not is_buyer else ""),
        f"Lucro no strike: {profit_at_strike:.2f}"
    ]
    ax_info.clear()
    ax_info.axis('off')

    # Dividir a lista em duas colunas
    n = len(info_text)
    mid = (n + 1) // 2  # arredonda para cima no caso de número ímpar
    left_texts = info_text[:mid]
    right_texts = info_text[mid:]

    # Exibe a coluna da esquerda
    y_left = 0.95
    for line in left_texts:
        ax_info.text(0.05, y_left, line, fontsize=8, transform=ax_info.transAxes, color=TEXT_COLOR)
        y_left -= 0.08

    # Exibe a coluna da direita
    y_right = 0.95
    for line in right_texts:
        ax_info.text(0.55, y_right, line, fontsize=8, transform=ax_info.transAxes, color=TEXT_COLOR)
        y_right -= 0.08

    # --- Funções dos botões ---
def reset_params(event):
    slider_S.reset()
    slider_K.reset()
    slider_T.reset()
    slider_sigma.reset()
    slider_r.reset()
    update()

def save_figure(event):
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    perspective = radio_perspective.value_selected.lower()
    filename = f"black_scholes_{radio_greek.value_selected.lower()}_{perspective}_{timestamp}.png"
    fig_main.savefig(filename, dpi=300, bbox_inches='tight')
    plt.figtext(0.70, 0.05, f"Salvo como {filename}", ha="center", 
               bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))
    fig_main.canvas.draw_idle()

def toggle_comparison_mode(event):
    global comparison_mode_active, checkbox_status
    comparison_mode_active = any(checkbox_status)
    if comparison_mode_active:
        current_greek = radio_greek.value_selected
        greek_idx = greek_options.index(current_greek)
        checkbox_status[greek_idx] = True
    update()

def update_checkbox(label):
    global checkbox_status
    idx = greek_options.index(label)
    checkbox_status[idx] = not checkbox_status[idx]
    toggle_comparison_mode(None)

def plot3d(event):
    from mpl_toolkits.mplot3d import Axes3D
    S0 = slider_S.val
    K = slider_K.val
    T0 = slider_T.val
    sigma = slider_sigma.val
    r = slider_r.val
    opt_type = radio_option.value_selected
    greek = radio_greek.value_selected
    perspective = radio_perspective.value_selected
    is_buyer = (perspective == 'Comprador')
    
    # Obtém o parâmetro selecionado para visualização 3D
    selected_param = radio_param3d.value_selected
    
    calc = OptionCalculator(S0, K, T0, sigma, r, opt_type)
    S_vals = np.linspace(0.5 * S0, 1.5 * S0, 50)
    
    # Determina qual parâmetro variar com base na seleção do usuário
    if selected_param == 'Volatilidade (σ)':
        param_name = 'Volatilidade (σ)'
        param_vals = np.linspace(max(0.05, sigma/2), min(1.0, sigma*2), 50)
        Z = np.zeros((len(param_vals), len(S_vals)))
        for i, param_val in enumerate(param_vals):
            for j, S_val in enumerate(S_vals):
                calc.S = S_val
                calc.sigma = param_val
                greek_val = calc.get_greek_value(greek)
                if not is_buyer and greek != 'Gamma':
                    greek_val = -greek_val
                Z[i, j] = greek_val
    elif selected_param == 'Tempo (T)':
        param_name = 'Tempo até Expiração (T)'
        param_vals = np.linspace(0.01, max(2.0, T0*1.5), 50)
        Z = np.zeros((len(param_vals), len(S_vals)))
        for i, param_val in enumerate(param_vals):
            for j, S_val in enumerate(S_vals):
                calc.S = S_val
                calc.T = param_val
                greek_val = calc.get_greek_value(greek)
                if not is_buyer and greek != 'Gamma':
                    greek_val = -greek_val
                Z[i, j] = greek_val
    else:  # Taxa de Juros (r)
        param_name = 'Taxa de Juros (r)'
        param_vals = np.linspace(0.01, 0.15, 50)
        Z = np.zeros((len(param_vals), len(S_vals)))
        for i, param_val in enumerate(param_vals):
            for j, S_val in enumerate(S_vals):
                calc.S = S_val
                calc.r = param_val
                greek_val = calc.get_greek_value(greek)
                if not is_buyer and greek != 'Gamma':
                    greek_val = -greek_val
                Z[i, j] = greek_val
                
    S_grid, Param_grid = np.meshgrid(S_vals, param_vals)
    fig3d = plt.figure(figsize=(10,8))
    gs3d = gridspec.GridSpec(1, 2, width_ratios=[1.5, 1])
    ax3d = fig3d.add_subplot(gs3d[0], projection='3d')
    surf = ax3d.plot_surface(S_grid, Param_grid, Z, cmap=cm.viridis, edgecolor='none', alpha=0.8)
    ax3d.plot_surface(S_grid, Param_grid, np.zeros_like(Z), color='gray', alpha=0.2)
    ax3d.set_title(f"Superfície 3D de {greek} ({opt_type.upper()}) - {perspective}", 
                  fontsize=11, fontweight='bold')
    ax3d.set_xlabel("(S)", fontsize=9)
    ax3d.set_ylabel(param_name, fontsize=9)
    ax3d.set_zlabel(greek, fontsize=9)
    ax_contour = fig3d.add_subplot(gs3d[1])
    contour = ax_contour.contourf(S_grid, Param_grid, Z, 20, cmap=cm.viridis)
    ax_contour.contour(S_grid, Param_grid, Z, 10, colors='white', linewidths=0.5, alpha=0.7)
    ax_contour.set_title(f"Mapa de Calor de {greek} - {perspective}", fontsize=11, fontweight='bold')
    ax_contour.set_xlabel("(S)", fontsize=9)
    ax_contour.set_ylabel(param_name, fontsize=9)
    
    # Adiciona linhas de referência para o valor atual do parâmetro
    if param_name == 'Volatilidade (σ)':
        ax_contour.axhline(y=sigma, color='red', linestyle='--', alpha=0.7)
        ax_contour.text(S_vals[0], sigma, f'σ={sigma:.2f}', color='red', fontsize=8, ha='left', va='bottom')
    elif param_name == 'Tempo até Expiração (T)':
        ax_contour.axhline(y=T0, color='red', linestyle='--', alpha=0.7)
        ax_contour.text(S_vals[0], T0, f'T={T0:.2f}', color='red', fontsize=8, ha='left', va='bottom')
    else:
        ax_contour.axhline(y=r, color='red', linestyle='--', alpha=0.7)
        ax_contour.text(S_vals[0], r, f'r={r:.2f}', color='red', fontsize=8, ha='left', va='bottom')
    
    ax_contour.axvline(x=S0, color='white', linestyle='--', alpha=0.7)
    ax_contour.axvline(x=K, color='black', linestyle='--', alpha=0.7)
    cbar = fig3d.colorbar(contour, ax=ax_contour, shrink=0.5, aspect=15)
    cbar.set_label(greek, fontsize=8)
    cbar.ax.tick_params(labelsize=7)
    ax_contour.text(S0, param_vals[0], 'S atual', color='white', fontsize=7, ha='center', va='bottom', 
                   bbox=dict(boxstyle="round", fc="gray", alpha=0.7))
    ax_contour.text(K, param_vals[0], 'Strike', color='black', fontsize=7, ha='center', va='bottom', 
                   bbox=dict(boxstyle="round", fc="white", alpha=0.7))
    fig3d.suptitle(f"Análise Avançada de {greek} - Modelo Black-Scholes ({perspective})", 
                  fontsize=12, fontweight='bold')
    ax3d.tick_params(axis='both', which='major', labelsize=8)
    ax_contour.tick_params(axis='both', which='major', labelsize=8)
    fig3d.tight_layout()
    plt.subplots_adjust(top=0.9, wspace=0.2)
    plt.show()

# --- Layout Principal com o novo gráfico de payoff ---
fig_main = plt.figure(figsize=(12,10))  # Aumentamos um pouco a altura para acomodar o novo gráfico
fig_main.canvas.manager.set_window_title('Visualizador Avançado de Black-Scholes com Payoff')

# Define os eixos com posições manuais para um layout limpo
ax_greek = fig_main.add_axes([0.05, 0.68, 0.58, 0.25])  # Reduzimos um pouco para acomodar payoff
ax_price = fig_main.add_axes([0.05, 0.41, 0.58, 0.22])  # Ajustamos a posição
ax_payoff = fig_main.add_axes([0.05, 0.18, 0.58, 0.18])  # Novo gráfico para payoff
ax_info  = fig_main.add_axes([0.05, 0.01, 0.58, 0.13])  # Reduzimos e ajustamos a posição

# --- Painel de Controles (Sidebar à direita) ---
axcolor = 'lightgray'
# Sliders – posicionados verticalmente na sidebar
ax_S = plt.axes([0.70, 0.80, 0.25, 0.03], facecolor=axcolor)
ax_K = plt.axes([0.70, 0.75, 0.25, 0.03], facecolor=axcolor)
ax_T = plt.axes([0.70, 0.70, 0.25, 0.03], facecolor=axcolor)
ax_sigma = plt.axes([0.70, 0.65, 0.25, 0.03], facecolor=axcolor)
ax_r = plt.axes([0.70, 0.60, 0.25, 0.03], facecolor=axcolor)

slider_S = Slider(ax_S, 'S', 50, 150, valinit=100, valstep=0.5, color=HIGHLIGHT_COLOR)
slider_K = Slider(ax_K, 'K', 50, 150, valinit=100, valstep=0.5, color='red')
slider_T = Slider(ax_T, 'T', 0.1, 2, valinit=1, valstep=0.05, color=COLORS[2])
slider_sigma = Slider(ax_sigma, 'σ', 0.05, 0.5, valinit=0.2, valstep=0.01, color=COLORS[3])
slider_r = Slider(ax_r, 'r', 0.01, 0.10, valinit=0.05, valstep=0.005, color=COLORS[4])

slider_S.on_changed(update)
slider_K.on_changed(update)
slider_T.on_changed(update)
slider_sigma.on_changed(update)
slider_r.on_changed(update)

# Radio buttons para selecionar a grega e o tipo de opção
rax_greek = plt.axes([0.70, 0.50, 0.25, 0.09], facecolor=axcolor)
radio_greek = RadioButtons(rax_greek, greek_options, activecolor=HIGHLIGHT_COLOR)
radio_greek.on_clicked(update)
for text in radio_greek.labels:
    text.set_fontsize(8)

rax_option = plt.axes([0.70, 0.40, 0.25, 0.07], facecolor=axcolor)
radio_option = RadioButtons(rax_option, ('call', 'put'), activecolor=HIGHLIGHT_COLOR)
radio_option.on_clicked(update)
for text in radio_option.labels:
    text.set_fontsize(8)

# NOVO: Radio buttons para selecionar a perspectiva (comprador/vendedor)
rax_perspective = plt.axes([0.70, 0.30, 0.25, 0.07], facecolor=axcolor)
radio_perspective = RadioButtons(rax_perspective, ('Comprador', 'Vendedor'), activecolor=HIGHLIGHT_COLOR)
radio_perspective.on_clicked(update)
for text in radio_perspective.labels:
    text.set_fontsize(8)

# Radio buttons para parâmetro de visualização 3D
rax_param3d = plt.axes([0.70, 0.23, 0.25, 0.05], facecolor=axcolor)
radio_param3d = RadioButtons(rax_param3d, ['Volatilidade (σ)', 'Tempo (T)', 'Taxa (r)'], activecolor=HIGHLIGHT_COLOR)
radio_param3d.set_active(1)  # Tempo como padrão inicial
for text in radio_param3d.labels:
    text.set_fontsize(8)

'''
# Check button para o modo comparativo (ajustado para nova posição)
rax_compare = plt.axes([0.70, 0.23, 0.25, 0.05], facecolor=axcolor)
checkbox_compare = CheckButtons(rax_compare, ['Comparativo'], [False])
checkbox_compare.on_clicked(toggle_comparison_mode)
for text in checkbox_compare.labels:
    text.set_fontsize(8)
'''

# Botões de ação – Reset, Salvar e Plot 3D (ajustados para nova posição)
ax_reset = plt.axes([0.70, 0.17, 0.07, 0.04])
button_reset = Button(ax_reset, 'Reset', color=axcolor, hovercolor='0.975')
button_reset.on_clicked(reset_params)

ax_save = plt.axes([0.78, 0.17, 0.07, 0.04])
button_save = Button(ax_save, 'Salvar', color=axcolor, hovercolor='0.975')
button_save.on_clicked(save_figure)

ax_button3d = plt.axes([0.86, 0.17, 0.07, 0.04])
button_3d = Button(ax_button3d, 'Plot 3D', color=axcolor, hovercolor='0.975')
button_3d.on_clicked(plot3d)

# Adiciona botão para mostrar/esconder gráfico de payoff (ajustado para nova posição)
ax_toggle_payoff = plt.axes([0.70, 0.10, 0.23, 0.04])
button_toggle_payoff = Button(ax_toggle_payoff, 'Mostrar/Ocultar Payoff', color=axcolor, hovercolor='0.975')
button_toggle_payoff.on_clicked(toggle_payoff_visibility)

# Título principal centralizado
fig_main.suptitle('Visualizador Avançado de Black-Scholes: Análise de Gregas, Preços e Payoff', 
                 fontsize=16, fontweight='bold', color=TEXT_COLOR)

# Conecta o manipulador de eventos de teclado para atalhos
def on_key(event):
    if event.key == 'r':
        reset_params(None)
    elif event.key == '3':
        plot3d(None)
    elif event.key == 's':
        save_figure(None)
    elif event.key == 'p':
        # Atalho para alternar entre visualizar o gráfico de payoff ou escondê-lo
        toggle_payoff_visibility(None)
    elif event.key == 'v':
        # NOVO: Atalho para alternar entre comprador e vendedor
        current_index = 0 if radio_perspective.value_selected == 'Comprador' else 1
        new_index = 1 - current_index  # Alterna entre 0 e 1
        radio_perspective.set_active(new_index)
    elif event.key == 'right':
        slider_S.set_val(min(150, slider_S.val + 1))
    elif event.key == 'left':
        slider_S.set_val(max(50, slider_S.val - 1))
    elif event.key == 'up':
        slider_sigma.set_val(min(0.5, slider_sigma.val + 0.01))
    elif event.key == 'down':
        slider_sigma.set_val(max(0.05, slider_sigma.val - 0.01))
    elif event.key == '+':
        slider_T.set_val(min(2, slider_T.val + 0.1))
    elif event.key == '-':
        slider_T.set_val(max(0.1, slider_T.val - 0.1))

fig_main.canvas.mpl_connect('key_press_event', on_key)

# Inicializa os gráficos
update()
plt.show()       