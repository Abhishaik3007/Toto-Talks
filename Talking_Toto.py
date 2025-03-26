from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
import customtkinter as ctk
from PIL import Image
import threading
import sys
import os

# Model and prompt template
template = """
Your name is Toto a character Monkey and u are my AI 
Although u dont have to behave like a monkey too much feels not ok
You have to answer the question below
Here is the conversation history: {context}

Question: {question}
o
Answer:
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Function to resolve resource paths
def resource_path(relative_path):
    try:
        
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# SlidePanel class for animated navbar
class SlidePanel(ctk.CTkFrame):
    def __init__(self, parent, start_pos, end_pos, button_height, bg_color, app_instance):
        super().__init__(master=parent, fg_color=bg_color)

        self.app_instance = app_instance

        # General attributes
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = abs(start_pos - end_pos)
        self.button_height = button_height
        
        # Store colors
        self.configure(bg_color=bg_color, fg_color='#fff')

        # Animation logic
        self.pos = self.start_pos
        self.in_start_pos = True

        # Adjusted vertical position
        self.place(relx=self.start_pos, rely=0.2 - (button_height/parent.winfo_height()), relwidth=self.width, relheight=0.33)
        self.lift()

        # Inner frame for customization
        self.inner_frame = ctk.CTkFrame(self, fg_color='#6e768c', bg_color=bg_color, corner_radius=10)
        self.inner_frame.pack()

        # Example widgets inside the panel
        ctk.CTkButton(self.inner_frame, text='', border_color='#000', border_width=1.2, 
                       fg_color='#9b5de5', hover_color='#B07FEA', command=lambda: self.app_instance.change_theme('violet')).pack(padx=15, pady=(8,5))
        ctk.CTkButton(self.inner_frame, text='', border_color='#000', border_width=1.2, 
                       fg_color='#137547', hover_color='#054a29', command=lambda: self.app_instance.change_theme('green')).pack(padx=15, pady=5)
        ctk.CTkButton(self.inner_frame, text='', border_color='#000', border_width=1.2, 
                       fg_color='#5289c0', hover_color='#2b5379', command=lambda: self.app_instance.change_theme('blue')).pack(padx=15, pady=5)
        ctk.CTkButton(self.inner_frame, text='', border_color='#000', border_width=1.2, 
                       fg_color='#25a18e', hover_color='#56ab91', command=lambda: self.app_instance.change_theme('dayGreen')).pack(padx=15, pady=5)
        ctk.CTkButton(self.inner_frame, text='', border_color='#000', border_width=1.2, 
                       fg_color='#00b4d8', hover_color='#6096ba', command=lambda: self.app_instance.change_theme('dayBlue')).pack(padx=15, pady=5)
        ctk.CTkButton(self.inner_frame, text='', border_color='#000', border_width=1.2, 
                      fg_color='#f6efe2', hover_color='#454955', command=lambda: self.app_instance.change_theme('dayNight')).pack(padx=15, pady=5)
        ctk.CTkButton(self.inner_frame, text='Home', border_color='#000', border_width=1.2, 
                       fg_color='#9b5de5', hover_color='#B07FEA',).pack(padx=15, pady=5)

    def animate(self):
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos < self.end_pos:
            self.pos += 0.01  # Adjust speed here
            self.place(relx=self.pos+0.02, rely=0.23 - (self.button_height/self.winfo_height()), relwidth=self.width, relheight=0.33)
            self.lift()
            self.after(10, self.animate_forward)
            self.update()
            self.update_idletasks()
        else:
            self.in_start_pos = False
            self.lift()

    def animate_backwards(self):
        if self.pos > self.start_pos:
            self.pos -= 0.01  # Adjust speed here
            self.place(relx=self.pos-0.02, rely=0.23 - (self.button_height/self.winfo_height()), relwidth=self.width, relheight=0.33)
            self.lift()
            self.after(10, self.animate_backwards)
            self.update()
            self.update_idletasks()
        else:
            self.in_start_pos = True
            self.lift()

#FIXME: also day theme toto icons??
#TODO: smtg to make it look like toto is typing and all uk

# Main application class
class Toto_Talks(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Toto Talks")
        self.geometry("400x700")
        self.minsize(400, 700)
        # self.resizable(False, False)
        self.Font = ctk.CTkFont(family="Cascadia Code", size=25)
        self.Foont = ctk.CTkFont(family="Cascadia Code", size=35)
        
        self.config(background='#0e1621')

        self.icon = resource_path('./toto_Talks/feeling.ico')
        self.iconbitmap(self.icon)
        
        self.bg = '#0e1621'
        self.box_bg = '#17212b'
        self.user_bg = '#2c7da0'
        self.toto_bg = '#012a4a'
        self.butt = '#014f86'
        self.butt_hov = '#2b5379'

        self.context = ""
        
        # Store references to message labels
        self.user_message_labels = []
        self.toto_message_labels = []

        # Font Family
        self.font = ctk.CTkFont(family="Cascadia Code", size=14)
        self.text_color = '#fff'
        
        self.purple = resource_path('./toto_Talks/purple.png')
        self.purple_icon = ctk.CTkImage(light_image=Image.open(os.path.join(self.purple)), size=(30, 30))
        self.green = resource_path('./toto_Talks/green.png')
        self.green_icon = ctk.CTkImage(light_image=Image.open(os.path.join(self.green)), size=(30, 30))
        self.blue = resource_path('./toto_Talks/blue.png')
        self.blue_icon = ctk.CTkImage(light_image=Image.open(os.path.join(self.blue)), size=(30, 30))
        self.dayGreen = resource_path('./toto_Talks/dayGreen.png')
        self.dayGreen_icon = ctk.CTkImage(light_image=Image.open(os.path.join(self.dayGreen)), size=(30, 30))
        self.dayBlue = resource_path('./toto_Talks/dayBlue.png')
        self.dayBlue_icon = ctk.CTkImage(light_image=Image.open(os.path.join(self.dayBlue)), size=(30, 30))
        self.dayNight = resource_path('./toto_Talks/dayNight.png')
        self.dayNight_icon = ctk.CTkImage(light_image=Image.open(os.path.join(self.dayNight)), size=(30, 30))

        self.bind('<Return>', lambda event: self.send_message())
        self.bind('<Escape>', lambda event: self.quit())

        # Inside Toto_Talks __init__ method
        # Load the background image
        image_path = "./toto_Talks/Toto_Talks.jpg"  # Replace with the path to your image
        image = Image.open(image_path)
        resized_image = image.resize((400, 700), Image.Resampling.LANCZOS)  # Resize the image to fit the window
        self.bg_image = ctk.CTkImage(light_image=resized_image, dark_image=resized_image, size=(400, 700))
        
        self.create_Home()

    def create_Home(self):
        # Create a label to display the background image
        self.bg_label = ctk.CTkLabel(self,text='', image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)  # Fill the entire window
        # self.animated_panel = SlidePanel(self, start_pos=-0.3, end_pos=0, button_height=40, bg_color=self.bg, app_instance=self)
        
        self.butt_frame = ctk.CTkFrame(self,bg_color="#f6efe2", fg_color="#f6efe2")
        self.start_button = ctk.CTkButton(self.butt_frame,width = 160 ,text="Start", fg_color='#523b19', text_color="#f6efe2",font = self.Font, bg_color='#f6efe2', hover_color='#6d5022', command=self.ready_ChatArea)
        self.start_button.pack(pady = 10)
        
        self.themes_button = ctk.CTkButton(self.butt_frame,width = 160, text="Themes", fg_color='#523b19', text_color="#f6efe2",font = self.Font, bg_color='#f6efe2', hover_color='#6d5022', command=self.ready_themePage)
        self.themes_button.pack(pady = 10)
        
        self.tata_button = ctk.CTkButton(self.butt_frame,width = 160, text="Tata...", fg_color='#523b19', text_color="#f6efe2",font = self.Font, bg_color='#f6efe2', hover_color='#6d5022', command=self.quit)
        self.tata_button.pack(pady = 10)
        
        self.butt_frame.pack(side = 'bottom', pady = 60)
    
    def ready_ChatArea(self):
        self.butt_frame.destroy()
        self.bg_label.destroy()
        self.create_ChatArea()
    
    def create_ChatArea(self):
        # Inside Toto_Talks __init__ method
        # self.animated_panel = SlidePanel(self, start_pos=-0.3, end_pos=0, button_height=40, bg_color=self.bg, app_instance=self)

        # Create the chat area
        self.chat_area = ctk.CTkScrollableFrame(self, fg_color=self.bg, bg_color=self.bg, scrollbar_button_color=self.bg, scrollbar_button_hover_color=self.bg)
        self.chat_area.pack(padx=0, pady=0, fill='both', expand=True)

        # Create a frame for the entry and send button
        self.entry_frame = ctk.CTkFrame(self, fg_color=self.bg, bg_color=self.bg)
        self.entry_frame.pack(padx=5, pady=(0, 5), fill='both', ipadx=5, ipady=5)

        # Create the message entry box
        self.message_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Talk to me...", placeholder_text_color=self.text_color, font=self.font, fg_color=self.box_bg, bg_color=self.bg, height=35)
        self.message_entry.pack(side='left', padx=2, fill='x', expand=True)

        # Create the send button
        self.send_button = ctk.CTkButton(self.entry_frame, text="Send", font=self.font, text_color='#fff', fg_color=self.butt, hover_color=self.butt_hov, bg_color=self.bg, command=self.send_message, height=36, width=100)
        self.send_button.pack(side='right', padx=2)
        
        # self.theme_button = ctk.CTkButton(self, image=self.blue_icon, text='', width=32,fg_color=self.bg, bg_color=self.bg, hover_color=self.bg, command=self.toggle_navbar)
        # self.theme_button.place(x=2, y=2)
        
        self.chat_home_button = ctk.CTkButton(self, image=self.blue_icon, text='', width=32,fg_color=self.bg, bg_color=self.bg, hover_color=self.bg, command=self.home_from_chat)
        self.chat_home_button.place(x=0.5, y=2)

    def home_from_chat(self):
        self.message_entry.destroy()
        self.send_button.destroy()
        self.entry_frame.destroy()
        self.chat_home_button.destroy()
        self.chat_area.destroy()
        self.create_Home()

    def ready_themePage(self):
        self.butt_frame.destroy()
        self.bg_label.destroy()
        self.create_themePage()
    
    def create_themePage(self):
        self.Head = ctk.CTkLabel(self, text="Toto Color UP!!!",fg_color="#f6efe2", font=self.Foont, text_color='#523b19', bg_color= self.bg,corner_radius=10)
        self.Head.pack(pady=30)
        
        self.Tframe = ctk.CTkFrame(self, fg_color="#f6efe2", bg_color=self.bg)
        # Create rounded corners using CTkFrame, arranged in a 2x4 grid
        self.t1_frame = ctk.CTkButton(self.Tframe, text='Cosmic \nBloom',bg_color="#f6efe2", font=self.Font, height=25, corner_radius=10,text_color='#fff',
                                      fg_color='#9b5de5', hover_color='#B07FEA', command=lambda: self.change_theme('violet'))
        self.t1_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
        self.t2_frame = ctk.CTkButton(self.Tframe, text='Forest \nGlow',bg_color="#f6efe2", font=self.Font, height=25, corner_radius=10,text_color='#fff',
                                       fg_color='#137547', hover_color='#054a29', command=lambda: self.change_theme('green'))
        self.t2_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.t3_frame = ctk.CTkButton(self.Tframe, text='Arctic \nVeil',bg_color="#f6efe2", font=self.Font, height=25, corner_radius=10,text_color='#fff',
                                       fg_color='#5289c0', hover_color='#2b5379', command=lambda: self.change_theme('blue'))
        self.t3_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
        self.t4_frame = ctk.CTkButton(self.Tframe, text='Mint \nDaylight',bg_color="#f6efe2", font=self.Font, height=25, corner_radius=10,text_color='#fff',
                                       fg_color='#25a18e', hover_color='#56ab91', command=lambda: self.change_theme('dayGreen'))
        self.t4_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.t5_frame = ctk.CTkButton(self.Tframe, text='Sky \nSurge',bg_color="#f6efe2", font=self.Font, height=25, corner_radius=10,text_color='#fff',
                                       fg_color='#00b4d8', hover_color='#6096ba', command=lambda: self.change_theme('dayBlue'))
        self.t5_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    
        self.t6_frame = ctk.CTkButton(self.Tframe, text='Obsidian \nLight',bg_color="#f6efe2", font=self.Font, height=25, corner_radius=10,text_color='#fff',
                                       fg_color='#454955', hover_color='#3a3e49', command=lambda: self.change_theme('dayNight'))
        self.t6_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        self.Tframe.grid_rowconfigure(0, weight=1)
        self.Tframe.grid_rowconfigure(1, weight=1)
        self.Tframe.grid_rowconfigure(2, weight=1)
        self.Tframe.grid_columnconfigure(0, weight=1)
        self.Tframe.grid_columnconfigure(1, weight=1)
        
        self.Tframe.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.Home_button = ctk.CTkButton(self,width = 160 ,text="Home", fg_color='#523b19', text_color="#f6efe2",font = self.Font, bg_color=self.bg, hover_color='#6d5022', command=self.go_Home)
        self.Home_button.pack(pady = 40)

    def go_Home(self):
        self.Head.destroy()
        self.Tframe.destroy()
        self.Home_button.destroy()
        self.create_Home()

    def change_theme(self, theme):
        # Define the theme colors
        if theme == 'violet':
            self.img = self.purple_icon
            self.bg = '#0F0D1C'
            self.box_bg = '#231A2F'
            self.user_bg = '#9b5de5'
            self.toto_bg = '#3A2B61'
            self.butt = '#9b5de5'
            self.butt_hov = '#B07FEA'
            self.font = ctk.CTkFont(family="Cascadia Code", size=14)
        elif theme == 'green':
            self.img = self.green_icon
            self.text_color='#fff'
            self.bg = '#0B120A'
            self.box_bg = '#0d2818'
            self.user_bg = '#5e8d5b'
            self.toto_bg = '#2a4526'
            self.butt = '#5e8d5b'
            self.butt_hov = '#2a4526'
            self.font = ctk.CTkFont(family="Courier New", size=14, weight='bold')
        elif theme == 'blue':
            self.img = self.blue_icon
            self.img= self.blue_icon
            self.text_color='#fff'
            self.bg = '#0e1621'
            self.box_bg = '#17212b'
            self.user_bg = '#2c7da0'
            self.toto_bg = '#012a4a'
            self.butt = '#014f86'
            self.butt_hov = '#2b5379'
            self.font = ctk.CTkFont(family="Cascadia Code", size=14)
        elif theme == 'dayGreen':
            self.img = self.dayGreen_icon
            self.text_color='#fff'
            self.bg = '#CEEFD0'
            self.box_bg = '#2d6a4f'
            self.user_bg = '#25a18e'
            self.toto_bg = '#4D9078'
            self.butt = '#25a18e'
            self.butt_hov = '#45B4A3'
            self.font = ctk.CTkFont(family="Courier New", size=14, weight='bold')
        elif theme == 'dayBlue':
            self.img = self.dayBlue_icon
            self.text_color='#fff'
            self.bg = '#cae9ff'
            self.box_bg = '#6096ba'
            self.user_bg = '#1b4965'
            self.toto_bg = '#6096ba'
            self.butt = '#274c77'
            self.butt_hov = '#1b4965'
            self.font = ctk.CTkFont(family="Courier New", size=14, weight='bold')
        elif theme == 'dayNight':
            self.img = self.dayNight_icon
            self.text_color='#fff'
            self.bg = '#fefae0'
            self.box_bg = '#4a5759'
            self.user_bg = '#161616'
            self.toto_bg = '#4a5759'
            self.butt = '#000'
            self.butt_hov = '#161616'
            self.font = ctk.CTkFont(family="Cascadia Code", size=14)
    
        # Apply the changes to the UI components
        self.configure(bg_color=self.bg, fg_color=self.bg)  # Update the background color of the main window
        self.chat_area.configure(fg_color=self.bg, scrollbar_button_color=self.bg, scrollbar_button_hover_color=self.bg)  # Update chat area
        self.entry_frame.configure(fg_color=self.bg)  # Update the entry frame
        self.message_entry.configure(fg_color=self.box_bg, font=self.font, text_color=self.text_color, placeholder_text_color=self.text_color)  # Update the message entry
        self.send_button.configure(fg_color=self.butt, hover_color=self.butt_hov, font=self.font, text_color=self.text_color)  # Update the send button
        self.animated_panel.configure(fg_color=self.bg)  # Update the animated panel
        self.theme_button.configure(image=self.img, fg_color=self.bg, bg_color=self.bg, hover_color=self.bg)  # Update the theme button
        self.Tframe.configure(fg_color=self.bg, bg_color=self.bg)
        self.t1_frame.configure(bg_color=self.bg)
        self.t2_frame.configure(bg_color=self.bg)
        self.t3_frame.configure(bg_color=self.bg)
        self.t4_frame.configure(bg_color=self.bg)
        self.t5_frame.configure(bg_color=self.bg)
        self.t6_frame.configure(bg_color=self.bg)

        # Update the colors of all user and Toto messages based on the current theme
        for label in self.user_message_labels:
            parent_frame = label.master
            parent_frame.configure(fg_color=self.bg)
            label.configure(bg_color=self.bg, fg_color=self.user_bg, font= self.font, text_color=self.text_color)
        for label in self.toto_message_labels:
            parent_frame = label.master
            parent_frame.configure(fg_color=self.bg)
            label.configure(bg_color=self.bg, fg_color=self.toto_bg, font= self.font, text_color=self.text_color)
        
        # Update the UI
        self.update()
        self.update_idletasks()

    def toggle_navbar(self):
        self.animated_panel.animate()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.show_user(f"{message}")
            self.message_entry.delete(0, 'end')
            self.chat_area.update_idletasks()

            threading.Thread(target=self.handle_convo, args=(message,)).start()
            self.chat_area.update_idletasks()

            self.chat_area._parent_canvas.yview_moveto(1)

    def handle_convo(self, message):
        result = chain.invoke({"context": self.context, "question": message})
        self.context += f"\nHuman: {message}\nToto: {result}"
        self.show_toto(result)

    def show_user(self, message):
        font = ctk.CTkFont(family="Cascadia Code", size=12)

        userPP_path = resource_path('./toto_Talks/angel.ico')
        userPP_width = 30
        userPP_height = 30

        self.user_text_body = ctk.CTkFrame(self.chat_area, fg_color=self.bg)
        self.user_text_body.pack(fill='x')

        user_PP = ctk.CTkImage(light_image=Image.open(os.path.join(userPP_path)), size=(userPP_width, userPP_height))
        user_pp = ctk.CTkLabel(self.user_text_body, image=user_PP, text='')
        user_pp.pack(side='right')

        user_text = ctk.CTkLabel(self.user_text_body, text=message, justify='right', font=self.font, bg_color=self.bg, text_color=self.text_color, fg_color=self.user_bg, corner_radius=5, anchor='e', wraplength=250)
        user_text.pack(side='right', padx=5, pady=5, ipadx=2, ipady=5, fill='x')
        
        # Store the label for future updates
        self.user_message_labels.append(user_text)
        # self.text_colors()

        self.chat_area.update_idletasks()
        self.chat_area._parent_canvas.yview_moveto(1)

    def show_toto(self, reply):
        font = ctk.CTkFont(family="Cascadia Code", size=12)

        totoPP_path = resource_path('./toto_Talks/happy.ico')
        totoPP_width = 30
        totoPP_height = 30

        self.toto_text_body = ctk.CTkFrame(self.chat_area, fg_color=self.bg)
        self.toto_text_body.pack(fill='x')

        toto_PP = ctk.CTkImage(light_image=Image.open(os.path.join(totoPP_path)), size=(totoPP_width, totoPP_height))
        toto_pp = ctk.CTkLabel(self.toto_text_body, image=toto_PP, text='')
        toto_pp.pack(side='left', padx=5)

        toto_text = ctk.CTkLabel(self.toto_text_body, text=reply, justify='left', font=self.font, bg_color=self.bg, text_color=self.text_color, fg_color=self.toto_bg, corner_radius=5, anchor='w', wraplength=250)
        toto_text.pack(side='left', pady=5, ipadx=2, ipady=5, fill='x')
        
        # Store the label for future updates
        self.toto_message_labels.append(toto_text)
        # self.text_colors()

        self.chat_area.update_idletasks()
        self.chat_area._parent_canvas.yview_moveto(1)

if __name__ == "__main__":
    app = Toto_Talks()
    app.mainloop()