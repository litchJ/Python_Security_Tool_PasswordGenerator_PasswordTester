# Import lists for password generation and tkinter gui
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

# password checker with rating score 
def check_password(password):
    notes = []
    score = 0

    # checks to see if password is at least 8 characters long
    if len(password) >= 8:
        score += 1
    else:
        notes.append("Use at least 8 characters")

    # checks to see if it has lowercase letters
    if any(ch.islower() for ch in password):
        score += 1
    else:
        notes.append("Add a lowercase letter")

    # checks to see if it has uppercase letters
    if any(ch.isupper() for ch in password):
        score += 1
    else:
        notes.append("Add an uppercase letter")

    # checks for numbers
    if any(ch.isdigit() for ch in password):
        score += 1
    else:
        notes.append("Add a number")

    # checks for special characters
    if any(ch in string.punctuation for ch in password):
        score += 1
    else:
        notes.append("Add a special character or symbol")

    # return rating based on score calculation
    if score <= 2:
        return "weak", notes, score
    elif score <= 4:
        return "medium", notes, score
    else:
        return "strong", ["This is a strong password"], score
     
#adding label and a onscreen bar to change colours depending on score
def set_strength_style(result):
    #changing based on weak medium strong think red, orange, green
    if result == "strong":
        strength_label.config(fg="#15803d")
        style.configure("blue.Horizontal.TProgressbar", background="#15803d")
    elif result == "medium":
        strength_label.config(fg="#d97706")
        style.configure("blue.Horizontal.TProgressbar", background="#d97706")
    else:
        strength_label.config(fg="#dc2626")
        style.configure("blue.Horizontal.TProgressbar", background="#dc2626")

#check button clicking 
def run_checker():
    #gets the password entered by the user
    user_password = password_entry.get().strip()
    
    #add warning if the box is empty validation
    if user_password =="":
        messagebox.showwarning("Missing input", "please enter a password")
        return
    
    #Cehcks password strength against score
    result, notes, score = check_password(user_password)
    
    #updates the label and bar for results
    strength_text.set(f"strength: {result}")
    set_strength_style(result)
    strength_bar["value"] = (score / 5) * 100
    
    #display feedback notes in a text box
    feedback_box.config(state="normal")
    feedback_box.delete("1.0", tk.END)
    
    for line in notes:
        feedback_box.insert(tk.END, "• " + line + "\n")

    feedback_box.config(state="disabled")

# the password generator and variables 
def make_password():
    #try pull length from spinbox
    try:
        length = int(length_box.get())
    except ValueError:
        messagebox.showerror("invalid length", "enter a valid length")
        return
    
    #read the options selected 
    use_lower = lower_var.get()
    use_upper = upper_var.get()
    use_numbers = number_var.get()
    use_symbols = symbol_var.get()
    
    chosen_chars = []
    char_pool = ""
    
    #added lowercase letters when selected
    if use_lower:
        chosen_chars.append(string.ascii_lowercase)
        char_pool += string.ascii_lowercase
    
    #adding uppercase letters wehn selected
    if use_upper:
        chosen_chars.append(string.ascii_uppercase)
        char_pool += string.ascii_uppercase
    
    #adding numbers when selected
    if use_numbers:
        chosen_chars.append(string.digits)
        char_pool += string.digits
    
    #adding symbols when selected
    if use_symbols:
        chosen_chars.append(string.punctuation)
        char_pool += string.punctuation
    
    # adding validation for when no char tpye selected
    if not chosen_chars:
        messagebox.showwarning("no options selected", "tick at least one character type")
        return
    
    #password length validation to include a char type
    if length < len(chosen_chars):
        messagebox.showwarning(
            "length too short", 
            "length must be at least the same number of chracter types selected"
        )
        return
    
    password_list = []
    
    #adding one from each selected type first
    for group in chosen_chars:
        password_list.append(random.choice(group))
    
    #fill out rest from pool of chars
    for _ in range(length - len(chosen_chars)):
        password_list.append(random.choice(char_pool))

    #shuffle randomly so chars arent in smae positions 
    random.shuffle(password_list)
    
    #convert the list into final string for password
    final_password = "".join(password_list)
    generated_text.set(final_password)
    status_text.set("password generated")
    
# copy to clipboard function
def copy_password():
    #pull generated pass
    password = generated_text.get()
    
    #if no password to copy throw warning
    if password == "":
        messagebox.showwarning("nothing to copy", "generate a password first")
        return

    #copy password to clipboard 
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()
    status_text.set("password copied to clipboard")
    
# Clear and reset functions
def clear_all():
    #clear the checker input
    password_entry.delete(0, tk.END)
    
    #reset label and bar after clear
    strength_text.set("strength")
    strength_label.config(fg="#0f172a")
    strength_bar["value"] = 0
    
    #clearing feedback box
    feedback_box.config(state="normal")
    feedback_box.delete("1.0", tk.END)
    feedback_box.config(state="disabled")
    
    #clear a generated password
    generated_text.set("")
    status_text.set("")
    
    #reset password length to default as 12
    length_box.delete(0, tk.END)
    length_box.insert(0,"12")
    
    #enable all character type options on reset
    lower_var.set(True)
    upper_var.set(True)
    number_var.set(True)
    symbol_var.set(True)
    
    #hide entered password again by default
    show_var.set(False)
    password_entry.config(show="*")
    
#enables showor hide password toggle in box function 
def toggle_password():
    #if chckbox is ticked show the password
    if show_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

#Main window setup  don't mess with this unless resizing default --- will break everything again
root = tk.Tk()
root.title("password generator & checker")
root.geometry("820x920")
root.minsize(720,780)
root.resizable(True, True)
root.configure(bg="#eaf4ff")


#attempted colour settings may change later on 
app_bg = "#eaf4ff"
panel_bg = "#f8fbff"
dark_text = "#0f172a"
muted_text = "#475569"
title_blue = "#1e3a8a"
main_blue = "#2563eb"
button_blue = "#3b82f6"
white = "#ffffff"

# progress bar styling 
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "blue.Horizontal.TProgressbar",
    troughcolor="#dbeafe",
    background=main_blue
)

# font settings 
title_font = ("Arial", 16, "bold")
head_font = ("Arial", 11, "bold")
normal_font = ("Arial", 10)
button_font = ("Arial", 10, "bold")

# main frame
main_frame = tk.Frame(root, bg=app_bg, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# title
title = tk.Label(
    main_frame,
    text="password generator & checker",
    font=title_font,
    bg=app_bg,
    fg=dark_text
)
title.pack(pady=(0, 10))

# Checker section basic frames with groove 
# frame for password tester title
checker_frame = tk.LabelFrame(
    main_frame,
    text="pasword stregnth tester",
    font=head_font,
    bg=panel_bg,
    fg=title_blue,
    padx=15,
    pady=15,
    bd=2,
    relief="groove"
)
checker_frame.pack(fill="x", pady=(0, 20))

checker_info = tk.Label(
    checker_frame,
    text="test how secure your password is",
    font=normal_font,
    bg=panel_bg,
    fg=muted_text
)
checker_info.pack(anchor="w", pady=(0, 10))

password_label = tk.Label(
    checker_frame,
    text="enter password:",
    font=normal_font,
    bg=panel_bg,
    fg=dark_text
)
password_label.pack(anchor="w")

#input password area

password_entry = tk.Entry(
    checker_frame,
    font=normal_font,
    width=50,
    relief="solid",
    bd=1,
    bg=white,
    fg=dark_text,
    insertbackground=dark_text,
    show="*"
)
password_entry.pack(fill="x", pady=(5, 8))

show_var = tk.BooleanVar(value=False)

show_check = tk.Checkbutton(
    checker_frame,
    text="show password",
    variable=show_var,
    command=toggle_password,
    font=normal_font,
    bg=panel_bg,
    fg=dark_text,
    activebackground=panel_bg,
    selectcolor=panel_bg
)
show_check.pack(anchor="w", pady=(0, 10))

# create a small frame inside the checker section
checker_buttons = tk.Frame(checker_frame, bg=panel_bg)
checker_buttons.pack(fill="x", pady=(0, 10))

# creates check button, clicks and runs the checker function from earlier 
check_btn = tk.Button(
    checker_buttons,
    text="Check strength",      
    command=run_checker,   
    # styling for buttons       
    font=button_font,              
    bg=main_blue,                   
    fg=white,                       
    activebackground="#1d4ed8",     
    activeforeground=white,         
    padx=12,                        
    pady=6,                         
    relief="flat"                   
)
# ensure button is on the left of frame
check_btn.pack(side="left", padx=(0, 10))
# creates clear and reset button, calls clear function from earlier 
clear_btn = tk.Button(
    checker_buttons,
    text="clear/reset",             
    command=clear_all,  
    # styling for clear button          
    font=button_font,               
    bg=button_blue,                 
    fg=white,                       
    activebackground=main_blue,     
    activeforeground=white,         
    padx=12,                        
    pady=6,                         
    relief="flat"                   
)
# places the button next to check 
clear_btn.pack(side="left")

#uses stringvar to store text, lets label update automatically
strength_text = tk.StringVar(value="strength: ")

#creates label to show strength of password, uses values set earlier
strength_label = tk.Label(
    checker_frame,
    textvariable=strength_text,
    #styling crap     
    font=("Arial", 12, ""),         
    bg=panel_bg,                    
    fg=dark_text                    
)

#makes sure the label is below button
strength_label.pack(anchor="w", pady=(0, 8))

#makes progress bar show pass strength, fills up from 0 - 100 from score
strength_bar = ttk.Progressbar(
    checker_frame,
    style="blue.Horizontal.TProgressbar",# calls the custom style made earlier
    orient="horizontal",  # makes the bar go left to right
    mode="determinate",   # makes bar fill to a specific value
    maximum=100   # makes the bar full at 100
)
# makes the bar stretch across the section, looks cleaneer
strength_bar.pack(fill="x", pady=(0, 12))

# feedback box label ontop
feedback_label = tk.Label(
    checker_frame,
    text="feedback:",
    font=normal_font,
    bg=panel_bg,
    fg=dark_text
)
feedback_label.pack(anchor="w")

#feedback box, showing previous made suggestions
feedback_box = tk.Text(
    checker_frame,
    #styling for box --
    height=6,                       
    wrap="word",                    
    font=normal_font,
    bg=white,                       
    fg=dark_text,                   
    relief="solid",                 
    bd=1,                           
    insertbackground=dark_text      
)
# fills area of section 
feedback_box.pack(fill="x")

#makes sure user cant type in feedback box
feedback_box.config(state="disabled")

# password generator section
# creating labelframe same as before
generator_frame = tk.LabelFrame(
    main_frame,
    text="password generator",      
    font=head_font,                 
    bg=panel_bg,                    
    fg=title_blue,                  
    padx=15,                        
    pady=15,                        
    bd=2,                           
    relief="groove"                 
)

#stretches frame to fill area
generator_frame.pack(fill="x")

#secondary title and description for use
generator_info = tk.Label(
    generator_frame,
    text="choose legnth of password and characters",
    font=normal_font,
    bg=panel_bg,
    fg=muted_text
)
generator_info.pack(anchor="w", pady=(0, 10))

#labels password length setting
length_label = tk.Label(
    generator_frame,
    text="password length:",
    font=normal_font,
    bg=panel_bg,
    fg=dark_text
)
length_label.pack(anchor="w")

#uses spinbox to let user pick length using arrows or typing
length_box = tk.Spinbox(
    generator_frame,
    from_=4,  #min pass length
    to=64,   #max pass length
    width=10,    #styling
    font=normal_font,
    bg=white,
    fg=dark_text,
    insertbackground=dark_text,   
    relief="solid",
    bd=1
)

#clears box
length_box.delete(0, tk.END)


#sets default to 12 length
length_box.insert(0, "12")

#forces spinbox in gen section
length_box.pack(anchor="w", pady=(5, 12))

#checkbox section with label and options
options_label = tk.Label(
    generator_frame,
    text="characters to include:",
    font=normal_font,
    bg=panel_bg,
    fg=dark_text
)
options_label.pack(anchor="w")

#frame for checkboxes
options_frame = tk.Frame(generator_frame, bg=panel_bg)
options_frame.pack(fill="x", pady=(8, 12))

#creates booleanvar for checkboxes, true is checked
lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
number_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)

#checkbox for lowercase
lower_check = tk.Checkbutton(
    options_frame,
    text="lowercase",               
    variable=lower_var,             
    font=normal_font,
    bg=panel_bg,
    fg=dark_text,
    activebackground=panel_bg,
    selectcolor=panel_bg
)
#makes checkbox in a grid
lower_check.grid(row=0, column=0, sticky="w", padx=5, pady=5)

#checkbox for uppercase
upper_check = tk.Checkbutton(
    options_frame,
    text="UPPERCASE",
    variable=upper_var,
    font=normal_font,
    #styling box
    bg=panel_bg,
    fg=dark_text,
    activebackground=panel_bg,
    selectcolor=panel_bg
)
upper_check.grid(row=0, column=1, sticky="w", padx=5, pady=5)

#checkbox for numbers
number_check = tk.Checkbutton(
    options_frame,
    text="numbers",
    variable=number_var,
    #styling bs
    font=normal_font,
    bg=panel_bg,
    fg=dark_text,
    activebackground=panel_bg,
    selectcolor=panel_bg
)
number_check.grid(row=1, column=0, sticky="w", padx=5, pady=5)

#checkbox for the symbols
symbol_check = tk.Checkbutton(
    options_frame,
    text="symbols",
    variable=symbol_var,
    #styling bs
    font=normal_font,
    bg=panel_bg,
    fg=dark_text,
    activebackground=panel_bg,
    selectcolor=panel_bg
)
symbol_check.grid(row=1, column=1, sticky="w", padx=5, pady=5)

#frames for buttons
generator_buttons = tk.Frame(generator_frame, bg=panel_bg)
generator_buttons.pack(fill="x", pady=(0, 12))

#generate button, calls function
generate_btn = tk.Button(
    generator_buttons,
    text="generate",
    command=make_password, # called function on press
    font=button_font,
    bg=main_blue,
    fg=white,
    activebackground="#1d4ed8",
    activeforeground=white,
    padx=12,
    pady=6,
    relief="flat"
)
#puts button left
generate_btn.pack(side="left", padx=(0, 10))

#copy button calls function
copy_btn = tk.Button(
    generator_buttons,
    text="copy",
    command=copy_password, # called function on press
    font=button_font,
    bg=button_blue,
    fg=white,
    activebackground=main_blue,
    activeforeground=white,
    padx=12,
    pady=6,
    relief="flat"
)
#placement next to button
copy_btn.pack(side="left")

#label for output box
generated_label = tk.Label(
    generator_frame,
    text="generated password:",
    font=normal_font,
    bg=panel_bg,
    fg=dark_text
)
generated_label.pack(anchor="w")


#creatstringvar 
generated_text = tk.StringVar()

#creates entry boxd
generated_entry = tk.Entry(
    generator_frame,
    textvariable=generated_text,
    font=normal_font,
    width=50,
    relief="solid",
    bd=1,
    bg=white,
    fg=dark_text,
    insertbackground=dark_text
)
#stretching to width again
generated_entry.pack(fill="x", pady=(5, 8))

#creates stringvar for status message 
status_text = tk.StringVar(value="")

#label to display status
status_label = tk.Label(
    generator_frame,
    textvariable=status_text,#forces auto update on change
    font=normal_font,
    bg=panel_bg,
    fg=muted_text
)
status_label.pack(anchor="w")

#starts tkinter loop
#dont remove this ever, app will not open
root.mainloop()