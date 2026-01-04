# IFLOW 项目上下文文档

## 项目概述

本项目是一个**吉安市不动产登记系统录入（银行）自动化系统**，旨在通过自动化技术简化银行不动产登记业务的数据录入流程。系统采用前后端分离架构，提供影像处理、OCR识别、数据整理和自动化录入等功能。

### 技术栈

**前端（bdc-page）**
- **框架**: Vue 3 + TypeScript + Vite
- **UI库**: Arco Design Vue
- **状态管理**: Pinia + pinia-plugin-persistedstate（持久化）
- **网络请求**: Axios
- **其他**: number-to-zh-currency（数字转大写中文）、vue-draggable-plus（拖拽）

**后端（bdc-service）**
- **框架**: FastAPI（异步Web框架）
- **页面自动化**: DrissionPage
- **数据处理**: pandas、openpyxl（Excel读写）
- **OCR**: 硅基流动接口
- **系统交互**: pywin32（WPS实时读写）
- **数据库**: SQLite3
- **打包工具**: Nuitka

## 项目结构

```
auto-work-bdc/
├── bdc-page/              # 前端项目（Vue3 + TypeScript）
│   ├── src/
│   │   ├── components/    # 核心组件
│   │   │   ├── Config.vue          # 配置信息
│   │   │   ├── ImageProcessing.vue # 影像处理
│   │   │   ├── InformationOCR.vue  # 整理信息/OCR
│   │   │   └── PushTask.vue        # 提交任务
│   │   ├── store/        # Pinia状态管理
│   │   └── App.vue       # 主应用（Tab页结构）
│   └── package.json
├── bdc-service/          # 后端服务（Python + FastAPI）
│   └── app/
│       ├── main.py       # FastAPI主入口
│       ├── Config.py     # 配置管理
│       ├── routers/      # API路由
│       │   ├── Setting.py    # 设置相关
│       │   ├── ImgProcess.py # 影像处理
│       │   └── Pushtask.py   # 任务推送
│       ├── core/         # 核心业务逻辑
│       │   ├── ImageOCR.py        # OCR识别
│       │   ├── ImageProgram.py    # 图像处理
│       │   ├── PushBusinessTask.py # 业务任务推送
│       │   └── WorkConfig.py      # 工作配置
│       ├── config/       # 配置文件
│       │   ├── config.ini
│       │   └── 业务参数.xlsx
│       └── static/       # 静态文件（打包的前端）
└── project-bulid/        # 构建和打包相关
    └── .venv/           # Python 3.8.10 虚拟环境（生产环境）
```

## 核心功能模块

### 1. 配置信息（Config）
- 工作目录设置
- 影像归档目录配置
- 业务数据记录表及数据库配置

### 2. 影像处理（ImageProcessing）
- 业务类型选择
- 业务材料选择
- 影像分类及OCR识别（带缩略图）
- 图片归档

### 3. 整理信息（InformationOCR）
- 根据业务类型整理必要数据
- OCR提取关键信息
- 业务数据写入Excel或数据库

### 4. 提交任务（PushTask）
- 自动化录入数据（异步处理）
- 与不动产登记系统集成

## 支持的业务类型

### 抵押登记
- **合并登记**: 预告登记及预告抵押登记
- **预告抵押**: 仅预告抵押（需查询预告买卖证号）
- **一般抵押登记**
- **最高额抵押登记**

### 解押
- **预告解押**
- **解押**

### 业务材料
- 不动产登记申请表
- 不动产登记询问笔录
- 不动产登记委托书
- 不动产抵押权注销证明
- 申请人身份证明（身份证）
- 房屋所有权证明（房产证/不动产权证）
- 银行借款合同
- 银行抵押合同
- 不动产登记证明（预告/抵押）
- 商品房预售合同
- 关于抵押预告登记的约定
- 结婚证或具结保证书
- 其他（情况说明等）

## 构建和运行

### 前端开发（bdc-page）

```bash
cd bdc-page

# 安装依赖
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

**前端构建产物位置**: `bdc-page/dist/`

### 后端开发（bdc-service）

```bash
cd bdc-service

# 创建虚拟环境（Python 3.8.10）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器（支持热重载）
python app/main.py
```

**后端服务地址**: `http://0.0.0.0:8002`

### 生产环境打包

**要求**: Windows 7 32位，Python 3.8.10 32位

```bash
cd project-bulid/app

# 使用Nuitka打包
nuitka --standalone \
  --output-dir=../dist \
  --plugin-enable=tk-inter \
  --show-progress \
  --show-memory \
  --include-data-dir=./config=config \
  --include-data-dir=./static=static \
  --mingw64 main.py
```

**打包输出目录**: `project-bulid/dist/`

## 开发约定

### 前端开发约定
- 使用 **Vue 3 Composition API** (`<script setup>`)
- 使用 **TypeScript** 进行类型检查
- 组件使用 **Arco Design Vue** UI组件库
- 状态管理使用 **Pinia**，配合持久化插件
- 遵循 **Vue 3 官方风格指南**

### 后端开发约定
- 使用 **FastAPI** 异步框架
- 路由模块化（routers目录）
- 核心业务逻辑分离（core目录）
- 配置统一管理（Config.py）
- 使用 **DrissionPage** 进行页面自动化操作
- 遵循 **FastAPI** 最佳实践

### 配置管理
- 全局配置：`bdc-service/app/config/config.ini`
- 工作目录配置：工作目录下的 `config/config.ini`
- 业务参数：Excel文件 `业务参数.xlsx`

### 跨域处理
后端已配置CORS中间件，允许所有来源的跨域请求：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 前后端集成

后端通过 `StaticFiles` 挂载前端静态文件：
```python
app.mount("/", StaticFiles(directory="app/static", html=True), name="page")
```

**集成流程**：
1. 前端构建：`cd bdc-page && npm run build`
2. 复制构建产物：将 `bdc-page/dist/*` 复制到 `bdc-service/app/static/`
3. 启动后端服务：`python bdc-service/app/main.py`
4. 访问：`http://localhost:8000`

## API路由

- `GET /home`: 服务联通测试
- `/setting/*`: 设置相关API（路由：`routers.Setting`）
- `/imgprocess/*`: 影像处理API（路由：`routers.ImgProcess`）
- `/pushtask/*`: 任务推送API（路由：`routers.Pushtask`）

## 环境要求

### 开发环境
- **Node.js**: 支持 npm
- **Python**: 3.8+（推荐 3.10+）
- **操作系统**: Windows/Linux/Mac

### 生产环境
- **操作系统**: Windows 7 32位
- **Python**: 3.8.10 32位
- **浏览器**: Chrome/Edge（用于页面自动化）

## 依赖说明

### 前端主要依赖
- `@arco-design/web-vue`: Arco Design Vue组件库
- `axios`: HTTP客户端
- `pinia`: Vue状态管理
- `pinia-plugin-persistedstate`: Pinia持久化插件
- `vue-draggable-plus`: 拖拽功能
- `number-to-zh-currency`: 数字转大写中文

### 后端主要依赖
- `fastapi`: Web框架
- `uvicorn`: ASGI服务器
- `DrissionPage`: 页面自动化
- `pandas`: 数据处理
- `openpyxl`: Excel读写
- `pywin32`: Windows系统交互
- `nuitka`: Python打包工具

## 注意事项

1. **生产环境打包**: 必须使用 Python 3.8.10 32位版本，以确保与目标环境兼容
2. **配置文件路径**: 配置文件使用绝对路径，注意跨平台的路径处理
3. **前端构建**: 每次修改前端代码后，需要重新构建并复制到后端static目录
4. **OCR服务**: 使用硅基流动的OCR接口，确保网络连接和API密钥配置正确
5. **页面自动化**: DrissionPage需要浏览器环境，生产环境需安装Chrome或Edge浏览器

## 常见问题

### 前端开发服务器无法启动
- 检查是否安装依赖：`npm install`
- 检查端口是否被占用

### 后端服务跨域问题
- 已配置CORS中间件，如仍有问题检查浏览器控制台错误
- 确保前端API请求地址正确

### 打包后运行失败
- 确保使用正确的Python版本（3.8.10 32位）
- 检查 `--include-data-dir` 参数是否正确包含config和static目录
- 确保目标环境有必要的运行时依赖

## 项目维护

**版本控制**: Git
**远程仓库**: https://gitee.com/lcydatacenter/auto-work-bdc.git

**提交规范**:
- 前端修改：`feat(frontend): 描述`
- 后端修改：`feat(backend): 描述`
- 文档更新：`docs: 描述`
- Bug修复：`fix: 描述`