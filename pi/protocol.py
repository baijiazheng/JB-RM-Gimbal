#!/usr/bin/env python3
# encoding: utf-8
"""串口协议：18 字节二进制帧

帧格式：
  偏移  长度  内容
  0     2     0xAA 0x55          帧头
  2     4     yaw      float32   水平角（度）
  6     4     pitch    float32   垂直角（度）
  10    4     dist     float32   距离（米）
  14    1     fire     uint8
  15    1     status   uint8
  16    1     checksum （buf[2..15] 求和 & 0xFF）
  17    1     0x0D               帧尾
"""
import struct

FRAME_SIZE = 18
HEAD = b'\xAA\x55'
TAIL = 0x0D

# 状态码
ST_NO_TARGET = 0
ST_TRACKING  = 1
ST_ALIGNED   = 2


def pack(yaw, pitch, dist_m, fire=0, status=ST_TRACKING):
    """打包成 18 字节帧"""
    payload = struct.pack('<fffBB', float(yaw), float(pitch),
                          float(dist_m), int(fire), int(status))
    assert len(payload) == 14, f"payload 应 14 字节，实际 {len(payload)}"
    checksum = sum(payload) & 0xFF
    frame = HEAD + payload + bytes([checksum, TAIL])
    assert len(frame) == FRAME_SIZE, f"帧应 18 字节，实际 {len(frame)}"
    return frame


def unpack(frame):
    """解包（用于回环测试）"""
    if len(frame) != FRAME_SIZE:
        return None
    if frame[:2] != HEAD or frame[17] != TAIL:
        return None
    if (sum(frame[2:16]) & 0xFF) != frame[16]:
        return None
    yaw, pitch, dist, fire, status = struct.unpack('<fffBB', frame[2:16])
    return {"yaw": yaw, "pitch": pitch, "dist": dist,
            "fire": fire, "status": status}


if __name__ == '__main__':
    # 自测
    f = pack(12.34, -5.67, 0.35, 1, ST_ALIGNED)
    print(f"帧长: {len(f)} 字节")
    print(f"十六进制: {f.hex(' ')}")
    d = unpack(f)
    print(f"解包: {d}")
    assert abs(d['yaw'] - 12.34) < 1e-4
    assert abs(d['pitch'] - (-5.67)) < 1e-4
    assert abs(d['dist'] - 0.35) < 1e-4
    assert d['fire'] == 1 and d['status'] == ST_ALIGNED
    print("✅ 自测通过")
