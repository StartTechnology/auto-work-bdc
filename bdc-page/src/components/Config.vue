<template>
  <a-layout class="config-container">
    <!-- 主体内容 -->
    <a-layout-content class="content-wrapper">
      <!-- 连接配置卡片 -->
      <a-card
        title="连接配置"
        class="config-card connection-card"
        :bordered="false"
      >
        <!-- 服务器地址配置 -->
        <a-row :gutter="[16, 24]" align="center" class="config-row">
          <a-col :span="2">
            <span class="config-label">服务器地址</span>
          </a-col>
          <a-col :span="12">
            <a-input
              v-model="serverAddress"
              placeholder="请输入服务器地址（如：http://localhost:5000）"
              class="input-field"
              allow-clear
            >
              <template #prefix>
                <cloud-server-outlined />
              </template>
            </a-input>
          </a-col>
          <a-col :span="4">
            <a-button
              type="primary"
              ghost
              class="test-btn animated-btn"
              @click="serverAddressTest"
            >
              <wifi-outlined />
              测试连接
            </a-button>
          </a-col>
        </a-row>

        <!-- 工作目录配置 -->
        <a-row :gutter="[16, 24]" align="center" class="config-row">
          <a-col :span="2">
            <span class="config-label">工作目录</span>
          </a-col>
          <a-col :span="12">
            <a-input
              v-model="workDirectory"
              placeholder="请输入工作目录路径"
              class="input-field"
              allow-clear
            >
              <template #prefix>
                <folder-open-outlined />
              </template>
            </a-input>
          </a-col>
          <a-col :span="6">
            <!-- 占位列，保持对齐 -->
          </a-col>
        </a-row>
      </a-card>

      <!-- 业务配置表格区域 -->
      <a-card title="业务配置" class="config-card table-card" :bordered="false">
        
        <template #extra>
          <a-tag  checkable color="red" :default-checked="true">"1"表示必需</a-tag>
          <a-tag style="margin: 5px;" checkable color="arcoblue" :default-checked="true">"0"表示非必需</a-tag>
          <a-space>
            <a-button type="dashed" class="action-btn animated-btn" @click="openBusinessConfigFile">
              <edit-outlined />
              编辑配置
            </a-button>
            <a-button type="dashed" class="action-btn animated-btn" @click="updateBusinessConfig">
              <reload-outlined />
              刷新配置
            </a-button>
          </a-space>
        </template>

        <!-- 动态表格 -->
        <a-table
          :columns="tableColumns"
          :data="tableData"
          :pagination="false"
          bordered
          size="middle"
          class="biz-table animated-table"
          :scroll="{ x: '100%' , y: 400 }"
        >
        </a-table>
      </a-card>

      <!-- 底部操作按钮 -->
      <a-card class="action-card" :bordered="false">
        <a-space :size="20" class="action-buttons">
          <a-button
            type="primary"
            size="large"
            class="primary-btn animated-btn"
            @click="savePageConfig"
          >
            <save-outlined />
            保存配置
          </a-button>
          <a-button size="large" class="secondary-btn animated-btn" @click="resetPageConfig">
            <redo-outlined />
            重置配置
          </a-button>
          <a-button size="large" class="secondary-btn animated-btn" @click="getPageConfig">
            <folder-open-outlined />
            读取配置
          </a-button>
        </a-space>
      </a-card>
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from 'axios';
import {
  CloudServerOutlined,
  WifiOutlined,
  FolderOpenOutlined,
  EditOutlined,
  ReloadOutlined,
  SaveOutlined,
  RedoOutlined,
} from "@ant-design/icons-vue";
import { Message } from "@arco-design/web-vue";

import { PageConfig } from "../store/config";
const pageConfig = PageConfig();
// 响应式数据定义
const serverAddress = ref<string>("");
const workDirectory = ref<string>("");

// 表格列配置
const tableColumns = ref([]);
const tableData = ref([]);

onMounted(() => {resetPageConfig();});
//测试服务器是否联通，结果以通知形式返回
function serverAddressTest() {
    if(!serverAddress.value.trim())
    {
        Message.error({content:"服务器地址不能为空",duration:1500,closable:true});
        return
    }
    axios.get(serverAddress.value).then(
        (res)=>{
            if(res.status ==200)
            {
                Message.success({ content: "服务器连接成功", duration: 800 });
            }
            else{
                Message.error({ content: "服务器连接失败", duration: 1500,closable:true});
            }
        }
    ).catch(()=>{Message.error({ content: "服务器连接失败", duration: 1500,closable:true});});
    
}

//刷新业务配置信息
function updateBusinessConfig() {
    axios.get(pageConfig.business_config_url).then((res)=>{
        // console.log(res.data);
        tableColumns.value=res.data.columns;
        tableData.value=res.data.data;

        pageConfig.business_config_colums=tableColumns.value;
        pageConfig.business_config_data=tableData.value;
    }).catch((err)=>{console.log(err)});
}
//编辑业务信息 打开业务文件
function openBusinessConfigFile()
{
  axios.get(pageConfig.business_config_set_url).catch((err)=>{
    console.log(err)
    Message.error({ content: "文件打开失败", duration: 1500,closable:true});
  })
}
//从服务器读取配置（包括业务配置）
async function getPageConfig(): Promise<void> {
    pageConfig.server_url=serverAddress.value;
    await pageConfig.getConfigFromServer();
    resetPageConfig();
}
//保存配置到服务器和本地缓存
function savePageConfig(): void {
    if(workDirectory.value=='')
    {
      Message.error('工作目录不能为空');
      return
    }
    pageConfig.server_url=serverAddress.value;
    pageConfig.work_dir=workDirectory.value;
    pageConfig.business_config_colums=tableColumns.value;
    pageConfig.business_config_data=tableData.value;
    //更改工作目录
    pageConfig.setWorkDir()
}
//重置配置 重新加载本地缓存配置
function resetPageConfig(): void {
  serverAddress.value = pageConfig.server_url;
  workDirectory.value = pageConfig.work_dir;
  tableColumns.value=pageConfig.business_config_colums;
  tableData.value=pageConfig.business_config_data;
}
</script>

<style lang="less" scoped>
// 浅色系中国色配色方案
@primary-color: #6e7f9e; // 青灰色 - 柔和的主色调
@secondary-color: #8ba3a7; // 淡青色 - 辅助色调
@accent-color: #d4a86a; // 赭色 - 点缀色调
@background-color: #f5f2eb; // 浅米色 - 背景色
@card-bg: #ffffff; // 卡片背景色
@text-color: #333333; // 墨色 - 主要文字色
@border-color: #e8e8e8; // 淡灰色边框

// 光影效果变量
@shadow-base: 0 4px 12px rgba(0, 0, 0, 0.08);
@shadow-hover: 0 8px 25px rgba(110, 127, 158, 0.15);
@shadow-active: 0 2px 8px rgba(110, 127, 158, 0.2);
@shadow-card: 0 6px 16px rgba(0, 0, 0, 0.05);

// 动画变量
@transition-base: all 0.3s ease;
@transition-slow: all 0.5s ease;

.config-container {
  min-height: 100vh;
  background: -webkit-linear-gradient(135deg, @background-color 0%, #f0ebe0 100%); /* Safari 5.1-6.0 */
  background: -o-linear-gradient(135deg, @background-color 0%, #f0ebe0 100%); /* Opera 11.1-12.0 */
  background: -moz-linear-gradient(135deg, @background-color 0%, #f0ebe0 100%); /* Firefox 3.6-15 */
  background: linear-gradient(135deg, @background-color 0%, #f0ebe0 100%); /* 标准语法 */
  padding: 24px;
  -webkit-animation: fadeIn 0.8s ease-out;
  animation: fadeIn 0.8s ease-out;

  .page-header {
    background: transparent;
    padding: 0 0 24px 0;
    -webkit-animation: slideDown 0.6s ease-out;
    animation: slideDown 0.6s ease-out;

    :deep(.ant-page-header-heading) {
      border-bottom: none;
    }

    :deep(.ant-page-header-heading-title) {
      color: @primary-color;
      font-size: 28px;
      font-weight: 600;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    :deep(.ant-page-header-heading-sub-title) {
      color: @secondary-color;
      font-size: 16px;
    }
  }

  .content-wrapper {
    max-width: 1400px;
    margin: 0 auto;
  }

  .config-card {
    margin-bottom: 24px;
    border-radius: 12px;
    box-shadow: @shadow-card;
    background: @card-bg;
    -webkit-backdrop-filter: blur(10px); /* Safari 9+ */
    backdrop-filter: blur(10px); /* 标准语法 */
    border: 1px solid rgba(255, 255, 255, 0.5);
    -webkit-transition: @transition-base;
    -o-transition: @transition-base;
    transition: @transition-base;
    -webkit-animation: cardAppear 0.5s ease-out;
    animation: cardAppear 0.5s ease-out;

    &:hover {
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
      -webkit-transform: translateY(-2px);
      -ms-transform: translateY(-2px);
      transform: translateY(-2px);
    }

    :deep(.ant-card-head) {
      border-bottom: 2px solid fade(@accent-color, 30%);
      background: -webkit-linear-gradient(135deg, fade(@primary-color, 3%) 0%, fade(@secondary-color, 3%) 100%); /* Safari 5.1-6.0 */
      background: -o-linear-gradient(135deg, fade(@primary-color, 3%) 0%, fade(@secondary-color, 3%) 100%); /* Opera 11.1-12.0 */
      background: -moz-linear-gradient(135deg, fade(@primary-color, 3%) 0%, fade(@secondary-color, 3%) 100%); /* Firefox 3.6-15 */
      background: linear-gradient(135deg, fade(@primary-color, 3%) 0%, fade(@secondary-color, 3%) 100%); /* 标准语法 */
      border-radius: 12px 12px 0 0;

      .ant-card-head-title {
        color: @text-color;
        font-size: 18px;
        font-weight: 600;
        padding: 16px 0;
      }
    }

    // 连接配置卡片特殊样式
    &.connection-card {
      :deep(.ant-card-body) {
        padding: 24px;
      }

      .config-row {
        margin-bottom: 8px;

        .config-label {
          color: @text-color;
          font-weight: 500;
          font-size: 14px;
          display: -webkit-box;
          display: -ms-flexbox;
          display: flex;
          -webkit-box-align: center;
          -ms-flex-align: center;
          align-items: center;
          height: 100%;
        }
      }
    }

    .input-field {
      border-radius: 8px;
      border: 1px solid @border-color;
      -webkit-transition: @transition-base;
      -o-transition: @transition-base;
      transition: @transition-base;
      height: 40px;

      &:focus,
      &:hover {
        border-color: @primary-color;
        box-shadow: 0 0 0 2px fade(@primary-color, 15%);
        -webkit-transform: translateY(-1px);
        -ms-transform: translateY(-1px);
        transform: translateY(-1px);
      }

      :deep(.ant-input) {
        font-size: 14px;
      }
    }

    .test-btn {
      border-radius: 8px;
      font-weight: 500;
      -webkit-transition: @transition-base;
      -o-transition: @transition-base;
      transition: @transition-base;
      box-shadow: @shadow-base;
      height: 40px;
      width: 100%;
    }
  }

  .table-card {
    -webkit-animation: cardAppear 0.7s ease-out;
    animation: cardAppear 0.7s ease-out;

    :deep(.ant-table) {
      border-radius: 8px;
      overflow: hidden;
      -webkit-transition: @transition-base;
      -o-transition: @transition-base;
      transition: @transition-base;

      .ant-table-thead > tr > th {
        background: -webkit-linear-gradient(135deg, @primary-color, lighten(@primary-color, 8%)); /* Safari 5.1-6.0 */
        background: -o-linear-gradient(135deg, @primary-color, lighten(@primary-color, 8%)); /* Opera 11.1-12.0 */
        background: -moz-linear-gradient(135deg, @primary-color, lighten(@primary-color, 8%)); /* Firefox 3.6-15 */
        background: linear-gradient(135deg, @primary-color, lighten(@primary-color, 8%)); /* 标准语法 */
        color: white;
        font-weight: 600;
        text-align: center;
        border-bottom: 2px solid fade(@accent-color, 30%);
        padding: 12px 8px;
        -webkit-transition: @transition-base;
        -o-transition: @transition-base;
        transition: @transition-base;
      }

      .ant-table-tbody > tr {
        -webkit-transition: @transition-base;
        -o-transition: @transition-base;
        transition: @transition-base;

        &:hover > td {
          background: fade(@secondary-color, 5%);
          -webkit-transform: scale(1.01);
          -ms-transform: scale(1.01);
          transform: scale(1.01);
        }

        > td {
          border-color: fade(@border-color, 50%);
          padding: 12px 8px;
          -webkit-transition: @transition-base;
          -o-transition: @transition-base;
          transition: @transition-base;
        }
      }
    }

    .animated-table {
      -webkit-animation: tableAppear 0.8s ease-out;
      animation: tableAppear 0.8s ease-out;
    }

    .table-input {
      border: 1px solid @border-color;
      border-radius: 4px;
      -webkit-transition: @transition-base;
      -o-transition: @transition-base;
      transition: @transition-base;

      &:focus {
        border-color: @primary-color;
        box-shadow: 0 0 0 2px fade(@primary-color, 15%);
      }
    }

    .action-btn {
      border-radius: 6px;
      font-weight: 500;
      -webkit-transition: @transition-base;
      -o-transition: @transition-base;
      transition: @transition-base;
      box-shadow: @shadow-base;
    }
  }

  .action-card {
    text-align: center;
    background: transparent;
    -webkit-animation: slideUp 0.6s ease-out;
    animation: slideUp 0.6s ease-out;

    .action-buttons {
      display: -webkit-box;
      display: -ms-flexbox;
      display: flex;
      -webkit-box-pack: center;
      -ms-flex-pack: center;
      justify-content: center;
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
    }
  }

  // 动画按钮样式
  .animated-btn {
    position: relative;
    overflow: hidden;

    &::before {
      content: "";
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: -webkit-linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
      background: -o-linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
      -webkit-transition: left 0.5s;
      -o-transition: left 0.5s;
      transition: left 0.5s;
    }

    &:hover::before {
      left: 100%;
    }

    &:hover {
      -webkit-transform: translateY(-2px);
      -ms-transform: translateY(-2px);
      transform: translateY(-2px);
      box-shadow: @shadow-hover;
    }

    &:active {
      -webkit-transform: translateY(0);
      -ms-transform: translateY(0);
      transform: translateY(0);
      box-shadow: @shadow-active;
    }
  }

  .primary-btn {
    background: -webkit-linear-gradient(135deg, @primary-color, darken(@primary-color, 8%)); /* Safari 5.1-6.0 */
    background: -o-linear-gradient(135deg, @primary-color, darken(@primary-color, 8%)); /* Opera 11.1-12.0 */
    background: -moz-linear-gradient(135deg, @primary-color, darken(@primary-color, 8%)); /* Firefox 3.6-15 */
    background: linear-gradient(135deg, @primary-color, darken(@primary-color, 8%)); /* 标准语法 */
    border: none;
    border-radius: 8px;
    padding: 0 32px;
    height: 44px;
    font-weight: 600;
    box-shadow: @shadow-base;
    -webkit-transition: @transition-base;
    -o-transition: @transition-base;
    transition: @transition-base;
    color: white;

    &:hover {
      background: -webkit-linear-gradient(135deg, lighten(@primary-color, 5%), @primary-color);
      background: -o-linear-gradient(135deg, lighten(@primary-color, 5%), @primary-color);
      background: linear-gradient(135deg, lighten(@primary-color, 5%), @primary-color);
      -webkit-transform: translateY(-2px) scale(1.02);
      -ms-transform: translateY(-2px) scale(1.02);
      transform: translateY(-2px) scale(1.02);
    }

    &:active {
      -webkit-transform: translateY(0) scale(1);
      -ms-transform: translateY(0) scale(1);
      transform: translateY(0) scale(1);
    }
  }

  .secondary-btn {
    border: 2px solid @secondary-color;
    color: @secondary-color;
    border-radius: 8px;
    padding: 0 32px;
    height: 44px;
    font-weight: 600;
    background: transparent;
    box-shadow: @shadow-base;
    -webkit-transition: @transition-base;
    -o-transition: @transition-base;
    transition: @transition-base;

    &:hover {
      background: fade(@secondary-color, 10%);
      color: darken(@secondary-color, 10%);
      border-color: darken(@secondary-color, 10%);
      -webkit-transform: translateY(-2px) scale(1.02);
      -ms-transform: translateY(-2px) scale(1.02);
      transform: translateY(-2px) scale(1.02);
    }

    &:active {
      -webkit-transform: translateY(0) scale(1);
      -ms-transform: translateY(0) scale(1);
      transform: translateY(0) scale(1);
    }
  }
}

// 关键帧动画定义 - 添加Webkit前缀以兼容Safari和旧版浏览器
@-webkit-keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@-webkit-keyframes slideDown {
  from {
    opacity: 0;
    -webkit-transform: translateY(-20px);
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    -webkit-transform: translateY(0);
    transform: translateY(0);
  }
}
@keyframes slideDown {
  from {
    opacity: 0;
    -webkit-transform: translateY(-20px);
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    -webkit-transform: translateY(0);
    transform: translateY(0);
  }
}

@-webkit-keyframes slideUp {
  from {
    opacity: 0;
    -webkit-transform: translateY(20px);
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    -webkit-transform: translateY(0);
    transform: translateY(0);
  }
}
@keyframes slideUp {
  from {
    opacity: 0;
    -webkit-transform: translateY(20px);
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    -webkit-transform: translateY(0);
    transform: translateY(0);
  }
}

@-webkit-keyframes cardAppear {
  from {
    opacity: 0;
    -webkit-transform: scale(0.95) translateY(10px);
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    -webkit-transform: scale(1) translateY(0);
    transform: scale(1) translateY(0);
  }
}
@keyframes cardAppear {
  from {
    opacity: 0;
    -webkit-transform: scale(0.95) translateY(10px);
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    -webkit-transform: scale(1) translateY(0);
    transform: scale(1) translateY(0);
  }
}

@-webkit-keyframes tableAppear {
  from {
    opacity: 0;
    -webkit-transform: translateX(-10px);
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    -webkit-transform: translateX(0);
    transform: translateX(0);
  }
}
@keyframes tableAppear {
  from {
    opacity: 0;
    -webkit-transform: translateX(-10px);
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    -webkit-transform: translateX(0);
    transform: translateX(0);
  }
}

// 响应式设计
@media (max-width: 768px) {
  .config-container {
    padding: 16px;

    .content-wrapper {
      padding: 0;
    }

    .config-card.connection-card {
      .config-row {
        .ant-col {
          &:first-child {
            margin-bottom: 8px;
          }

          span.config-label {
            -webkit-box-pack: flex-start;
            -ms-flex-pack: flex-start;
            justify-content: flex-start;
          }
        }
      }
    }

    .action-card .action-buttons {
      -webkit-box-orient: vertical;
      -webkit-box-direction: normal;
      -ms-flex-direction: column;
      flex-direction: column;
      gap: 12px;

      .ant-btn {
        width: 100%;
        margin: 4px 0;
      }
    }
  }
}
</style>
