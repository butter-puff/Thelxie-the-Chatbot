import tkinter as tk
from tkinter import scrolledtext

class ChatbotGUI:
    def __init__(self, root, handle_query_callback):
        self.root = root
        self.root.title("Chatbot")
        self.handle_query = handle_query_callback

        # Set the color scheme
        self.root.configure(bg='#FFD1DC')
        self.text_color = '#800080'
        self.entry_color = '#FF69B4'
        self.button_color = '#FF1493'

        self.user_icon = tk.PhotoImage(file='user_icon.png').subsample(4, 4)
        self.bot_icon = tk.PhotoImage(file='bot_icon.png').subsample(4, 4)

        self.create_widgets()

    def create_widgets(self):

        heading_label = tk.Label(self.root, text="Thelxie", font=("Helvetica", 16, "bold"), bg='#FFD1DC', fg=self.text_color)
        heading_label.pack()

        subheading_label = tk.Label(self.root, text="Bot powered by Jannat Anees", font=("Helvetica", 10), bg='#FFD1DC', fg=self.text_color)
        subheading_label.pack()

        bot_icon_label = tk.Label(self.root, image=self.bot_icon, bg='#FFD1DC')
        bot_icon_label.pack(pady=10)

        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=20, bg='#FFD1DC', fg=self.text_color)
        self.chat_display.pack(padx=10, pady=10)

        welcome_message = "Chirp Chirp. This is Thelxie, a bot powered by Jannat Anees. I will find you the best possible phone! <3"
        self.chat_display.insert(tk.END, f"Thelxie: {welcome_message}\n", "bot")
        self.chat_display.tag_configure("bot", foreground=self.text_color)

        self.user_input = tk.Entry(self.root, width=40, bg=self.entry_color)
        self.user_input.pack(padx=10, pady=10)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message, bg=self.button_color)
        self.send_button.pack(padx=10, pady=10)

    def send_message(self):
        user_input_text = self.user_input.get()

        self.chat_display.image_create(tk.END, image=self.user_icon)
        self.chat_display.insert(tk.END, f"You: {user_input_text}\n", "user")
        self.chat_display.tag_configure("user", foreground=self.entry_color)

        bot_response = self.handle_query(user_input_text)

        self.chat_display.image_create(tk.END, image=self.bot_icon)
        self.chat_display.insert(tk.END, f"Thelxie: {bot_response}\n", "bot")
        self.chat_display.tag_configure("bot", foreground=self.text_color)

        self.user_input.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()

    chatbot_gui = ChatbotGUI(root, handle_query)

    root.mainloop()
