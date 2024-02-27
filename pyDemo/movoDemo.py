import pyautogui
import time

#启动！
if __name__=='__main__':
    #初始坐标
    previous_x, previous_y = pyautogui.position()
    #一直找
    while True:    
        current_x, current_y = pyautogui.position()
        print('鼠标当前位置：x = {}, y = {}'.format(current_x, current_y))
        diff_x = current_x - previous_x
        diff_y = current_y - previous_y
        print('鼠标位置变化：x = {}, y = {}'.format(diff_x, diff_y))
        previous_x, previous_y = current_x, current_y
        print("###############################")
        time.sleep(3)
