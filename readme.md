# 不动产登记系统录入（银行）自动化系统

一个基于前后端分离架构的不动产登记业务自动化录入系统，帮助银行简化不动产登记业务的数据录入流程。

## 📋 项目简介

本系统通过影像处理、OCR识别、数据整理和自动化录入等技术，实现不动产登记业务的高效处理。支持抵押登记、解押等多种业务类型，大幅减少人工录入工作量。

## 🚀 核心功能

- **配置管理**：工作目录、影像归档路径、数据库配置
- **影像处理**：业务类型选择、材料分类、图片归档
- **OCR识别**：自动提取不动产登记相关关键信息
- **数据整理**：业务数据结构化处理，支持Excel和数据库存储
- **自动化录入**：与不动产登记系统集成，异步处理业务任务

## 🛠 技术栈

### 前端
- Vue 3 + TypeScript + Vite
- Arco Design Vue（UI组件库）
- Pinia（状态管理 + 持久化）
- Axios（HTTP请求）

### 后端
- FastAPI（异步Web框架）
- DrissionPage（页面自动化）
- Pandas + OpenPyxl（数据处理）
- SQLite3（数据库）
- Nuitka（打包工具）

## 📦 安装指南

### 前置要求

- Node.js（支持npm）
- Python 3.8+（生产环境需Python 3.8.10 32位）
- Git

### 克隆项目

```bash
git clone https://gitee.com/lcydatacenter/auto-work-bdc.git
cd auto-work-bdc
```

### 前端安装

```bash
cd bdc-page
npm install
```

### 后端安装

```bash
cd bdc-service

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 🏃 快速开始

### 开发模式

**启动前端**：
```bash
cd bdc-page
npm run dev
```
访问：http://localhost:5173

**启动后端**：
```bash
cd bdc-service
python app/main.py
```
访问：http://localhost:8000

### 生产部署

**1. 构建前端**：
```bash
cd bdc-page
npm run build
```

**2. 复制静态文件到后端**：
将 `bdc-page/dist` 目录下的所有文件复制到 `bdc-service/app/static/`

**3. 启动后端服务**：
```bash
cd bdc-service
python app/main.py
```

**4. 访问应用**：
http://localhost:8000

## 📁 项目结构

```
auto-work-bdc/
├── bdc-page/              # 前端项目
│   ├── src/
│   │   ├── components/    # 核心组件
│   │   ├── store/        # 状态管理
│   │   └── App.vue       # 主应用
│   └── package.json
├── bdc-service/          # 后端服务
│   └── app/
│       ├── main.py       # 主入口
│       ├── routers/      # API路由
│       ├── core/         # 核心业务逻辑
│       ├── config/       # 配置文件
│       └── static/       # 静态文件
└── project-bulid/        # 构建打包
```

## 📊 支持的业务类型

### 抵押登记
- 合并登记（预告登记及预告抵押登记）
- 预告抵押
- 一般抵押登记
- 最高额抵押登记

### 解押
- 预告解押
- 解押

### 业务材料
- 不动产登记申请表
- 不动产登记询问笔录
- 不动产登记委托书
- 身份证明、房产证
- 借款合同、抵押合同
- 不动产登记证明
- 商品房预售合同等

## 🔧 构建打包

### 生产环境打包

**要求**：Windows 7 32位，Python 3.8.10 32位

```bash
cd project-bulid/app

nuitka --standalone \
  --output-dir=../dist \
  --plugin-enable=tk-inter \
  --show-progress \
  --show-memory \
  --include-data-dir=./config=config \
  --include-data-dir=./static=static \
  --mingw64 main.py
```

打包输出：`project-bulid/dist/`

## 📝 开发指南

### 前端开发
```bash
cd bdc-page
npm run dev        # 开发模式
npm run build      # 构建生产版本
npm run preview    # 预览构建结果
```

### 后端开发
```bash
cd bdc-service
python app/main.py # 启动开发服务器（支持热重载）
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！


## 📞 联系方式

如有问题，请通过以下方式联系：
- 提交 Issue

## ⚠️ 注意事项

1. 生产环境必须使用 Python 3.8.10 32位版本
2. 前端修改后需重新构建并复制到后端static目录
3. 确保OCR服务（硅基流动）配置正确
4. 页面自动化需要Chrome或Edge浏览器环境

## 📚 相关文档

- [IFLOW.md](./IFLOW.md) - 详细的项目上下文文档
- [bdc-page/README.md](./bdc-page/README.md) - 前端项目说明
- [bdc-service/readme.md](./bdc-service/readme.md) - 后端服务说明