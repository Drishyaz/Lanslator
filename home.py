import PySimpleGUI as pg
import os
import compiler_api as comp
from sys import *
#import lexer as l
import parser_1 as p

def font_window() :
    font_style = [
        'System','Terminal','Modern','Roman','Script','Courier','Arial','Calibri','Cambria','Candara','Consolas','Constantia','Georgia','Onyx'
    ]
    font_style_col = [
        [pg.Input(key = '-style-',expand_x=True)],
        [pg.Listbox(font_style,enable_events=True, size = (40,15),key='-style_list-',expand_x=True)],
    ]
    sample_font = [
        [pg.Text('Sample font look', font = ('Arial',12))],
        [pg.Text('AaByYyZz',font = ('Arial',22), key = '-sample-')]
    ]
    btn_col = [
        [pg.OK()],
        [pg.Cancel()]
    ]
    layout = [
        [pg.Column(font_style_col)],
        [
            pg.Column(sample_font),
            pg.VSeperator(),
            pg.Column(btn_col)
        ]
    ]
    
    window = pg.Window("Font", layout, modal = True, size = (400,400))

    while True:
        event,values = window.read()
        sample = 'AaByYyZz'
        if event == pg.WIN_CLOSED or event == 'Cancel':
            break

        elif event == '-style_list-':
            selected_style = values['-style_list-'][0]
            window['-style-'].update(selected_style)
            try:
                window['-sample-'].update(font = (selected_style,22)) 
            except NameError:
                window['-sample-'].update(font = (selected_style,22))

        elif event == 'OK':
            #selected_style = values['-style_list-'][0]
            break
            
    window.close()
    try:
        return selected_style
    except UnboundLocalError:
        pass

menu_bar = [
    ['File',['Browse','Save Source','Save Target']],
    ['Compile',['Compile','Check Usage']],
    ['Translate',['Translate','Interchange']],
    ['Settings',['Font']]
]

languages = ['Java','Python']

# READS THE FONT PROPERTIES FROM THE font_settings FILE
with open("font_settings.txt","r") as f:
    lines = f.read()

# EXTRACTS THE FONT PROPERTIES FROM THE FILE AND UPDATES THE EDITORS ACCORDINGLY
font = ["",12]
content = lines.split(':')
font[0] = lines[1]
font = tuple(font)

text_col_one = [
    [
        pg.Combo(languages, expand_x = True, enable_events = True, readonly = False, key = '-COMBO1-'),
        pg.Button("Clr",key = '-CLR1-')
    ],
    [pg.Multiline(size=(50,30), font=font, enable_events=True, key='-IN-',expand_x=True)]
]
text_col_two = [
    [
        pg.Combo(languages, expand_x = True, enable_events = True, readonly = False, key = '-COMBO2-'),
        pg.Button("Clr",key = '-CLR2-')
    ],
    [pg.Multiline(size=(50,30), font=font, enable_events=True, key='-OUT-',expand_x=True)]
]
error_col = [
    [
        pg.Text('Compiler Box',expand_x=True),
        pg.Button('Clear',key='-CLR3-')
    ],
    [
        pg.Multiline(size=(30,10), font=font, enable_events=True, key='-ERROR-', expand_x=True)
    ]
]

layout = [
    [pg.Menu(menu_bar)],
    [
        pg.Column(text_col_one),
        pg.VSeperator(),
        pg.Column(text_col_two)
    ],
    [error_col]
]

window = pg.Window("Lanslator",layout,font=('Arial',12), resizable=True, size = (1000,850))

while True:
    event, values = window.read()

    if event == pg.WIN_CLOSED:
        break
    elif event == "Browse":
        file = pg.popup_get_file('Select a Python or Java file')
        if file and (file.endswith(".py") or file.endswith(".java")):
            path = file.split('/')
            file_name = path[-1]
            with open(file) as f:
                lines = f.read()
        
            window["-COMBO1-"].update(file_name)
            window["-IN-"].update(lines)

            if file.endswith(".py"):
                window['-COMBO2-'].update('Java')
            elif file.endswith(".java"):
                window['-COMBO2-'].update('Python')
        else:
            pg.popup("You didn't select a file OR you have to select .py or .java files")
        
    elif event == '-CLR1-':
        window['-IN-'].update('')
    elif event == '-CLR2-':
        window['-OUT-'].update('')
    elif event == '-CLR3-':
        window['-ERROR-'].update('')

    elif event == 'Save Source':
        updated_content = values['-IN-']
        with open(file,'w') as f:
            f.write(updated_content)
        pg.popup('File Updated!')

    elif event == 'Save Target':
        try:
            fname = pg.popup_get_text('Enter file name to save as:',title='Save File')
            updated_content = values['-OUT-']
            current_direc = os.getcwd()
            flocation = os.path.join    (current_direc,fname)
            if os.path.exists(flocation):
                pg.popup('The file with the given name \'' + fname + '\' already exists.')
            else:
                with open(fname,'x') as f:
                    f.write(updated_content)
                window['-COMBO2-'].update(fname)
                pg.popup('File Updated!')
        
        except TypeError:
            pass

    elif event == 'Interchange':
        prog1 = values['-COMBO1-']
        prog2 = values['-COMBO2-']
        window['-COMBO1-'].update(prog2)
        if prog1.endswith('.py'):
            window['-COMBO2-'].update('Python')
        elif prog1.endswith('.java'):
            window['-COMBO2-'].update('Java')
        window['-IN-'].update('')
        window['-OUT-'].update('')

    elif event == 'Compile':
        code = values['-IN-']
        if code == "":
            window['-ERROR-'].update('Code Editor is Empty!')
        else:
            res = comp.main(code)
            window['-ERROR-'].update(res)

    elif event == 'Check Usage':
        window['-ERROR-'].update(comp.check_usage())

    elif event == 'Translate':
        source_code = values['-IN-']
        #l.parse(code)
        target_code = p.main(source_code)
        window['-OUT-'].update(target_code)

    elif event == 'Font':
        val = font_window()
        if val == None:
            pass
        else:
            # EVERYTIME NEW FONT STYLE AND SIZE SELCTED, IT IS UPDATED IN THE font_settings FILE
            # SO WHENEVER A NEW WINDOW IS OPENED IT WILL OPEN WITH THE PREVIOUSLY UPDATED FONT SETTINGS
            with open('font_settings.txt',"w") as f:
                content = "font:"+ val
                f.write(content)
            # UPDATES THE EDITOR'S FONT PROPERTIES ACCORDINGLY
            window['-IN-'].update(font=val)
            window['-OUT-'].update(font=val)
            #pg.set_options(font=val)

window.close()
