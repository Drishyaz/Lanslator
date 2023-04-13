import PySimpleGUI as pg
import compiler_api as comp

buttons_row = [
    pg.Button("Browse"),
    pg.Input('File Name', key = "-FILE NAME-"),
    pg.Button('Compile'),
    pg.Button('Interchange'),
    pg.Button('Translate'),
    pg.Button('Save')
]

languages = ['Java','Python']
text_col_one = [
    [
        pg.Combo(languages, expand_x = True, enable_events = True, readonly = False, key = '-COMBO1-'),
        pg.Button("Clr",key = '-CLR1-')
    ],
    [pg.Multiline(size = (50,60), enable_events=True, key='-IN-', expand_y=True)]
]
text_col_two = [
    [
        pg.Combo(languages, expand_x = True, enable_events = True, readonly = False, key = '-COMBO2-'),
        pg.Button("Clr",key = '-CLR2-')
    ],
    [pg.Multiline(size = (50,60), enable_events=True, key='-OUT-', expand_y=True)]
]
error_col = [
    [
        pg.Text('Compiler Box'),
        pg.Button('Clear')
    ],
    [
        pg.Multiline()
    ]
]

layout = [
    [buttons_row],
    [
        pg.Column(text_col_one),
        pg.VSeperator(),
        pg.Column(text_col_two)
    ],
    [error_col]
]

window = pg.Window("Lanslator",layout, size = (800,600))

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
        
            window["-FILE NAME-"].update(file_name)
            window["-IN-"].update(lines)

            if file.endswith(".py"):
                window['-COMBO1-'].update('Python')
                window['-COMBO2-'].update('Java')
            elif file.endswith(".java"):
                window['-COMBO1-'].update('Java')
                window['-COMBO2-'].update('Python')
        else:
            pg.popup("You didn't select a file OR you have to select .py or .java files")
        
    elif event == '-CLR1-':
        window['-IN-'].update('')
    elif event == '-CLR2-':
        window['-OUT-'].update('')

    elif event == 'Save':
        updated_content = values['-IN-']
        with open(file,'w') as f:
            f.write(updated_content)
        pg.popup('File Updated!')

    elif event == 'Interchange':
        prog1 = values['-COMBO1-']
        prog2 = values['-COMBO2-']
        window['-COMBO1-'].update(prog2)
        window['-COMBO2-'].update(prog1)
        window['-IN-'].update('')
        window['-OUT-'].update('')

    elif event == 'Compile':
        comp.main()
        #STILL WORKING ON IT

window.close()