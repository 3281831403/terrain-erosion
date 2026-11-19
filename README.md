# 地形侵蚀：坡度、汇流与沉积

地形被雨水冲刷后坡度图和高程图对不上：邻域权重重复计入、雨量单位不一致、河道下切没有最小坡度约束、沉积物不分粒径、瓦片接缝错位、法线不重算、盆地不填洼、侵蚀强度不钳制、缓存版本不校验、批量瓦片不统一提交。

## 目录结构

```
README.md
conftest.py
.gitignore
terrain/__init__.py
terrain/erosion.py
tests/test_erosion.py
```

## 当前状态

`terrain/erosion.py` 中所有函数只保留签名与文档字符串，函数体统一
`raise NotImplementedError`。`tests/test_erosion.py` 有 15 个参数化用例，
初始全部失败。

## 需要修复的 10 个问题

1. 邻域权重去重，边界单元不重复计入
2. 雨量与汇流累积统一到 0–1
3. 河道下切加最小坡度约束
4. 沉积物按粒径分级搬运
5. 多分辨率瓦片接缝对齐
6. 侵蚀后重算法线
7. 无出路盆地填洼
8. 侵蚀强度参数钳制
9. 高度图缓存版本校验
10. 批量瓦片统一提交或回滚

## 验收

```bash
python -m pytest -q
```

初始应得到 `15 failed`，且没有 collection error。实现 `terrain/erosion.py`
后 15 条用例应全部通过。
