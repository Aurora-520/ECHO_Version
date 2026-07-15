# Tests

V0 测试使用标准库 `unittest`，避免把当前缺少 pytest 误报为代码失败：

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -v
```

安装 dev 依赖后，同一批 `unittest.TestCase` 也可由 pytest 收集。硬件和 OpenCV 测试必须在
对应环境具备后单独记录，不能由本目录的纯软件测试替代。
