import RPi.GPIO as GPIO
import time


def main():
    cmd_crockwise = "cw"
    cmd_counterclockwise = "ccw"
    s_controller = ServoController()
    functions = {}
    functions[cmd_crockwise] = s_controller.rotate_clockwise
    functions[cmd_counterclockwise] = s_controller.rotate_counterclockwise
    while True:
        print("時計回：cw, 反時計回：ccw")
        cmd = input()
        try:
            functions[cmd]()
        except:
            del s_controller
            break

class ServoController:
    def __init__(self, servo_sensor_pin=5, servo_pwm_pin=4, rotation_timeout_s=5):
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
        #GPIO.PWM( [ピン番号] , [周波数Hz] )
        #SG92RはPWMサイクル:20ms(=50Hz), 制御パルス:0.5ms〜2.4ms, (=2.5%〜12%)。
        self.servo = GPIO.PWM(self.SERVO_PWM_PIN, 50)
        self.servo.start(0)
    
    def rotate_clockwise(self):
        """
        TODO: いくら何でもビジーウェイトはひどすぎるので、以下の記事を参考に割り込みを使用する
        Raspberryでボタン押下をGPIOの割り込みで検出
        https://qiita.com/atmaru/items/2282445d327b0af0e6c1#%E9%85%8D%E7%B7%9A
        """
        self.servo.start(0)
        time.sleep(0.5)
        self.servo.ChangeDutyCycle(5)
        start_time = time.time()
        before_state = GPIO.input(self.SERVO_SENSOR_PIN)
        while time.time() - start_time < self.ROTATION_TIMEOUT_S:
            if GPIO.input(self.SERVO_SENSOR_PIN) == GPIO.HIGH:
                if before_state == GPIO.LOW:
                    print("chamged 0")
                    break
            else:
                print("chamged 1")
                before_state = GPIO.LOW 
        self.servo.ChangeDutyCycle(7)
        time.sleep(0.02)
        self.servo.stop()
        print("[on %s] Complete %s" % (self.__getattribute__.__name__, self.rotate_clockwise.__name__))
    
    def rotate_counterclockwise(self):
        """
        TODO: いくら何でもビジーウェイトはひどすぎるので、以下の記事を参考に割り込みを使用する
        Raspberryでボタン押下をGPIOの割り込みで検出
        https://qiita.com/atmaru/items/2282445d327b0af0e6c1#%E9%85%8D%E7%B7%9A
        """
        self.servo.start(0)
        time.sleep(0.5)
        self.servo.ChangeDutyCycle(7)
        start_time = time.time()
        before_state = GPIO.input(self.SERVO_SENSOR_PIN)
        while time.time() - start_time < self.ROTATION_TIMEOUT_S:
            time.sleep(0.01)
            if GPIO.input(self.SERVO_SENSOR_PIN) == GPIO.HIGH:
                if before_state == GPIO.LOW: break
            else:
                before_state = GPIO.LOW
        self.servo.ChangeDutyCycle(5)
        self.servo.stop()
        time.sleep(0.02)
        print("[on %s] Complete %s" % (self.__getattribute__.__name__, self.rotate_counterclockwise.__name__))

    def __del__(self):
        GPIO.cleanup()
        print("[on %s] Complete servo.stop() and GPIO.cleanup()" % (self.__getattribute__.__name__, ))


if __name__ == "__main__":
    main()