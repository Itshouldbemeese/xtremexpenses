WINDOW_TITLE = "🫎Moose's Expenses Tracker v0.1.0🫎"

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400


def window_size(width, height):
    '''
    Determine the size and position of the window based
    on the width and height of the screen it's displayed
    on.
    int -- width
    int -- height
    '''
    
    center_x = int((width / 2) - (WINDOW_WIDTH / 2))
    center_y = int((height / 2) - (WINDOW_HEIGHT / 2))

    window_geometry = \
        f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}"

    return window_geometry