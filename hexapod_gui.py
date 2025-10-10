import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import serial
import serial.tools.list_ports

class HexapodGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🕷️ Hexapod Control GUI")
        self.root.geometry("950x740")
        self.root.configure(bg="#E6F0FA")

        self.serial_conn = None
        self.connected = False
        self.movement_reset_timer = None
        self.movement_reset_delay = 1500  # milliseconds (1.5s)

        # Try auto-connection
        self.try_auto_connect()

        # ----- Styles -----
        style = ttk.Style()
        style.configure("TLabel", background="#E6F0FA", font=("Arial", 14))
        style.configure("TButton", font=("Arial", 13))
        style.configure("TFrame", background="#E6F0FA")

        # ----- Frames -----
        self.connection_frame = ttk.LabelFrame(root, text="Connection", padding=10)
        self.connection_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.controls_frame = ttk.LabelFrame(root, text="Movement Controls", padding=20)
        self.controls_frame.grid(row=1, column=0, padx=20, pady=10)

        self.movement_monitor_frame = ttk.LabelFrame(root, text="Movement Monitor", padding=10)
        self.movement_monitor_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.advanced_frame = ttk.LabelFrame(root, text="Advanced Settings", padding=15)
        self.advanced_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.status_frame = ttk.LabelFrame(root, text="Status Monitor", padding=10)
        self.status_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=10, sticky="ns")

        # ----- Connection Panel -----
        ttk.Label(self.connection_frame, text="Select Port:").grid(row=0, column=0, padx=10)
        self.port_combo = ttk.Combobox(self.connection_frame, width=15, state="readonly")
        self.port_combo.grid(row=0, column=1, padx=10)
        self.refresh_ports()

        ttk.Button(self.connection_frame, text="Connect", command=self.connect_arduino).grid(row=0, column=2, padx=10)
        ttk.Button(self.connection_frame, text="Refresh", command=self.refresh_ports).grid(row=0, column=3, padx=10)

        # ----- Load Images -----
        try:
            arrow = Image.open("RightArrow.png").resize((60, 60))
            self.img_up = ImageTk.PhotoImage(arrow.rotate(90))
            self.img_down = ImageTk.PhotoImage(arrow.rotate(270))
            self.img_left = ImageTk.PhotoImage(arrow.rotate(180))
            self.img_right = ImageTk.PhotoImage(arrow)
        except Exception:
            self.img_up = self.img_down = self.img_left = self.img_right = None

        # ----- Movement Buttons -----
        tk.Button(self.controls_frame, text="Front", image=self.img_up, compound="top",
                  bg="#FFA500", font=("Arial", 12), command=self.move_front).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.controls_frame, text="Left", image=self.img_left, compound="top",
                  bg="#FFA500", font=("Arial", 12), command=self.move_left).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.controls_frame, text="Right", image=self.img_right, compound="top",
                  bg="#FFA500", font=("Arial", 12), command=self.move_right).grid(row=1, column=2, padx=10, pady=10)
        tk.Button(self.controls_frame, text="Back", image=self.img_down, compound="top",
                  bg="#FFA500", font=("Arial", 12), command=self.move_back).grid(row=1, column=1, padx=10, pady=10)

        # ----- Movement Monitor -----
        self.current_move_text = tk.StringVar(value="Idle 💤")
        self.current_move_label = ttk.Label(self.movement_monitor_frame,
                                            textvariable=self.current_move_text,
                                            font=("Arial", 16, "bold"), foreground="blue")
        self.current_move_label.pack(padx=5, pady=5)

        # ----- Advanced Settings -----
        ttk.Label(self.advanced_frame, text="Speed:").grid(row=0, column=0, padx=10)
        self.speed_slider = ttk.Scale(self.advanced_frame, from_=0, to=100, orient="horizontal",
                                      command=self.update_speed)
        self.speed_slider.set(50)
        self.speed_slider.grid(row=0, column=1, padx=10)

        ttk.Label(self.advanced_frame, text="Leg Height:").grid(row=1, column=0, padx=10)
        self.height_slider = ttk.Scale(self.advanced_frame, from_=0, to=50, orient="horizontal",
                                       command=self.update_height)
        self.height_slider.set(25)
        self.height_slider.grid(row=1, column=1, padx=10)

        # ----- Status Monitor -----
        self.status_text = tk.StringVar(value="Initializing connection...")
        ttk.Label(self.status_frame, textvariable=self.status_text).pack(anchor="w", pady=5)
        self.status_box = tk.Text(self.status_frame, height=25, width=45, wrap="word", state="normal")
        self.status_box.pack()

        # ----- Keyboard Controls -----
        for key in ["w", "a", "s", "d", "<Up>", "<Left>", "<Down>", "<Right>"]:
            root.bind_all(key, self.handle_keypress)

        self.log("GUI Initialized ✅")

    # ---------------- SERIAL HANDLING ----------------
    def try_auto_connect(self):
        """Attempt to auto-connect to any available Arduino."""
        try:
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                try:
                    self.serial_conn = serial.Serial(port.device, 9600, timeout=1)
                    self.connected = True
                    print(f"Auto-connected to {port.device}")
                    return
                except serial.SerialException:
                    continue
            self.connected = False
        except Exception:
            self.connected = False

    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo["values"] = ports
        if ports:
            self.port_combo.set(ports[0])
        else:
            self.port_combo.set("No ports found")

    def connect_arduino(self):
        port = self.port_combo.get()
        try:
            self.serial_conn = serial.Serial(port, 9600, timeout=1)
            self.connected = True
            self.update_status(f"✅ Connected to Arduino on {port}")
        except Exception as e:
            self.connected = False
            self.serial_conn = None
            self.update_status(f"⚠️ Connection failed: {e}")

    def send_command(self, command):
        """Send serial command to Arduino or simulate if not connected."""
        if self.connected and self.serial_conn:
            try:
                self.serial_conn.write(command.encode())
                self.log(f"Sent → {command.strip()}")
            except Exception as e:
                self.update_status(f"⚠️ Error sending: {e}")
        else:
            self.log(f"[SIM] Command: {command.strip()}")

    # ---------------- MOVEMENT COMMANDS ----------------
    def move_front(self, *_): self._move_action("🕷️ Moving Forward", "F")
    def move_back(self, *_): self._move_action("🕷️ Moving Backward", "B")
    def move_left(self, *_): self._move_action("↩️ Turning Left", "L")
    def move_right(self, *_): self._move_action("↪️ Turning Right", "R")

    def _move_action(self, label_text, command):
        self.current_move_text.set(label_text)
        self.send_command(command)
        # Reset movement label after 1.5s
        if self.movement_reset_timer:
            self.root.after_cancel(self.movement_reset_timer)
        self.movement_reset_timer = self.root.after(self.movement_reset_delay, self.reset_movement_status)

    def reset_movement_status(self):
        self.current_move_text.set("Idle 💤")

    # ---------------- SLIDERS ----------------
    def update_speed(self, val):
        self.send_command(f"S{int(float(val))}\n")

    def update_height(self, val):
        self.send_command(f"H{int(float(val))}\n")

    # ---------------- KEYBOARD ----------------
    def handle_keypress(self, event):
        self.root.focus_set()  # prevent typing in widgets
        key = event.keysym.lower()
        if key in ["w", "up"]:
            self.move_front()
        elif key in ["s", "down"]:
            self.move_back()
        elif key in ["a", "left"]:
            self.move_left()
        elif key in ["d", "right"]:
            self.move_right()

    # ---------------- UI HELPERS ----------------
    def update_status(self, msg):
        self.status_text.set(msg)
        self.log(msg)

    def log(self, msg):
        self.status_box.insert(tk.END, msg + "\n")
        self.status_box.see(tk.END)
        print(msg)


# ---------------- MAIN APP ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HexapodGUI(root)
    if app.connected:
        app.update_status("✅ Connected to Arduino automatically.")
    else:
        app.update_status("⚠️ No Arduino detected — running in simulation mode.")
    root.mainloop()
