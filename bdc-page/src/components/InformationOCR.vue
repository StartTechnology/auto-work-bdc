<template>
  <a-layout class="information-ocr-container">
    <!-- 左侧面板 -->
    <a-layout-sider class="left-panel" :width="500">
      <!-- 材料类型选择和操作区域 -->
      <div class="selection-section">
        <a-space :size="16" class="selection-controls">
          <a-select
            v-model="selectedMaterialType"
            placeholder="请选择材料类型"
            class="material-select"
            allow-clear
          >
            <a-option
              v-for="type in businessConfig.business_materials"
              :key="type"
              :value="type"
              >{{ type }}</a-option
            >
          </a-select>

          <a-select
            v-model="selectedOCRType"
            placeholder="请选择OCR类型"
            class="material-select"
          >
            <a-option
              v-for="type in businessConfig.OCRTYPE"
              :key="type.value"
              :value="type.value"
              :disabled="type.is_loading"
              >{{ type.name }}</a-option
            >
          </a-select>

          <a-button
            type="primary"
            @click="handleStartOCR"
            class="ocr-button"
            :loading="ocrLoading"
          >
            <template #icon>
              <icon-scan />
            </template>
            开始OCR
          </a-button>
        </a-space>
      </div>

      <!-- 缩略图网格区域 -->
      <div class="thumbnails-section">
        <div class="thumbnails-header">
          <span class="section-title">材料缩略图</span>
          <a-checkbox
            v-model="selectAll"
            @change="handleSelectAll"
            class="select-all-checkbox"
          >
            全选
          </a-checkbox>
        </div>

        <a-row :gutter="[12, 12]" class="thumbnails-grid">
          
          <a-col
            v-for="(thumbnail) in thumbnails"
            :key="thumbnail.img.path"
            :span="12"
          >
            <a-checkbox
                v-model="thumbnail.selected"
                class="thumbnail-checkbox"
              >
              <template #checkbox="{ checked }">
            <div
              class="thumbnail-card"
              :class="{ 'thumbnail-selected': checked }"
              
            >
              <a-image
                :src="thumbnail.img.url"
                :alt="thumbnail.img.name"
                width="190"
                class="thumbnail-img"
                showLoader 
                :preview="false"
              ></a-image>

              <div class="thumbnail-info">
                <span class="thumbnail-name">{{ thumbnail.img.name }}</span>
              </div>
            </div>
            </template>
            </a-checkbox>
          </a-col>
        
        </a-row>
      </div>
    </a-layout-sider>

    <!-- 右侧信息展示区域 -->
    <a-layout-content class="right-panel">
      <a-tabs type="rounded" class="info-tabs">
        <template #extra>
          <a-button type="primary" @click="handleArchive">影像归档</a-button>
        </template>
        <!-- 客户信息标签页 -->
        <a-tab-pane key="customer" title="客户信息">
            <a-table
              :columns="customerTableTitle"
              :data="businessConfig.customer"
              :pagination="false"
              style="margin-top: 20px;"
            >
              <template #name="{ rowIndex }">
                <a-input
                  v-if="businessConfig.customer[rowIndex]"
                  v-model="businessConfig.customer[rowIndex].name"
                  placeholder="请输入客户姓名..."
                  allow-clear
                >
                </a-input>
              </template>
              <template #id="{ rowIndex }">
                <a-input
                  v-if="businessConfig.customer[rowIndex]"
                  v-model="businessConfig.customer[rowIndex].id"
                  placeholder="请输入客户证件号码..."
                  allow-clear
                ></a-input>
              </template>
              <template #phone="{ rowIndex }">
                <a-input
                  v-if="businessConfig.customer[rowIndex]"
                  v-model="businessConfig.customer[rowIndex].phone"
                  placeholder="请输入客户联系方式..."
                  allow-clear
                ></a-input>
              </template>
              <template #optional="{ rowIndex }">
                <a-button @click="handleDeleteCustomer(rowIndex)"
                  ><icon-delete
                /></a-button>
              </template>
            </a-table>
            
            <a-button type="text" long  @click="handAddCustomer">
              新增行
            </a-button>
            
            
        </a-tab-pane>

        <!-- 贷款信息标签页 -->
        <a-tab-pane key="loan" title="贷款信息" v-if="!businessConfig.business_type.includes('解押')">
          
            <a-form :model="business_form" style="margin-top: 20px;">
              <!-- 贷款种类 -->
              <a-form-item label="贷款种类:">
                <a-select
                  v-model="businessConfig.loan_type"
                  placeholder="请选择贷款种类"
                  style="width: 480px"
                  allow-clear
                >
                  <a-option
                    v-for="type in loan_type"
                    :key="type"
                    :value="type"
                    >{{ type }}</a-option
                  >
                </a-select>
              </a-form-item>
              <!-- 客户经理 -->
               <a-form-item label="客户经理:">
                <a-select
                  v-model="businessConfig.loan_manager"
                  placeholder="请选择客户经理"
                  style="width: 480px"
                  allow-clear
                  allow-search
                >
                  <a-option
                    v-for="manager in loan_manager"
                    :key="manager"
                    :value="manager"
                    >{{ manager }}</a-option
                  >
                </a-select>
              </a-form-item>
              <a-form-item label="合同编号:">
                <a-input
                  v-model="businessConfig.loan_contract[0]"
                  placeholder="请输入合同编号"
                  allow-clear
                  style="width: 480px"
                ></a-input>
              </a-form-item>
              <a-form-item label="贷款金额（元）:">
                <a-input-number
                  v-model="businessConfig.loan_amount[0]"
                  placeholder="请输入贷款金额"
                  hide-button
                  allow-clear
                  style="width: 480px"
                ></a-input-number>
                <a-tag checkable color="arcoblue" v-if="businessConfig.loan_amount[0] != ''&&businessConfig.loan_amount[0] != null">{{ numberToZhCurrency(businessConfig.loan_amount[0]!) }}</a-tag>
              </a-form-item>

              <a-form-item label="贷款期限:">
                <a-range-picker
                  format="YYYYMMDD"
                  v-model="loan_tream"
                  value-format="YYYYMMDD"
                  style="width: 254px"
                ></a-range-picker>
              </a-form-item>
              <a-form-item label="担保范围:">
                <a-textarea placeholder="请输入担保范围（200字以内）"
                allow-clear
                v-model="businessConfig.loan_guarantee"
                style="width: 480px;"
                :max-length="200"
                show-word-limit
                auto-size/>
              </a-form-item>
            </a-form>
          
        </a-tab-pane>
          
        <!-- 抵押信息标签页 -->
        <a-tab-pane key="mortgage" title="抵押信息" >
          <a-space
            direction="vertical"
            fill
            v-if="!businessConfig.business_type.includes('合并登记')">
            <a-table
              :columns="certificateTableTitle"
              :data="certificate"
              :pagination="false"
              style="margin-top: 20px;"
            >
          <template #id="{ rowIndex }">
                <a-input
                  v-model="businessConfig.certificate[rowIndex]"
                  placeholder="请输入权证编号..."
                  allow-clear
                >
                </a-input>
          </template>
          <template #optional="{ rowIndex }">
                <a-button @click="handleDeletecertificate(rowIndex)"
                  ><icon-delete
                /></a-button>
            </template>
            
          </a-table>
            <a-button type="text" long  @click="handAddcertificate">
              新增行
            </a-button>
          </a-space>


          <a-form :model="business_form" style="margin-top: 20px;" v-else>
          <!-- 购房合同 -->
              <a-form-item label="购房合同号:">
                <a-input
                  v-model="businessConfig.customer_contract"
                  placeholder="请输入购房合同编号（备案合同）"
                  allow-clear
                  style="width: 480px"
                ></a-input>
              </a-form-item>
          <!-- 选择开发商信息 -->
            <a-form-item label="开发商:">
                <a-select
                  v-model="businessConfig.developer_info"
                  placeholder="请选择开发商"
                  style="width: 480px"
                  allow-clear
                  allow-search
                  value-key="id"
                >
                  <a-option
                    v-for="item in developer"
                    :key="item.id"
                    :value="item"
                    >{{ item.name }}</a-option>
                </a-select>
              </a-form-item>
          </a-form>

        </a-tab-pane>
      </a-tabs>
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
// ==================================================
// 引入Arco Design Vue组件和图标
// ==================================================
import { ref, reactive, computed, watch ,toRefs } from "vue";
import { numberToZhCurrency} from "number-to-zh-currency";
import { Message,Notification  } from "@arco-design/web-vue";
import {
  IconScan,
  IconDelete,
} from "@arco-design/web-vue/es/icon";

import { BusinessConfig, type CustomerInfo } from "../store/BusinessConfig";
import { ImgConfig, type ImgItem } from "../store/ImgConfig.ts";
import axios from "axios";


const businessConfig = BusinessConfig();
const imgConfig = ImgConfig();

// ==================================================
// 类型定义
// ==================================================
interface Thumbnail {
  img: ImgItem;
  selected: boolean;
}


// ==================================================
// 响应式数据
// ==================================================
// 材料类型选择
const selectedMaterialType = ref<string>("");
const selectedOCRType = ref<string>("");

// OCR处理状态
const ocrLoading = ref<boolean>(false);

// 缩略图数据
const thumbnails = ref([] as Thumbnail[]);

watch(selectedMaterialType, () => {
  thumbnails.value.length = 0;
  let filter_imgs = [];
  if (selectedMaterialType.value == "") {
    filter_imgs = imgConfig.images;
  } else {
    filter_imgs = imgConfig.images.filter(
      (item) => item.categories == selectedMaterialType.value
    );
  }

  for (let img of filter_imgs) {
    thumbnails.value.push({ img: img, selected: false });
  }
});

// 全选状态
const selectAll = computed({
  get: () =>
    thumbnails.value.length > 0 &&
    thumbnails.value.every((item) => item.selected),
  set: (value: boolean) => {
    thumbnails.value.forEach((item) => {
      item.selected = value;
    });
  },
});

// 处理全选
const handleSelectAll = (checked: boolean) => {
  thumbnails.value.forEach((item) => {
    item.selected = checked;
  });
};

//贷款种类
const loan_type= ref<string[]>([]);
//客户经理
const loan_manager= ref<string[]>([]);
//担保范围
let loan_guarantee:any;
//开发商信息
const developer = ref<CustomerInfo[]>([]);

watch([()=>businessConfig.loan_amount[0],()=>businessConfig.loan_type], () => {
      businessConfig.loan_guarantee = loan_guarantee[businessConfig.loan_type];
      if (businessConfig.loan_amount[0] != ""&&businessConfig.loan_amount[0] != null && businessConfig.loan_guarantee.includes("MONEY")) {
        let MONEY:string=numberToZhCurrency(businessConfig.loan_amount[0]!) as string;
        MONEY=MONEY.substring(3);
        businessConfig.loan_guarantee=businessConfig.loan_guarantee.replace("MONEY", MONEY);
        businessConfig.loan_guarantee=businessConfig.loan_guarantee.replace("money", businessConfig.loan_amount[0]!);
      }
});

const props = defineProps({
  isActive: Boolean
});
const { isActive } = toRefs(props); // 使用 toRefs 保持响应性
//初始化数据
watch(isActive,() => {
  thumbnails.value.length = 0;
  for (let img of imgConfig.images) {
    thumbnails.value.push({ img: img, selected: false });
  }

  axios.get(businessConfig.get_loan_type_url).then((res) => {
    loan_type.value = res.data;
  });
  axios.get(businessConfig.get_loan_manager_url).then((res) => {
    loan_manager.value = res.data;
  });
  axios.get(businessConfig.get_loan_guarantee_url).then((res) => {
    loan_guarantee= res.data;
  });
  axios.get(businessConfig.get_developer_info_url).then((res) => {
    developer.value.length = 0;
    res.data.forEach((element:any) => {
      developer.value.push({name:element[0],id:element[1],phone:element[2]});
      //console.log(developer.value);
    });
  })
})

// 开始OCR处理
const handleStartOCR = async () => {
  
  const selectedItems = thumbnails.value.filter((item) => item.selected);
  if (selectedItems.length === 0) {
    Message.warning("请先选择要识别的材料");
    return;
  }
  if (selectedOCRType.value == "") {
    Message.warning("请选择OCR类别");
    return;
  }

  let selectOCRType=businessConfig.OCRTYPE.find((item) => item.value == selectedOCRType.value);
  
  selectOCRType!.is_loading = true;
  const selectedOCRType_value=selectedOCRType.value;
  const selectedOCRType_name=selectOCRType!.name;
  businessConfig.OCRMessage.push(selectedOCRType_name);
  axios
    .post(imgConfig.ocr_imgs_url, {
      file_list: thumbnails.value
        .filter((item) => item.selected)
        .map((item) => item.img.path),
      ocr_type: parseInt(selectedOCRType_value),
    })
    .then((res) => {
      //console.log(res.data);
      switch (selectedOCRType_value) {
        case "1":
          res.data.forEach((item: any) => {
            businessConfig.customer.unshift({
              name: item.name,
              id: item.id,
              phone: "",
            });
          });
          break;
        case "2":
          res.data.forEach((item: any) => {
            if(item.contract!=null){
            businessConfig.loan_contract.unshift(item.contract);}
          });
          break;
        case "3":
          res.data.forEach((item: any) => {
            if(item.loan!=null){
            businessConfig.loan_amount.unshift(item.loan);}
          });
          break;
        case "4":
          res.data.forEach((item: any) => {
            if(item!=null){
            businessConfig.loan_tream.unshift(item);}
          });
          break;
        case "5":
          res.data.forEach((item: any) => {
            if(item.id!=null){businessConfig.certificate.unshift(item.id);}
          });
          break;
        case "6":
          res.data.forEach((item: any) => {
            if(item.id!=null){businessConfig.certificate.unshift(item.id);}
          });
          break;
      }

      //删除OCR信息队列中的对应值
      const index:number= businessConfig.OCRMessage.indexOf(selectedOCRType_name)
      if(index>-1){businessConfig.OCRMessage.splice(index,1)}

    })
    .catch((err) => {
      Message.error("OCR请求错误：" + err);
      selectOCRType!.is_loading = false;
      //删除OCR信息队列中的对应值
      const index:number= businessConfig.OCRMessage.indexOf(selectedOCRType_name)
      if(index>-1){businessConfig.OCRMessage.splice(index,1)}
    })
    .finally(() => {
      selectOCRType!.is_loading = false;
    });
    //清除选择
    selectedOCRType.value = ""
    //清除选中状态
    thumbnails.value.forEach((item) => {
      item.selected = false;
    });
};

//根据OCR信息对应显示当前的通知信息
watch(businessConfig.OCRMessage,()=>{
  if(businessConfig.OCRMessage.length>0){
    const into_content:string=businessConfig.OCRMessage.join(" ");
    Notification.info({
        id:'ocr_information',
        title: '正在OCR图片信息',
        content: into_content,
        closable: true,
        duration:999999999,
    })
  }
  else{
        Notification.success({
        id:'ocr_information',
        title: 'OCR已完成',
        content: '所有图片已处理完成',
        closable: true,
        duration:2000,
    })
  }
},{deep:true})

//客户信息表格数据标题
const customerTableTitle = reactive([
  {
    title: "客户姓名",
    dataIndex: "name",
    align: "center",
    slotName: "name",
    tooltip: "true",
    
  },
  {
    title: "证件号码",
    dataIndex: "id",
    align: "center",
    slotName: "id",
    tooltip: "true",
    minWidth:"200"
  },
  {
    title: "联系方式",
    dataIndex: "phone",
    align: "center",
    slotName: "phone",
    tooltip: "true",
  },
  {
    title: "操作",
    slotName: "optional",
    align: "center",
  },
]);

//删除客户信息
const handleDeleteCustomer = (index: number) => {
  if (businessConfig.customer[index]) {
    businessConfig.customer.splice(index, 1);
  }
};
//新加客户信息行
watch(businessConfig.customer, () => {
  let customer_length = businessConfig.customer.length;
  if (
    customer_length == 0 ||
    businessConfig.customer[customer_length - 1]?.id != "" ||
    businessConfig.customer[customer_length - 1]?.name != ""
  ) {
    businessConfig.customer.push({ name: "", id: "", phone: "" });
  }
});
//新增客户信息的按钮
function handAddCustomer() {
  businessConfig.customer.push({ name: "", id: "", phone: "" });
}

//占位无作用 不可删除
const business_form = reactive({});
//日期
const loan_tream = computed({
  get: () => {
    return [
      businessConfig.loan_tream[0]?.start,
      businessConfig.loan_tream[0]?.end,
    ];
  },
  set: (value: string[]) => {
    if (value != undefined && value.length > 1) {
      if (businessConfig.loan_tream.length == 0) {
        businessConfig.loan_tream.push({ start: value[0]!, end: value[1]! });
      }
      else{
        businessConfig.loan_tream[0]!.start=value[0]!;
        businessConfig.loan_tream[0]!.end=value[1]!;
      }
    } else {
      businessConfig.loan_tream.length = 0;
    }
  },
});
//权证信息数据标题
const certificateTableTitle=reactive([
  {
    title: "权证编号",
    dataIndex: "id",
    align: "center",
    slotName: "id",
    tooltip: "true",
  },
  {
    title: "操作",
    slotName: "optional",
    align: "center",
  },
]);
const certificate=computed(()=>{
  return businessConfig.certificate.map((item)=>{return {'id':item}})
});
//删除权证单行信息
const handleDeletecertificate=(index:number)=>{
  if (businessConfig.certificate[index]||businessConfig.certificate[index]=='') {
    businessConfig.certificate.splice(index, 1);
  }
}
//新加权证信息行
watch(businessConfig.certificate, () => {
  let certificate_length = businessConfig.certificate.length;
  if (
    certificate_length == 0 ||
    businessConfig.certificate[certificate_length - 1]!= "" 
    ) {
    businessConfig.certificate.push('');
  }
});
//新增权证信息行的按钮
function handAddcertificate() {
  businessConfig.certificate.push('');
}

//影像归档
const changeTab_emit=defineEmits<{(e:'tab-change',key:string):void}>();
function handleArchive() {
  
  axios.post(imgConfig.archive_img_url, {
    path:imgConfig.temp_img_dir,
    category:businessConfig.business_type,
    file_list:businessConfig.customer.map(item=>{return item.name}).slice(0,-1)
  }).then((res)=>{
    imgConfig.img_dir=res.data;
    changeTab_emit('tab-change','4');
  }).catch(
    (err)=>{
      Message.error("影像归档请求错误："+err.message);
    }
  );

}


</script>

<style lang="less" scoped>
// ==================================================
// 主容器样式
// ==================================================
.information-ocr-container {
  height: 100vh;
  background-color: #f5f6f7;

  // 布局过渡动画
  transition: all 0.3s ease-in-out;
}

// ==================================================
// 左侧面板样式
// ==================================================
.left-panel {
  background: #fff;
  border-right: 1px solid #e5e6eb;
  padding: 16px;
  display: flex;
  flex-direction: column;
  height: 100%;

  .selection-section {
    margin-bottom: 20px;

    .selection-controls {
      width: 100%;

      .material-select {
        flex: 1;
      }

      .ocr-button {
        min-width: 100px;
      }
    }
  }

  .thumbnails-section {
    flex: 1;
    overflow-y: auto;

    .thumbnails-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;

      .section-title {
        font-size: 16px;
        font-weight: 600;
        color: #1d2129;
      }

      .select-all-checkbox {
        font-size: 14px;
      }
    }

    .thumbnails-grid {
      max-height: calc(100vh - 200px);
      overflow-y: auto;

      .thumbnail-card {
        position: relative;
        border: 2px solid #f0f0f0;
        border-radius: 8px;
        padding: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        background: #fff;

        &:hover {
          border-color: #3491fa;
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

          .thumbnail-overlay {
            opacity: 1;
          }
        }

        &.thumbnail-selected {
          border-color: #3491fa;
          background-color: #f0f8ff;
        }

        .thumbnail-checkbox {
          position: absolute;
          top: 8px;
          left: 8px;
          z-index: 2;
        }

        .thumbnail-image {
          position: relative;
          width: 100%;
          height: 120px;
          overflow: hidden;
          border-radius: 4px;
          margin-bottom: 8px;

          .thumbnail-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
          }

          .thumbnail-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.3s ease;

            .zoom-icon {
              color: #fff;
              font-size: 24px;
            }
          }
        }

        .thumbnail-info {
          text-align: center;

          .thumbnail-name {
            display: block;
            font-size: 12px;
            color: #1d2129;
            margin-bottom: 4px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
          }

          .thumbnail-size {
            font-size: 11px;
            color: #86909c;
          }
        }
      }
    }
  }
}

// ==================================================
// 右侧面板样式
// ==================================================
.right-panel {
  padding: 16px;
  background: #fff;
  margin: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

  .info-tabs {
    height: 100%;

    :deep(.arco-tabs-content) {
      padding-top: 0;
    }

    .info-section {
      .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;

        .section-title {
          margin: 0;
          color: #1d2129;
          font-weight: 600;
        }
      }

      .editable-table {
        :deep(.arco-table-th) {
          background-color: #f7f8fa;
          font-weight: 600;
        }

        .field-name {
          font-weight: 500;
          color: #4e5969;
        }

        .ocr-result-input,
        :deep(.arco-input) {
          border: 1px solid #e5e6eb;
          transition: border-color 0.3s ease;

          &:focus {
            border-color: #3491fa;
            box-shadow: 0 0 0 2px rgba(52, 145, 250, 0.1);
          }
        }

        .confidence-tag {
          font-weight: 600;
          border: none;
        }
      }
    }
  }
}

// ==================================================
// 响应式设计
// ==================================================
@media (max-width: 1200px) {
  .information-ocr-container {
    flex-direction: column;

    .left-panel {
      width: 100% !important;
      height: 40vh;
    }

    .right-panel {
      margin: 8px;
    }
  }
}

// ==================================================
// 动画定义
// ==================================================
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.thumbnail-card {
  animation: fadeIn 0.5s ease;
}

// 为每个缩略图卡片添加延迟动画
.thumbnails-grid .a-col {
  &:nth-child(odd) .thumbnail-card {
    animation-delay: 0.1s;
  }
  &:nth-child(even) .thumbnail-card {
    animation-delay: 0.2s;
  }
}
</style>
