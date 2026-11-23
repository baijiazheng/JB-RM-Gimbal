#!/usr/bin/env python3
# encoding: utf-8
"""回环测试：发一帧，看 STM32 是否回发

★ STM32 端需要配合（收到后原样回发），如果没有，
  就用这个脚本只测"树莓派能发出去"（用示波器/逻辑分析仪看波形）

用法：
  python3 loopback_test.py            # 发 1 帧，等回复
  python3 loopback_test.py --listen   # 只听（看 STM32 发什么过来）
"""
import sys
import time
import serial

from protocol import pack, unpack, ST_TRACKING


def main():
    listen_only = '--listen' in sys.argv

    ser = serial.Serial('/dev/ttyS0', 115200, timeout=0.5)
    print(f"串口打开: /dev/ttyS0 @ 115200")

    if listen_only:
        print("只听模式，Ctrl-C 退出")
        try:
            while True:
                data = ser.read(64)
                if data:
                    print(f"收到 {len(data)} 字节: {data.hex(' ')}")
        except KeyboardInterrupt:
            pass
    else:
        frame = pack(12.34, -5.67, 0.35, 1, ST_TRACKING)
        print(f"发送 {len(frame)} 字节: {frame.hex(' ')}")
        ser.write(frame)
        time.sleep(0.1)

        resp = ser.read(18)
        if resp:
            print(f"收到 {len(resp)} 字节: {resp.hex(' ')}")
            d = unpack(resp)
            print(f"解包: {d}" if d else "❌ 校验失败")
        else:
            print("❌ 没收到回复（ST 端可能没做回环）")

    ser.close()


if __name__ == '__main__':
    main()
