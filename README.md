# 银行系统

这是一个简单的银行系统，包含服务器端和客户端。服务器使用 FastAPI 构建，客户端是一个基于 Click 的命令行工具。

## 安装

1. 克隆此仓库：
   ```
   git clone https://github.com/libingkun-work/sample_banking_system.git
   cd sample_banking_system
   ```

2. 创建并激活虚拟环境：
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

## 使用方法

### 启动服务器

在一个终端窗口中运行：
    ```
    python server.py
    ```

服务器将在 `http://localhost:8000` 上运行。


### 使用客户端

在另一个终端窗口中，您可以使用以下命令：

1. 创建账户：
   ```
   python client.py create-account 123456 1000
   ```

2. 存款：
   ```
   python client.py deposit 123456 500
   ```

3. 取款：
   ```
   python client.py withdraw 123456 200
   ```

4. 转账：
   ```
   python client.py transfer 123456 789012 300
   ```

5. 查看余额：
   ```
   python client.py balance 123456
   ```

6. 导出csv:
   ```
   python client.py export -f data.csv
   ```
7. 导入csv数据：
   ```
   python client.py import-data -f data.csv
   ```

注意：所有的账号都必须是6位数字字符串。

## 运行测试

要运行测试，请使用以下命令：

    ```
    python -m unittest test_bank.py
    ```

这将运行 `test_bank.py` 文件中的所有测试用例。

## 项目结构

- `server.py`: FastAPI 服务器
- `client.py`: Click 命令行客户端
- `bank.py`: 银行系统的核心逻辑
- `account.py`: 账户模型
- `test_bank.py`: 单元测试
