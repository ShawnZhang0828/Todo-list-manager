from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkcalendar import Calendar
from Task import Task
import os.path

root = Tk()
root.title("To-Do List Manager")
root.iconbitmap('icon.ico')
root.geometry("370x520")

calendar_image = Image.open("calendar.jpg")
calendar_image = ImageTk.PhotoImage(calendar_image.resize((20,20)))

on_switch_image = ImageTk.PhotoImage(Image.open("switch_on.png").resize((54,27)))
off_switch_image = ImageTk.PhotoImage(Image.open("switch_off.png").resize((54,27)))

# Switch Between Main window and create_new_list/open_list/user_instruction windows
def create_new_list():
    create = True
    if os.path.isfile("ToDoList.txt"):
        response = messagebox.askyesno("File Existed","You have created a file, recreate a new one will overwrite the original one. Continue?")
        if response == 0:
            create = False
    if create == True:
        date_entry.delete(0, END)
        subject_entry_1.delete(0, END)
        subject_entry_2.delete(0, END)
        subject_entry_3.delete(0, END)
        main_frame.pack_forget()
        create_new_list_frame.pack()

def open_list():
    main_frame.pack_forget()
    try:
        open_list_frame.pack()
    except:
        response = messagebox.askyesno("File Not Exist", "You haven't create a file yet, create one now?")
        if response == 0:
            root.destroy()
        else:
            create_new_list()

def setting():
    main_frame.pack_forget()
    setting_frame.pack()

def switch(on, setting):
    # open the settings file to be modified
    with open("Settings.txt", "r") as f:
        lines = f.readlines()
        lines_copy = lines.copy()
        # iterate through every setting to find the one to be changed
        for i,line in enumerate(lines):
            if setting in line:
                # redraw the button with the opposite image, and modify the file
                if on:
                    status_button.config(image=off_switch_image, command=lambda: switch(False, setting))
                    lines_copy[i] = lines_copy[i].replace("On", "Off")
                else:
                    status_button.config(image=on_switch_image, command=lambda: switch(True, setting))
                    lines_copy[i] = lines_copy[i].replace("Off", "On")
    # overwrite the file with the updated setting
    with open("Settings.txt", "w") as f:
        for line in lines_copy:
            f.write(line)

# def user_instruction():
#     main_frame.pack_forget()
#     user_instruction_frame.pack()

def back_to_main(frame_name):
    if frame_name == create_new_list_frame:
        for i,(label, entry) in enumerate(subject_label_entry_list):
            if i >= 3:
                label.grid_forget()
                entry.grid_forget()
    frame_name.pack_forget()
    main_frame.pack()

# =======================Functions to select a date using Calendar==============
def creation_date_confirm(calendar, window):
    global date_entry
    date_entry.delete(0, END)
    date_entry.insert(0, calendar.get_date())

    window.destroy()

def add_tasks_date_confirm():
    global add_tasks_date_entry

def select_date():
    # Pop a new window to select date
    select_date_window = Toplevel()
    select_date_window.title("Select Date")
    select_date_window.iconbitmap('icon.ico')
    select_date_window.geometry("290x260")

    # Create the calendar
    cal = Calendar(select_date_window, selectmode='day', year=2020, month=5, day=22)
    cal.pack(pady=(20,0))

    # Create confirm button
    confirm_date_button = Button(select_date_window, text="Select", command=lambda: creation_date_confirm(cal, select_date_window))
    confirm_date_button.pack(pady=(30,0))

# =================Functions for create_new_list window=========================
def submit_new_list():
    f = open("ToDoList.txt", "w")
    f.write("Date: "+date_entry.get()+'\n')
    for label, entry in subject_label_entry_list:
        f.write(entry.get()+': None(+)\n')
    f.close()

    response = messagebox.showinfo("File Created", "You have created the new file. Restart to use the app.")
    if response == "ok":
        root.destroy()

# Add a new subject to create_new_list_frame
def add_subject():
    global subject_num
    global submit_new_list_button
    global another_subject_button
    global create_new_list_back_button

    subject_num += 1

    # Get rid of the buttons created before since they are in a new position (new subjects are added)
    submit_new_list_button.grid_forget()
    another_subject_button.grid_forget()
    create_new_list_back_button.grid_forget()

    # Create the subject label and the entry according the current subject number
    subject_label = Label(create_new_list_frame, text=f"Subject {subject_num}: ", font=("Calibri", 14))
    subject_label.grid(row=subject_num+1, column=0, padx=(10,14))
    subject_entry = Entry(create_new_list_frame, width=32)
    subject_entry.grid(row=subject_num+1, column=1)
    subject_label_entry_list.append((subject_label, subject_entry))

    # Create new submit, another subject, and create new list buttons in the new position
    submit_new_list_button = Button(create_new_list_frame, text="Submit", command=submit_new_list, font=("Calibri", 14))
    submit_new_list_button.grid(row=subject_num+2, column=0, pady=(30,0))

    another_subject_button = Button(create_new_list_frame, text="Add a subject", command=add_subject, font=("Calibri", 14))
    another_subject_button.grid(row=subject_num+2, column=1, pady=(30,0))

    create_new_list_back_button = Button(create_new_list_frame, text="Back", command=lambda: back_to_main(create_new_list_frame), font=("Calibri", 14))
    create_new_list_back_button.grid(row=subject_num+3, column=1, padx=(30,0), pady=(20, 10))

# ========================Functions for Read_only frame=========================
def read_all_tasks():
    read_all_tasks_window = Toplevel()
    read_all_tasks_window.title("Read Tasks")
    read_all_tasks_window.iconbitmap('icon.ico')
    read_all_tasks_window.geometry("370x480")

    # Create a frame in read all tasks window

    read_all_tasks_filter_frame = LabelFrame(read_all_tasks_window, borderwidth=0)

    # Add filter options
    date_selection = StringVar()
    date_list = Task.find_date("ToDoList.txt")
    date_list.append("All")
    # Create a drop down menu to select different date
    date_filter_dropdown = OptionMenu(read_all_tasks_filter_frame, date_selection, *date_list)
    date_selection.set(date_list[-1])
    date_filter_dropdown.grid(row=1, column=1)

    # Create date Label (filter by date)
    date_label = Label(read_all_tasks_filter_frame, text="By Date", font=("Calibri", 12))
    date_label.grid(row=0, column=1)

    completed_selection = StringVar()
    # Create a drop down menu to select different completion status
    completed_filter_dropdown = OptionMenu(read_all_tasks_filter_frame, completed_selection, *["Completed","Not Completed", "All"])
    completed_selection.set("All")
    completed_filter_dropdown.grid(row=1, column=2)

    # Create completed Label (filter by completed)
    completed_label = Label(read_all_tasks_filter_frame, text="By Completed", font=("Calibri", 12))
    completed_label.grid(row=0, column=2)

    # find the latest day(not used) and all the subjects
    latest_date, subjects = Task.date_subject_finder("ToDoList.txt")
    var_list = []
    # Create a list of variables to store the values for checkboxes
    for i in range(len(subjects)):
        var_list.append(IntVar())
    # Create checkboxes for every subject
    for i,subject in enumerate(subjects):
        var = var_list[i]
        subject_check_button = Checkbutton(read_all_tasks_filter_frame, text=subject, variable=var)
        subject_check_button.grid(row=2+i//4, column=i%4)

    # Create the apply button (apply the filter options)
    apply_button = Button(read_all_tasks_filter_frame, text="Apply", font=("Calibri", 12),
                command=lambda: redraw_listbox([var.get() for var in var_list], subjects, date_selection.get(), completed_selection.get(), read_all_tasks_window))
    apply_button.grid(row=3+len(subjects)//4,column=0, columnspan=4)

    # display the filter frame
    read_all_tasks_filter_frame.pack()

    # display all the tasks (before filter)
    with open("ToDoList.txt", "r") as f:
        read_all_tasks_listbox(read_all_tasks_window, f.readlines())

# create a function to display the listbox (of tasks) frame
def read_all_tasks_listbox(window, line_list, filtered=False):
    global read_all_tasks_listbox_frame, tasks_listbox, tasks_read_scrollbar

    # forget the frame structure before to draw a new one (if it is already filtered)
    if filtered == True:
        read_all_tasks_listbox_frame.destroy()
        tasks_listbox.destroy()
        tasks_read_scrollbar.destroy()

    # Create the listbox frame
    read_all_tasks_listbox_frame = LabelFrame(window, borderwidth=0)

    # Create a scrollbar for the listbox
    tasks_read_scrollbar = Scrollbar(read_all_tasks_listbox_frame, orient=VERTICAL)

    # Create a listbox to display all the tasks
    tasks_listbox = Listbox(read_all_tasks_listbox_frame, width=50, height=20, yscrollcommand=tasks_read_scrollbar)

    # pack and configure the scollbar and the listbox
    tasks_read_scrollbar.config(command=tasks_listbox.yview)
    tasks_read_scrollbar.pack(side=RIGHT, fill=Y)
    tasks_listbox.pack()

    # Used when color the rows
    insert_count = 0
    date_insert_index = []
    subject_insert_index = []
    not_completed_insert_index = []
    completed_insert_index = []

    # Display texts in the file line by line
    print (line_list)
    for line in line_list:

        first_word = line.split(":")[0]

        # find the date and insert into the listbox
        if "Date" in first_word:
            date = line.split(":")[1].strip("\n")
            tasks_listbox.insert(END, line.strip("\n"))
            date_insert_index.append(insert_count)
            insert_count += 1
        # find the subjects and insert into the listbox
        else:
            subject = first_word
            tasks_listbox.insert(END, subject)
            if subject != "\n":
                subject_insert_index.append(insert_count)
            insert_count += 1

        # find the tasks and insert into the listbox
        if "Date" not in first_word and len(line.strip("\n")) != 0:
            tasks = Task.get_tasks_from_line(date, subject, line)
            for task in tasks:
                if task.name == "":
                    # counter the special case encountered after filtering
                    tasks_listbox.insert(END, "N/A")
                else:
                    tasks_listbox.insert(END, f"      {task.name}   -  Completed: {task.completed}")
                # highlight with different color between completed and not-completed tasks
                    if task.completed == False:
                        not_completed_insert_index.append(insert_count)
                    else:
                        completed_insert_index.append(insert_count)
                insert_count += 1
            tasks_listbox.insert(END, "===========================")
            insert_count += 1

    # color specific entries
    for date_row in date_insert_index:
         tasks_listbox.itemconfig(date_row, bg='#ffe680')
    for subject_row in subject_insert_index:
        tasks_listbox.itemconfig(subject_row, bg='lightblue')
    for not_completed_row in not_completed_insert_index:
        tasks_listbox.itemconfig(not_completed_row, bg="#ff8080")
    for completed_row in completed_insert_index:
        tasks_listbox.itemconfig(completed_row, bg="#99ffbb")

    read_all_tasks_listbox_frame.pack(pady=(10,0))

# Create a function to redraw the listbox (after filtering)
def redraw_listbox(var_list, subject_list, date, completed, window):
    # find the list of subjects that need to be kept after filtering based on the values of the checkboxes
    filtered_subject_list = []
    for i,var in enumerate(var_list):
        if var == 1:
            filtered_subject_list.append(subject_list[i])
    # if no checkboxes are checked, then keep all the subjects
    if len(filtered_subject_list) == 0:
        filtered_subject_list = "All"

    # get the filtered list of texts
    filtered_tasks_list = Task.filter(date, filtered_subject_list, completed, "ToDoList.txt")
    read_all_tasks_listbox(window, filtered_tasks_list, True)
# ========================Functions for add_subjects_afterwards window==========
def add_subject_afterwards_to_file(subject_name, window, entry):
    # Try to add the new subject to the file
    added = Task.add_new_subject_to_file("ToDoList.txt", subject_name)

    # Pop up a messagebox says the subject is existed
    if added == "Repeated":
        response = messagebox.askyesno("Repeated Subject", "It seems like this subject has been already added. Want to add another one?")
        if response == 0:
            window.destroy()
        else:
            entry.delete(0, END)
    # Pop up a messagebox says the subject has been added successfully
    elif added == "Success":
        entry.delete(0, END)
        response = messagebox.showinfo("Successfully Added", "Done! The new subject has been added")

def add_subject_afterwards():
    # Pop a window for add a new subject
    add_subject_afterwards_window = Toplevel()
    add_subject_afterwards_window.title("Add A Task")
    add_subject_afterwards_window.iconbitmap('icon.ico')
    add_subject_afterwards_window.geometry("330x150")

    # Create a frame to display all widgets
    add_subject_afterwards_frame = LabelFrame(add_subject_afterwards_window, borderwidth=0)

    # Create add subject label and ask subject label
    add_subject_afterwards_label = Label(add_subject_afterwards_frame, text="Add a new subject", font=("Calibri", 15),
                                    borderwidth=2, relief="groove")
    add_subject_afterwards_label.grid(row=0, column=0, columnspan=2)
    ask_subject_afterwards_label = Label(add_subject_afterwards_frame, text="Name of the subject: ", font=("Calibri", 12))
    ask_subject_afterwards_label.grid(row=1, column=0, pady=(20,0))

    # Create enter subject entry
    add_subject_afterwards_entry = Entry(add_subject_afterwards_frame, width=20)
    add_subject_afterwards_entry.grid(row=1, column=1, pady=(20,0))

    # Create add button
    add_subject_afterwards_button = Button(add_subject_afterwards_frame, text="Add", font=("Calibri", 12),
                                        command=lambda: add_subject_afterwards_to_file(add_subject_afterwards_entry.get(),
                                                                add_subject_afterwards_window,add_subject_afterwards_entry))
    add_subject_afterwards_button.grid(row=2, column=0, columnspan=2, pady=(20,0))

    add_subject_afterwards_frame.pack(pady=(5,0))
# ========================Functions for complete tasks window===================
def complete_tasks():
    # pop a new window for completing tasks
    complete_tasks_window = Toplevel()
    complete_tasks_window.title("Complete Tasks")
    complete_tasks_window.iconbitmap('icon.ico')
    complete_tasks_window.geometry("335x350")

    # create a frame to display all the widgets
    complete_tasks_frame = LabelFrame(complete_tasks_window, borderwidth=0)

    # for changing background
    insert_count = 0
    subject_row = []

    with open("ToDoList.txt", "r") as f:
        lines = f.readlines()

        # find the latest date and all related tasks in that date
        latest_date, subjects = Task.date_subject_finder("ToDoList.txt")
        latest_date_list = [line for line in lines if latest_date in line ]
        latest_date_index = lines.index(latest_date_list[0])
        relevant_tasks = lines[latest_date_index+1:latest_date_index+1+len(subjects)]
        relevant_tasks_object_list = []

        # create a label for date
        date_label = Label(complete_tasks_frame, text=f"Today is {latest_date}\n Here is what you haven't completed", font=("Calibri", 12))
        date_label.pack(pady=(5,6))

        # Create a scrollbar for the complete_tasks listbox
        complete_tasks_scrollbar = Scrollbar(complete_tasks_frame, orient=VERTICAL)

        # Create a listbox to display all the tasks
        complete_tasks_listbox = Listbox(complete_tasks_frame, width=50, height=12, yscrollcommand=complete_tasks_scrollbar,
                                    selectmode=MULTIPLE)

        # pack and configure the scollbar and the listbox
        complete_tasks_scrollbar.config(command=complete_tasks_listbox.yview)
        complete_tasks_scrollbar.pack(side=RIGHT, fill=Y)
        complete_tasks_listbox.pack(pady=(0,6))

        # iterate through lines in the latest date
        for index, line in enumerate(relevant_tasks):
            relevant_tasks_object_list.append(subjects[index])
            tasks = Task.get_tasks_from_line(latest_date, subjects[index], line)
            complete_tasks_listbox.insert(END, f"{subjects[index]}")
            subject_row.append(insert_count)
            insert_count += 1
            # display tasks line by line
            for task in tasks:
                if task.completed == False:
                    relevant_tasks_object_list.append(task)
                    complete_tasks_listbox.insert(END, f"{task.name}")
                    insert_count += 1

    # change the colors
    for row_index in subject_row:
        complete_tasks_listbox.itemconfig(row_index, bg='#dcf1f7')

    complete_task_submit_button = Button(complete_tasks_frame, text="Complet Select Tasks", font=("Calibri", 12),
                                    command=lambda: complete_tasks_submit(complete_tasks_listbox, relevant_tasks_object_list, complete_tasks_window))
    complete_task_submit_button.pack()

    complete_tasks_frame.pack()

def complete_tasks_submit(listbox, object_list, window):
    selections = list(listbox.curselection())
    # print (listbox.get(selections[0]))
    # print (object_list[selections[0]].name)
    dates, subjects = Task.date_subject_finder("ToDoList.txt")
    completed_object_list = [object for i,object in enumerate(object_list) if i in selections and object.name not in subjects]
    Task.make_it_complete("ToDoList.txt", completed_object_list)
    window.destroy()






# ========================Functions for open_existed_list window================
def add_tasks():
    # Pop a window to add tasks
    add_tasks_window = Toplevel()
    add_tasks_window.title("Add Tasks")
    add_tasks_window.iconbitmap('icon.ico')
    add_tasks_window.geometry("335x350")

    # reponse = messagebox.showinfo("Successfully Added", "The tasks are added successfully!")

    calendar_image_add_tasks = Image.open("calendar.jpg")
    calendar_image_add_tasks = ImageTk.PhotoImage(calendar_image_add_tasks.resize((20,20)))

    # Create add_task frame
    add_task_frame = LabelFrame(add_tasks_window, borderwidth=0)

    # Find current date and subjects
    date, subjects = Task.date_subject_finder("ToDoList.txt")

    subject_label_list = []
    subject_entry_list = []

    # Create labels and entries for user to input their tasks
    for i,subject in enumerate(subjects):
        label = Label(add_task_frame, text=subject, font=("Calibri", 14))
        label.grid(row=i+1, column=0, padx=(10,30), sticky=W)
        subject_label_list.append(label)
        entry = Entry(add_task_frame, width=30)
        entry.grid(row=i+1, column=1, sticky=W)
        subject_entry_list.append(entry)

    # Create date label
    current_date_label = Label(add_task_frame, text=f"Today is {date}", font=("Calibri", 14))
    current_date_label.grid(row=0, column=0, columnspan=2)

    # Create today/tomorrow choice Button
    add_tasks_today_button = Button(add_task_frame, text="Add To Today", font=("Calibri", 12),
                                        command=lambda: add_tasks_today(subject_entry_list, add_tasks_window))
    add_tasks_today_button.grid(row=len(subjects)+1, column=0, pady=(10,10))
    add_tasks_tomorrow_button = Button(add_task_frame, text="Add To Another Day",
                                        command=lambda: add_tasks_tomorrow(subjects, add_task_frame, calendar_image_add_tasks, subject_entry_list, add_tasks_window),
                                        font=("Calibri", 12))
    add_tasks_tomorrow_button.grid(row=len(subjects)+1, column=1, pady=(10,10))

    add_task_frame.pack()


def add_tasks_today(entry_list, window):
    reponse = messagebox.showinfo("Successfully Added", "The tasks are added successfully!")

    # get the tasks added
    tasks_list_by_subject = []
    for entry in entry_list:
        tasks_list = entry.get().split(",")
        tasks_list_by_subject.append(tasks_list)

    Task.add_to_today("ToDoList.txt", tasks_list_by_subject)

    window.destroy()

def add_tasks_tomorrow(subject_list, frame, image, subject_entry_list, window):
    global date_label, date_entry
    # Create date label and entry
    date_label = Label(frame, text="Date of The Day:", font=("Calibri", 12))
    date_label.grid(row=len(subject_list)+2, column=0, padx=(10, 14))
    date_entry = Entry(frame, width=20)
    date_entry.grid(row=len(subject_list)+2, column=1, sticky=W)

    # open the file to read the lines
    f = open("ToDoList.txt", "r")
    lines = f.readlines()
    f.close()

    date, subjects = Task.date_subject_finder("ToDoList.txt")

    # Find the uncompleted tasks from yesterday
    subject_index = 0
    # Create a blank list to store the tasks that haven't been completed
    subject_uncompleted_tasks = [[]]*len(subjects)
    for line in lines:
        # Find date for instanciate task objects
        if "Date:" in line:
            date = line.split(": ")[1].strip("\n")
        # Update the uncompleted list
        elif subjects[subject_index] in line:
            tasks = Task.get_tasks_from_line(date,subjects[subject_index],line)
            uncompleted = []
            for task in tasks:
                if task.completed == False:
                    uncompleted.append(task.name)
            subject_uncompleted_tasks[subject_index] = uncompleted
            subject_index += 1
            if subject_index == len(subjects):
                subject_index = 0

    f = open("Settings.txt","r+")
    lines = f.readlines()
    if lines[0].split(": ")[1] == "On":
        # Insert the uncompleted tasks into the entry
        for i,entry in enumerate(subject_entry_list):
            for index,task in enumerate(subject_uncompleted_tasks[i]):
                if index != len(subject_uncompleted_tasks[i])-1:
                    entry.insert(END, task+",")
                else:
                    entry.insert(END, task)

        # Pop up a messagebox at the first time the user use this feature
        if lines[0].split(": ")[2].strip("\n") == "Ask":
            response = messagebox.askyesno("Auto Add Notification", f'''Auto Add is turned on by default. Turn in off?\t
(This message will not show up again)''')
            lines[0] = lines[0].replace("Ask", "Asked")
            if response == 1:
                lines[0] = lines[0].replace("On", "Off")
            # Not show up again
            f.seek(0)
            for line in lines:
                f.write(line)

    f.close()




    # Craete a date selection button
    calendar_button = Button(frame, image=image, command=select_date)
    calendar_button.grid(row=len(subject_list)+2, column=1, padx=(96,0))

    # Create a submit button
    add_task_tomorrow_submit_button = Button(frame, text="Submit", font=("Calibri", 12),
                                    command=lambda: add_task_tomorrow_submit(subject_entry_list, window))
    add_task_tomorrow_submit_button.grid(row=len(subject_list)+3, column=0, columnspan=2, pady=(10,0))

def add_task_tomorrow_submit(entry_list, window):
    global date_entry

    reponse = messagebox.showinfo("Successfully Added", "The tasks are added successfully!")

    tasks_list_by_subject = []
    for entry in entry_list:
        tasks_list = entry.get().split(",")
        tasks_list_by_subject.append(tasks_list)
    Task.add_to_tomorrow(date_entry.get(), tasks_list_by_subject, "ToDoList.txt")

    window.destroy()


# ==============================================================================
# Creat main frame
main_frame = LabelFrame(root, borderwidth=0)

# Create app_name Label
app_name_label = Label(main_frame, text="To-Do List Manager", font=("Calibri", 30))
app_name_label.pack(pady=(80,5))

# Create Motto Label
motto_label = Label(main_frame, text="\t-To make your goal clearer", font=("Ink Free", 14))
motto_label.pack(pady=(0,60))

# Create create_list button
create_list_button = Button(main_frame, text="Create New List", command=create_new_list, font=("Calibri", 18))
create_list_button.pack(pady=(0,10), ipadx=7)

# Create open_list button
open_list_button = Button(main_frame, text="Open Existed List", command=open_list, font=("Calibri", 18))
open_list_button.pack(pady=(0,10))

# Create setting button
setting_button = Button(main_frame, text="Settings", command=setting, font=("Calibri", 18))
setting_button.pack(pady=(0,10), ipadx=44)

# # Create user_instruction button
# user_instruction_button = Button(main_frame, text="User Instruction", command=user_instruction, font=("Calibri", 18))
# user_instruction_button.pack(pady=(0,10), ipadx=6)

# Create version label
version_label = Label(main_frame, text="1.0.2", font=("Calibri", 13))
version_label.pack(padx=(300,0),pady=(80,0))

main_frame.pack()

# ==============================================================================
subject_num = 3
subject_label_entry_list = []

# Create create_new_list frame
create_new_list_frame = LabelFrame(root, borderwidth=0)

# Create the title label
create_new_list_title_label = Label(create_new_list_frame, text="Create a New List", font=("Calibri", 30), borderwidth=2, relief="groove")
create_new_list_title_label.grid(row=0, column=0, columnspan=2, pady=(40,30))

# Create date label and entry
date_label = Label(create_new_list_frame, text="Date of Today:", font=("Calibri", 14))
date_label.grid(row=1, column=0, padx=(10, 14))
date_entry = Entry(create_new_list_frame, width=27)
date_entry.grid(row=1, column=1, sticky=W)

# Craete a date selection button
calendar_button = Button(create_new_list_frame, image=calendar_image, command=select_date)
calendar_button.grid(row=1, column=1, sticky=E)

# Create subject labels and entries
subject_label_1 = Label(create_new_list_frame, text="Subject 1: ", font=("Calibri", 14))
subject_label_1.grid(row=2, column=0, padx=(10,14))
subject_entry_1 = Entry(create_new_list_frame, width=32)
subject_entry_1.grid(row=2, column=1)
subject_label_entry_list.append((subject_label_1, subject_entry_1))

subject_label_2 = Label(create_new_list_frame, text="Subject 2: ", font=("Calibri", 14))
subject_label_2.grid(row=3, column=0, padx=(10,14))
subject_entry_2 = Entry(create_new_list_frame, width=32)
subject_entry_2.grid(row=3, column=1)
subject_label_entry_list.append((subject_label_2, subject_entry_2))

subject_label_3 = Label(create_new_list_frame, text="Subject 3: ", font=("Calibri", 14))
subject_label_3.grid(row=4, column=0, padx=(10,14))
subject_entry_3 = Entry(create_new_list_frame, width=32)
subject_entry_3.grid(row=4, column=1)
subject_label_entry_list.append((subject_label_3, subject_entry_3))

# Create submit_new_list button
submit_new_list_button = Button(create_new_list_frame, text="Submit", command=submit_new_list, font=("Calibri", 14))
submit_new_list_button.grid(row=subject_num+2, column=0, pady=(30,0))

# Create another_subject button
another_subject_button = Button(create_new_list_frame, text="Add a subject", command=add_subject, font=("Calibri", 14))
another_subject_button.grid(row=subject_num+2, column=1, pady=(30,0))

create_new_list_back_button = Button(create_new_list_frame, text="Back", command=lambda: back_to_main(create_new_list_frame), font=("Calibri", 14))
create_new_list_back_button.grid(row=subject_num+3, column=1, padx=(30,0), pady=(20, 10))

# ==============================================================================
# Create open_list frame
if os.path.isfile("ToDoList.txt"):
    open_list_frame = LabelFrame(root, borderwidth=0)

    # Create title label
    open_list_title_label = Label(open_list_frame, text="Choose a Mode...", font=("Calibri", 24), borderwidth=2, relief="groove")
    open_list_title_label.pack(pady=(60,0))

    # Create Mode Buttons
    read_only_button = Button(open_list_frame, text="Read Only", font=("Calibri", 16), command=read_all_tasks)
    read_only_button.pack(pady=(50,0), ipadx=24)
    add_subject_button = Button(open_list_frame, text="Add a Subject", font=("Calibri", 16), command=add_subject_afterwards)
    add_subject_button.pack(pady=(10,0), ipadx=9)
    complete_task_button = Button(open_list_frame, text="Complete Tasks", font=("Calibri", 16), command=complete_tasks)
    complete_task_button.pack(pady=(10,0))
    add_tasks_button = Button(open_list_frame, text="Add Tasks", command=add_tasks, font=("Calibri", 16))
    add_tasks_button.pack(pady=(10,0), ipadx=24)

    open_list_back_button = Button(open_list_frame, text="Back", command=lambda: back_to_main(open_list_frame), font=("Calibri", 14))
    open_list_back_button.pack(side=BOTTOM, padx=(200,0), pady=(40, 10))
#===============================================================================
#Create setting frame
setting_frame = LabelFrame(root, borderwidth=0)

# create setting label
setting_label = Label(setting_frame, text="Settings", font=("Calibri", 24), borderwidth=2, relief="groove")
setting_label.grid(row=0, column=0, columnspan=2, sticky=W, pady=20)

# iterate through the file to draw a label and a button for every setting
with open("Settings.txt", "r") as f:
    lines = f.readlines()
    # initialize three lists to store different attributes for settings
    names = []
    status = []
    addition = []
    for line in lines:
        names.append(line.split(": ")[0])
        status.append(line.split(": ")[1])
        addition.append(line.split(": ")[2])
    # draw the label and the button
    for i,name in enumerate(names):
        name_label = Label(setting_frame, text=name, font=("Calibri", 15))
        name_label.grid(row=i+1, column=0, padx=(0,100), pady=(30,0))
        if status[i] == "On":
            status_button = Button(setting_frame, image=on_switch_image, command=lambda: switch(True, name))
        else:
            status_button = Button(setting_frame, image=off_switch_image, command=lambda: switch(False, name))
        status_button.grid(row=i+1, column=1, pady=(30,0))

setting_back_button = Button(setting_frame, text="Back", command=lambda: back_to_main(setting_frame), font=("Calibri", 14))
setting_back_button.grid(row=1+len(names), column=0, columnspan=2, sticky=E, pady=(50,0))

# # ==============================================================================
# # Create user_instruction frame
# user_instruction_frame = LabelFrame(root, borderwidth=0)
#
# instruction_1 = "Create a file before you first use this app."
# instruction_2 = "Seperate the tasks with',' when adding tasks"
# instruction_3 = "(without space)"
#
# instruction1_label = Label(user_instruction_frame, text=instruction_1, font=("Calibri", 12))
# instruction2_label = Label(user_instruction_frame, text=instruction_2, font=("Calibri", 12))
# instruction3_label = Label(user_instruction_frame, text=instruction_3, font=("Calibri", 12))
#
# instruction1_label.grid(row=0, column=0, sticky=W)
# instruction2_label.grid(row=1, column=0, sticky=W)
# instruction3_label.grid(row=2, column=0, sticky=W)
#
# user_instruction_back_button = Button(user_instruction_frame, text="Back", command=lambda: back_to_main(user_instruction_frame), font=("Calibri", 12))
# user_instruction_back_button.grid(row=3, column=0, sticky=E)



root.mainloop()
