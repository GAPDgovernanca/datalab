# First, set the backend before importing other matplotlib components
import matplotlib
matplotlib.use('TkAgg')  # Using TkAgg backend which is more reliable

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy.stats import norm
import matplotlib.gridspec as gridspec

# Print version info for debugging
print(f"Matplotlib version: {matplotlib.__version__}")
print(f"Active backend: {matplotlib.get_backend()}")

# Black-Scholes functions for option pricing
def d1(S, K, r, sigma, T):
    """Calculate d1 from the Black-Scholes formula"""
    return (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def d2(S, K, r, sigma, T):
    """Calculate d2 from the Black-Scholes formula"""
    return d1(S, K, r, sigma, T) - sigma * np.sqrt(T)

def bs_call_price(S, K, r, sigma, T):
    """Calculate call option price using Black-Scholes formula"""
    if T <= 0:
        return max(0, S - K)
    D1 = d1(S, K, r, sigma, T)
    D2 = d2(S, K, r, sigma, T)
    return S * norm.cdf(D1) - K * np.exp(-r * T) * norm.cdf(D2)

def bs_put_price(S, K, r, sigma, T):
    """Calculate put option price using Black-Scholes formula"""
    if T <= 0:
        return max(0, K - S)
    D1 = d1(S, K, r, sigma, T)
    D2 = d2(S, K, r, sigma, T)
    return K * np.exp(-r * T) * norm.cdf(-D2) - S * norm.cdf(-D1)

def synthetic_long_stock(stock_range, K, r, sigma, T):
    """Create synthetic long stock using call and short put"""
    calls = [bs_call_price(s, K, r, sigma, T) for s in stock_range]
    puts = [bs_put_price(s, K, r, sigma, T) for s in stock_range]
    return [c - p for c, p in zip(calls, puts)]

def put_call_parity_demo():
    """Create interactive demonstration of put-call parity"""
    # Initial parameters
    S_init, K_init = 100, 100
    r_init, sigma_init, T_init = 0.05, 0.2, 1
    
    # Setup figure with improved size
    fig = plt.figure(figsize=(15, 9))
    
    # Adjust the layout using gridspec for better proportions
    # Giving more space to the plots and less to the other elements
    gs = gridspec.GridSpec(3, 2, height_ratios=[0.5, 4, 1.5])
    
    # Title and explanation
    ax_title = plt.subplot(gs[0, :])
    ax_title.axis('off')
    ax_title.text(0.5, 0.6, 'Put-Call Parity Interactive Demonstration', 
                 horizontalalignment='center', fontsize=18, fontweight='bold')
    ax_title.text(0.5, 0.2, 
                 'Put-Call Parity Equation: C + PV(K) = P + S\n'
                 'Where C = Call Price, P = Put Price, S = Stock Price, PV(K) = Present Value of Strike', 
                 horizontalalignment='center', fontsize=12)
    
    # Option prices plot - slightly larger for better visibility
    ax_options = plt.subplot(gs[1, 0])
    
    # Parity plot
    ax_parity = plt.subplot(gs[1, 1])
    
    # Values and explanation area - reorganized
    ax_values = plt.subplot(gs[2, :])
    ax_values.axis('off')
    
    # Create compact slider section with better organization
    # Put sliders in a separate figure region
    slider_color = 'lightgoldenrodyellow'
    slider_width = 0.65
    slider_height = 0.02  # Reduced height
    slider_left = 0.18
    slider_bottom = 0.08  # More compact placement
    
    # Compact slider placement with consistent spacing
    ax_slider_s = plt.axes([slider_left, slider_bottom, slider_width, slider_height], facecolor=slider_color)
    ax_slider_k = plt.axes([slider_left, slider_bottom - 0.03, slider_width, slider_height], facecolor=slider_color)
    ax_slider_r = plt.axes([slider_left, slider_bottom - 0.06, slider_width, slider_height], facecolor=slider_color)
    ax_slider_sigma = plt.axes([slider_left, slider_bottom - 0.09, slider_width, slider_height], facecolor=slider_color)
    ax_slider_t = plt.axes([slider_left, slider_bottom - 0.12, slider_width, slider_height], facecolor=slider_color)
    
    # Create sliders with basic parameters only (no formatting parameters)
    s_slider = Slider(ax_slider_s, 'Stock Price (S)', 50, 150, valinit=S_init)
    k_slider = Slider(ax_slider_k, 'Strike Price (K)', 50, 150, valinit=K_init)
    r_slider = Slider(ax_slider_r, 'Risk-free Rate (r)', 0, 0.1, valinit=r_init)
    sigma_slider = Slider(ax_slider_sigma, 'Volatility (σ)', 0.05, 0.5, valinit=sigma_init)
    t_slider = Slider(ax_slider_t, 'Time (years)', 0.1, 2, valinit=T_init)
    
    def update_plots(val=None):
        """Update plots with current slider values"""
        # Get current slider values
        S = s_slider.val
        K = k_slider.val
        r = r_slider.val
        sigma = sigma_slider.val
        T = t_slider.val
        
        # Clear plots
        ax_options.clear()
        ax_parity.clear()
        ax_values.clear()
        
        # Calculate option prices
        call_price = bs_call_price(S, K, r, sigma, T)
        put_price = bs_put_price(S, K, r, sigma, T)
        pv_k = K * np.exp(-r * T)
        
        # Check parity
        left_side = call_price + pv_k
        right_side = put_price + S
        difference = left_side - right_side
        
        # Generate a range of stock prices
        stock_range = np.linspace(max(0.5 * K, S - 50), S + 50, 100)
        
        # Calculate option prices for the range
        call_prices = [bs_call_price(s, K, r, sigma, T) for s in stock_range]
        put_prices = [bs_put_price(s, K, r, sigma, T) for s in stock_range]
        
        # Calculate parity values
        left_sides = [c + pv_k for c in call_prices]
        right_sides = [p + s for p, s in zip(put_prices, stock_range)]
        
        # Calculate synthetic stock position
        synthetic_stock = synthetic_long_stock(stock_range, K, r, sigma, T)
        
        # Plot option prices with improved aesthetics
        ax_options.plot(stock_range, call_prices, 'b-', label='Call Price', linewidth=2)
        ax_options.plot(stock_range, put_prices, 'r-', label='Put Price', linewidth=2)
        ax_options.axvline(x=K, color='g', linestyle='--', label='Strike Price')
        ax_options.axvline(x=S, color='black', linestyle=':', label='Current Stock Price')
        ax_options.set_title('Option Prices vs Stock Price', fontsize=14)
        ax_options.set_xlabel('Stock Price', fontsize=12)
        ax_options.set_ylabel('Option Price', fontsize=12)
        ax_options.legend(fontsize=10)
        ax_options.grid(True, alpha=0.3)
        
        # Ensure y-axis limits prevent point annotations from being cut off
        y_min, y_max = ax_options.get_ylim()
        buffer = max(5, (y_max - y_min) * 0.1)  # At least 5 units or 10% of range
        ax_options.set_ylim(max(0, y_min - buffer), y_max + buffer)
        
        # Plot parity relationship with improved aesthetics
        ax_parity.plot(stock_range, left_sides, 'b-', label='C + PV(K)', linewidth=2)
        ax_parity.plot(stock_range, right_sides, 'r--', label='P + S', linewidth=2)
        ax_parity.plot(stock_range, synthetic_stock, 'g:', label='Synthetic Stock (C - P)', linewidth=2)
        ax_parity.plot(stock_range, stock_range, 'k-.', alpha=0.5, label='Stock Price Line')
        ax_parity.axvline(x=S, color='black', linestyle=':', label='Current Stock Price')
        ax_parity.set_title('Put-Call Parity Relationship', fontsize=14)
        ax_parity.set_xlabel('Stock Price', fontsize=12)
        ax_parity.set_ylabel('Portfolio Value', fontsize=12)
        ax_parity.legend(fontsize=10)
        ax_parity.grid(True, alpha=0.3)
        
        # Add annotations to show specific values at current stock price
        ax_options.scatter(S, call_price, color='blue', s=50, zorder=5)
        ax_options.scatter(S, put_price, color='red', s=50, zorder=5)
        ax_options.annotate(f'C={call_price:.2f}', (S, call_price), xytext=(5, 5), 
                           textcoords='offset points', fontsize=10, fontweight='bold')
        ax_options.annotate(f'P={put_price:.2f}', (S, put_price), xytext=(5, -15), 
                           textcoords='offset points', fontsize=10, fontweight='bold')
        
        # Display values in a cleaner layout with better spacing
        # Create two side-by-side text boxes
        values_text = (
            f"Current Values:\n"
            f"Call Price (C): ${call_price:.2f}\n"
            f"Put Price (P): ${put_price:.2f}\n"
            f"Stock Price (S): ${S:.2f}\n"
            f"Present Value of Strike (PV(K)): ${pv_k:.2f}\n\n"
            f"Put-Call Parity Check:\n"
            f"C + PV(K) = ${left_side:.2f}\n"
            f"P + S = ${right_side:.2f}\n"
            f"Difference = ${difference:.5f}\n"
            f"Parity holds? {'Yes' if abs(difference) < 0.01 else 'No'}"
        )
        
        # Better positioning for values text box
        ax_values.text(0.05, 0.5, values_text, fontsize=12, 
                      verticalalignment='center', transform=ax_values.transAxes,
                      bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
        
        # Add explanation with improved formatting
        explanation = (
            "Put-Call Parity demonstrates that:\n\n"
            "1. Long Call + Cash (PV(K)) = Long Put + Long Stock\n"
            "2. Long Call - Long Put = Synthetic Long Stock\n"
            "3. Long Put - Long Call = Synthetic Short Stock\n\n"
            "If this relationship is violated, arbitrage is possible.\n"
            "Traders can profit by buying the undervalued side\n"
            "and selling the overvalued side."
        )
        
        # Better positioning for explanation text box
        ax_values.text(0.55, 0.5, explanation, fontsize=12,
                      verticalalignment='center', transform=ax_values.transAxes,
                      bbox=dict(facecolor='lightyellow', alpha=0.8, boxstyle='round,pad=0.5'))
        
        fig.canvas.draw_idle()
    
    # Connect sliders to update function
    s_slider.on_changed(update_plots)
    k_slider.on_changed(update_plots)
    r_slider.on_changed(update_plots)
    sigma_slider.on_changed(update_plots)
    t_slider.on_changed(update_plots)
    
    # Initial plot
    update_plots()
    
    # Add a reset button in a better position
    reset_ax = plt.axes([0.85, 0.02, 0.1, 0.04])
    reset_button = Button(reset_ax, 'Reset', color=slider_color, hovercolor='0.975')
    
    def reset(event):
        """Reset all sliders to initial values"""
        s_slider.reset()
        k_slider.reset()
        r_slider.reset()
        sigma_slider.reset()
        t_slider.reset()
    
    reset_button.on_clicked(reset)
    
    # Better spacing for the whole figure
    plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.15, hspace=0.3)
    
    plt.show()

# Run the demonstration
if __name__ == "__main__":
    print("Put-Call Parity Interactive Demonstration")
    print("----------------------------------------")
    print("This program demonstrates the concept of put-call parity, a fundamental")
    print("relationship in option pricing theory that states:")
    print("")
    print("    C + PV(K) = P + S    ")
    print("")
    print("Where:")
    print("  C = Call option price")
    print("  P = Put option price")
    print("  S = Stock price")
    print("  PV(K) = Present value of strike price K = K * e^(-r*T)")
    print("")
    print("Use the sliders to adjust parameters and observe how the relationship holds.")
    print("The left graph shows option prices, while the right graph shows the parity relationship.")
    print("")
    print("Opening interactive visualization...")
    
    try:
        put_call_parity_demo()
    except Exception as e:
        print(f"Error running the demo: {e}")
        print("\nTrying alternative backend...")
        try:
            # Try with a different backend
            matplotlib.use('Agg')
            print("Switched to 'Agg' backend - This might produce a static image only")
            put_call_parity_demo()
        except Exception as e2:
            print(f"Error with alternative backend: {e2}")
            print("\nPlease try with a different matplotlib backend:")
            print("Add this line at the top of your script:")
            print("    import matplotlib; matplotlib.use('WebAgg')  # or 'TkAgg', 'Qt5Agg', etc.")