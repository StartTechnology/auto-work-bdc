# 吉安市不动产登记系统录入（银行）自动化开发文档
## 技术栈
### （前端 页面）TypeScript
- 包管理器：npm
- 前端框架：Vue3 Vite
- 状态管理及持久化库：pinia pinia-plugin-persist
- ~~表格前端库：Lucksheet~~
- UI框架库：Arco Design Vue
- ~~动画效果库：~~
- 网络请求库：axios
- ~~拖拽效果实现库：vue-draggable-plus~~
- ~~页面操作库：playwright~~
- 前端数字转大写中文数字库：number-to-zh-currency
### 技术栈（服务端）Python
- 包管理器:pip venv
- 页面操作库:Drissionpage
- 接口及服务器: faspapi
- 数据库：sqlite3
- OCR接口：硅基流动
- ~~中间件及消息队列：funbooste~~
- excel读取及数据转化：pandas
- wps实时读写：pywin32
- 打包发布：
  - [ ] pyinstaller
  - [x] nuitka
## 开发文档
### 设置及初始化设置
1. 配置工作目录
   1. 配置文件路径
   2. 影像归档目录
   3. 业务数据记录表及数据库
2. 设置自动化操作的必要步骤
### 图像分类及图片归档
1. - [ ] 业务类型选择
2. - [ ] 业务材料选择
3. - [ ] 影像分类及OCR(有缩略图)
4. - [ ] 图片归档
### 整理数据及写入（Excel或Sqlite）
1. 根据业务类型整理必要数据
2. 业务数据写入excel或数据库
### 数据录入自动化（Python 服务器 ）
1. 自动化录入数据（异步）
2. ~~进度显示及完成通知~~
## 业务信息
### 业务类型分类
#### 抵押登记
- 合并登记（预告登记及预告抵押登记）
- 预告抵押（仅预告抵押，楼盘已做预告登记，需要查询预告买卖证号）
- 一般抵押登记
- 最高额抵押登记
#### 解押
- 预告解押
- 解押
#### 变更登记
> 暂无
### 业务材料
- 不动产登记申请表
- 不动产登记询问笔录
- 不动产登记委托书
- 不动产抵押权注销证明
- 申请人身份证明（身份证）
- 房屋所有权证明（房产证）
  - 房产证
  - 不动产权证
- 银行借款合同
- 银行抵押合同
- 不动产登记证明
  - 预告抵押登记证明
  - 抵押登记证明
- 商品房预售合同
- 关于抵押预告登记的约定
- 结婚证或具结保证书
- 其他（情况说明等）
## 生产环境及说明
- win7 32位 
- python 3.8.10 32位
- python使用包：Drissionpage fastapi pandas pywin32 uvicorn nuitka
- 编译命令：nuitka --standalone --output-dir=../dist --plugin-enable=tk-inter --show-progress --show-memory --include-data-dir=./config=config --include-data-dir=./static=static --mingw64 main.py 