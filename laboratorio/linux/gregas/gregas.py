#!/usr/bin/env python3
"""
Visualização Interativa das Gregas de Opções – Matplotlib Interativo

Requisitos:
    - Python 3.13
    - Bibliotecas: numpy, matplotlib, scipy

Funcionalidades:
    • Ajuste interativo dos parâmetros: 
        - S (Preço do Ativo), K (Strike), T (Tempo até expiração),
          σ (Volatilidade) e r (Taxa de juros)
    • Escolha do tipo de opção: call ou put
    • Seleção da grega a ser visualizada (Delta, Gamma, Theta, Vega, Rho)
    • Gráfico 2D dinâmico que se atualiza conforme os parâmetros
    • Botão para gerar um gráfico 3D da grega selecionada
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy.stats import norm

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
        return self.S * norm.pdf(d1) * np.sqrt(self.T)

    def rho(self):
        d2 = self.d2()
        if self.option_type == 'call':
            return self.K * self.T * np.exp(-self.r*self.T) * norm.cdf(d2)
        else:
            return -self.K * self.T * np.exp(-self.r*self.T) * norm.cdf(-d2)

# --- Função para atualizar o gráfico 2D conforme os controles ---
def update(val):
    S0 = slider_S.val
    K = slider_K.val
    T = slider_T.val
    sigma = slider_sigma.val
    r = slider_r.val
    opt_type = radio_option.value_selected
    greek = radio_greek.value_selected

    calc = OptionCalculator(S0, K, T, sigma, r, opt_type)
    S_vals = np.linspace(0.5*S0, 1.5*S0, 200)
    greek_vals = []
    for S in S_vals:
        calc.S = S
        if greek == 'Delta':
            greek_vals.append(calc.delta())
        elif greek == 'Gamma':
            greek_vals.append(calc.gamma())
        elif greek == 'Theta':
            greek_vals.append(calc.theta())
        elif greek == 'Vega':
            greek_vals.append(calc.vega())
        elif greek == 'Rho':
            greek_vals.append(calc.rho())
    line_2d.set_xdata(S_vals)
    line_2d.set_ydata(greek_vals)
    ax_2d.relim()
    ax_2d.autoscale_view()
    fig_2d.canvas.draw_idle()

# --- Função para gerar o gráfico 3D (em nova janela) ---
def plot3d(event):
    from mpl_toolkits.mplot3d import Axes3D  # import local para evitar conflito com 2D
    S0 = slider_S.val
    K = slider_K.val
    T0 = slider_T.val
    sigma = slider_sigma.val
    r = slider_r.val
    opt_type = radio_option.value_selected
    greek = radio_greek.value_selected

    calc = OptionCalculator(S0, K, T0, sigma, r, opt_type)
    S_vals = np.linspace(0.5*S0, 1.5*S0, 50)
    T_vals = np.linspace(0.01, T0, 50)
    S_grid, T_grid = np.meshgrid(S_vals, T_vals)
    Z = np.zeros_like(S_grid)
    for i in range(S_grid.shape[0]):
        for j in range(S_grid.shape[1]):
            calc.S = S_grid[i,j]
            calc.T = T_grid[i,j]
            if greek == 'Delta':
                Z[i,j] = calc.delta()
            elif greek == 'Gamma':
                Z[i,j] = calc.gamma()
            elif greek == 'Theta':
                Z[i,j] = calc.theta()
            elif greek == 'Vega':
                Z[i,j] = calc.vega()
            elif greek == 'Rho':
                Z[i,j] = calc.rho()
    fig3d = plt.figure()
    ax3d = fig3d.add_subplot(111, projection='3d')
    surf = ax3d.plot_surface(S_grid, T_grid, Z, cmap=cm.viridis, edgecolor='none')
    ax3d.set_title(f"Superfície 3D de {greek}")
    ax3d.set_xlabel("Preço do Ativo (S)")
    ax3d.set_ylabel("Tempo até Expiração (T)")
    ax3d.set_zlabel(greek)
    fig3d.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

# --- Criação da interface interativa com Matplotlib ---
fig_2d, ax_2d = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.35)
S0_init = 100
K_init = 100
T_init = 1
sigma_init = 0.2
r_init = 0.05

calc_init = OptionCalculator(S0_init, K_init, T_init, sigma_init, r_init, 'call')
S_vals_init = np.linspace(0.5*S0_init, 1.5*S0_init, 200)
# Por padrão, plotamos o Delta
line_2d, = ax_2d.plot(S_vals_init, [calc_init.delta() for _ in S_vals_init], lw=2)
ax_2d.set_xlabel("Preço do Ativo (S)")
ax_2d.set_ylabel("Valor da Grega")
ax_2d.set_title("Gráfico 2D (por padrão: Delta)")

# Cria e posiciona os sliders para os parâmetros
axcolor = 'lightgoldenrodyellow'
ax_S = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_K = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_T = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_sigma = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
ax_r = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

slider_S = Slider(ax_S, 'S', 50, 150, valinit=S0_init)
slider_K = Slider(ax_K, 'K', 50, 150, valinit=K_init)
slider_T = Slider(ax_T, 'T', 0.1, 2, valinit=T_init)
slider_sigma = Slider(ax_sigma, 'σ', 0.1, 1, valinit=sigma_init)
slider_r = Slider(ax_r, 'r', 0.0, 0.1, valinit=r_init)

slider_S.on_changed(update)
slider_K.on_changed(update)
slider_T.on_changed(update)
slider_sigma.on_changed(update)
slider_r.on_changed(update)

# Radio buttons para o tipo de opção
rax_option = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
radio_option = RadioButtons(rax_option, ('call', 'put'))
radio_option.on_clicked(update)

# Radio buttons para seleção da grega
rax_greek = plt.axes([0.025, 0.25, 0.15, 0.2], facecolor=axcolor)
radio_greek = RadioButtons(rax_greek, ('Delta', 'Gamma', 'Theta', 'Vega', 'Rho'))
radio_greek.on_clicked(update)

# Botão para plotar o gráfico 3D
ax_button = plt.axes([0.8, 0.9, 0.1, 0.05])
button_3d = Button(ax_button, 'Plot 3D')
button_3d.on_clicked(plot3d)

plt.show()
