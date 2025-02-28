#!/usr/bin/env python3
"""
Visualizador Avançado do Modelo Black-Scholes com PyQtGraph
Implementação de alta performance para análise interativa de opções

Recursos:
    • Visualização 3D acelerada por hardware das superfícies das gregas
    • Interface interativa com feedback em tempo real
    • Análise detalhada de preços, gregas e payoff
    • Sistema de presets para cenários de mercado
    • Ferramentas de análise comparativa
    • Exportação de resultados e gráficos
"""

import sys
import math
import numpy as np
from scipy.stats import norm
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import pyqtgraph.opengl as gl
from datetime import datetime
import json

# Configuração do estilo PyQtGraph
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

# Paleta de cores consistente
COLORS = {
    'Delta': (0, 114, 189),    # Azul
    'Gamma': (217, 83, 25),    # Laranja
    'Theta': (237, 177, 32),   # Amarelo
    'Vega': (126, 47, 142),    # Roxo
    'Rho': (119, 172, 48),     # Verde
    'Price': (77, 190, 238),   # Azul claro
    'Strike': (217, 83, 25),   # Vermelho
    'Payoff': (0, 0, 255),     # Azul
    'Profit': (0, 128, 0),     # Verde
    'Loss': (255, 0, 0),       # Vermelho
    'Reference': (128, 128, 128),  # Cinza
    'Highlight': (255, 127, 14)    # Laranja
}

# --- Classe para cálculos do modelo Black-Scholes (mantida do código original) ---
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
        original_S = self.S
        self.S = original_S
        premium = self.price()
        payoff = self.payoff_at_expiry(S_at_expiry)
        self.S = original_S
        
        if is_buyer:
            return payoff - premium
        else:
            return premium - payoff

# --- Classe Principal do Visualizador Black-Scholes ---
class BlackScholesVisualizer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuração da janela principal
        self.setWindowTitle("Black-Scholes Advanced Visualizer")
        self.resize(1200, 800)
        
        # Dados de estado
        self.saved_state = None
        self.comparison_active = False
        self.is_3d_interactive = False
        
        # Valores iniciais dos parâmetros
        self.S0 = 100.0
        self.K = 100.0
        self.T = 1.0
        self.sigma = 0.2
        self.r = 0.05
        self.option_type = 'call'
        self.greek = 'Delta'
        self.is_buyer = True
        self.param3d = 'Tempo (T)'
        
        # Configuração do layout principal
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        # Painel esquerdo para gráficos 2D
        self.left_panel = QtWidgets.QWidget()
        self.left_layout = QtWidgets.QVBoxLayout()
        self.left_panel.setLayout(self.left_layout)
        
        # Painel central para visualização 3D
        self.center_panel = QtWidgets.QWidget()
        self.center_layout = QtWidgets.QVBoxLayout()
        self.center_panel.setLayout(self.center_layout)
        
        # Painel direito para controles
        self.right_panel = QtWidgets.QWidget()
        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_panel.setLayout(self.right_layout)
        
        # Adicionar painéis ao layout principal
        self.main_layout.addWidget(self.left_panel, 1)
        self.main_layout.addWidget(self.center_panel, 1)
        self.main_layout.addWidget(self.right_panel, 0)
        
        # Inicialização dos componentes da interface
        self.setup_plots()
        self.setup_controls()
        self.setup_menu()
        self.connect_signals()
        
        # Atualização inicial
        self.update_all()

    def setup_plots(self):
        """Configuração de todos os elementos visuais (gráficos 2D e 3D)"""
        # --- Configuração dos gráficos 2D ---
        
        # Gráfico da Grega vs. Preço do Ativo
        self.greek_plot = pg.PlotWidget(title="Greek vs. Asset Price")
        self.greek_plot.setLabel('left', 'Value')
        self.greek_plot.setLabel('bottom', 'Asset Price (S)')
        self.greek_plot.showGrid(x=True, y=True)
        self.greek_plot.addLegend()
        
        # Linha de referência em y=0
        self.greek_zero_line = pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen('k', width=1, style=QtCore.Qt.DashLine))
        self.greek_plot.addItem(self.greek_zero_line)
        
        # Linha vertical para valor atual de S
        self.greek_s_line = pg.InfiniteLine(pos=self.S0, angle=90, 
                                           pen=pg.mkPen(COLORS['Reference'], width=1, style=QtCore.Qt.DashLine))
        self.greek_plot.addItem(self.greek_s_line)
        
        # Curva principal da grega
        self.greek_curve = self.greek_plot.plot(pen=pg.mkPen(COLORS['Delta'], width=2.5),
                                              name="Delta")
        
        # Curva para modo comparativo
        self.greek_compare_curve = self.greek_plot.plot(pen=pg.mkPen(COLORS['Reference'], width=2, style=QtCore.Qt.DashLine),
                                                     name="Comparison")
        self.greek_compare_curve.hide()  # Inicialmente oculta
        
        # Ponto de marcação para valor atual
        self.greek_point = pg.ScatterPlotItem(size=10, brush=pg.mkBrush(COLORS['Delta']))
        self.greek_plot.addItem(self.greek_point)
        
        # Rótulo para valor atual
        self.greek_label = pg.TextItem(text="", anchor=(0.5, 1), color=COLORS['Delta'])
        self.greek_label.setFont(QtGui.QFont("Arial", 9))
        self.greek_plot.addItem(self.greek_label)
        
        # Tooltip interativo
        self.greek_tooltip = pg.TextItem(text="", anchor=(0, 1), fill=pg.mkBrush(255, 255, 255, 200))
        self.greek_tooltip.setZValue(100)
        self.greek_plot.addItem(self.greek_tooltip)
        self.greek_tooltip.hide()
        
        # Configuração do tooltip
        def greek_mouse_moved(evt):
            pos = evt[0]
            if self.greek_plot.sceneBoundingRect().contains(pos):
                mouse_point = self.greek_plot.getPlotItem().vb.mapSceneToView(pos)
                x = mouse_point.x()
                # Encontrar o valor y mais próximo
                if len(self.greek_curve.xData) > 0:
                    idx = np.abs(self.greek_curve.xData - x).argmin()
                    y = self.greek_curve.yData[idx]
                    self.greek_tooltip.setText(f"S: {x:.2f}\n{self.greek}: {y:.4f}")
                    self.greek_tooltip.setPos(x, y)
                    self.greek_tooltip.show()
            else:
                self.greek_tooltip.hide()
        
        self.greek_proxy = pg.SignalProxy(self.greek_plot.scene().sigMouseMoved, rateLimit=30, slot=greek_mouse_moved)
        
        # --- Gráfico de Preço da Opção ---
        self.price_plot = pg.PlotWidget(title="Option Price")
        self.price_plot.setLabel('left', 'Price')
        self.price_plot.setLabel('bottom', 'Asset Price (S)')
        self.price_plot.showGrid(x=True, y=True)
        
        # Linha vertical para strike price
        self.price_k_line = pg.InfiniteLine(pos=self.K, angle=90, 
                                           pen=pg.mkPen(COLORS['Strike'], width=1.5, style=QtCore.Qt.DashLine))
        self.price_plot.addItem(self.price_k_line)
        
        # Linha vertical para valor atual de S
        self.price_s_line = pg.InfiniteLine(pos=self.S0, angle=90, 
                                           pen=pg.mkPen(COLORS['Reference'], width=1, style=QtCore.Qt.DashLine))
        self.price_plot.addItem(self.price_s_line)
        
        # Curva principal de preço
        self.price_curve = self.price_plot.plot(pen=pg.mkPen(COLORS['Price'], width=2.5))
        
        # Áreas para ITM/OTM
        # Criar curvas vazias para inicialização
        self.itm_curve1 = pg.PlotCurveItem()
        self.itm_curve2 = pg.PlotCurveItem()
        # Áreas para ITM/OTM
        self.itm_region = pg.FillBetweenItem(curve1=self.itm_curve1, curve2=self.itm_curve2, brush=pg.mkBrush(0, 255, 0, 50))
        self.price_plot.addItem(self.itm_region)
        
        # Ponto de marcação para valor atual
        self.price_point = pg.ScatterPlotItem(size=10, brush=pg.mkBrush(COLORS['Price']))
        self.price_plot.addItem(self.price_point)
        
        # Rótulo para valor atual
        self.price_label = pg.TextItem(text="", anchor=(0.5, 0), color=COLORS['Price'])
        self.price_label.setFont(QtGui.QFont("Arial", 9))
        self.price_plot.addItem(self.price_label)
        
        # ITM/OTM labels
        self.itm_label = pg.TextItem("ITM", anchor=(0.5, 0.5), color='green')
        self.otm_label = pg.TextItem("OTM", anchor=(0.5, 0.5), color='red')
        self.price_plot.addItem(self.itm_label)
        self.price_plot.addItem(self.otm_label)
        
        # --- Gráfico de Payoff e Profit ---
        self.payoff_plot = pg.PlotWidget(title="Payoff at Expiry")
        self.payoff_plot.setLabel('left', 'Value')
        self.payoff_plot.setLabel('bottom', 'Asset Price at Expiry (S)')
        self.payoff_plot.showGrid(x=True, y=True)
        self.payoff_plot.addLegend()
        
        # Linha horizontal em y=0 (break-even)
        self.payoff_zero_line = pg.InfiniteLine(pos=0, angle=0, 
                                               pen=pg.mkPen('k', width=1.5))
        self.payoff_plot.addItem(self.payoff_zero_line)
        
        # Linha vertical para strike price
        self.payoff_k_line = pg.InfiniteLine(pos=self.K, angle=90, 
                                            pen=pg.mkPen(COLORS['Strike'], width=1.5, style=QtCore.Qt.DashLine))
        self.payoff_plot.addItem(self.payoff_k_line)
        
        # Linha vertical para valor atual de S
        self.payoff_s_line = pg.InfiniteLine(pos=self.S0, angle=90, 
                                            pen=pg.mkPen(COLORS['Reference'], width=1, style=QtCore.Qt.DashLine))
        self.payoff_plot.addItem(self.payoff_s_line)
        
        # Curvas para payoff e profit
        self.payoff_curve = self.payoff_plot.plot(pen=pg.mkPen(COLORS['Payoff'], width=1.5, style=QtCore.Qt.DashLine),
                                                name="Payoff")
        self.profit_curve = self.payoff_plot.plot(pen=pg.mkPen(COLORS['Profit'], width=2.5),
                                                name="Profit/Loss")
        
        # Criar curvas vazias para inicialização de regiões
        self.profit_curve1 = pg.PlotCurveItem()
        self.profit_curve2 = pg.PlotCurveItem()
        self.loss_curve1 = pg.PlotCurveItem()
        self.loss_curve2 = pg.PlotCurveItem()
        # Áreas para lucro/prejuízo
        self.profit_region = pg.FillBetweenItem(curve1=self.profit_curve1, curve2=self.profit_curve2, brush=pg.mkBrush(0, 255, 0, 50))
        self.loss_region = pg.FillBetweenItem(curve1=self.loss_curve1, curve2=self.loss_curve2, brush=pg.mkBrush(255, 0, 0, 50))
        self.payoff_plot.addItem(self.profit_region)
        self.payoff_plot.addItem(self.loss_region)
        
        # Linhas para breakeven points
        self.breakeven_lines = []
        
        # Rótulos para máximo lucro/prejuízo
        self.max_profit_label = pg.TextItem("", anchor=(0.5, 0), color='green')
        self.max_profit_label.setFont(QtGui.QFont("Arial", 9))
        self.payoff_plot.addItem(self.max_profit_label)
        
        self.max_loss_label = pg.TextItem("", anchor=(0.5, 1), color='red')
        self.max_loss_label.setFont(QtGui.QFont("Arial", 9))
        self.payoff_plot.addItem(self.max_loss_label)
        
        # --- Painel de informações ---
        self.info_text = pg.TextItem("", anchor=(0, 0))
        self.info_text.setFont(QtGui.QFont("Arial", 9))
        
        self.info_plot = pg.PlotWidget()
        self.info_plot.getPlotItem().hideAxis('left')
        self.info_plot.getPlotItem().hideAxis('bottom')
        self.info_plot.addItem(self.info_text)
        
        # --- Configuração do gráfico 3D ---
        self.view3d = gl.GLViewWidget()
        self.view3d.setCameraPosition(distance=50, elevation=40, azimuth=-45)
        
        # Adicionar grid 3D para referência
        self.grid_x = gl.GLGridItem()
        self.grid_x.setSize(40, 40, 1)
        self.grid_x.setSpacing(1, 1, 0)
        self.view3d.addItem(self.grid_x)
        
        self.grid_z = gl.GLGridItem()
        self.grid_z.setSize(40, 40, 1)
        self.grid_z.setSpacing(1, 1, 0)
        self.grid_z.rotate(90, 1, 0, 0)
        self.view3d.addItem(self.grid_z)
        
        self.grid_y = gl.GLGridItem()
        self.grid_y.setSize(40, 40, 1)
        self.grid_y.setSpacing(1, 1, 0)
        self.grid_y.rotate(90, 0, 1, 0)
        self.view3d.addItem(self.grid_y)
        
        # Adicionar superfície 3D
        self.surface = gl.GLSurfacePlotItem(shader='shaded')
        self.view3d.addItem(self.surface)
        
        # Plano Z=0 (importante para análise de gregas)
        verts = np.array([
            [20, 20, 0], [20, -20, 0], [-20, -20, 0], [-20, 20, 0]
        ])
        faces = np.array([
            [0, 1, 2], [0, 2, 3]
        ])
        colors = np.array([
            [0.7, 0.7, 0.7, 0.3], [0.7, 0.7, 0.7, 0.3], 
            [0.7, 0.7, 0.7, 0.3], [0.7, 0.7, 0.7, 0.3]
        ])
        
        self.z0_plane = gl.GLMeshItem(vertexes=verts, faces=faces, vertexColors=colors, 
                                     smooth=False, drawEdges=False)
        self.view3d.addItem(self.z0_plane)
        
        # Título para o gráfico 3D
        self.view3d_title = QtWidgets.QLabel("3D Surface Analysis")
        self.view3d_title.setAlignment(QtCore.Qt.AlignCenter)
        self.view3d_title.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        
        # Adicionar os plots aos painéis
        self.left_layout.addWidget(self.greek_plot, 1)
        self.left_layout.addWidget(self.price_plot, 1)
        self.left_layout.addWidget(self.payoff_plot, 1)
        self.left_layout.addWidget(self.info_plot, 0)
        
        self.center_layout.addWidget(self.view3d_title)
        self.center_layout.addWidget(self.view3d)
        
        # Detectar interação com o gráfico 3D para otimização
        def on_view3d_mouse_press():
            self.is_3d_interactive = True
        
        def on_view3d_mouse_release():
            self.is_3d_interactive = False
            # Atualizar com alta resolução após interação
            QtCore.QTimer.singleShot(500, lambda: self.update_3d_surface(high_res=True))
        
        # Conectar sinais de interação
        self.view3d.mousePressBg = on_view3d_mouse_press
        self.view3d.mouseReleaseSignal = on_view3d_mouse_release

    def setup_controls(self):
        """Configuração dos controles de interação (sliders, radio buttons, etc.)"""
        # --- Título do painel de controles ---
        control_title = QtWidgets.QLabel("Parameters")
        control_title.setAlignment(QtCore.Qt.AlignCenter)
        control_title.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.right_layout.addWidget(control_title)
        
        # --- Painel de presets ---
        presets_group = QtWidgets.QGroupBox("Presets")
        presets_layout = QtWidgets.QVBoxLayout()
        presets_group.setLayout(presets_layout)
        
        presets_controls = QtWidgets.QHBoxLayout()
        self.preset_combo = QtWidgets.QComboBox()
        self.preset_combo.addItem("Default")
        self.preset_combo.addItem("High Volatility")
        self.preset_combo.addItem("Low Interest Rate")
        self.preset_combo.addItem("Short Term")
        self.preset_combo.addItem("Deep ITM Call")
        self.preset_combo.addItem("Deep OTM Put")
        
        self.load_preset_btn = QtWidgets.QPushButton("Load")
        self.save_preset_btn = QtWidgets.QPushButton("Save As...")
        
        presets_controls.addWidget(self.preset_combo, 2)
        presets_controls.addWidget(self.load_preset_btn, 1)
        presets_controls.addWidget(self.save_preset_btn, 1)
        
        presets_layout.addLayout(presets_controls)
        self.right_layout.addWidget(presets_group)
        
        # --- Sliders para parâmetros ---
        params_group = QtWidgets.QGroupBox("Option Parameters")
        params_layout = QtWidgets.QVBoxLayout()
        params_group.setLayout(params_layout)
        
        # Slider para S (preço do ativo)
        s_layout = QtWidgets.QHBoxLayout()
        self.s_label = QtWidgets.QLabel(f"Asset Price (S): {self.S0:.1f}")
        self.s_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.s_slider.setRange(50, 150)
        self.s_slider.setValue(int(self.S0))
        self.s_slider.setTracking(True)
        
        s_layout.addWidget(self.s_label)
        s_layout.addWidget(self.s_slider)
        params_layout.addLayout(s_layout)
        
        # Slider para K (strike price)
        k_layout = QtWidgets.QHBoxLayout()
        self.k_label = QtWidgets.QLabel(f"Strike Price (K): {self.K:.1f}")
        self.k_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.k_slider.setRange(50, 150)
        self.k_slider.setValue(int(self.K))
        self.k_slider.setTracking(True)
        
        k_layout.addWidget(self.k_label)
        k_layout.addWidget(self.k_slider)
        params_layout.addLayout(k_layout)
        
        # Slider para T (tempo até expiração)
        t_layout = QtWidgets.QHBoxLayout()
        self.t_label = QtWidgets.QLabel(f"Time to Expiry (T): {self.T:.2f}")
        self.t_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.t_slider.setRange(1, 200)
        self.t_slider.setValue(int(self.T * 100))
        self.t_slider.setTracking(True)
        
        t_layout.addWidget(self.t_label)
        t_layout.addWidget(self.t_slider)
        params_layout.addLayout(t_layout)
        
        # Slider para sigma (volatilidade)
        sigma_layout = QtWidgets.QHBoxLayout()
        self.sigma_label = QtWidgets.QLabel(f"Volatility (σ): {self.sigma:.0%}")
        self.sigma_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sigma_slider.setRange(5, 50)
        self.sigma_slider.setValue(int(self.sigma * 100))
        self.sigma_slider.setTracking(True)
        
        sigma_layout.addWidget(self.sigma_label)
        sigma_layout.addWidget(self.sigma_slider)
        params_layout.addLayout(sigma_layout)
        
        # Slider para r (taxa de juros)
        r_layout = QtWidgets.QHBoxLayout()
        self.r_label = QtWidgets.QLabel(f"Interest Rate (r): {self.r:.0%}")
        self.r_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.r_slider.setRange(1, 10)
        self.r_slider.setValue(int(self.r * 100))
        self.r_slider.setTracking(True)
        
        r_layout.addWidget(self.r_label)
        r_layout.addWidget(self.r_slider)
        params_layout.addLayout(r_layout)
        
        self.right_layout.addWidget(params_group)
        
        # --- Radio buttons para tipo de opção ---
        option_group = QtWidgets.QGroupBox("Option Type")
        option_layout = QtWidgets.QHBoxLayout()
        option_group.setLayout(option_layout)
        
        self.call_radio = QtWidgets.QRadioButton("Call")
        self.put_radio = QtWidgets.QRadioButton("Put")
        self.call_radio.setChecked(True)
        
        option_layout.addWidget(self.call_radio)
        option_layout.addWidget(self.put_radio)
        
        self.right_layout.addWidget(option_group)
        
        # --- Radio buttons para grega ---
        greek_group = QtWidgets.QGroupBox("Greek")
        greek_layout = QtWidgets.QVBoxLayout()
        greek_group.setLayout(greek_layout)
        
        self.delta_radio = QtWidgets.QRadioButton("Delta")
        self.gamma_radio = QtWidgets.QRadioButton("Gamma")
        self.theta_radio = QtWidgets.QRadioButton("Theta")
        self.vega_radio = QtWidgets.QRadioButton("Vega")
        self.rho_radio = QtWidgets.QRadioButton("Rho")
        
        self.delta_radio.setChecked(True)
        
        greek_layout.addWidget(self.delta_radio)
        greek_layout.addWidget(self.gamma_radio)
        greek_layout.addWidget(self.theta_radio)
        greek_layout.addWidget(self.vega_radio)
        greek_layout.addWidget(self.rho_radio)
        
        self.right_layout.addWidget(greek_group)
        
        # --- Radio buttons para perspectiva ---
        perspective_group = QtWidgets.QGroupBox("Perspective")
        perspective_layout = QtWidgets.QHBoxLayout()
        perspective_group.setLayout(perspective_layout)
        
        self.buyer_radio = QtWidgets.QRadioButton("Buyer")
        self.seller_radio = QtWidgets.QRadioButton("Seller")
        self.buyer_radio.setChecked(True)
        
        perspective_layout.addWidget(self.buyer_radio)
        perspective_layout.addWidget(self.seller_radio)
        
        self.right_layout.addWidget(perspective_group)
        
        # --- Radio buttons para parâmetro 3D ---
        param3d_group = QtWidgets.QGroupBox("3D Parameter")
        param3d_layout = QtWidgets.QVBoxLayout()
        param3d_group.setLayout(param3d_layout)
        
        self.vol_radio = QtWidgets.QRadioButton("Volatility (σ)")
        self.time_radio = QtWidgets.QRadioButton("Time (T)")
        self.rate_radio = QtWidgets.QRadioButton("Interest Rate (r)")
        
        self.time_radio.setChecked(True)
        
        param3d_layout.addWidget(self.vol_radio)
        param3d_layout.addWidget(self.time_radio)
        param3d_layout.addWidget(self.rate_radio)
        
        self.right_layout.addWidget(param3d_group)
        
        # --- Modo comparativo ---
        compare_group = QtWidgets.QGroupBox("Comparison")
        compare_layout = QtWidgets.QVBoxLayout()
        compare_group.setLayout(compare_layout)
        
        self.compare_check = QtWidgets.QCheckBox("Compare with saved state")
        self.save_state_btn = QtWidgets.QPushButton("Save current state")
        
        compare_layout.addWidget(self.compare_check)
        compare_layout.addWidget(self.save_state_btn)
        
        self.right_layout.addWidget(compare_group)
        
        # --- Botões de ação ---
        actions_layout = QtWidgets.QHBoxLayout()
        
        self.reset_btn = QtWidgets.QPushButton("Reset")
        self.save_img_btn = QtWidgets.QPushButton("Save Image")
        
        actions_layout.addWidget(self.reset_btn)
        actions_layout.addWidget(self.save_img_btn)
        
        self.right_layout.addLayout(actions_layout)
        
        # --- Toggle para visualização de payoff ---
        self.payoff_check = QtWidgets.QCheckBox("Show Payoff Graph")
        self.payoff_check.setChecked(True)
        self.right_layout.addWidget(self.payoff_check)
        
        # --- Espaçador para ajustar layout vertical ---
        self.right_layout.addStretch(1)

    def setup_menu(self):
            """Configuração do menu principal"""
            menubar = self.menuBar()
            
            # Menu Arquivo
            file_menu = menubar.addMenu('File')
            
            new_action = QtWidgets.QAction('New', self)
            new_action.setShortcut('Ctrl+N')
            new_action.triggered.connect(self.reset_all)
            
            save_action = QtWidgets.QAction('Save Config...', self)
            save_action.setShortcut('Ctrl+S')
            save_action.triggered.connect(self.save_config)
            
            load_action = QtWidgets.QAction('Load Config...', self)
            load_action.setShortcut('Ctrl+O')
            load_action.triggered.connect(self.load_config)
            
            export_action = QtWidgets.QAction('Export Image...', self)
            export_action.setShortcut('Ctrl+E')
            export_action.triggered.connect(self.export_image)
            
            exit_action = QtWidgets.QAction('Exit', self)
            exit_action.setShortcut('Ctrl+Q')
            exit_action.triggered.connect(self.close)
            
            file_menu.addAction(new_action)
            file_menu.addAction(save_action)
            file_menu.addAction(load_action)
            file_menu.addSeparator()
            file_menu.addAction(export_action)
            file_menu.addSeparator()
            file_menu.addAction(exit_action)
            
            # Menu View
            view_menu = menubar.addMenu('View')
            
            toggle_payoff_action = QtWidgets.QAction('Toggle Payoff Graph', self)
            toggle_payoff_action.setShortcut('Ctrl+P')
            toggle_payoff_action.triggered.connect(self.toggle_payoff)
            
            toggle_3d_action = QtWidgets.QAction('Toggle 3D View', self)
            toggle_3d_action.setShortcut('Ctrl+3')
            toggle_3d_action.triggered.connect(self.toggle_3d)
            
            view_menu.addAction(toggle_payoff_action)
            view_menu.addAction(toggle_3d_action)
            
            # Menu Tools
            tools_menu = menubar.addMenu('Tools')
            
            calc_action = QtWidgets.QAction('Option Calculator...', self)
            calc_action.setShortcut('Ctrl+C')
            calc_action.triggered.connect(self.show_calculator)
            
            tools_menu.addAction(calc_action)
            
            # Menu Help
            help_menu = menubar.addMenu('Help')
            
            about_action = QtWidgets.QAction('About', self)
            about_action.triggered.connect(self.show_about)
            
            help_menu.addAction(about_action)

    def connect_signals(self):
        """Conecta todos os signals aos slots correspondentes"""
        # Sliders
        self.s_slider.valueChanged.connect(self.on_s_changed)
        self.k_slider.valueChanged.connect(self.on_k_changed)
        self.t_slider.valueChanged.connect(self.on_t_changed)
        self.sigma_slider.valueChanged.connect(self.on_sigma_changed)
        self.r_slider.valueChanged.connect(self.on_r_changed)
        
        # Radio buttons para tipo de opção
        self.call_radio.toggled.connect(self.on_option_type_changed)
        
        # Radio buttons para grega
        self.delta_radio.toggled.connect(lambda: self.on_greek_changed('Delta') if self.delta_radio.isChecked() else None)
        self.gamma_radio.toggled.connect(lambda: self.on_greek_changed('Gamma') if self.gamma_radio.isChecked() else None)
        self.theta_radio.toggled.connect(lambda: self.on_greek_changed('Theta') if self.theta_radio.isChecked() else None)
        self.vega_radio.toggled.connect(lambda: self.on_greek_changed('Vega') if self.vega_radio.isChecked() else None)
        self.rho_radio.toggled.connect(lambda: self.on_greek_changed('Rho') if self.rho_radio.isChecked() else None)
        
        # Radio buttons para perspectiva
        self.buyer_radio.toggled.connect(self.on_perspective_changed)
        
        # Radio buttons para parâmetro 3D
        self.vol_radio.toggled.connect(lambda: self.on_param3d_changed('Volatilidade (σ)') if self.vol_radio.isChecked() else None)
        self.time_radio.toggled.connect(lambda: self.on_param3d_changed('Tempo (T)') if self.time_radio.isChecked() else None)
        self.rate_radio.toggled.connect(lambda: self.on_param3d_changed('Taxa (r)') if self.rate_radio.isChecked() else None)
        
        # Botões e checkboxes
        self.reset_btn.clicked.connect(self.reset_all)
        self.save_img_btn.clicked.connect(self.export_image)
        self.payoff_check.toggled.connect(self.toggle_payoff)
        self.compare_check.toggled.connect(self.toggle_comparison)
        self.save_state_btn.clicked.connect(self.save_current_state)
        
        # Presets
        self.load_preset_btn.clicked.connect(self.load_selected_preset)
        self.save_preset_btn.clicked.connect(self.save_preset)

    # --- Event handlers para controles ---
    def on_s_changed(self, value):
        self.S0 = float(value)
        self.s_label.setText(f"Asset Price (S): {self.S0:.1f}")
        self.update_all()
        
    def on_k_changed(self, value):
        self.K = float(value)
        self.k_label.setText(f"Strike Price (K): {self.K:.1f}")
        self.update_all()
        
    def on_t_changed(self, value):
        self.T = float(value) / 100  # Convert to range 0.01 - 2.0
        self.t_label.setText(f"Time to Expiry (T): {self.T:.2f}")
        self.update_all()
        
    def on_sigma_changed(self, value):
        self.sigma = float(value) / 100  # Convert to range 0.05 - 0.5
        self.sigma_label.setText(f"Volatility (σ): {self.sigma:.0%}")
        self.update_all()
        
    def on_r_changed(self, value):
        self.r = float(value) / 100  # Convert to range 0.01 - 0.1
        self.r_label.setText(f"Interest Rate (r): {self.r:.0%}")
        self.update_all()
        
    def on_option_type_changed(self, checked):
        self.option_type = 'call' if self.call_radio.isChecked() else 'put'
        self.update_all()
        
    def on_greek_changed(self, greek):
        self.greek = greek
        self.update_all()
        
    def on_perspective_changed(self, checked):
        self.is_buyer = self.buyer_radio.isChecked()
        self.update_all()
        
    def on_param3d_changed(self, param):
        self.param3d = param
        self.update_3d_surface()
        
    def toggle_payoff(self, checked=None):
        if checked is None:
            self.payoff_check.setChecked(not self.payoff_check.isChecked())
            return
            
        self.payoff_plot.setVisible(checked)
        self.update_layout()
        
    def toggle_3d(self):
        current_visible = self.view3d.isVisible()
        self.view3d.setVisible(not current_visible)
        self.view3d_title.setVisible(not current_visible)
        
    def toggle_comparison(self, checked):
        self.comparison_active = checked
        if checked and self.saved_state is None:
            self.save_current_state()
            
        self.greek_compare_curve.setVisible(checked)
        self.update_all()
        
    def save_current_state(self):
        self.saved_state = {
            'S0': self.S0,
            'K': self.K,
            'T': self.T,
            'sigma': self.sigma,
            'r': self.r,
            'option_type': self.option_type,
            'greek': self.greek,
            'is_buyer': self.is_buyer,
            'param3d': self.param3d
        }
        
        if self.comparison_active:
            self.update_greek_plot()
            
    def update_layout(self):
        """Ajusta o layout dinâmicamente"""
        # Implementação simplificada - na versão completa, ajustaria espaçamentos
        pass

    # --- Métodos para presets ---
    def load_selected_preset(self):
        preset_name = self.preset_combo.currentText()
        
        if preset_name == "Default":
            self.S0 = 100.0
            self.K = 100.0
            self.T = 1.0
            self.sigma = 0.2
            self.r = 0.05
            self.option_type = 'call'
            self.greek = 'Delta'
            self.param3d = 'Tempo (T)'
            self.is_buyer = True
        elif preset_name == "High Volatility":
            self.S0 = 100.0
            self.K = 100.0
            self.T = 1.0
            self.sigma = 0.4
            self.r = 0.05
            self.option_type = 'call'
            self.greek = 'Vega'
            self.param3d = 'Tempo (T)'
            self.is_buyer = True
        elif preset_name == "Low Interest Rate":
            self.S0 = 100.0
            self.K = 100.0
            self.T = 1.0
            self.sigma = 0.2
            self.r = 0.01
            self.option_type = 'call'
            self.greek = 'Rho'
            self.param3d = 'Volatilidade (σ)'
            self.is_buyer = True
        elif preset_name == "Short Term":
            self.S0 = 100.0
            self.K = 100.0
            self.T = 0.1
            self.sigma = 0.2
            self.r = 0.05
            self.option_type = 'call'
            self.greek = 'Gamma'
            self.param3d = 'Volatilidade (σ)'
            self.is_buyer = True
        elif preset_name == "Deep ITM Call":
            self.S0 = 130.0
            self.K = 100.0
            self.T = 0.5
            self.sigma = 0.2
            self.r = 0.05
            self.option_type = 'call'
            self.greek = 'Delta'
            self.param3d = 'Tempo (T)'
            self.is_buyer = True
        elif preset_name == "Deep OTM Put":
            self.S0 = 130.0
            self.K = 100.0
            self.T = 0.5
            self.sigma = 0.2
            self.r = 0.05
            self.option_type = 'put'
            self.greek = 'Delta'
            self.param3d = 'Tempo (T)'
            self.is_buyer = True
            
        # Atualizar sliders e radio buttons
        self.update_controls()
        # Atualizar gráficos
        self.update_all()
        
    def save_preset(self):
        name, ok = QtWidgets.QInputDialog.getText(self, 'Save Preset', 
                                               'Enter preset name:')
        if ok and name:
            # Em uma implementação completa, salvaria em arquivo
            self.preset_combo.addItem(name)
            self.preset_combo.setCurrentText(name)
            
    def update_controls(self):
        """Atualiza controles para refletir o estado atual"""
        # Atualizar sliders
        self.s_slider.setValue(int(self.S0))
        self.k_slider.setValue(int(self.K))
        self.t_slider.setValue(int(self.T * 100))
        self.sigma_slider.setValue(int(self.sigma * 100))
        self.r_slider.setValue(int(self.r * 100))
        
        # Atualizar radio buttons
        self.call_radio.setChecked(self.option_type == 'call')
        self.put_radio.setChecked(self.option_type == 'put')
        
        if self.greek == 'Delta':
            self.delta_radio.setChecked(True)
        elif self.greek == 'Gamma':
            self.gamma_radio.setChecked(True)
        elif self.greek == 'Theta':
            self.theta_radio.setChecked(True)
        elif self.greek == 'Vega':
            self.vega_radio.setChecked(True)
        elif self.greek == 'Rho':
            self.rho_radio.setChecked(True)
            
        self.buyer_radio.setChecked(self.is_buyer)
        self.seller_radio.setChecked(not self.is_buyer)
        
        if self.param3d == 'Volatilidade (σ)':
            self.vol_radio.setChecked(True)
        elif self.param3d == 'Tempo (T)':
            self.time_radio.setChecked(True)
        else:
            self.rate_radio.setChecked(True)
            
        # Atualizar labels
        self.s_label.setText(f"Asset Price (S): {self.S0:.1f}")
        self.k_label.setText(f"Strike Price (K): {self.K:.1f}")
        self.t_label.setText(f"Time to Expiry (T): {self.T:.2f}")
        self.sigma_label.setText(f"Volatility (σ): {self.sigma:.0%}")
        self.r_label.setText(f"Interest Rate (r): {self.r:.0%}")

    # --- Métodos principais de atualização ---
    def update_all(self):
        """Atualiza todos os gráficos e informações"""
        self.update_greek_plot()
        self.update_price_plot()
        self.update_payoff_plot()
        self.update_info_panel()
        
        # Atualizar o gráfico 3D somente se não estiver em interação
        if not self.is_3d_interactive:
            self.update_3d_surface()
            
    def update_greek_plot(self):
        """Atualiza o gráfico da grega selecionada"""
        # Inicializa calculadora
        calc = OptionCalculator(self.S0, self.K, self.T, self.sigma, self.r, self.option_type)
        
        # Gera valores de S
        S_vals = np.linspace(max(0.5 * self.S0, 1), 1.5 * self.S0, 200)
        
        # Calcula valores da grega para cada S
        greek_vals = []
        for S in S_vals:
            calc.S = S
            greek_val = calc.get_greek_value(self.greek)
            
            # Inverter o sinal das gregas para o vendedor, exceto Gamma
            if not self.is_buyer and self.greek != 'Gamma':
                greek_val = -greek_val
                
            greek_vals.append(greek_val)
            
        # Atualiza a curva da grega
        self.greek_curve.setData(S_vals, greek_vals)
        
        # Define a cor baseada na grega
        color = COLORS.get(self.greek, COLORS['Delta'])
        self.greek_curve.setPen(pg.mkPen(color, width=2.5))
        self.greek_point.setBrush(pg.mkBrush(color))
        
        # Atualiza título do gráfico
        perspective = "Buyer" if self.is_buyer else "Seller"
        self.greek_plot.setTitle(f"{self.greek} vs. Asset Price ({self.option_type.upper()}) - {perspective}")
        
        # Atualiza linhas de referência
        self.greek_s_line.setPos(self.S0)
        
        # Atualiza ponto atual
        calc.S = self.S0
        greek_val = calc.get_greek_value(self.greek)
        if not self.is_buyer and self.greek != 'Gamma':
            greek_val = -greek_val
            
        self.greek_point.setData([self.S0], [greek_val])
        
        # Atualiza rótulo
        self.greek_label.setText(f"{self.greek}: {greek_val:.4f}")
        self.greek_label.setPos(self.S0, greek_val)
        self.greek_label.setColor(color)
        
        # Modo comparativo
        if self.comparison_active and self.saved_state is not None:
            # Cria uma calculadora para o estado salvo
            saved_calc = OptionCalculator(
                self.saved_state['S0'], 
                self.saved_state['K'], 
                self.saved_state['T'], 
                self.saved_state['sigma'], 
                self.saved_state['r'], 
                self.saved_state['option_type']
            )
            
            # Calcula valores da grega salva
            saved_greek_vals = []
            for S in S_vals:
                saved_calc.S = S
                saved_greek_val = saved_calc.get_greek_value(self.greek)
                
                # Inverter o sinal das gregas para o vendedor, exceto Gamma
                if not self.saved_state['is_buyer'] and self.greek != 'Gamma':
                    saved_greek_val = -saved_greek_val
                    
                saved_greek_vals.append(saved_greek_val)
                
            # Atualiza a curva comparativa
            self.greek_compare_curve.setData(S_vals, saved_greek_vals)
            self.greek_compare_curve.show()
        else:
            self.greek_compare_curve.hide()
            
    def update_price_plot(self):
        """Atualiza o gráfico de preço da opção"""
        # Inicializa calculadora
        calc = OptionCalculator(self.S0, self.K, self.T, self.sigma, self.r, self.option_type)
        
        # Gera valores de S
        S_vals = np.linspace(max(0.5 * self.S0, 1), 1.5 * self.S0, 200)
        
        # Calcula preços para cada S
        price_vals = []
        for S in S_vals:
            calc.S = S
            price_vals.append(calc.price())
            
        # Atualiza a curva de preço
        self.price_curve.setData(S_vals, price_vals)
        
        # Atualiza título do gráfico
        self.price_plot.setTitle(f"Price ({self.option_type.upper()})")
        
        # Atualiza linhas de referência
        self.price_k_line.setPos(self.K)
        self.price_s_line.setPos(self.S0)
        
        # Destaca regiões ITM/OTM
        itm_curve = pg.PlotCurveItem()
        
        if self.option_type == 'call':
            itm_x = [S for S in S_vals if S > self.K]
            itm_y = [price_vals[i] for i, S in enumerate(S_vals) if S > self.K]
            
            if itm_x:
                itm_curve.setData(itm_x, itm_y)
                self.itm_region.setCurves(itm_curve, self.price_curve)
                
                # Posicionar labels ITM/OTM
                itm_mid_x = (min(itm_x) + max(itm_x)) / 2
                itm_mid_y = max(itm_y) / 4
                self.itm_label.setPos(itm_mid_x, itm_mid_y)
                self.otm_label.setPos(self.K * 0.75, max(price_vals) / 4)
        else:
            itm_x = [S for S in S_vals if S < self.K]
            itm_y = [price_vals[i] for i, S in enumerate(S_vals) if S < self.K]
            
            if itm_x:
                itm_curve.setData(itm_x, itm_y)
                self.itm_region.setCurves(itm_curve, self.price_curve)
                
                # Posicionar labels ITM/OTM
                itm_mid_x = (min(itm_x) + max(itm_x)) / 2
                itm_mid_y = max(itm_y) / 4
                self.itm_label.setPos(itm_mid_x, itm_mid_y)
                self.otm_label.setPos(self.K * 1.25, max(price_vals) / 4)
                
        # Atualiza ponto atual
        calc.S = self.S0
        current_price = calc.price()
        self.price_point.setData([self.S0], [current_price])
        
        # Atualiza rótulo
        self.price_label.setText(f"Price: {current_price:.2f}")
        self.price_label.setPos(self.S0, current_price)
        
    def update_payoff_plot(self):
        """Atualiza o gráfico de payoff e profit"""
        if not self.payoff_plot.isVisible():
            return
            
        # Inicializa calculadora
        calc = OptionCalculator(self.S0, self.K, self.T, self.sigma, self.r, self.option_type)
        
        # Gera valores de S
        S_vals = np.linspace(max(0.5 * self.S0, 1), 1.5 * self.S0, 200)
        
        # Calcula payoff e profit para cada S
        payoff_vals = calc.payoff_at_expiry(S_vals)
        profit_vals = [calc.profit_at_expiry(S, self.is_buyer) for S in S_vals]
        
        # Se for o vendedor, inverte o payoff para visualização
        display_payoff = payoff_vals if self.is_buyer else [-p for p in payoff_vals]
        
        # Atualiza as curvas
        self.payoff_curve.setData(S_vals, display_payoff)
        self.profit_curve.setData(S_vals, profit_vals)
        
        # Atualiza título do gráfico
        perspective = "Buyer" if self.is_buyer else "Seller"
        self.payoff_plot.setTitle(f"Payoff at Expiry ({self.option_type.upper()}) - {perspective}")
        
        # Atualiza linhas de referência
        self.payoff_k_line.setPos(self.K)
        self.payoff_s_line.setPos(self.S0)
        
        # Atualiza regiões de lucro/prejuízo
        profit_curve = pg.PlotCurveItem()
        loss_curve = pg.PlotCurveItem()
        zero_curve = pg.PlotCurveItem()
        zero_curve.setData(S_vals, np.zeros_like(S_vals))
        
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
            profit_curve.setData(profit_x, profit_y)
            self.profit_region.setCurves(profit_curve, zero_curve)
            
            # Mostrar valor máximo de lucro
            max_profit = max(profit_vals)
            max_profit_idx = np.argmax(profit_vals)
            max_profit_x = S_vals[max_profit_idx]
            self.max_profit_label.setText(f"Max Profit: {max_profit:.2f}")
            self.max_profit_label.setPos(max_profit_x, max_profit)
            self.max_profit_label.show()
        else:
            self.max_profit_label.hide()
            
        if loss_x:
            loss_curve.setData(loss_x, loss_y)
            self.loss_region.setCurves(loss_curve, zero_curve)
            
            # Mostrar valor máximo de prejuízo
            max_loss = min(profit_vals)
            max_loss_idx = np.argmin(profit_vals)
            max_loss_x = S_vals[max_loss_idx]
            self.max_loss_label.setText(f"Max Loss: {max_loss:.2f}")
            self.max_loss_label.setPos(max_loss_x, max_loss)
            self.max_loss_label.show()
        else:
            self.max_loss_label.hide()
            
        # Calcular e marcar pontos de break-even
        # Remover linhas antigas
        for line in self.breakeven_lines:
            self.payoff_plot.removeItem(line)
        self.breakeven_lines = []
        
        for i in range(len(profit_vals) - 1):
            if (profit_vals[i] <= 0 and profit_vals[i+1] >= 0) or (profit_vals[i] >= 0 and profit_vals[i+1] <= 0):
                # Interpolação linear para calcular o break-even
                ratio = abs(profit_vals[i]) / (abs(profit_vals[i]) + abs(profit_vals[i+1]))
                breakeven_x = S_vals[i] + ratio * (S_vals[i+1] - S_vals[i])
                
                # Criar linha vertical
                be_line = pg.InfiniteLine(pos=breakeven_x, angle=90, 
                                         pen=pg.mkPen('k', width=1, style=QtCore.Qt.DotLine))
                self.payoff_plot.addItem(be_line)
                self.breakeven_lines.append(be_line)
                
                # Criar label
                be_label = pg.TextItem(f"BE: {breakeven_x:.2f}", anchor=(0.5, 0))
                be_label.setPos(breakeven_x, 0)
                self.payoff_plot.addItem(be_label)
                self.breakeven_lines.append(be_label)
                
    def update_info_panel(self):
        """Atualiza o painel de informações"""
        # Inicializa calculadora
        calc = OptionCalculator(self.S0, self.K, self.T, self.sigma, self.r, self.option_type)
        
        # Calcula valores
        current_price = calc.price()
        payoff_at_strike = calc.payoff_at_expiry(self.K)
        profit_at_strike = calc.profit_at_expiry(self.K, self.is_buyer)
        
        # Calcula break-even aproximado
        if self.option_type == 'call':
            breakeven_approx = self.K + current_price
        else:
            breakeven_approx = self.K - current_price
            
        # Ajusta texto para perspectiva
        perspective_text = "Buyer" if self.is_buyer else "Seller"
        premium_text = "paid" if self.is_buyer else "received"
        
        # Ajusta sinais das gregas para vendedor
        delta = calc.delta()
        gamma = calc.gamma()
        theta = calc.theta()
        vega = calc.vega() * 100
        rho = calc.rho() * 100
        
        if not self.is_buyer:
            delta = -delta
            theta = -theta
            vega = -vega
            rho = -rho
            
        # Formata o texto de informações
        info_text = [
            f"<span style='font-weight:bold'>Black-Scholes Model</span>",
            f"Type: <b>{self.option_type.upper()}</b> | Perspective: <b>{perspective_text}</b>",
            f"S = {self.S0:.2f} | K = {self.K:.2f} | Moneyness: {self.S0/self.K:.2f}",
            f"T = {self.T:.2f} years | σ = {self.sigma:.1%} | r = {self.r:.1%}",
            f"Price: {current_price:.4f} ({premium_text})",
            f"Delta: {delta:.4f}",
            f"Gamma: {gamma:.4f}",
            f"Theta: {theta:.4f}/day",
            f"Vega: {vega:.4f} (for 1% Δσ)",
            f"Rho: {rho:.4f} (for 1% Δr)",
            f"Approx. break-even: {breakeven_approx:.2f}",
            f"Payoff at strike: {payoff_at_strike:.2f}{' (paid)' if not self.is_buyer else ''}",
            f"Profit at strike: {profit_at_strike:.2f}"
        ]
        
        # Atualiza o texto
        self.info_text.setHtml("<br>".join(info_text))
            
    def update_3d_surface(self, high_res=False):
        """Atualiza a superfície 3D"""
        # Inicializa calculadora
        calc = OptionCalculator(self.S0, self.K, self.T, self.sigma, self.r, self.option_type)
        
        # Determina a resolução baseada no estado de interação
        if high_res:
            resolution = 50
        elif self.is_3d_interactive:
            resolution = 20  # Baixa resolução durante interação
        else:
            resolution = 40  # Resolução média por padrão
        
        # Gera valores de S (eixo x)
        x_vals = np.linspace(0.5 * self.S0, 1.5 * self.S0, resolution)
        
        # Determine qual parâmetro variar (eixo y)
        if self.param3d == 'Volatilidade (σ)':
            param_name = 'Volatility (σ)'
            y_vals = np.linspace(max(0.05, self.sigma/2), min(1.0, self.sigma*2), resolution)
            param_func = lambda val: setattr(calc, 'sigma', val)
            param_current = self.sigma
        elif self.param3d == 'Tempo (T)':
            param_name = 'Time to Expiry (T)'
            y_vals = np.linspace(0.01, max(2.0, self.T*1.5), resolution)
            param_func = lambda val: setattr(calc, 'T', val)
            param_current = self.T
        else:  # Taxa (r)
            param_name = 'Interest Rate (r)'
            y_vals = np.linspace(0.01, 0.15, resolution)
            param_func = lambda val: setattr(calc, 'r', val)
            param_current = self.r
            
        # Calcular matriz Z (valores da grega na grade)
        z_grid = np.zeros((len(y_vals), len(x_vals)))
        
        # Calcular valores Z (superfície da grega)
        for i, param_val in enumerate(y_vals):
            for j, S_val in enumerate(x_vals):
                calc.S = S_val
                param_func(param_val)
                greek_val = calc.get_greek_value(self.greek)
                
                # Inverter valor para o vendedor, exceto Gamma
                if not self.is_buyer and self.greek != 'Gamma':
                    greek_val = -greek_val
                    
                z_grid[i, j] = greek_val
                
        # Atualizar título da visualização 3D
        perspective = "Buyer" if self.is_buyer else "Seller"
        self.view3d_title.setText(f"3D Surface: {self.greek} vs. {param_name} ({self.option_type.upper()}) - {perspective}")
        
        # Gerar cores baseadas nos valores
        colors = np.zeros((len(y_vals), len(x_vals), 4))
        
        # Normalizar para coloração
        vmin, vmax = np.min(z_grid), np.max(z_grid)
        norm = (z_grid - vmin) / (vmax - vmin) if vmax > vmin else z_grid * 0 + 0.5
        
        # Esquema de cores - azul para positivo, vermelho para negativo
        colors[:,:,0] = np.where(z_grid < 0, 0.8 * (1 - norm), 0)  # Red
        colors[:,:,1] = 0.3 + 0.2 * norm  # Green - slightly varied
        colors[:,:,2] = np.where(z_grid >= 0, 0.8 * norm, 0)  # Blue
        colors[:,:,3] = 0.9  # Alpha - semi-transparent

        try:
            # Configurar superfície 3D com o formato correto para GLSurfacePlotItem
            self.surface.setData(x=x_vals, y=y_vals, z=z_grid, colors=colors)
            
            # Atualizar plano Z=0
            verts = np.array([
                [1.5 * self.S0, 0.01, 0], [1.5 * self.S0, y_vals[-1], 0], 
                [0.5 * self.S0, y_vals[-1], 0], [0.5 * self.S0, 0.01, 0]
            ])
            self.z0_plane.setMeshData(vertexes=verts, faces=np.array([[0, 1, 2], [0, 2, 3]]))
        except Exception as e:
            print(f"Erro na atualização da superfície 3D: {e}")

    # --- Métodos para menu e ações ---
    def reset_all(self):
        """Resetar todos os parâmetros para valores padrão"""
        self.S0 = 100.0
        self.K = 100.0
        self.T = 1.0
        self.sigma = 0.2
        self.r = 0.05
        self.option_type = 'call'
        self.greek = 'Delta'
        self.is_buyer = True
        self.param3d = 'Tempo (T)'
        
        # Atualizar controles para refletir o estado
        self.update_controls()
        
        # Atualizar visualização
        self.update_all()
        
    def save_config(self):
        """Salvar configuração atual em arquivo"""
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Configuration", "", "JSON Files (*.json);;All Files (*)", 
            options=options
        )
        
        if filename:
            # Garantir extensão .json
            if not filename.endswith('.json'):
                filename += '.json'
                
            # Preparar configuração
            config = {
                'S0': self.S0,
                'K': self.K,
                'T': self.T,
                'sigma': self.sigma,
                'r': self.r,
                'option_type': self.option_type,
                'greek': self.greek,
                'is_buyer': self.is_buyer,
                'param3d': self.param3d
            }
            
            # Salvar em arquivo
            with open(filename, 'w') as f:
                json.dump(config, f, indent=4)
                
            QtWidgets.QMessageBox.information(self, "Success", f"Configuration saved to {filename}")
                
    def load_config(self):
        """Carregar configuração de arquivo"""
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Load Configuration", "", "JSON Files (*.json);;All Files (*)", 
            options=options
        )
        
        if filename:
            try:
                # Carregar do arquivo
                with open(filename, 'r') as f:
                    config = json.load(f)
                    
                # Atualizar parâmetros
                self.S0 = config.get('S0', 100.0)
                self.K = config.get('K', 100.0)
                self.T = config.get('T', 1.0)
                self.sigma = config.get('sigma', 0.2)
                self.r = config.get('r', 0.05)
                self.option_type = config.get('option_type', 'call')
                self.greek = config.get('greek', 'Delta')
                self.is_buyer = config.get('is_buyer', True)
                self.param3d = config.get('param3d', 'Tempo (T)')
                
                # Atualizar controles e visualização
                self.update_controls()
                self.update_all()
                
                QtWidgets.QMessageBox.information(self, "Success", f"Configuration loaded from {filename}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load configuration: {str(e)}")
                
    def export_image(self):
        """Exportar imagem dos gráficos"""
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)", 
            options=options
        )
        
        if filename:
            # Garantir extensão
            if not (filename.endswith('.png') or filename.endswith('.jpg')):
                filename += '.png'
                
            try:
                # Criar screenshot da janela
                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(self.winId())
                screenshot.save(filename)
                
                QtWidgets.QMessageBox.information(self, "Success", f"Image saved to {filename}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save image: {str(e)}")
                
    def show_calculator(self):
        """Mostrar calculadora de opções"""
        # Criar janela de calculadora básica
        calc_dialog = QtWidgets.QDialog(self)
        calc_dialog.setWindowTitle("Option Calculator")
        calc_dialog.setMinimumWidth(400)
        
        # Layout
        layout = QtWidgets.QVBoxLayout()
        calc_dialog.setLayout(layout)
        
        # Campos de entrada
        form_layout = QtWidgets.QFormLayout()
        
        s_input = QtWidgets.QDoubleSpinBox()
        s_input.setRange(1, 1000)
        s_input.setValue(self.S0)
        s_input.setDecimals(2)
        
        k_input = QtWidgets.QDoubleSpinBox()
        k_input.setRange(1, 1000)
        k_input.setValue(self.K)
        k_input.setDecimals(2)
        
        t_input = QtWidgets.QDoubleSpinBox()
        t_input.setRange(0.01, 10)
        t_input.setValue(self.T)
        t_input.setDecimals(2)
        t_input.setSingleStep(0.05)
        
        sigma_input = QtWidgets.QDoubleSpinBox()
        sigma_input.setRange(0.01, 1)
        sigma_input.setValue(self.sigma)
        sigma_input.setDecimals(2)
        sigma_input.setSingleStep(0.01)
        
        r_input = QtWidgets.QDoubleSpinBox()
        r_input.setRange(0, 0.2)
        r_input.setValue(self.r)
        r_input.setDecimals(3)
        r_input.setSingleStep(0.005)
        
        option_type = QtWidgets.QComboBox()
        option_type.addItems(["Call", "Put"])
        option_type.setCurrentIndex(0 if self.option_type == 'call' else 1)
        
        form_layout.addRow("Asset Price (S):", s_input)
        form_layout.addRow("Strike Price (K):", k_input)
        form_layout.addRow("Time to Expiry (T):", t_input)
        form_layout.addRow("Volatility (σ):", sigma_input)
        form_layout.addRow("Interest Rate (r):", r_input)
        form_layout.addRow("Option Type:", option_type)
        
        layout.addLayout(form_layout)
        
        # Resultado
        result_group = QtWidgets.QGroupBox("Results")
        result_layout = QtWidgets.QVBoxLayout()
        result_group.setLayout(result_layout)
        
        result_text = QtWidgets.QTextEdit()
        result_text.setReadOnly(True)
        result_layout.addWidget(result_text)
        
        layout.addWidget(result_group)
        
        # Botões
        button_layout = QtWidgets.QHBoxLayout()
        
        calculate_btn = QtWidgets.QPushButton("Calculate")
        close_btn = QtWidgets.QPushButton("Close")
        apply_btn = QtWidgets.QPushButton("Apply to Main View")
        
        button_layout.addWidget(calculate_btn)
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # Função de cálculo
        def calculate():
            try:
                # Obter valores
                s = s_input.value()
                k = k_input.value()
                t = t_input.value()
                sigma = sigma_input.value()
                r = r_input.value()
                opt_type = 'call' if option_type.currentText() == "Call" else 'put'
                
                # Calcular
                calc = OptionCalculator(s, k, t, sigma, r, opt_type)
                price = calc.price()
                delta = calc.delta()
                gamma = calc.gamma()
                theta = calc.theta()
                vega = calc.vega() * 100
                rho = calc.rho() * 100
                
                # Exibir resultado
                result_html = f"""
                <h3>Option Pricing Results</h3>
                <p><b>Price:</b> {price:.4f}</p>
                <p><b>Delta:</b> {delta:.4f}</p>
                <p><b>Gamma:</b> {gamma:.4f}</p>
                <p><b>Theta:</b> {theta:.4f}/day</p>
                <p><b>Vega:</b> {vega:.4f} (for 1% Δσ)</p>
                <p><b>Rho:</b> {rho:.4f} (for 1% Δr)</p>
                """
                result_text.setHtml(result_html)
                
            except Exception as e:
                result_text.setHtml(f"<p style='color:red'>Error: {str(e)}</p>")
                
        # Função para aplicar valores à visualização principal
        def apply_to_main():
            self.S0 = s_input.value()
            self.K = k_input.value()
            self.T = t_input.value()
            self.sigma = sigma_input.value()
            self.r = r_input.value()
            self.option_type = 'call' if option_type.currentText() == "Call" else 'put'
            
            self.update_controls()
            self.update_all()
            
            QtWidgets.QMessageBox.information(calc_dialog, "Success", "Values applied to main view")
            
        # Conectar signals
        calculate_btn.clicked.connect(calculate)
        apply_btn.clicked.connect(apply_to_main)
        close_btn.clicked.connect(calc_dialog.close)
        
        # Calcular valores iniciais
        calculate()
        
        # Exibir dialog
        calc_dialog.exec_()
        
    def show_about(self):
        """Mostrar informações sobre o programa"""
        about_text = """
        <h2>Black-Scholes Advanced Visualizer</h2>
        <p>Version 2.0</p>
        <p>A high performance interactive visualization tool for option pricing and sensitivities using the Black-Scholes model.</p>
        <p>Features:</p>
        <ul>
            <li>Interactive 2D and 3D visualizations</li>
            <li>Real-time parameter manipulation</li>
            <li>Deep analysis of option Greeks</li>
            <li>Scenario comparison</li>
            <li>Payoff and profit profiles</li>
        </ul>
        """
        
        QtWidgets.QMessageBox.about(self, "About", about_text)

    def closeEvent(self, event):
        """Manipulador para evento de fechamento da janela"""
        reply = QtWidgets.QMessageBox.question(
            self, 'Exit Confirmation',
            'Are you sure you want to exit?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# --- Função principal ---
def main():
    """Função principal para iniciar a aplicação"""
    # Garantir tratamento de exceções de alta resolução
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    
    app = QtWidgets.QApplication(sys.argv)
    
    # Definir estilo da aplicação
    app.setStyle('Fusion')
    
    # Criar e exibir janela principal
    main_window = BlackScholesVisualizer()
    main_window.show()
    
    # Executar loop de eventos
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
