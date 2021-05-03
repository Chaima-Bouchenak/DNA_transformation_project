# coding ~utf-8

"""
User interface project setUp
"""
import tkinter as tk
from tkinter import ttk
from tkinter import Button, Tk
from tkinter.filedialog import asksaveasfile, askopenfile
from tkinter.messagebox import askquestion, showerror, showinfo
from step_by_step import Steps
import json
import os


class UserInterface(tk.Tk):
    """Set the global interface of the project, user friendly :)
    """

    def __init__(self) -> None:
        """ constructor
        """
        super().__init__()
        self.Steps = None
        self.title('Welcome to our DNA compression project') # set Tk main window title

    def tk_main_window(self) -> None:
        """ Prepare the main Tk window
        set the text box widget and guide user with labels
        """

        Main_Text_Box.text_box_widget(self)  # set the text box widget

        # set user Guide labels
        user = tk.Label(self, text='Please click above or enter the desired sequence in the box below*',
                        font='Raleway 10 bold', fg='#737073')
        user.place(x=110, y=30)

        note = tk.Label(self, text='*', font='Raleway 10 bold', fg='#737073')
        note.place(x=30, y=170)

        note_1 = tk.Label(self, text='- BWT retransofmation : the sequence must have a "$" signe'
                          , font='Raleway 10 bold', fg='#737073')
        note_1.place(x=40, y=180)

        note_2 = tk.Label(self, text='- Huffman decompression : no inpute sequence, choose adequate files (Tree + compressed sequence)',
                          font='Raleway 10 bold', fg='#737073')
        note_2.place(x=40, y=200)

    def main_windoow_buttons(self) -> None:
        """create button for each process of the project in the main Tk window
        There's four general process
        """
        # Set up a buttons names in a list
        buttons = ["BWT transformation", "BWT retransformation", "compression huffman", "decompression huffman"]
        widgets_button = {}
        i, j = 0, 0

        # Generate specific place for each button
        for idi in buttons:
            button = Button(text=idi)
            widgets_button[idi] = button
            button.grid(row=i + 1, column=j)

            j += 1
        # Bind each button to it specific function
        widgets_button[buttons[0]].config(command=self.bwt_encryption)
        widgets_button[buttons[1]].config(command=self.bwt_decryption)
        widgets_button[buttons[2]].config(command=self.compression)
        widgets_button[buttons[3]].config(command=self.decompression)

    def popup_window(self, title) -> None:
        """ create popup windows on the main one
            title : the title of the popup window
        """
        # set up variables as global to use then every where when needed
        global top
        global next_button
        global next_button_text

        # creation of the popup window
        top = tk.Toplevel()  # setup
        top.title(title)
        Main_Text_Box.text_box_widget(top)  # add text box in the popup window
        next_button_text = tk.StringVar()
        next_button = tk.Button(top, textvariable=next_button_text, height=2, width=10)  # create the next step button
        next_button_text.set('next step')  # name the button
        next_button.place(x=550, y=100)  # place it on the popup window

    def get_text_box_sequence(self) -> str:
        """ get the user sequence of the text box presented in the main Tk window.
        """
        seq_content = text_box_window.get(1.0, 'end') # get sequence from text box widget
        return seq_content  # save it for later treatment/process

    def open_in_file(self, decompression: bool = None):

        """ reate the file chooser for the interface
            for the decompression process (when decompression=True)
            choose text file of the decompression and the Tree json file
            for the other process,
            open the user specific text file
        """

        if not decompression:

            file = askopenfile(parent=self, mode='r', title='choose a file',
                               filetypes=(('Text files', '*.txt'), ('Fasta file', '*.fasta')))

            self.Steps = Steps(file.name)
            size_of_original_file = os.path.getsize(file.name)

            return size_of_original_file

        else:
            showinfo('Huffman Decompression process', 'please pick up the txt file and the json Tree file to decompress')

            file_decompress = askopenfile(parent=self, mode='r', title='Choose a decompression file',
                                          filetypes=(('Text file', '*.txt'), ("All Files", "*.*")))
            self.Steps = Steps(file_decompress.name)

            json_file = askopenfile(parent=self, mode='r', title='Choose the associated json file',
                                    filetypes=(('Json file', '*.json'), ('All File', '*.*')))

            with open(json_file.name) as f:
                data = json.load(f)

            return (file_decompress, data)

    def save_file(self, tree_decomp_data: dict = None, sequence: str = None) -> None:

        """ A method to save the files
            compression, two files: text first of compressed sequence "unicode"
            and json file of decompression Tree
        """

        if tree_decomp_data: # in decompress process
            file_to_save = asksaveasfile(initialdir=os.getcwd(), title="Select File", mode='w',
                                         defaultextension='txt')

            with open(file_to_save.name, 'w', encoding='utf8') as f, open(
                    file_to_save.name[:-4] + '_json_file.json', 'w') as jsn:
                f.write(unicode)
                json.dump(tree_decomp_data, jsn)

            size_of_compressed_file = os.path.getsize(file_to_save.name)
            showinfo('Saved file',
                     'Well done !\nThe size of the compressed file has significantly decreased')
            top.quit()

        else:  # in remain processes
            file_to_save = asksaveasfile(initialdir=os.getcwd(), title="Select File", mode='w', defaultextension='txt')
            with open(file_to_save.name, 'w', encoding='utf8') as f:
                f.write(sequence)
            showinfo('Saved File', 'File downloaded in your machine!')
            top.quit()

    def compression(self, all_in_one: bool = None) -> None:

        """ A method to proceed the compression process step by step and the compression
            process is one/'s (all_in_one).
        """

        global binary_sequence
        global encoder
        global unicode
        global size_of_original_file

        # Get user basic ADN sequence , uncompressed
        seq_content = self.get_text_box_sequence()

        try:
            if not all_in_one: # if user choice is step by step display
                if seq_content == '\n': # if sequence is empty
                    size_of_original_file = self.open_in_file() # ask user to use a file
                    self.Steps.get_sequence_from_file()

                else: # if used provided the DNA sequence correctly
                    self.Steps = Steps('')
                    self.Steps.sequence = seq_content.strip() # take off spaces

                self.popup_window('Huffman compression')

                results = self.Steps.compression_process_without_bwt(self.Steps.sequence)
                encoder = results.pop('encoder')

                unicode = results[list(results)[-1]]
                binary_sequence = results[list(results)[1]]

                self.compression_decompression_helper(results)

            else: # if user choice is all in one display

                results = self.Steps.compression_process_without_bwt(self.Steps.sequence)
                encoder = results.pop('encoder')

                unicode = results[list(results)[-1]]
                binary_sequence = results[list(results)[1]]

                self.compression_decompression_helper(results)

        except:
            showerror('Error file!', 'Please enter the right file')

    def compression_decompression_helper(self, results: dict, decompression: bool = None,
                                         all_in_one_dec: bool = None) -> None:

        """ help the step by step compression and decompression process
        """

        try:
            first_key = list(results)[0]
            inserted_object = first_key + '\n' + results[first_key] + '\n'
            self.insert_in_text_box(inserted_object)

            if decompression:
                if all_in_one_dec:
                    next_button.configure(command=lambda: self.delete_text_box(first_key, results,
                                                                               decompression=True, all_in_one_dec=True))
                else:
                    next_button.configure(command=lambda: self.delete_text_box(first_key, results, decompression=True))

            else:
                next_button.configure(command=lambda: self.delete_text_box(first_key, results))

        except IndexError:
            if decompression:
                if all_in_one_dec:
                    self.all_in_one_compression_decompression_helper(all_in_one_dec=True)
                else:
                    self.save_processed_file(decompression=True)
                    text_box.delete(3.0, 'end')
            else:
                self.save_processed_file()

    def delete_text_box(self, first_key: str, results: dict, decompression: bool = None, all_in_one_dec: bool = None) -> None:

        """This method is created to delete the text in the text box.
        """

        if decompression:
            text_box.delete(1.0, 'end')

            if len(results) != 0:
                results.pop(first_key)

                if all_in_one_dec:
                    self.compression_decompression_helper(results, decompression=True, all_in_one_dec=True)
                else:
                    self.compression_decompression_helper(results, decompression=True)
            else:
                self.save_file(sequence=decompressed_sequence)
        else:
            text_box.delete(1.0, 'end')

            if len(results) != 0:
                results.pop(first_key)
                self.compression_decompression_helper(results)
            else:
                tree_decomp_data = {
                    'encoder': encoder,
                    'binary_seq': binary_sequence
                }
                self.save_file(tree_decomp_data)

    def insert_in_text_box(self, inserted_object: str) -> None:
        """ A method to insert text in the text box
        """
        global text_box

        # adding a scroll bar
        yscrollbar = tk.Scrollbar(top)

        # creating the text box
        text_box = tk.Text(top, height=10, width=40,
                           yscrollcommand=yscrollbar.set)

        text_box.insert('end', inserted_object)
        text_box.tag_configure('center', justify='center')
        text_box.tag_add('center', 1.0, 'end')
        text_box.place(x=160, y=50)
        yscrollbar.place(in_=text_box, relx=1.0, relheight=1.0, bordermode='outside')
        yscrollbar.config(command=text_box.yview)

    def save_processed_file(self, decompression: bool = None) -> None:

        """ A method that creates save patterns (add a save button and a responsive paragraph to
            tell that the process is achived and ask if we want to save the sequence in a file or not)
        """

        next_button_text.set('Save')
        text_box.insert('end', '\nFinish, whould you like to save the sequence?')
        text_box.tag_configure('center', justify='center')
        text_box.tag_add('center', 1.0, 'end')
        next_button.place_configure(x=250, y=200)

    def decompression(self, all_in_one_dec: bool = None) -> None:

        """ process step by step or the all_in_one(=True) Huffman decompression
            Notice: for the decompression we can't enter sequence manually because we need the json file.
        """
        global decompressed_sequence

        try:
            seq_content = self.get_text_box_sequence()

            if seq_content != '\n':
                showerror('Error!', 'Please enter a file')
                text_box_window.delete(1.0, 'end')

            files = self.open_in_file(decompression=True)
            self.popup_window('Huffman decompression')
            file_decompress = files[0]
            json_file = files[1]

            results_deco = self.Steps.decompression_process_without_bwt(file_decompress.name, json_file['encoder'],
                                                                             json_file['binary_seq'])
            decompressed_sequence = results_deco[list(results_deco)[-1]]

            if all_in_one_dec:
                self.compression_decompression_helper(results_deco, decompression=True, all_in_one_dec=True)
            else:
                self.compression_decompression_helper(results_deco, decompression=True)
        except:
            showerror('Error file!', 'Please enter the right file')

    def bwt_encryption(self, all_in_one: bool = None) -> None:
        """ proceed BWT transformation process, as user preference : step by step or all in one (=True).
        """
        global bwt_matrix
        global gen
        global bwt_sequence
        global size_of_original_file

        seq_content = self.get_text_box_sequence()

        try:
            if seq_content == '\n':
                size_of_original_file = self.open_in_file()
                self.Steps.get_sequence_from_file()
            else:
                self.Steps = Steps('')
                self.Steps.sequence = seq_content.strip()

            # widget to ask question
            ask_quest = askquestion('BWT Transformation',
                                    'Would you like it to be done step by step ?')
            results_bwt = self.Steps.bwt_encryption_step_by_step()
            bwt_matrix = results_bwt[0]
            bwt_sequence = results_bwt[1]

            if ask_quest == 'yes':
                gen = 'First Step: BWT matrix construction '
                self.popup_window('BWT Transformation')
                self.insert_in_text_box(gen)

                if all_in_one:
                    next_button.configure(command=lambda: self.get_next(gen, all_in_one=True))
                else:
                    next_button.configure(command=lambda: self.get_next(gen))

            else: # if the anszer is no
                self.popup_window('BWT Transformation')
                text = 'The Bwt sequence\n' + bwt_sequence
                self.insert_in_text_box(text)

                if not all_in_one:
                    self.save_processed_file()
                    next_button.configure(command=lambda: self.save_file(sequence=bwt_sequence))
                else:
                    next_button.configure(command=self.all_in_one_compression_helper)

        except AttributeError:
            showerror('File Error', 'Please enter the right file!')

    def step_tw_bwt_dec(self) -> None:
        """Helper method to proceed the Burrows Wheeler step by step encryption
        """

        gen = 'Step2: Sorted matrix construction,\nThe bwt sequence is the one who has $ in the end'
        self.insert_in_text_box(gen)
        next_button.configure(command=lambda: self.get_next(gen, decryption=True, row_index=row_index))

    def bwt_decryption(self, all_in_one_dec: bool = None):
        """ proceed BWT re-transformation process, as user preference : step by step.
               """
        global bwt_matrix_re
        global sequence_re
        global row_index

        seq_content = self.get_text_box_sequence()
        if all_in_one_dec:
            self.Steps.sequence = decompressed_sequence

        else:
            if seq_content == '\n':
                self.open_in_file()
                self.Steps.get_sequence_from_file()
                self.popup_window('BWT decryption')
            else:
                self.Steps = Steps('')
                self.Steps.sequence = seq_content.strip()
                self.popup_window('BWT decryption')

        results_bwt = self.Steps.bwt_decryption()
        bwt_matrix_re = results_bwt[0]
        sequence_index = results_bwt[1]
        sequence_re = sequence_index[0]
        row_index = sequence_index[1]
        gen = 'Step 1: The Bwt sequence \n' + self.Steps.sequence
        self.insert_in_text_box(gen)
        next_button.configure(command=self.step_tw_bwt_dec)

    def all_in_one_compression_decompression_helper(self, all_in_one_dec=None):

        """ Helper method for the all_in_one compression and decompression process
        """
        if all_in_one_dec:
            text = 'Now the decryption process'
            self.insert_in_text_box(text)
            next_button.configure(command=lambda: self.bwt_decryption(all_in_one_dec=True))

        else:
            gen = 'Now the compression process'
            self.insert_in_text_box(gen)
            self.Steps.sequence = bwt_sequence
            next_button.configure(command=lambda: self.compression(all_in_one=True))

    def get_next(self, gen: str, decryption: bool = None, row_index: int = None, all_in_one: bool = None):
        """ Get the next display of the Burrows Wheeler Matrix generator
        @:param
            gen: the seq_content to be inserted in the text box
            decryption: a boolean to precise if we procees the encryption or the decryption process. Defaults to None.
            row_index : the index of the row of the original sequence in the Burrows Wheeler reconstruction matrix
                             this variable is used to proceed the coloration of the sequence in the matrix. Defaults to None.
            all_in_one (bool): for the all_in_one compression process
        """
        if not decryption:

            try:
                gen = ''
                gen += text_box.get("1.0", "end") + next(bwt_matrix)
                self.insert_in_text_box(gen)

            except StopIteration:
                sorted_bwt = []
                indexx = 3

                bwt = self.Steps.bwt_encryption_step_by_step()
                sorted_matrix = ''

                for i in sorted(bwt[0]):
                    sorted_matrix += str(i) + '\n'
                    sorted_bwt.append(str(i))

                gen = 'Step 2: The sort of the matrix\nThe BWT sequence is presented in the last column\n' + sorted_matrix + '\n\nBwt Sequence: ' + bwt_sequence
                self.insert_in_text_box(gen)

                for i in sorted_bwt:
                    j = str(indexx) + '.' + str(len(i) - 1)
                    text_box.tag_add('color', j)
                    text_box.tag_config('color', foreground='red')
                    indexx += 1

                if not all_in_one:
                    self.save_processed_file()
                    next_button.configure(command=lambda: self.save_file(sequence=bwt_sequence))

                else:
                    next_button.configure(command=self.all_in_one_compression_decompression_helper)
        else:
            try:
                gen = ''
                gen += text_box.get("1.0", "end") + next(bwt_matrix_re)
                self.insert_in_text_box(gen)

            except StopIteration:
                gen = text_box.get("1.0", "end") + "\n\nThe sequence: " + str(sequence_re)
                self.insert_in_text_box(gen)
                text_box.tag_add('color_re', str(3 + row_index) + '.0',
                                 str(3 + row_index) + '.' + str(len(sequence_re) + 1))
                text_box.tag_config('color_re', foreground='red')
                self.save_processed_file()
                next_button.configure(command=lambda: self.save_file(sequence=sequence_re))

    def main_loop(self) -> None:
        """Main loop of our tkinter object, for the appearence of the interface
        """
        self.mainloop()

class Main_Text_Box:

    """Set the main text box in the Tk window, for first and step by step display """

    @staticmethod
    def text_box_widget(root:tk.Tk) -> None:
        """ A static method to place the logo (genome.png) in the window.
        """
        global text_box_window  # set as global variable to be used every where when needed

        root.geometry('650x250')  # chosen dimensions of the Tk window
        yscrollbar = tk.Scrollbar(root)  # scroll bar for long text displays
        text_box_window = tk.Text(root, height=10, width=40,
                           yscrollcommand=yscrollbar.set) # create the main text box
        # text_box_window.tag_add('center', 1.0, 'end')
        text_box_window.place(x=160, y=50) # set the text box in the window

        yscrollbar.place(in_=text_box_window, relx=1.0, relheight=1.0, bordermode='outside') # put scroll bar inside the text box
        yscrollbar.config(command=text_box_window.yview)  # scrollbar function
