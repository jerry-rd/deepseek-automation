# DeepSeek Chat Automation

这个 Python 脚本可以自动化与[DeepSeek Chat](https://chat.deepseek.com/)的交互，包括：

- 使用手机号和密码自动登录
- 自动提问自定义问题
- 自动截取回答的屏幕截图

This Python script automates interactions with [DeepSeek Chat](https://chat.deepseek.com/), including:

- Logging in with your phone number and password
- Asking custom questions
- Taking screenshots of responses

## 设置 (Setup)

1. 安装所需依赖：

   ```
   pip install -r requirements.txt
   ```

2. 下载 ChromeDriver：

   ```
   python download_chromedriver_134.py
   ```

   这将下载适用于您系统的 ChromeDriver 并将其放置在当前目录中。

3. **配置您的登录凭据**（重要）：

   - 编辑`.env`文件，填入您的 DeepSeek 手机号和密码：
     ```
     DEEPSEEK_PHONE=your_actual_phone_number
     DEEPSEEK_PASSWORD=your_actual_password
     ```
   - 请确保使用您的实际 DeepSeek 手机号和密码替换示例值
   - 手机号格式示例：+86xxxxxxxxxx 或 xxxxxxxxxx（根据 DeepSeek 的要求）

4. **准备问题配置文件**（可选）：
   - 默认配置文件为`questions_config.txt`
   - 每行一个问题
   - 使用随机模式时，将从此文件中随机选择问题

## 使用方法 (Usage)

### 提问单个问题

```
python deepseek_automation.py --question "您的问题"
```

### 提问多个问题（命令行指定）

```
python deepseek_automation.py --questions "第一个问题" "第二个问题" "第三个问题"
```

### 从文件中提问多个问题

创建一个文本文件，每行一个问题，然后运行：

```
python deepseek_automation.py --questions-file sample_questions.txt
```

### 随机选择问题

从配置文件中随机选择一个问题进行提问：

```
python deepseek_automation.py --random
```

使用自定义配置文件：

```
python deepseek_automation.py --random --config my_questions.txt
```

### 高级选项

设置问题之间的等待时间（默认为 3 秒）：

```
python deepseek_automation.py --questions-file questions.txt --wait-time 10
```

设置每个问题的最大尝试次数（默认为 3 次）：

```
python deepseek_automation.py --questions-file questions.txt --max-retries 5
```

组合使用多个选项：

```
python deepseek_automation.py --random --config my_questions.txt --wait-time 15 --max-retries 2
```

## 屏幕截图 (Screenshots)

屏幕截图保存在`screenshots`目录中，文件名中包含时间戳。此外，脚本还会在登录过程中保存以下截图：

- `initial_page.png` - 初始页面
- `login_form.png` - 登录表单
- `filled_login_form.png` - 填写完成的登录表单
- `login_success.png` - 登录成功的页面
- `login_failed.png` - 登录失败时的页面（如果发生）
- `options_checked.png` - 勾选深度思考和联网搜索选项后的页面
- `question_sent.png` - 发送问题后的页面
- `response_received.png` - 收到回答后的页面

## 故障排除 (Troubleshooting)

- 如果遇到 ChromeDriver 问题，请确保您有与 Chrome 浏览器版本匹配的正确版本。您可以从[ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)手动下载并放置在当前目录中。
- 确保您的 Chrome 浏览器是最新的。
- 如果遇到网络连接问题，请检查您的防火墙设置。
- 如果登录失败，请检查您的`.env`文件中的手机号和密码是否正确。
- 如果登录界面有变化，查看`login_form.png`截图，确认登录界面的实际情况。
- 如果问题提问失败，脚本会自动重试（默认最多 3 次）。您可以使用`--max-retries`参数增加重试次数。

## 注意事项 (Notes)

- 该脚本使用 Chrome 浏览器。请确保您已安装 Chrome。
- 如果要在无头模式下运行（无浏览器 UI），请取消`setup_driver()`函数中的 headless 选项的注释。
- 脚本会等待响应完成后再截图，但非常长的响应可能会超时。
- 如果 DeepSeek Chat 界面发生变化，可能需要更新 XPath 选择器。
