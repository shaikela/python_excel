import datetime
import time
def build_text_menu(menu_options,option_name,title):
    time.sleep(1)
    if title is not None:
        print (title)
    while True:
        for option in menu_options.keys():
            print (option, '=>', menu_options[option])
        answer = input("please select "+option_name+" :")
        if answer not in menu_options.keys():
            errhandler(answer)
            continue 
        else:
            return answer



def errhandler(option_arg):    
    print("invalid option: "+str(option_arg))

def timestamp():
    today = datetime.date.today().strftime("%d%m%y")
    now=datetime.datetime.now().strftime("%H%M%S")
    ts=str(today)+'-'+str(now)

