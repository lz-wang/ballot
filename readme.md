# 简易抽签工具

## 开发

### 安装依赖

```shell
pip install -r requirements.txt
```

### 项目结构

- 入口文件: `ballot.py`
- UI相关: `window.py`
- 抽签源码: `worker.py`
- 图标文件: `ballot.ico`

### 打包

```shell
pyinstaller -F -w -i ballot.ico --clean --win-private-assemblies ballot.py
```