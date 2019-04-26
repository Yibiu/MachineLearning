# Auto UDP



UDP自动测试脚本

```c++
PC (pc_start/pc_stop)
|
|
|
\/ (udp_start/udp_stop)
UDP
|  (udp_cvt_start/udp_cvt_stop)
|
|
\/
Client (client_start/client_stop)
```

配置文件示例：

```ini
[COMMON]
round=1
count=2
point0=100,100,1,2
point1=500,500,1,2

[PC]
pc_log=./pc_log.log
pc_start=PC_START
pc_stop=PC_STOP

[UDP]
udp_log=./udp_log.log
udp_start=UDP_START
udp_stop=UDP_STOP
udp_cvt_start=UDP_CVT_START
udp_cvt_stop=UDP_CVT_STOP

[CLIENT]
client_log=./client.log
client_start=CLIENT_START
client_stop=CLIENT_STOP
```

pointx：x坐标，y坐标，单击1/双击2，停顿秒数

pc_log为读本地文件方式；udp_log和client_log为adb方式；当文件路径不存在的时候不进行统计，相应结果为0。

