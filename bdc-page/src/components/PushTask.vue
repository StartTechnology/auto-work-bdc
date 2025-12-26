<template>
  <a-card class="push-task-card" :bordered="true">
    <!-- 任务信息显示区域 -->
    <div class="task-info-section">
      <a-typography-title :heading="4" class="section-title">
        📋 任务信息
      </a-typography-title>
      <a-typography-title :heading="5">
        {{ taskInfo.business_type }}
      </a-typography-title>
      <a-descriptions
        :column="3"
        size="medium"
        bordered
        title="客户信息"
        :data="showCustomersInfo"
      />
      <a-descriptions
        :column="2"
        size="medium"
        bordered
        title="贷款信息"
        :data="showLoanInfo"
      >
      <a-descriptions-item v-for="item of showLoanInfo" :label="item.label" :span="item.span ?? 1">
          {{ item.value }}
        </a-descriptions-item>
      </a-descriptions>

      <a-descriptions
        :column="3"
        size="medium"
        bordered
        title="抵押信息">
        <a-descriptions-item v-for="item of showMortgageInfo" :label="item.label" :span="item.span ?? 1">
          {{ item.value }}
        </a-descriptions-item>
        </a-descriptions>
    </div>

    <!-- 操作区域 -->
    <div class="operation-section">
      <!-- 影像归档目录区域 -->
      <div class="input-group">
        <a-typography-title :heading="6" class="input-title">
          🖼️ 影像目录
        </a-typography-title>
          <a-input
            v-model="imgConfig.img_dir"
            placeholder="请输入影像目录路径"
            allow-clear
            class="path-input"
            :style="{ width: '500px' }"
          >
          </a-input>
      </div>

      <!-- 写入Excel目录区域 -->
      <div class="input-group">
        <a-typography-title :heading="6" class="input-title">
          📊 写入Excel目录
        </a-typography-title>
        <div class="input-row">
          <a-input
            v-model="pageConfig.businessXlsx_path"
            placeholder="请输入Excel输出目录路径"
            allow-clear
            class="path-input"
            :style="{ width: '500px' }"
          >
          </a-input>
          <a-button type="primary" class="action-button" @click="saveXlsxPath"> 保存路径 </a-button>
          <a-button type="primary" class="action-button" @click="writeExcel"> 写入Excel </a-button>
        </div>
      </div>
    </div>

    <!-- 提交任务按钮 -->
    <div class="submit-section">
      <a-button type="primary" status="success" long class="submit-button" @click="submitTask">
        🚀 提交任务
      </a-button>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import { BusinessConfig } from "../store/BusinessConfig";
import { ImgConfig } from "../store/ImgConfig.ts";
import { PageConfig } from "../store/config.ts"
import axios from "axios";
import { Message } from "@arco-design/web-vue";
const businessConfig = BusinessConfig();
const imgConfig = ImgConfig();
const pageConfig = PageConfig();

onMounted(() => {
  axios.get(pageConfig.get_businessXlsx_url).then((res)=>{
    pageConfig.businessXlsx_path=res.data;
  });

});

const taskInfo = computed(() => {
  let task = {
    business_type: businessConfig.business_type,
    customers: businessConfig.customer.slice(0, -1),
  } as any;

  //补充电话号码
  for (let i = 0; i < task.customers.length; i++) {
    if (i == 0) {
      continue;
    }
    if (task.customers[i].phone == "") {
      task.customers[i].phone = task.customers[i - 1].phone;
    }
  }

  if (businessConfig.loan_type != "") {
    task.loan_type = businessConfig.loan_type;
    task.loan_manger = businessConfig.loan_manager;
    task.loan_contract = businessConfig.loan_contract[0];
    task.loan_amount = businessConfig.loan_amount[0];
    task.loan_tream = businessConfig.loan_tream[0];
    task.loan_guarantee = businessConfig.loan_guarantee;
  }
  if (businessConfig.certificate.length > 1) {
    task.certificate = businessConfig.certificate.slice(0, -1);
  }
  if (businessConfig.business_type.includes("合并登记")) {
    task.obligor = businessConfig.developer_info;
    task.purchase_contract = businessConfig.customer_contract;
  }
  task.img_path = imgConfig.img_dir;
  return task;
});

//展示信息对象
//客户信息
const showCustomersInfo = computed(() => {
  let customersInfo = [] as any;
  for (let i = 0; i < taskInfo.value.customers.length; i++) {
    customersInfo.push(
      {
        label: "姓名：",
        value: taskInfo.value.customers[i].name,
      },
      {
        label: "身份证号：",
        value: taskInfo.value.customers[i].id,
      },
      {
        label: "电话：",
        value: taskInfo.value.customers[i].phone,
      }
    );
  }
  return customersInfo;
});
//贷款信息
const showLoanInfo = computed(() => {
  if ("loan_type" in taskInfo.value) {
    return [
      {
        label: "贷款类型：",
        value: taskInfo.value.loan_type,
        span:1
      },
      {
        label: "客户经理",
        value: taskInfo.value.loan_manger,
        span:1
      },
      {
        label: "贷款金额：",
        value: taskInfo.value.loan_amount+" 元",
        span:1
      },
      {
        label: "贷款期限：",
        value:
          taskInfo.value.loan_tream?.start +
          " 至 " +
          taskInfo.value.loan_tream?.end,
          span:1
      },
      {
        label: "合同编号：",
        value: taskInfo.value.loan_contract,
        span:2
      },
      {
        label: "担保范围",
        value: taskInfo.value.loan_guarantee,
        span:2
      },
    ];
  }
  return [];
});
//抵押信息
const showMortgageInfo = computed(() => {
  let mortgageInfo = [] as any;
  if ("obligor" in taskInfo.value){
    mortgageInfo.push({
      label: "购房备案合同号",
      value: taskInfo.value.purchase_contract,
      span: 3
    });
    mortgageInfo.push({
      label: "开发商名称",
      value: taskInfo.value.obligor.name,
      span: 3
    });
    mortgageInfo.push({
      label: "开发商证件号码",
      value: taskInfo.value.obligor.id,
      span: 3
    });
    mortgageInfo.push({
      label: "开发商联系方式",
      value: taskInfo.value.obligor.phone,
      span: 3
    });
    return mortgageInfo;
  } 
  else if ("certificate" in taskInfo.value) {
    let mortgageInfo = [] as any;
    for (let i = 0; i < taskInfo.value.certificate.length; i++) {
      mortgageInfo.push({
        label: "权证编号",
        value: taskInfo.value.certificate[i],
        span: 3
      });
    }
    return mortgageInfo;
  }
   
  
});

//保存xlsx地址
function saveXlsxPath() {
  axios.post(pageConfig.set_businessXlsx_url, { path: pageConfig.businessXlsx_path }).then(() => {
    Message.success("保存地址成功");
  }).catch((err) => {
    Message.error("保存地址失败:"+err.message);
  })
  ;
}

//写入excel
function writeExcel() {
  axios.post(businessConfig.write_data_url,{"business_info":taskInfo.value,'path':pageConfig.businessXlsx_path}).then(()=>{
    Message.success("写入完成");
  });
}

//提交任务
const changeTab_emit=defineEmits<{(e:'tab-change',key:string):void}>();
function submitTask()
{
  axios.post(businessConfig.submit_task_url,taskInfo.value).then(()=>{
    Message.success("任务完成");
    businessConfig.reset();
    imgConfig.images.length=0;
    changeTab_emit('tab-change','2');
  })
}
</script>

<style lang="less" scoped>
.push-task-card {
  max-width: 800px;
  margin: 20px auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border-radius: 12px;

  &:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
  }
}

.section-title {
  margin-bottom: 16px;
  color: #1f2937;
  font-weight: 600;
}

.input-group {
  margin-bottom: 24px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
  transition: all 0.3s ease;

  &:hover {
    background: #f1f5f9;
    transform: scale(1.01);
  }
}

.input-title {
  margin-bottom: 12px;
  color: #374151;
  font-weight: 500;
}

.input-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.path-input {
  transition: all 0.3s ease;

  &:focus-within {
    box-shadow: 0 0 0 2px rgba(var(--primary-6), 0.1);
  }
}

.action-button {
  transition: all 0.3s ease;
  border-radius: 6px;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(var(--primary-6), 0.3);
  }

  &:active {
    transform: translateY(0);
  }
}

.submit-section {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.submit-button {
  height: 48px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;

  &:hover:not(.arco-btn-disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(var(--primary-6), 0.4);
  }

  &:active {
    transform: translateY(0);
  }
}

.task-descriptions {
  margin-bottom: 8px;

  :deep(.arco-descriptions-item-label) {
    font-weight: 500;
    color: #6b7280;
  }

  :deep(.arco-descriptions-item-value) {
    color: #1f2937;
    font-weight: 400;
  }
}

.operation-section {
  margin: 24px 0;
}

// 响应式设计
@media (max-width: 768px) {
  .push-task-card {
    margin: 10px;
    border-radius: 8px;
  }

  .input-row {
    flex-direction: column;
    align-items: stretch;
  }

  .path-input {
    width: 100% !important;
  }

  .action-button {
    width: 100%;
  }
}

// 加载动画
:deep(.arco-btn-loading) {
  opacity: 0.8;
}

// 卡片标题样式优化
:deep(.arco-card-header) {
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 16px;
  margin-bottom: 16px;
}
</style>
