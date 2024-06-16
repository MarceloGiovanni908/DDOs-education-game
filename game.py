import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Server Class
class Server:
    def __init__(self, health=100):
        self.health = health
        self.defenses = []

    def apply_attack(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def apply_defense(self, defense):
        self.defenses.append(defense)

    def remove_defense(self, defense):
        if defense in self.defenses:
            self.defenses.remove(defense)

    def display_status(self):
        status = f"Server Health: {self.health}\nActive Defenses: {', '.join([d.name for d in self.defenses])}"
        return status

# Attack Class
class Attack:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

# Defense Class
class Defense:
    def __init__(self, name, reduction):
        self.name = name
        self.reduction = reduction

# Game Class
class DDOSGame:
    def __init__(self, ui):
        self.server = Server()
        self.attacks = [
            Attack("SYN Flood", 20),
            Attack("HTTP Flood", 15),
            Attack("UDP Flood", 25)
        ]
        self.defenses = [
            Defense("Firewall", 10),
            Defense("Rate Limiting", 5),
            Defense("IP Blocking", 20)
        ]
        self.ui = ui

    def start(self):
        self.ui.update_server_status(self.server.display_status())

    def attack(self, attack_index):
        attack = self.attacks[attack_index]
        damage = attack.damage - sum(defense.reduction for defense in self.server.defenses)
        if damage < 0:
            damage = 0
        self.server.apply_attack(damage)
        messagebox.showinfo("Attack", f"{attack.name} executed! Damage dealt: {damage}")
        self.ui.update_server_status(self.server.display_status())
        self.ui.display_attack_visual(attack.name)
        self.check_game_over()

    def defend(self, defense_index):
        defense = self.defenses[defense_index]
        self.server.apply_defense(defense)
        messagebox.showinfo("Defense", f"{defense.name} activated! Reduction applied: {defense.reduction}")
        self.ui.update_server_status(self.server.display_status())

    def check_game_over(self):
        if self.server.health <= 0:
            messagebox.showinfo("Game Over", "The server has been taken down! Game Over.")
            self.ui.window.destroy()

# UI Class
class DDOSGameUI:
    def __init__(self, root):
        self.window = root
        self.window.title("DDoS Simulation Game")
        self.window.geometry("800x600")

        # Load and set background image
        self.bg_image = Image.open("background.jpg")
        self.bg_image = self.bg_image.resize((800, 600), Image.ANTIALIAS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.window, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        self.game = DDOSGame(self)

        # Server Status Frame
        self.status_frame = tk.Frame(self.window, bg='lightgray', bd=5)
        self.status_frame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.2, anchor='n')
        self.status_label = tk.Label(self.status_frame, text="Server Status", font=("Helvetica", 16), bg='lightgray')
        self.status_label.pack(pady=5)
        self.server_status = tk.Label(self.status_frame, text="", font=("Helvetica", 14), bg='lightgray', fg="blue")
        self.server_status.pack()

        # Actions Frame
        self.actions_frame = tk.Frame(self.window, bg='lightgray', bd=5)
        self.actions_frame.place(relx=0.5, rely=0.35, relwidth=0.8, relheight=0.5, anchor='n')

        # Attack Options
        self.attack_label = tk.Label(self.actions_frame, text="Attack Options", font=("Helvetica", 16), bg='lightgray')
        self.attack_label.grid(row=0, column=0, padx=20)
        self.attack_buttons = []
        for i, attack in enumerate(self.game.attacks):
            btn = tk.Button(self.actions_frame, text=attack.name, font=("Helvetica", 14), command=lambda i=i: self.game.attack(i))
            btn.grid(row=i + 1, column=0, pady=5, padx=10)
            self.attack_buttons.append(btn)

        # Defense Options
        self.defense_label = tk.Label(self.actions_frame, text="Defense Options", font=("Helvetica", 16), bg='lightgray')
        self.defense_label.grid(row=0, column=1, padx=20)
        self.defense_buttons = []
        for i, defense in enumerate(self.game.defenses):
            btn = tk.Button(self.actions_frame, text=defense.name, font=("Helvetica", 14), command=lambda i=i: self.game.defend(i))
            btn.grid(row=i + 1, column=1, pady=5, padx=10)
            self.defense_buttons.append(btn)

        # Canvas for Attack Visualizations
        self.canvas = tk.Canvas(self.window, bg='white', bd=5)
        self.canvas.place(relx=0.5, rely=0.85, relwidth=0.8, relheight=0.2, anchor='n')

        self.game.start()

    def update_server_status(self, status):
        self.server_status.config(text=status)

    def display_attack_visual(self, attack_name):
        self.canvas.delete("all")
        if attack_name == "SYN Flood":
            for i in range(50):
                x1, y1 = random.randint(0, 800), random.randint(0, 100)
                x2, y2 = x1 + random.randint(10, 20), y1 + random.randint(10, 20)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='red')
        elif attack_name == "HTTP Flood":
            for i in range(10):
                x1, y1 = random.randint(0, 800), random.randint(0, 100)
                x2, y2 = x1 + random.randint(50, 100), y1 + random.randint(10, 20)
                self.canvas.create_oval(x1, y1, x2, y2, fill='blue')
        elif attack_name == "UDP Flood":
            for i in range(30):
                x = random.randint(0, 800)
                y = random.randint(0, 100)
                self.canvas.create_text(x, y, text='UDP', fill='green', font=("Helvetica", 14))

# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    ui = DDOSGameUI(root)
    root.mainloop()



    # Split the data into three categories.
train_images = data_generator.flow_from_dataframe(
    dataframe=train_df,
    x_col='Filepath',
    y_col='Label',
    target_size=(224, 224),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=32,
    shuffle=True,
    seed=42
)

#validation
val_images = data_generator.flow_from_dataframe(
    dataframe=valid_df,
    x_col='Filepath',
    y_col='Label',
    target_size=(224, 224),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=32,
    shuffle=True,
    seed=42
)
#testing
test_images = data_generator.flow_from_dataframe(
    dataframe=test_df,
    x_col='Filepath',
    y_col='Label',
    target_size=(224, 224),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=32,
    shuffle=False
)