import sys,os
import curses

template_path = "/home/aditya/WORKSPACE/stupid_projects/RUNNING/contest/templates/"

def refresh(stdscr):
    # Refresh the screen
    stdscr.clear()
    stdscr.refresh()
    stdscr.move(0, 0)

def take_input(display_str,stdscr):
    k = 0
    input_str = ""
    while (k != 10):
        refresh(stdscr)
        height, width = stdscr.getmaxyx()
        if k==263:
            input_str = input_str[:-1]
        elif k:
            input_str+=chr(k)
        stdscr.addstr(height//2,width//2,display_str.format(input_str),curses.color_pair(1))
        k = stdscr.getch()
        stdscr.clear()
    return input_str

def display_options(display_str,options,stdscr):
    num_options=len(options)
    option = 0
    k=0
    input_str=""
    while (k !=10):
        height, width = stdscr.getmaxyx()
        x = width//2
        y = height//2
        refresh(stdscr)
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            option = (option + 1)%num_options
        elif k == curses.KEY_UP:
            option = (option - 1)%num_options

        # Render status bar
        stdscr.addstr(y-1,x-4,display_str,curses.color_pair(2))

        for i in range(len(options)):
            if i==option:
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr(y+i,x,options[i])
                stdscr.attroff(curses.color_pair(3))
            else:
                stdscr.addstr(y+i,x,options[i])

        # Wait for next input
        k = stdscr.getch()
    return option


def draw_menu(stdscr):
    refresh(stdscr)
    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    contest_no = take_input("contest number:{}",stdscr)

    if not os.path.exists(contest_no ):
        os.system("mkdir " + contest_no )

    options = os.listdir(template_path)
    option = display_options("Choose the template:",options,stdscr)

    input_str=take_input("problem number (write in <char><part number(optional)> format): {}",stdscr)

    if not os.path.exists(contest_no+'/'+input_str+".cpp"):
        os.system("cp "+template_path+options[option]+" "+contest_no+'/'+input_str+".cpp")
    os.system("xdg-open "+contest_no+'/'+input_str+".cpp")

if __name__ == "__main__":
    curses.wrapper(draw_menu)
