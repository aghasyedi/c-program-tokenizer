import lexer,tkinter as tk
from tabulate import tabulate
from collections import Counter
from tkinter import filedialog

def main():
    file =''
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file = filedialog.askopenfilename()

    root.destroy()

    # file = '/Users/aghasyedi/Documents/Lexical/ShivyC-master/tests/general_tests/count/Count.c'
    if file =='':
        file ='test.c'
    code = [open(file).read() for file in [file]][0]

    list_token, tokens_type = lexer.tokenizer(code, file)

    operators = ['+', '-', '*', '**', '/', '//', '%', '<<', '>>', '&','|',
                 '^', '~', '<', '>', '<=', '>=', '==', '!=', '<>', '+=',
                 '-=', '*=', '/=', '//=', '%=', '**=', '&=', '|=', '^=', '>>=', '<<=']

    delimiters = ['(', ')', '[', ']', '{', '}', ',', ':', '.', '`', '=', ';']
    special_symbols = ["'", '"', '#', '\\', '@']

    # enable this to get without lines
    '''
    i = len(list_token)-1
    while i!=-1:
        if list_token[i] == "--blank--":
            list_token.pop(i)
            tokens_type.pop(i)
        i = i-1
    '''
    
    mydata = [[list_token[i], tokens_type[i]] for i in range(len(list_token))]
    head = ["Token", "Token Type"]

    #   Seperate Symbols into Delimiters(seperators), Operators, Special Symbols
    for i in range(len(mydata)):
        if str(mydata[i][0]) in operators:
            mydata[i][1] = 'Operator'
        if str(mydata[i][0]) in delimiters:
            mydata[i][1] = 'Seperator'
        if str(mydata[i][0]) in special_symbols:
            mydata[i][1] = 'Special Symbol'

    frequency_counter = Counter(tokens_type)
    num_elements = len(frequency_counter)

    print("\033[92m\033[1mFrequencies\033[0m")
    [print(f"    => {element:_<18s}{frequency}")      #prints the frequencies
        for index, (element, frequency) in enumerate(frequency_counter.items())
        if index < num_elements - 1]

    print("___________________________")
    print("Total number of tokens: ",len(list_token))

    
    formatted_data = tabulate(mydata, headers=head, tablefmt="fancy_grid")

    # Create window
    root = tk.Tk()
    root.title("Tabulated Data")
    root.focus_force()
    
    
    screen_width = root.winfo_screenwidth()-800
    screen_height = root.winfo_screenheight()-100
    root.geometry(f"{screen_width}x{screen_height}+750+0")      #screen size adjustment
    
    text = tk.Text(root, wrap="none")
    text.insert(tk.END, f"Total number of tokens: {len(list_token)}\n")
    text.insert(tk.END, "Press 'ESC' to exit\n")
    text.insert(tk.END, formatted_data)     #inserting data into table format
    text.insert(tk.END, "\nPress 'ESC' to exit")

    text.config(state=tk.DISABLED)          #disable text editing
    text.pack(fill=tk.BOTH, expand=True)


    rootx = tk.Tk()
    rootx.focus_force()
    rootx.title("Tabulated Data")
    
    
    screen_width = rootx.winfo_screenwidth()-800
    screen_height = rootx.winfo_screenheight()-100
    rootx.geometry(f"{screen_width}x{screen_height}+0+0")
    text_widget = tk.Text(rootx, wrap="none")
    text_widget.pack(side=tk.LEFT, fill=tk.Y)
    text_widget.insert(tk.END, code)
    text_widget.config(state=tk.DISABLED)
    text_widget.pack(fill=tk.BOTH, expand=True)
    
    root.bind("<Key>", lambda event: (root.destroy(), rootx.destroy()) if event.keysym == "Escape" else None)
    rootx.bind("<Key>", lambda event: (root.destroy(), rootx.destroy()) if event.keysym == "Escape" else None)

    
    '''STARTS THE WINDOW'''
    root.mainloop()
    rootx.mainloop()

    # for i in range(len(list_token)):
    #     print(list_token[i],"\t\t\t\t", tokens_type[i])

main()


'''
Keyword
Identifier
Symbol
Seperator
Operator
Constant
'''