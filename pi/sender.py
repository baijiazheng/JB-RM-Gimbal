#!/usr/bin/env python3
# encoding: utf-8
"""UART 发送器

用法：
  from sender import Sender
  s = Sender('/dev/ttyS0', 115200)
  s.send(yaw=10.5, pitch=0, dist=0.42, fire=0, status=1)
  s.close()
"""
import serial

from protocol import pack, ST_TRACKING


class Sender:
    def __init__(self, port='/dev/ttyS0', baudrate=115200, verbose=False):
        # ★ 树莓派 4B 用 /dev/ttyS0（mini UART，之前实测可用）
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        self.verbose = verbose
        self.count = 0

    def send(self, yaw, pitch, dist_m, fire=0, status=ST_TRACKING):
        frame = pack(yaw, pitch, dist_m, fire, status)
        self.ser.write(frame)
        self.count += 1
        if self.verbose:
            print(f"[{self.count}] yaw={yaw:.2f} pitch={pitch:.2f} "
                  f"dist={dist_m:.3f} fire={fire} status={status}")

    def close(self):
        if self.ser.is_open:
            self.ser.close()


if __name__ == '__main__':
    import time
    s = Sender(verbose=True)
    print("发送测试序列（Ctrl-C 退出）...")
    try:
        for yaw in [0, 10, 20, 10, 0, -10, -20, -10, 0]:
            s.send(yaw, 0, 0.35, 0, ST_TRACKING)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        s.close()
        print(f"\n共发送 {s.count} 帧")
