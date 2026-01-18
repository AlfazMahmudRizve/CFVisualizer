import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patheffects as path_effects

plt.style.use('dark_background')

class AimbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aimbot Visualizer v2.0")
        self.root.geometry("1100x700")
        self.root.configure(bg="#0f0f0f")

        self.x_data = [] # Start empty
        self.y_data = []
        self.coeffs = None # Store polynomial coefficients

        self.sidebar = tk.Frame(root, width=250, bg="#1a1a1a", padx=20, pady=20)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y)

        self._create_sidebar()

        self.plot_frame = tk.Frame(root, bg="#0f0f0f")
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._create_plot()
        self.update_plot()

    def _create_sidebar(self):
        tk.Label(self.sidebar, text="SYSTEM STATUS", font=("Consolas", 18, "bold"), 
                 fg="#00fa9a", bg="#1a1a1a").pack(pady=(0, 20))

        # --- MANUAL INPUT SECTION ---
        input_frame = tk.Frame(self.sidebar, bg="#1a1a1a")
        input_frame.pack(fill=tk.X, pady=10)

        tk.Label(input_frame, text="MANUAL INPUT:", font=("Consolas", 10, "bold"), fg="#888", bg="#1a1a1a").pack(anchor="w")

        # X Input
        row1 = tk.Frame(input_frame, bg="#1a1a1a")
        row1.pack(fill=tk.X, pady=2)
        tk.Label(row1, text="X:", font=("Consolas", 10), fg="white", bg="#1a1a1a", width=3).pack(side=tk.LEFT)
        self.entry_x = tk.Entry(row1, bg="#333", fg="white", insertbackground="white", bd=0, font=("Consolas", 10))
        self.entry_x.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Y Input
        row2 = tk.Frame(input_frame, bg="#1a1a1a")
        row2.pack(fill=tk.X, pady=2)
        tk.Label(row2, text="Y:", font=("Consolas", 10), fg="white", bg="#1a1a1a", width=3).pack(side=tk.LEFT)
        self.entry_y = tk.Entry(row2, bg="#333", fg="white", insertbackground="white", bd=0, font=("Consolas", 10))
        self.entry_y.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Add Button
        btn_config = {"font": ("Segoe UI", 10, "bold"), "bd": 0, "padx": 10, "pady": 5, "cursor": "hand2"}
        tk.Button(input_frame, text="[ INJECT DATA ]", command=self.add_manual_point, 
                  fg="#1a1a1a", bg="#00fa9a", **btn_config).pack(fill=tk.X, pady=10)

        # --- CONTROLS ---
        tk.Frame(self.sidebar, height=2, bg="#333").pack(fill=tk.X, pady=10)

        tk.Button(self.sidebar, text="[ REBOOT SYSTEM ]", command=self.reset_data, 
                  fg="white", bg="#d63340", **btn_config).pack(fill=tk.X, pady=5)
        
        tk.Button(self.sidebar, text="[ ACCESS ARCHIVES ]", command=self.show_math_explanation, 
                  fg="#1a1a1a", bg="#05d9e8", **btn_config).pack(fill=tk.X, pady=5)

        tk.Frame(self.sidebar, height=2, bg="#333").pack(fill=tk.X, pady=20)

        tk.Label(self.sidebar, text="TRAJECTORY DATA:", font=("Segoe UI", 10, "bold"), 
                 fg="#666", bg="#1a1a1a").pack(pady=(10, 5))
        
        self.eq_var = tk.StringVar()
        self.eq_label = tk.Label(self.sidebar, textvariable=self.eq_var, font=("Consolas", 10), 
                                 fg="#00fa9a", bg="#000", padx=10, pady=15, wraplength=200, justify=tk.LEFT)
        self.eq_label.pack(fill=tk.X)

    def add_manual_point(self):
        try:
            x_val = float(self.entry_x.get())
            y_val = float(self.entry_y.get())
            
            self.x_data.append(x_val)
            self.y_data.append(y_val)
            
            # Clear inputs
            self.entry_x.delete(0, tk.END)
            self.entry_y.delete(0, tk.END)
            
            self.update_plot()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric coordinates.")

    def _create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.fig.patch.set_facecolor('#0f0f0f')
        self.ax.set_facecolor('#0f0f0f')
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_click(self, event):
        if event.inaxes != self.ax: return
        self.x_data.append(event.xdata)
        self.y_data.append(event.ydata)
        self.update_plot()

    def reset_data(self):
        self.x_data = []
        self.y_data = []
        self.coeffs = None
        self.update_plot()

    def update_plot(self):
        self.ax.clear()
        self.coeffs = None # Reset coeffs before calculation
        
        # Grid and Visuals
        self.ax.grid(True, linestyle='--', color='#333333', alpha=0.5)
        self.ax.axhline(0, color='#666', linewidth=1)
        self.ax.set_title("/// TARGET PREDICTION VISUALIZER ///", color='#888', fontsize=12, pad=20, loc='left', fontfamily='Consolas')
        self.ax.tick_params(colors='#888', which='both')
        self.ax.spines['bottom'].set_color('#444')
        self.ax.spines['top'].set_color('#444') 
        self.ax.spines['right'].set_color('#444')
        self.ax.spines['left'].set_color('#444')

        has_legend_items = False

        if len(self.x_data) > 0:
            self.ax.scatter(self.x_data, self.y_data, color='#ff2a6d', s=120, marker='+', linewidth=2, label='SENSOR INPUT')
            has_legend_items = True

        if len(self.x_data) >= 3:
            try:
                coeffs = np.polyfit(self.x_data, self.y_data, 2)
                self.coeffs = coeffs # Store for explanation
                poly = np.poly1d(coeffs)

                a, b, c = coeffs
                self.eq_var.set(f"y = {a:.4f}x²\n+ {b:.4f}x\n+ {c:.4f}")

                max_x = max(self.x_data) if self.x_data else 10
                x_future = np.linspace(min(self.x_data, default=0), max_x + 50, 150)
                y_future = poly(x_future)

                # Glow Effect
                line, = self.ax.plot(x_future, y_future, color='#05d9e8', linestyle='-', linewidth=2, label='PREDICTED ARC')
                line.set_path_effects([path_effects.SimpleLineShadow(offset=(0,0), shadow_color='#05d9e8', alpha=0.3, linewidth=10),
                                       path_effects.Normal()])
                has_legend_items = True

                roots = poly.roots
                real_roots = [r for r in roots if np.isreal(r) and r > max(self.x_data, default=0)]
                if real_roots:
                    impact_x = real_roots[0].real
                    
                    self.ax.plot([impact_x], [0], marker='o', markersize=10, markerfacecolor='#00fa9a', markeredgecolor='white', markeredgewidth=2)
                    self.ax.text(impact_x, 2, f"IMPACT\n{impact_x:.1f}m", color='#00fa9a', ha='center', fontfamily='Consolas', fontsize=9)
                    self.ax.plot([0, impact_x], [0, 0], color='#00fa9a', linewidth=1, alpha=0.5)

            except Exception as e:
                self.eq_var.set("CALCULATION_ERROR")
        else:
            self.eq_var.set("AWAITING_DATA...")

        if has_legend_items:
            self.ax.legend(loc='upper right', facecolor='#0f0f0f', edgecolor='#333', labelcolor='#888')
        self.canvas.draw()

    def show_math_explanation(self):
        if self.coeffs is None or len(self.x_data) < 3:
            messagebox.showinfo("Insufficient Data", "Add at least 3 points to generate the calculation details.")
            return

        top = tk.Toplevel(self.root)
        top.title("CALCULATION LOG: STEP-BY-STEP")
        top.geometry("700x600")
        top.configure(bg="#1e1e1e")

        # Scrollable container
        canvas = tk.Canvas(top, bg="#1e1e1e", highlightthickness=0)
        scrollbar = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg="#1e1e1e")

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Helpers for styling
        def add_header(text):
            tk.Label(frame, text=text, font=("Consolas", 14, "bold"), fg="#00fa9a", bg="#1e1e1e", pady=10).pack(anchor="w", padx=20)
        def add_text(text, color="white"):
            tk.Label(frame, text=text, font=("Consolas", 10), fg=color, bg="#1e1e1e", justify=tk.LEFT).pack(anchor="w", padx=20)

        # 1. THE EQUATION
        a, b, c = self.coeffs
        add_header("1. POLYNOMIAL MODEL DETECTED")
        add_text(f"The Method of Least Squares minimized SSE to find:")
        add_text(f"y = ({a:.6f})x² + ({b:.6f})x + ({c:.6f})", color="#05d9e8")
        
        # 2. RESIDUALS TABLE
        add_header("2. DATA ANALYSIS (RESIDUALS)")
        add_text("Checking how well the curve fits your observations:")
        
        table_frame = tk.Frame(frame, bg="#252526", padx=10, pady=10)
        table_frame.pack(fill="x", padx=20, pady=5)
        
        # Table Headers
        headers = ["X (m)", "Observed Y (m)", "Model Y (m)", "Error (Resid)"]
        for col, text in enumerate(headers):
            tk.Label(table_frame, text=text, font=("Consolas", 10, "bold"), fg="#aaa", bg="#252526", width=15).grid(row=0, column=col)
        
        # Table Rows
        poly = np.poly1d(self.coeffs)
        total_sse = 0
        for i, (x_obs, y_obs) in enumerate(zip(self.x_data, self.y_data)):
            y_pred = poly(x_obs)
            resid = y_obs - y_pred
            total_sse += resid**2
            
            fg_col = "#00fa9a" if abs(resid) < 0.5 else ("#ff2a6d" if abs(resid) > 2.0 else "white")
            
            tk.Label(table_frame, text=f"{x_obs:.2f}", font=("Consolas", 10), fg="white", bg="#252526").grid(row=i+1, column=0)
            tk.Label(table_frame, text=f"{y_obs:.2f}", font=("Consolas", 10), fg="white", bg="#252526").grid(row=i+1, column=1)
            tk.Label(table_frame, text=f"{y_pred:.2f}", font=("Consolas", 10), fg="#05d9e8", bg="#252526").grid(row=i+1, column=2)
            tk.Label(table_frame, text=f"{resid:+.4f}", font=("Consolas", 10), fg=fg_col, bg="#252526").grid(row=i+1, column=3)

        add_text(f"\nTotal Sum of Squared Errors (SSE): {total_sse:.6f}", color="#ff2a6d")
        
        # 3. IMPACT CALCULATION
        add_header("3. IMPACT PREDICTION LOGIC")
        add_text("Solving for ground impact (y = 0):")
        add_text(f"0 = {a:.4f}x² + {b:.4f}x + {c:.4f}")
        add_text("Using the Quadratic Formula: x = [-b ± sqrt(b² - 4ac)] / 2a")
        
        disc = b**2 - 4*a*c
        add_text(f"Discriminant (Δ) = {b:.4f}² - 4({a:.4f})({c:.4f}) = {disc:.4f}")
        
        if disc >= 0:
            x1 = (-b + np.sqrt(disc)) / (2*a)
            x2 = (-b - np.sqrt(disc)) / (2*a)
            add_text(f"Roots found: x1={x1:.2f}, x2={x2:.2f}")
            target = max(x1, x2)
            add_text(f"Target selected (Positive/Forward): {target:.2f} meters", color="#00fa9a")
        else:
            add_text("No real roots found (Projectile never hits y=0).", color="#ff2a6d")

        tk.Button(frame, text="CLOSE LOG", command=top.destroy, bg="#d63340", fg="white", font=("Segoe UI", 10, "bold"), width=20).pack(pady=30)

if __name__ == "__main__":
    root = tk.Tk()
    app = AimbotApp(root)
    root.mainloop()