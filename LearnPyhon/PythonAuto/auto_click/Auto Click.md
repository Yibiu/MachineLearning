# Auto Click



自动点击脚本。

根据配置文件py_config.ini的内容进行点击操作：

```ini
[POINTS]
round=1
count=2
point0=100,100,1,2
point1=500,500,1,2
```

- round：测试轮数
- count：每轮要点击的点数
- pointx：第x-1个点。例如point0：`100,100` 为点坐标；`1`为单击(`2`为双击)；`2` 为点击该点后停顿的秒数。

