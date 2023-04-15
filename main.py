import tkinter.messagebox
import webbrowser
import pygame
import time
from functools import partial
from tkinter import ttk
import imdb_recommendation_system as ims
from tkHyperlinkManager import *


def play_menu_sound(option):

    if option == 'menu_bar':
        pygame.mixer.music.load('music/button-11.wav')
        pygame.mixer.music.play()
    elif option == 'quit':
        pygame.mixer.music.load('music/quit.wav')
        pygame.mixer.music.play()
        time.sleep(0.3)
        root.destroy()


def open_popup():
    tkinter.messagebox.showinfo('How it Works?', 'Using Cosine Similarity on IMDb dataset!')


def update_values():
    """
    :return: None
    Updates the content in the dropdown menu based on the keyword entered in the text field.
    """

    filter_str = combo1.get().lower()
    filter_str = ' '.join([word for word in re.split(r'\s+', filter_str) if word != ''])  # handling white space
    # if no input is provided show the entire database
    if filter_str == '':
        combo1['values'] = movie_data
    # else filter based on the input
    else:
        filtered_list_1 = []  # holds values that starts with the input string
        filtered_list_2 = []  # holds values that matches the input pattern in the database
        for value in movie_data:
            if value.lower().startswith(filter_str):
                filtered_list_1.append(value)
            elif filter_str in value.lower():
                filtered_list_2.append(value)
        combo1['values'] = filtered_list_1 + filtered_list_2  # so that values of filtered_list_1 appear first


def open_link(my_url):
    """
    :param my_url: URL
    :type my_url: str
    :return: None
    Opens the provided URL in your default browser.
    """

    webbrowser.open_new(url=my_url)


def get_text(event=None):
    """
    :param event: None
    :return: None
    Gets the recommendations and shows it in a text widget.
    """

    text_widget = Text(frame, font='Courier 13 italic', cursor='arrow', bg='#FFFAFA', height=11, width=65)
    hyperlink = HyperlinkManager(text_widget)
    text_widget.tag_configure('tag-center', justify='center')
    text_widget.tag_configure('tag-left', justify='left')
    query = combo1.get()  # get input from combo widget
    query = ' '.join([word for word in re.split(r'\s+', query) if word != ''])  # handling white space
    text = ims.get_recommendations(query)
    if text is None:  # if the movie/tv show not found print some tips
        text = "\n\n\nItem not found!\n"
        text_widget.insert(1.0, text, 'tag-center')
        text_widget.insert(END, '\nTry Searching again', 'tag-center')
    else:  # if found iterate over the DataFrame to create hyperlinks in the text widget
        text_widget.delete(1.0, END)  # clear previous entries
        for idx, title, imdb_url in text.itertuples():  # iterating over the DataFrame as tuples
            text_widget.insert(END, title, hyperlink.add(partial(open_link, imdb_url)))  # insert hyperlinks in the
            # widget
            if idx != 9:  # if not the last index, insert a new line after the previous entry
                text_widget.insert(END, '\n')
                text_widget.insert(END, '\n')
    text_widget.config(highlightcolor='black', highlightbackground="black", highlightthickness=2)
    text_widget.place(x=370, y=310)
    # adding scrollbar to the text widget
    scroll_y = Scrollbar(text_widget, orient='vertical', command=text_widget.yview)
    scroll_y.place(x=185*3 + 30, relheight=1)
    text_widget.configure(state='disabled', yscrollcommand=scroll_y.set)  # making the text widget un-editable


# initialize master window
root = Tk()  # creates a window in which we work our gui
root.title("Netflix-Recommendation")
root.geometry('1360x768')  # width x height
root.resizable(width=False, height=False)  # restricts window size


# creating a frame to place the widgetsS
frame = Frame(root).place(x=150, y=25)
frame_bg_image = PhotoImage(file=r'net1.png')
frame_label = Label(frame, height="150",width="350", image=frame_bg_image)
frame_label.pack()

# creating widgets
label1 = Label(frame, font='Courier 13 italic', text='Select a Movie/TV Show/Documentary!', height=2, width=65,
               bg='#c21a09', highlightthickness=2, highlightbackground="black")
movie_data = ims.get_movie_data()  # get the database of all the movies/tv shows
combo1 = ttk.Combobox(frame, width=64, font=("Courier", 13), postcommand=update_values, values=movie_data)
button1 = Button(frame, text='GO!', font='Arial 13 bold italic', bg='#800000', width=42, command=get_text)
instructions_text = Text(frame, font='Courier 13 italic', cursor='arrow', bg='#FFFAFA', height=11, width=65)

# print instructions in the text widget
instructions_text.tag_configure('tag-center', justify='center')
instructions_text.tag_configure('tag-center-underline', justify='center', underline=1)
instructions_text.tag_configure('tag-left', justify='left')
instructions_text.insert(1.0, '\nWelcome to Netflix recommendation system!\n', 'tag-center')
instructions_text.insert(END, "\nInstructions\n", 'tag-center-underline')
instructions_text.insert(END, "\n 1. Enter the keywords of a TV Show/Movie/Documentary. \n 2. Select from the "
                              "dropdown menu. \n 3. Press ENTER or 'GO!' to search. \n 4. Click on the Hyperlink to "
                              "take you to the IMDb website.", 'tag-center')
# placing widgets
instructions_text.config(highlightcolor='black', highlightbackground="black", highlightthickness=2)
instructions_text.place(x=370, y=310)
instructions_text.configure(state='disabled')
label1.place(x=370, y=150)
root.option_add('*TCombobox*Listbox.font', ("Courier", 13))
root.config(menu=menu)
combo1.place(x=370, y=213, height=32)
button1.place(x=480, y=260)
combo1.bind('<Return>', get_text)

# main loop
if __name__ == '__main__':
    pygame.mixer.init()
    root.mainloop()
