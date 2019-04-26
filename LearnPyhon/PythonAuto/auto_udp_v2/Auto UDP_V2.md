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
pause_error_keys=pc_start
round=1
count=2
point0=100,100,1,2
point1=500,500,1,2

[PC]
pc_log=./pc_log.log
pc_start=PC_START
pc_stop=PC_STOP
pc_ext_count=2
pc_ext_str0=pc_log0
pc_ext_str1=pc_log1

[UDP]
udp_log=./udp_log.log
udp_start=UDP_START
udp_stop=UDP_STOP
udp_cvt_start=UDP_CVT_START
udp_cvt_stop=UDP_CVT_STOP
udp_ext_count=2
udp_ext_str0=str0
udp_ext_str1=str1

[CLIENT]
client_log=./client.log
client_start=CLIENT_START
client_stop=CLIENT_STOP
client_ext_count=2
client_ext_str0=str0
client_ext_str1=str1
```

pause_error_keys: 错误停顿关键字。例如pause_error_key=pc_start，当pc_start关联的关键字错误时程序暂停，回车恢复运行。支持的错误关键字有：pc_start/pc_stop/udp_start/udp_stop/udp_cvt_start/udp_cvt_stop/client_start/client_stop，并且支持它们的组合形式，例如"pause_error_keys=pc_start,pc_stop"

xxx_ext_count：额外关键字个数；即以下的client_ext_str0~client_ext_strN都为额外关键字。

pointx：x坐标，y坐标，单击1/双击2，停顿秒数

pc_log为读本地文件方式；udp_log和client_log为adb方式；当文件路径不存在的时候不进行统计，相应结果为0。

