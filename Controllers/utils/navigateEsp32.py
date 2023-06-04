"""
This utility is used by "monitor_and_controlPanel.py" to
- delagate the task of sending navigation controls to the esp32
"""
import requests

# Setup..
directions = {
    'UP': 1,
    'DOWN': 2,
    'LEFT': 3,
    'RIGHT': 4,
    'STOP': 5
}

speeds = {
    +10: 'Raise Speed by 10',
    -10: 'Lower speed by 10'
}

current_speed:int = 150

## handlers..
def navigate(url:str, direction :str='STOP', verbose: bool=False):
    try:
        if verbose:
            print("[INFO] Received navigation command: ", direction)
            requests.get(url + "/control?var=direction&val={}".format(directions[direction]))
    except Exception as e:
        print("[ERROR] in navigateEsp32.py: Sending navigation commands error.")
        print(e)


def adjustSpeed(url:str, speed :int=current_speed, verbose: bool=False):
    try:
        if verbose:
            print("[INFO] Received speed adjust value: ", speeds[speed])
            requests.get(url + "/control?var=speed&val={}".format(current_speed+speed))
    except Exception as e:
        print("[ERROR] in navigateEsp32.py: Adjusting speed error.")
        print(e)