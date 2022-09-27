from tkinter import *
import sqlite3
from PIL import ImageTk, Image
import random
from tkinter import ttk
from tkinter import messagebox
import win32api
from tkinter import filedialog

# Main frame to switch frames
class Main(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        # Destroys current frame and replaces it with a new one.
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
            
        my_menu = Menu(self)
        self.config(menu=my_menu)

        # Create a menu
        admin_menu = Menu(my_menu)
        my_menu.add_cascade(label="Admin", menu=admin_menu)
        admin_menu.add_command(label="Modules", command=modules)
        admin_menu.add_separator()
        admin_menu.add_command(label="Name", command=questions)

        # Submenus
        user_menu = Menu(my_menu)
        my_menu.add_cascade(label="User", menu=user_menu)
        user_menu.add_command(label="Report")

        # Open file to print function
        def print():
            # Grab file
            print_file = filedialog.askopenfilename(initialdir="C:/Quiz/", title="Open file", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py")))

            if print_file:
                win32api.ShellExecute(0, "print", print_file, None, ".", 0)

        file_menu = Menu(my_menu)
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Print", command=print)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)


# Main page
class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        # Bug on the picture, it overlaps in some cases
        # Show img
        def show_img(self):
            global logo_label
            image_frame = Frame(self)
            image_frame.logo_img = ImageTk.PhotoImage(Image.open("myquizzz.jpg"))
            logo_label = Label(image = image_frame.logo_img)
            logo_label.pack()
        show_img(self)

        # Frame containing everything
        text_frame = Frame(self)
        text_frame.pack()
        text_frame.config(background="lightblue")
        asdf = Label(text_frame, text="Trading Algo Main Page", font=("Helvetica", 25), background="lightblue")
        asdf.pack(pady=20)
        global cont

        # Button
        cont = PhotoImage(file="continueImage.png")
        Button(text_frame, image=cont).pack(pady=5)


# Add, edit or delete modules in this class. Shows new window from the menu
class Modules():
    global modules
    # Function called from the manu bar
    def modules():
        # Move up the record
        def up():
            # Bug: Value is not stored
            # Solution: Put the values on a list and refresh the table
            rows = my_tree.selection()
            for row in rows:
                my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

        # Move down the record
        def down():
            # Bug: Value is not stored
            # Solution: Put the values on a list and refresh the table
            rows = my_tree.selection()
            for row in reversed(rows):
                my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

        # Show db on treeview
        def query_database():
            conn = sqlite3.connect('question_bank1.db')
            c = conn.cursor()

            c.execute("SELECT rowid, * FROM modules")
            records = c.fetchall()

            global count
            count = 0
            # Loop to display values and diff colours in the background
            for record in records:
                if count % 2 == 0:
                    my_tree.insert(parent="", index="end", iid=count, text="", values=(
                        record[0], record[1], record[2], record[3]), tags=("evenrow",))
                else:
                    my_tree.insert(parent="", index="end", iid=count, text="", values=(
                        record[0], record[1], record[2], record[3]), tags=("oddrow",))
                count += 1

            conn.commit()
            conn.close

        # Delete module on click
        def delete_module():
            conn = sqlite3.connect('question_bank1.db')
            c = conn.cursor()

            # Delete the ID that its on the entry
            c.execute("DELETE FROM modules WHERE id_number = ?",
                      (id_entry.get(),))

            # Eliminate the values on the entry
            row_entry.delete(0, END)
            id_entry.delete(0, END)
            subject_entry.delete(0, END)
            name_entry.delete(0, END)

            conn.commit()
            conn.close

            # Clear treeview
            my_tree.delete(*my_tree.get_children())

            # Run the database again
            query_database()

        # Add module on click
        def add_module():
            # Needs to be refreshed to see the changes
            conn = sqlite3.connect("question_bank1.db")
            c = conn.cursor()

            # Placeholder and dictionary to add values in it
            c.execute("INSERT INTO modules VALUES(:id_number, :subject, :name)",
                      {
                          'id_number': id_entry.get(),
                          'subject': subject_entry.get(),
                          'name': name_entry.get(),
                      })

            conn.commit()
            conn.close

            # Delete the values in the entry
            row_entry.delete(0, END)
            id_entry.delete(0, END)
            subject_entry.delete(0, END)
            name_entry.delete(0, END)

            # Clear treeview
            my_tree.delete(*my_tree.get_children())

            # Run the database again
            query_database()

        # Edit module when the values are on the entry
        def edit_module():
            conn = sqlite3.connect('question_bank1.db')
            c = conn.cursor()

            c.execute(""" UPDATE modules SET 
                    id_number = :id_number,
                    subject = :subject,
                    name = :name
                    WHERE oid  = :oid""",
                      {
                          'id_number': id_entry.get(),
                          'subject': subject_entry.get(),
                          'name': name_entry.get(),
                          'oid': row_entry.get(),
                      })

            conn.commit()
            conn.close

            # Delete entry values
            row_entry.delete(0, END)
            id_entry.delete(0, END)
            subject_entry.delete(0, END)
            name_entry.delete(0, END)

            # Clear treeview
            my_tree.delete(*my_tree.get_children())

            # Run the database again
            query_database()

        # Start the frame that contains everything
        modules_frame = Toplevel()
        modules_frame.config(background="lightblue")
        modules_frame.minsize(width=500, height=500)
        style = ttk.Style()
        # Pick a theme: default, clam, alt... For the top
        style.theme_use("clam")
        # Configure colors
        style.configure("Treeview",
                        background="silver",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="silver"
                        )
        style.map("Treeview", background=[("selected", "darkblue")])

        # Create treeview frame
        tree_frame = Frame(modules_frame)
        tree_frame.pack(pady=20)

        # Treeview scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        my_tree.pack()

        # Configure the scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define the columns
        my_tree["columns"] = ("Column", "ID_number", "Subject", "Name")

        # Columns config
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Column", anchor=W, width=50)
        my_tree.column("ID_number", anchor=W, width=90)
        my_tree.column("Subject", anchor=CENTER, width=100)
        my_tree.column("Name", anchor=W, width=250)

        # Headings, Change text for diff names
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Column", text="RowID", anchor=W)
        my_tree.heading("ID_number", text="ID_number", anchor=W)
        my_tree.heading("Subject", text="Subject", anchor=CENTER)
        my_tree.heading("Name", text="Name", anchor=W)

        conn = sqlite3.connect('question_bank1.db')
        c = conn.cursor()

        # Show data from db
        data = c.execute("SELECT rowid, * FROM modules")

        # Create stripped row tags, backgorund of the values
        my_tree.tag_configure("oddrow", background="white")
        my_tree.tag_configure("evenrow", background="lightblue")

        global count
        count = 0
        # Loop to display values and diff colours in the background
        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent="", index="end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3]), tags=("evenrow",))
            else:
                my_tree.insert(parent="", index="end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3]), tags=("oddrow",))
            count += 1

        # Frame containing the selected info
        lab_frame = LabelFrame(modules_frame, text="Record")
        lab_frame.config(background="lightblue")
        lab_frame.pack(pady=20)

        # Define labels
        row_label = Label(lab_frame, text="Row", bg="lightblue")
        row_label.grid(row=0, column=0)

        id_label = Label(lab_frame, text="ID Number", bg="lightblue")
        id_label.grid(row=0, column=1)

        subject_label = Label(lab_frame, text="Subject", bg="lightblue")
        subject_label.grid(row=0, column=2)

        name_label = Label(lab_frame, text="Name", bg="lightblue")
        name_label.grid(row=0, column=3)

        # Entry
        row_entry = Entry(lab_frame)
        row_entry.grid(row=1, column=0, padx=5, pady=5)

        id_entry = Entry(lab_frame)
        id_entry.grid(row=1, column=1, padx=5, pady=5)

        subject_entry = Entry(lab_frame)
        subject_entry.grid(row=1, column=2, padx=5, pady=5)

        name_entry = Entry(lab_frame)
        name_entry.grid(row=1, column=3, padx=5, pady=5)

        # Button
        btn_frame = LabelFrame(modules_frame, text="Commands")
        btn_frame.config(background="lightblue")
        btn_frame.pack()

        submit_button = Button(
            btn_frame, text="Save record", command=add_module)
        submit_button.grid(row=0, column=0, pady=10, padx=10)

        edit_button = Button(
            btn_frame, text="Edit record", command=edit_module)
        edit_button.grid(row=0, column=1, pady=10, padx=10)

        delete_button = Button(
            btn_frame, text="Delete record", command=delete_module)
        delete_button.grid(row=0, column=2, pady=10, padx=10)

        up_button = Button(btn_frame, text="Move up", command=up)
        up_button.grid(row=0, column=3, pady=10, padx=10)

        down_button = Button(btn_frame, text="Move down", command=down)
        down_button.grid(row=0, column=4, pady=10, padx=10)

        # On double click, get values from the treeview
        def clicker(e):
            select_record()

        # On click select a row
        my_tree.bind("<ButtonRelease-1>", clicker)

        def select_record():
            # Clear boxes
            row_entry.delete(0, END)
            id_entry.delete(0, END)
            subject_entry.delete(0, END)
            name_entry.delete(0, END)

            # Grab record number
            selected = my_tree.focus()
            # Grab record, in this case values.(text, values, id...)
            values = my_tree.item(selected, "values")

            row_entry.insert(0, values[0])
            id_entry.insert(0, values[1])
            subject_entry.insert(0, values[2])
            name_entry.insert(0, values[3])


class Questions():
    global questions
    # Called from the menu bar
    def questions():
        # Move up a row
        def up():
            # Bug: Value is not stored
            # Solution: Put the values on a list and refresh the table
            rows = my_tree.selection()
            for row in rows:
                my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

        # Move down a row
        def down():
            # Bug: Value is not stored
            # Solution: Put the values on a list and refresh the table
            rows = my_tree.selection()
            for row in reversed(rows):
                my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

        # Show values
        def query_database():
            conn = sqlite3.connect('question_bank1.db')
            c = conn.cursor()

            c.execute("SELECT rowid, * FROM questions")
            records = c.fetchall()

            global count
            count = 0
            # Loop to display values and diff colours in the background
            for record in records:
                if count % 2 == 0:
                    my_tree.insert(parent="", index="end", iid=count, text="", values=(
                        record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11]), tags=("evenrow",))
                else:
                    my_tree.insert(parent="", index="end", iid=count, text="", values=(
                        record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11]), tags=("oddrow",))
                count += 1

            conn.commit()
            conn.close

        # Delete a question on "click"
        def delete_question():
            conn = sqlite3.connect('question_bank1.db')
            c = conn.cursor()

            # Delete the ID that its on the entry
            c.execute("DELETE FROM questions WHERE id_number = ?",
                      (id_entry.get(),))

            # Clear boxes
            row_entry.delete(0, END)
            id_entry.delete(0, END)
            question_entry.delete(0, END)
            explanation_entry.delete(0, END)
            a1_entry.delete(0, END)
            a2_entry.delete(0, END)
            a3_entry.delete(0, END)
            a4_entry.delete(0, END)
            r1_entry.delete(0, END)
            r2_entry.delete(0, END)
            r3_entry.delete(0, END)
            r4_entry.delete(0, END)

            conn.commit()
            conn.close

            # Clear treeview
            my_tree.delete(*my_tree.get_children())

            # Run the database again
            query_database()

        def add_question():
            conn = sqlite3.connect("question_bank1.db")
            c = conn.cursor()

            # Placeholder and dictionary to add values in it
            c.execute("INSERT INTO questions VALUES(:id_number, :question, :a1, :a2, :a3, :a4, :r1, :r2, :r3, :r4, :explanation)",
                      {
                          'id_number': id_entry.get(),
                          'question': question_entry.get(),
                          'a1': a1_entry.get(),
                          'a2': a2_entry.get(),
                          'a3': a3_entry.get(),
                          'a4': a4_entry.get(),
                          'r1': r1_entry.get(),
                          'r2': r2_entry.get(),
                          'r3': r3_entry.get(),
                          'r4': r4_entry.get(),
                          'explanation': explanation_entry.get(),
                      })

            conn.commit()
            conn.close

            # Delete the values in the entry
            row_entry.delete(0, END)
            id_entry.delete(0, END)
            question_entry.delete(0, END)
            explanation_entry.delete(0, END)
            a1_entry.delete(0, END)
            a2_entry.delete(0, END)
            a3_entry.delete(0, END)
            a4_entry.delete(0, END)
            r1_entry.delete(0, END)
            r2_entry.delete(0, END)
            r3_entry.delete(0, END)
            r4_entry.delete(0, END)

            # Clear treeview
            my_tree.delete(*my_tree.get_children())

            # Run the database again
            query_database()

        def edit_question():
            conn = sqlite3.connect('question_bank1.db')
            c = conn.cursor()
            # Update from db
            c.execute(""" UPDATE questions SET 
                    id_number = :id_number,
                    question = :question,
                    a1 = :a1,
                    a2 = :a2,
                    a3 = :a3,
                    a4 = :a4,
                    r1 = :r1,
                    r2 = :r2,
                    r3 = :r3,
                    r4 = :r4
                    WHERE oid  = :oid""",
                      {
                          'id_number': id_entry.get(),
                          'question': question_entry.get(),
                          'a1': a1_entry.get(),
                          'a2': a2_entry.get(),
                          'a3': a3_entry.get(),
                          'a4': a4_entry.get(),
                          'r1': r1_entry.get(),
                          'r2': r2_entry.get(),
                          'r3': r3_entry.get(),
                          'r4': r4_entry.get(),
                          'explanation': explanation_entry.get(),
                          'oid': row_entry.get(),
                      })

            conn.commit()
            conn.close

            # Delete entry info
            row_entry.delete(0, END)
            id_entry.delete(0, END)
            question_entry.delete(0, END)
            explanation_entry.delete(0, END)
            a1_entry.delete(0, END)
            a2_entry.delete(0, END)
            a3_entry.delete(0, END)
            a4_entry.delete(0, END)
            r1_entry.delete(0, END)
            r2_entry.delete(0, END)
            r3_entry.delete(0, END)
            r4_entry.delete(0, END)

            # Clear treeview
            my_tree.delete(*my_tree.get_children())

            # Run the database again
            query_database()

        # Start the frame for this class, everything is inside this frame
        questions_frame = Toplevel()
        app.minsize(width=900, height=00)

        questions_frame.config(background="lightblue")
        questions_frame.minsize(width=700, height=650)
        style = ttk.Style()
        # Pick a theme: default, clam, alt... For the top
        style.theme_use("clam")
        # Configure colors
        style.configure("Treeview",
                        background="silver",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="silver"
                        )
        style.map("Treeview", background=[("selected", "darkblue")])

        # Create treeview frame
        tree_frame = Frame(questions_frame)
        tree_frame.pack(pady=20, padx=20)

        # Treeview scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        my_tree.pack()

        # Configure the scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define the columns
        my_tree["columns"] = ("Column", "ID_number", "Question", "a1",
                              "a2", "a3", "a4", "r1", "r2", "r3", "r4", "explanation")

        # Columns config
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Column", anchor=W, width=50)
        my_tree.column("ID_number", anchor=W, width=90)
        my_tree.column("Question", anchor=CENTER, width=180)
        my_tree.column("a1", anchor=W, width=180)
        my_tree.column("a2", anchor=W, width=180)
        my_tree.column("a3", anchor=W, width=180)
        my_tree.column("a4", anchor=W, width=180)
        my_tree.column("r1", anchor=W, width=50)
        my_tree.column("r2", anchor=W, width=50)
        my_tree.column("r3", anchor=W, width=50)
        my_tree.column("r4", anchor=W, width=50)
        my_tree.column("explanation", anchor=W, width=180)

        # Headings, Change text for diff names
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Column", text="RowID", anchor=W)
        my_tree.heading("ID_number", text="ID_number", anchor=W)
        my_tree.heading("Question", text="Question", anchor=CENTER)
        my_tree.heading("a1", text="Answer 1", anchor=W)
        my_tree.heading("a2", text="Answer 2", anchor=W)
        my_tree.heading("a3", text="Answer 3", anchor=W)
        my_tree.heading("a4", text="Answer 4", anchor=W)
        my_tree.heading("r1", text="Result 1", anchor=W)
        my_tree.heading("r2", text="Result 2", anchor=W)
        my_tree.heading("r3", text="Result 3", anchor=W)
        my_tree.heading("r4", text="Result 4", anchor=W)
        my_tree.heading("explanation", text="Explanation", anchor=W)

        conn = sqlite3.connect('question_bank1.db')
        c = conn.cursor()

        # Show data from db
        data = c.execute("SELECT rowid, * FROM questions")

        # Create stripped row tags, backgorund of the values
        my_tree.tag_configure("oddrow", background="white")
        my_tree.tag_configure("evenrow", background="lightblue")

        global count
        count = 0
        # Loop to display values and diff colours in the background
        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent="", index="end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11]), tags=("evenrow",))
            else:
                my_tree.insert(parent="", index="end", iid=count, text="", values=(
                    record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11]), tags=("oddrow",))
            count += 1

        # Frame containing the selected info
        lab_frame = LabelFrame(questions_frame, text="Record")
        lab_frame.config(background="lightblue")
        lab_frame.pack(pady=20)

        # Define labels
        row_label = Label(lab_frame, text="Row", bg="lightblue")
        row_label.grid(row=0, column=0)

        id_label = Label(lab_frame, text="ID Number", bg="lightblue")
        id_label.grid(row=0, column=1)

        question_label = Label(lab_frame, text="Question", bg="lightblue")
        question_label.grid(row=0, column=2)

        explanation_label = Label(
            lab_frame, text="Explanation", bg="lightblue")
        explanation_label.grid(row=0, column=3)

        a1_label = Label(lab_frame, text="Answer 1", bg="lightblue")
        a1_label.grid(row=2, column=0)

        a2_label = Label(lab_frame, text="Answer 2", bg="lightblue")
        a2_label.grid(row=2, column=1)

        a3_label = Label(lab_frame, text="Answer 3", bg="lightblue")
        a3_label.grid(row=2, column=2)

        a4_label = Label(lab_frame, text="Answer 4", bg="lightblue")
        a4_label.grid(row=2, column=3)

        r1_label = Label(lab_frame, text="Result 1", bg="lightblue")
        r1_label.grid(row=4, column=0)

        r2_label = Label(lab_frame, text="Result 2", bg="lightblue")
        r2_label.grid(row=4, column=1)

        r3_label = Label(lab_frame, text="Result 3", bg="lightblue")
        r3_label.grid(row=4, column=2)

        r4_label = Label(lab_frame, text="Result 4", bg="lightblue")
        r4_label.grid(row=4, column=3)

        # Entry
        row_entry = Entry(lab_frame)
        row_entry.grid(row=1, column=0, padx=5, pady=5)

        id_entry = Entry(lab_frame)
        id_entry.grid(row=1, column=1, padx=5, pady=5)

        question_entry = Entry(lab_frame)
        question_entry.grid(row=1, column=2, padx=5, pady=5)

        explanation_entry = Entry(lab_frame)
        explanation_entry.grid(row=1, column=3, padx=5, pady=5)

        a1_entry = Entry(lab_frame)
        a1_entry.grid(row=3, column=0, padx=5, pady=5)

        a2_entry = Entry(lab_frame)
        a2_entry.grid(row=3, column=1, padx=5, pady=5)

        a3_entry = Entry(lab_frame)
        a3_entry.grid(row=3, column=2, padx=5, pady=5)

        a4_entry = Entry(lab_frame)
        a4_entry.grid(row=3, column=3, padx=5, pady=5)

        r1_entry = Entry(lab_frame)
        r1_entry.grid(row=5, column=0, padx=5, pady=5)

        r2_entry = Entry(lab_frame)
        r2_entry.grid(row=5, column=1, padx=5, pady=5)

        r3_entry = Entry(lab_frame)
        r3_entry.grid(row=5, column=2, padx=5, pady=5)

        r4_entry = Entry(lab_frame)
        r4_entry.grid(row=5, column=3, padx=5, pady=5)

        # Button
        btn_frame = LabelFrame(questions_frame, text="Commands")
        btn_frame.config(background="lightblue")
        btn_frame.pack(pady=20)

        submit_button = Button(
            btn_frame, text="Save record", command=add_question)
        submit_button.grid(row=0, column=0, pady=10, padx=10)

        edit_button = Button(btn_frame, text="Edit record",
                             command=edit_question)
        edit_button.grid(row=0, column=1, pady=10, padx=10)

        delete_button = Button(
            btn_frame, text="Delete record", command=delete_question)
        delete_button.grid(row=0, column=2, pady=10, padx=10)

        up_button = Button(btn_frame, text="Move up", command=up)
        up_button.grid(row=0, column=3, pady=10, padx=10)

        down_button = Button(btn_frame, text="Move down", command=down)
        down_button.grid(row=0, column=4, pady=10, padx=10)

        # On double click, get values from the treeview
        def clicker(e):
            select_record()

        # On one click select a row
        my_tree.bind("<ButtonRelease-1>", clicker)

        def select_record():
            # Clear boxes
            row_entry.delete(0, END)
            id_entry.delete(0, END)
            question_entry.delete(0, END)
            explanation_entry.delete(0, END)
            a1_entry.delete(0, END)
            a2_entry.delete(0, END)
            a3_entry.delete(0, END)
            a4_entry.delete(0, END)
            r1_entry.delete(0, END)
            r2_entry.delete(0, END)
            r3_entry.delete(0, END)
            r4_entry.delete(0, END)

            # Grab record number
            selected = my_tree.focus()
            # Grab record, in this case values.(text, values, id...)
            values = my_tree.item(selected, "values")

            # Insert values from db/treeview to the entry
            row_entry.insert(0, values[0])
            id_entry.insert(0, values[1])
            question_entry.insert(0, values[2])
            a1_entry.insert(0, values[3])
            a2_entry.insert(0, values[4])
            a3_entry.insert(0, values[5])
            a4_entry.insert(0, values[6])
            r1_entry.insert(0, values[7])
            r2_entry.insert(0, values[8])
            r3_entry.insert(0, values[9])
            r4_entry.insert(0, values[10])
            explanation_entry.insert(0, values[11])


class StartGui(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # Create frame to have the bg in blue
        start_frame = Frame(self).pack()
        style = ttk.Style()
        # Pick a theme: default, clam, alt... For the top
        style.theme_use("clam")
        # Configure colors
        style.configure("Treeview", 
                        background= "silver",

                        foreground="black",
                        rowheight=25,
                        fieldbackground="silver"
        )
        style.map("Treeview", background=[("selected", "darkblue")])

        # Create treeview frame
        tree_frame = Frame(start_frame)
        tree_frame.pack(pady=20)
        
        # Treeview scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        my_tree.pack()

        # Configure the scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define the columns
        my_tree["columns"] = ("Column", "ID_number", "Subject", "Name")

        # Columns config
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Column", anchor=W, width=50)
        my_tree.column("ID_number", anchor=W, width=90)
        my_tree.column("Subject", anchor=CENTER, width=100)
        my_tree.column("Name", anchor=W, width=250)

        # Headings, Change text for diff names
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Column", text="RowID", anchor=W)
        my_tree.heading("ID_number", text="ID_number", anchor=W)
        my_tree.heading("Subject", text="Subject", anchor=CENTER)
        my_tree.heading("Name", text="Name", anchor=W)

        conn = sqlite3.connect('question_bank1.db')
        c = conn.cursor()

        # Show data from db
        data = c.execute("SELECT rowid, * FROM modules")
        
        # Create stripped row tags, backgorund of the values
        my_tree.tag_configure("oddrow", background="white")
        my_tree.tag_configure("evenrow", background="lightblue")

        global count
        count = 0 
        # Loop to display values and diff colours in the background
        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent="", index="end", iid=count, text="", values = (record[0], record[1], record[2], record[3]), tags=("evenrow",))
            else:
                my_tree.insert(parent="", index="end", iid=count, text="", values = (record[0], record[1], record[2], record[3]), tags=("oddrow",))
            count +=1

        # Frame containing the selected info
        lab_frame  = LabelFrame(start_frame, text="Record")
        lab_frame.config(background="lightblue")
        lab_frame.pack(pady=20)

        # Define labels
        row_label = Label(lab_frame, text="Row", bg="lightblue")
        row_label.grid(row=0, column=0)

        id_label = Label(lab_frame, text="ID Number", bg="lightblue")
        id_label.grid(row=0, column=1)

        subject_label = Label(lab_frame, text="Subject", bg="lightblue")
        subject_label.grid(row=0, column=2)

        name_label = Label(lab_frame, text="Name", bg="lightblue")
        name_label.grid(row=0, column=3)

        # Entry
        row_entry = Entry(lab_frame)
        row_entry.grid(row=1, column=0, padx=5, pady=10)

        id_entry = Entry(lab_frame)
        id_entry.grid(row=1, column=1, padx=5, pady=10)

        subject_entry = Entry(lab_frame)
        subject_entry.grid(row=1, column=2, padx=5, pady=10)

        name_entry = Entry(lab_frame)
        name_entry.grid(row=1, column=3, padx=5, pady=10)
        
        # On double click, get values from the treeview
        def clicker(e):
            select_record()
            
        # Select row on click
        my_tree.bind("<ButtonRelease-1>", clicker)

        # Delete records from the entry
        def select_record():
            '''
            When the user clicks on a module to start it, 
            it selects all the questions from the database and
            shuffles them.
            '''
            # Clear boxes
            row_entry.delete(0, END)
            id_entry.delete(0, END)
            subject_entry.delete(0, END)
            name_entry.delete(0, END)
            
            # Grab record number
            selected = my_tree.focus()
            # Grab record, in this case values.(text, values, id...)
            values = my_tree.item(selected, "values")
            
            # Insert values
            row_entry.insert(0, values[0])
            id_entry.insert(0, values[1])
            subject_entry.insert(0, values[2])
            name_entry.insert(0, values[3])

            conn = sqlite3.connect('question_bank1.db')
            c = conn.cursor()

            global lookup_record, all_questions
            lookup_record = id_entry.get() 
            # Get the value of all the rows with the same id
            c.execute("SELECT * FROM questions WHERE id_number = ?", (lookup_record,))
            all_questions = c.fetchall()
            
            # Shuffle the questions
            random.shuffle(all_questions)
            # print(all_questions)
            conn.commit()
            conn.close

        # Button
        btn_frame = Frame(self)
        btn_frame.config(bg="lightblue")
        btn_frame.pack()

        photo = PhotoImage(file="startButton.png")
        
        start_button = Button(btn_frame, image=photo)
        start_button.pack(padx=20, pady=20)


# Run the code
app = Main()
# app.state("zoomed")
app.configure(background="lightblue", highlightbackground="lightblue")

# Appear on the middle of the screen
app_width = 1000
app_height = 700
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width/2) - (app_width/2)
y = (screen_height/2) - (app_height/2)
app.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

app.minsize(width=900, height=670)
app.title("MyGui")
app.iconbitmap("logo.ico")
app.mainloop()