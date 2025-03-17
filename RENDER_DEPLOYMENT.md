# 在 Render 上部署学生个人品牌顾问应用

本指南将帮助您在 Render 平台上部署学生个人品牌顾问应用。

## 步骤 1: 创建 Render 账户

1. 访问 [Render 官网](https://render.com/) 并注册一个账户（如果您还没有账户）。
2. 完成注册流程并登录到您的 Render 控制台。

## 步骤 2: 连接 GitHub 仓库

1. 在 Render 控制台中，点击 "New" 按钮。
2. 选择 "Web Service" 选项。
3. 点击 "Connect account" 并选择 GitHub。
4. 授权 Render 访问您的 GitHub 账户。
5. 在仓库列表中找到并选择 `learn-burn-code-123/student-brand-advisor` 仓库。

## 步骤 3: 配置 Web 服务

1. 在 "Name" 字段中输入服务名称，例如 `student-brand-advisor`。
2. 确保 "Environment" 设置为 `Python`。
3. 在 "Build Command" 字段中输入 `pip install -r requirements.txt`。
4. 在 "Start Command" 字段中输入 `gunicorn app:app`。
5. 选择区域（推荐选择离您的目标用户最近的区域）。
6. 选择计划（可以从免费计划开始）。

## 步骤 4: 环境变量

在 "Environment Variables" 部分添加以下变量：
- `PYTHON_VERSION`: `3.10.0`

## 步骤 5: 高级选项

1. 在 "Advanced" 部分，您可以配置自动部署选项。建议启用 "Auto-Deploy" 以便每次推送到 GitHub 仓库时自动更新应用。
2. 如果您的应用需要更多资源，可以在此部分调整内存和 CPU 设置。

## 步骤 6: 创建 Web 服务

1. 检查所有配置是否正确。
2. 点击 "Create Web Service" 按钮。
3. Render 将开始构建和部署您的应用。这可能需要几分钟时间。

## 步骤 7: 访问您的应用

1. 部署完成后，Render 将提供一个 URL（例如 `https://student-brand-advisor.onrender.com`）。
2. 点击该 URL 或复制到浏览器中访问您的应用。

## 注意事项

- 首次部署时，应用将下载 Llama 3 模型，这可能需要一些时间。
- 如果您在免费计划上遇到内存限制问题，可以考虑升级到付费计划或在 `app.py` 中将 `SIMULATION_MODE` 设置为 `True` 来使用模拟模式。
- Render 免费计划的服务在一段时间不活动后会休眠，首次访问可能需要等待几秒钟才能启动。

## 故障排除

如果您遇到部署问题：

1. 检查 Render 日志以获取错误信息。
2. 确保所有依赖项都在 `requirements.txt` 文件中正确列出。
3. 验证 `gunicorn` 是否已包含在依赖项中。
4. 如果应用需要大量内存（例如加载 Llama 3 模型），请考虑升级到具有更多资源的计划。
