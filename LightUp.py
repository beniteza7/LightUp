import ply.lex as lex
import ply.yacc as yacc
import CodeGenerator as generate
import os

######################### LEXER #########################

tokens = [
    #Equals
    'EQUALS',
    #Color
    'RED', 'BLUE', 'GREEN', 'YELLOW', 'ORANGE', 'PURPLE', 'WHITE',
    # #RGB Color
    # 'RGB',
    #Animation Type
    'THEATER_CHASE_RAINBOW', 'RAINBOW', 'RAINBOW_CYCLE', 'COLOR_WIPE', 'THEATER_CHASE',
    #Number
    'NUMBER',
    #Parenthesis and coma
    'LP', 'RP', 'COMA',
    #Animate
    'ANIMATE',
    #Button Position
    'BUTTON_UP', 'BUTTON_DOWN',
    # Variable Name
    'NAME',
    #Start and End
    'START', 'END',
    #NEW LINE
    'NEW_LINE'
]

t_NUMBER = r'[0-9]+'
t_LP = r'\('
t_RP = r'\)'
t_COMA = r'\,'
t_EQUALS = r'\='
# t_ignore = ' '
t_ignore = ' \t\n'


def t_BUTTON_UP(t):
    r'BUTTON_UP'
    t.value = 'BUTTON_UP'
    return t


def t_BUTTON_DOWN(t):
    r'BUTTON_DOWN'
    t.value = 'BUTTON_DOWN'
    return t


def t_START(t):
    r'START'
    t.value = 'START'
    return t


def t_END(t):
    r'END'
    t.value = 'END'
    return t


def t_RED(t):
    r'RED'
    t.value = 'RED'
    return t


def t_BLUE(t):
    r'BLUE'
    t.value = 'BLUE'
    return t


def t_GREEN(t):
    r'GREEN'
    t.value = 'GREEN'
    return t


def t_YELLOW(t):
    r'YELLOW'
    t.value = 'YELLOW'
    return t


def t_ORANGE(t):
    r'ORANGE'
    t.value = 'ORANGE'
    return t


def t_PURPLE(t):
    r'PURPLE'
    t.value = 'PURPLE'
    return t


def t_WHITE(t):
    r'WHITE'
    t.value = 'WHITE'
    return t


def t_RGB(t):
    r'RGB'
    t.value = 'RGB'
    return t


def t_THEATER_CHASE_RAINBOW(t):
    r'THEATER_CHASE_RAINBOW'
    t.value = 'THEATER_CHASE_RAINBOW'
    return t


def t_RAINBOW_CYCLE(t):
    r'RAINBOW_CYCLE'
    t.value = 'RAINBOW_CYCLE'
    return t


def t_RAINBOW(t):
    r'RAINBOW'
    t.value = 'RAINBOW'
    return t


def t_COLOR_WIPE(t):
    r'COLOR_WIPE'
    t.value = 'COLOR_WIPE'
    return t


def t_THEATER_CHASE(t):
    r'THEATER_CHASE'
    t.value = 'THEATER_CHASE'
    return t


def t_ANIMATE(t):
    r'ANIMATE'
    t.value = 'ANIMATE'
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])


lexer = lex.lex()


def p_execute(p):
    '''
    execute : command
            | var_assign
            | empty
    '''
    print(p[1])


def p_var_assign(p):
    '''
    var_assign : NAME EQUALS color
               | NAME EQUALS rgb
               | NAME EQUALS miliseconds
               | NAME EQUALS animation
               | NAME EQUALS button_pos
    '''
    p[0] = ('=', p[1], p[3])
    generate.createVariable(p[0])


def p_command(p):
    '''
    command : ANIMATE animation color miliseconds
            | ANIMATE animation rgb miliseconds
            | START
            | END
    '''
    if p[1] == 'START':
        if os.path.isfile("arduinoCode.ino"):
            os.remove("arduinoCode.ino")
    elif p[1] == 'END':
        generate.upload()
        generate.terminalUpload()
    else:
        p[0] = (p[1], p[2], p[3], p[4])
        generate.animate(p[0])


def p_button_pos(p):
    '''
    button_pos : BUTTON_UP
               | BUTTON_DOWN
    '''
    p[0] = p[1]


def p_button_pos_var(p):
    '''
    button_pos : NAME
    '''
    p[0] = p[1]
    # p[0] = ('var', p[1])


def p_rgb(p):
    'rgb : LP NUMBER COMA NUMBER COMA NUMBER RP'
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]


def p_rgb_var(p):
    '''
    rgb : NAME
    '''
    p[0] = p[1]
    # p[0] = ('var', p[1])


def p_miliseconds(p):
    '''
    miliseconds : NUMBER
    '''
    p[0] = p[1]


def p_miliseconds_var(p):
    '''
    miliseconds : NAME
    '''
    p[0] = p[1]
    # p[0] = ('var', p[1])


def p_color(p):
    '''
    color : RED
          | BLUE
          | GREEN
          | YELLOW
          | ORANGE
          | PURPLE
          | WHITE
    '''
    p[0] = p[1]


def p_color_var(p):
    '''
    color : NAME
    '''
    p[0] = p[1]
    # p[0] = ('var', p[1])


def p_animation(p):
    '''
    animation : RAINBOW
              | RAINBOW_CYCLE
              | THEATER_CHASE_RAINBOW
              | COLOR_WIPE
              | THEATER_CHASE
    '''
    p[0] = p[1]


def p_animation_var(p):
    '''
    animation : NAME
    '''
    p[0] = p[1]
    # p[0] = ('var', p[1])


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def p_error(p):
    print("Syntax error found!")


parser = yacc.yacc()


def translateCode(p):
    try:
        LightUpSource = open(p, 'r')
    except IOError:
        print("Error opening file")
        exit()

    for line in LightUpSource:
        try:
            parser.parse(line)
        except IOError:
            print("Error opening file!")
            exit()


# file = 'LightUpCode.txt'
# translateCode(file)
