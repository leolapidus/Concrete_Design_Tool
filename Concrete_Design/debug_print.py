import sys

def debug(expression):
    frame = sys._getframe(1)

    v = eval(expression, frame.f_globals, frame.f_locals)

    try:
        print(expression, '=', v)
        print(expression, "'", '=', v.g)
    except:
        print(expression, '=', v)