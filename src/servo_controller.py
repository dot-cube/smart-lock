import sys
import time

import RPi.GPIO as GPIO
from settings import DETECTION_THRESHOLD


def main():
    cmd_crockwise = "cw"
    cmd_counterclockwise = "ccw"
    cmd_centerlize = "ct"
    s_controller = ServoController()
    functions = {}
    functions[cmd_crockwise] = s_controller.rotate_clockwise
    functions[cmd_counterclockwise] = s_controller.rotate_counterclockwise
    functions[cmd_centerlize] = s_controller.centerlize
    while True:
        print("時計回：cw, 反時計回：ccw, 静止位置キャリブレーション：ct")
        cmd = input()
        try:
            functions[cmd]()
        except:
            del s_controller
            break


class ServoController:
    def __init__(self, servo_sensor_pin=11, servo_pwm_pin=13, rotation_timeout_s=5):
        """
        GPIOピン番号で指定すること
        """
        self.SERVO_SENSOR_PIN = servo_sensor_pin
        self.SERVO_PWM_PIN = servo_pwm_pin
        self.ROTATION_TIMEOUT_S = rotation_timeout_s

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.SERVO_PWM_PIN, GPIO.OUT)
        GPIO.setup(self.SERVO_SENSOR_PIN, GPIO.IN)

        #「GPIO4出力」でPWMインスタンスを作成する。
        # GPIO.PWM( [ピン番号] , [周波数Hz] )
        # FS90RはPWMサイクル:20ms(=50Hz), 制御パルス:0.7ms〜2.3ms, (=3.5%〜11.5%)
        # デフォルトの静止点は1.5ms, (=7.5%)
        self.servo = GPIO.PWM(self.SERVO_PWM_PIN, 50)
        self.servo.start(0)

    def centerlize(self):
        """
        ローテーションサーボが停止するはずのデューティー比
        """
        self.servo.ChangeDutyCycle(7.5)
        print("何か文字を入力するとキャリブレーションを終了します")
        _ = input()
        self.servo.ChangeDutyCycle(0)
        print("[on %s] Complete %s" % (self.__getattribute__.__name__, sys._getframe().f_code.co_name))
    
    def rotate_clockwise(self):
        """
        TODO: いくら何でもビジーウェイトはひどすぎるので、以下の記事を参考に割り込みを使用する
        Raspberryでボタン押下をGPIOの割り込みで検出
        https://qiita.com/atmaru/items/2282445d327b0af0e6c1#%E9%85%8D%E7%B7%9A
        """
        self.servo.ChangeDutyCycle(6)
        detection_counter = 0
        start_time = time.time()
        before_state = GPIO.input(self.SERVO_SENSOR_PIN)
        while time.time() - start_time < self.ROTATION_TIMEOUT_S:
            if GPIO.input(self.SERVO_SENSOR_PIN) == GPIO.LOW:
                if before_state == GPIO.HIGH:
                    detection_counter += 1
                    # HACK: ラズパイのCPU使用率によっても最適な閾値が変わる可能性があるので、信頼性の高い手法に書き換える
                    if detection_counter > DETECTION_THRESHOLD:
                        print("Changed")
                        break
            else:
                before_state = GPIO.HIGH
                detection_counter = 0
        self.servo.ChangeDutyCycle(0)
        print("[on %s] Complete %s" % (self.__getattribute__.__name__, sys._getframe().f_code.co_name))
    
    def rotate_counterclockwise(self):
        """
        TODO: いくら何でもビジーウェイトはひどすぎるので、以下の記事を参考に割り込みを使用する
        Raspberryでボタン押下をGPIOの割り込みで検出
        https://qiita.com/atmaru/items/2282445d327b0af0e6c1#%E9%85%8D%E7%B7%9A
        """
        self.servo.ChangeDutyCycle(9)
        detection_counter = 0
        start_time = time.time()
        before_state = GPIO.input(self.SERVO_SENSOR_PIN)
        while time.time() - start_time < self.ROTATION_TIMEOUT_S:
            if GPIO.input(self.SERVO_SENSOR_PIN) == GPIO.LOW:
                if before_state == GPIO.HIGH:
                    detection_counter += 1
                    # HACK: ラズパイのCPU使用率によっても最適な閾値が変わる可能性があるので、信頼性の高い手法に書き換える
                    if detection_counter > DETECTION_THRESHOLD:
                        print("Changed")
                        break
            else:
                before_state = GPIO.HIGH
                detection_counter = 0
        self.servo.ChangeDutyCycle(0)
        print("[on %s] Complete %s" % (self.__getattribute__.__name__, sys._getframe().f_code.co_name))

    def __del__(self):
        self.servo.stop()
        GPIO.cleanup()
        print("[on %s] Complete servo.stop() and GPIO.cleanup()" % (self.__getattribute__.__name__, ))


if __name__ == "__main__":
    main()
