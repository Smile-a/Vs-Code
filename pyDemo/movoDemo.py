import pyautogui
import time

#启动！
if __name__=='__main__':
    sleepTime = 0.5
    #初始坐标
    previous_x, previous_y = pyautogui.position()
    print("hello 请输入你需要的触发间隔时间，回车确认,默认是0.5s噢！")
    sleepTime_input = input()  # 用户输入触发间隔时间
    if sleepTime_input:  # 如果用户有输入则更新sleepTime
        sleepTime = float(sleepTime_input)
    #一直找
    while True:    
        current_x, current_y = pyautogui.position()
        print('鼠标当前位置：x = {}, y = {}'.format(current_x, current_y))
        diff_x = current_x - previous_x
        diff_y = current_y - previous_y
        print('鼠标位置变化：x = {}, y = {}'.format(diff_x, diff_y))
        previous_x, previous_y = current_x, current_y
        print("###############################")
        time.sleep(sleepTime)
