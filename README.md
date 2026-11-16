# JB-RM-Gimbal · 单轴自瞄云台试验台

> 建立：2026-11-16
> 目的：验证「视觉 → 角度 → 舵机 → 瞄准」的最小闭环
> 定位：RM 自瞄的缩小版试验台（不是最终产品）

---

## 一、这是什么

```
树莓派（视觉）  ──UART 115200──→  STM32C8T6（控制）
   · 识别装甲板                      · 解析协议
   · PnP 算 yaw/pitch                · 驱动 MG996R 舵机
   · 发 18 字节二进制帧               · 激光笔指向目标
```

**★ 结构上就是 RM 的缩小版：视觉（Orin NX）+ 控制（C 板 STM32）**

---

## 二、目录结构

```
JB-RM-Gimbal/
├── stm32/yaw_gimbal/     CubeMX 工程（STM32F103C8T6）
│   ├── Core/Src/main.c        ← 主逻辑（UART 回调 + 舵机 PWM）
│   ├── Core/Src/tim.c         ← TIM2 PWM（★ 手动改过参数）
│   └── Makefile
├── pi/                   树莓派端代码
├── docs/
│   ├── 协议.md           ★ 18 字节二进制帧定义
│   └── 接线.md           ★ 引脚连接
└── README.md
```

---

## 三、硬件

| 部件 | 型号 | 说明 |
|---|---|---|
| **主控** | STM32F103C8T6（Blue Pill）| 72MHz，USART1 + TIM2 |
| **舵机** | MG996R | yaw 轴，10 kg·cm |
| **电源** | 5V/3A 独立电源 | ★ 不能从主控取电 |
| **烧录** | ST-Link V2 | SWD（PA13/PA14）|
| **树莓派** | 4B 8GB | /dev/ttyS0，115200 |
| **视觉** | DaBai DCW USB 相机 | 已标定 fx=360.72 |

---

## 四、快速开始

```bash
# ① 编译
cd stm32/yaw_gimbal
make -j4

# ② 烧录（ST-Link 插上）
st-flash write build/yaw_gimbal.bin 0x8000000

# ③ 树莓派端（另开终端）
cd pi
python3 send_test.py
```

---

## 五、当前状态

```
✅ CubeMX 工程生成（USART1 + TIM2 CH1 PWM + SWD）
✅ TIM2 参数已修正（PSC=71, ARR=19999 → 50Hz）
⬜ main.c 的 4 段代码（UART 回调 + 舵机控制）
⬜ 编译烧录
⬜ 回环测试
⬜ 舵机验证
⬜ 3D 打印云台结构
⬜ 视觉闭环
```

---

## 六、★ 注意

```
① tim.c 的 TIM2 参数是【手动改的】
   → CubeMX 重新 GENERATE CODE 会覆盖
   → 到时要在 CubeMX 里改（PSC=71, ARR=19999, Pulse=1500）

② 舵机必须独立 5V/3A 供电
   → 从主控取电会导致电压塌陷、主控重启

③ 三根 GND 必须连一起（树莓派 + STM32 + 舵机电源）
```
