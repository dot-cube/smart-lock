import sys

import RPi.GPIO as GPIO
from servo_controller import ServoController


def main():
    s_controller = ServoController()
    smart_lock = SmartLock()
    functions = {}
    functions["cw"] = s_controller.rotate_clockwise
    functions["ccw"] = s_controller.rotate_counterclockwise
    functions["ct"] = s_controller.centerlize
    
    option = get_options("--operation")
    if option == "lock":
        while not smart_lock.is_locked():
            functions["ccw"]()
        print("locked")
        return
    elif option == "unlock":
        while smart_lock.is_locked():
            functions["cw"]()
        print("unlocked")
        return

    while True:
        print("時計回：cw, 反時計回：ccw, 静止位置キャリブレーション：ct")
        cmd = input()
        try:
            functions[cmd]()
            print("is_locked: %s" % smart_lock.is_locked())
        except:
            del s_controller
            break


class SmartLock:
    def __init__(self, thumbturn_sensor_pin=17):
        self.THUMBTURN_SENSOR_PIN = thumbturn_sensor_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.THUMBTURN_SENSOR_PIN, GPIO.IN)

        self.LOCKED_STATUS = GPIO.HIGH

    def is_locked(self):
        return GPIO.input(self.THUMBTURN_SENSOR_PIN) == self.LOCKED_STATUS

    def __del__(self):
        pass


def get_options(op):
    """
    コマンドライン引数のオプションを検索し、オプションの値を取得する
    Parameters
    ----------
    op : string
        オプション (例："-p"
    
    Returns
    -------
    op_value : String
        オプションが見つかったら、オプションの後ろに指定されている値を返す
        見つからなかったらNoneを返す
    """
    args = sys.argv
    is_find = False  # 当該オプションを見つけた場合はフラグを立てる
    for val in args:
        if is_find:
            return val
        if val == op:
            is_find = True
    return None


if __name__ == "__main__":
    main()