<template>
  <div class="business-material-container">
    <!-- 背景动态光影效果 -->
    <div class="dynamic-light-effect"></div>

    <!-- 合并的业务信息区域 -->
    <div class="section combined-info-section">
      <a-card title="业务信息" class="glow-card">
        <div class="combined-info-content">
          <a-row :gutter="32" class="info-row">
            <a-col :xs="24" :md="12" :lg="8">
              <div class="info-item">
                <label class="info-label">业务类型选择</label>
                <a-select
                  v-model="selectedBusinessType"
                  class="business-select"
                  placeholder="请选择业务类型"
                  size="large"
                  allow-clear
                >
                  <a-option
                    v-for="type in businessTypes"
                    :key="type"
                    :value="type"
                  >
                    {{ type }}
                  </a-option>
                </a-select>
              </div>
            </a-col>

            <a-col :xs="24" :md="12" :lg="16">
              <div class="info-item">
                <label class="info-label">所需业务材料</label>
                <div class="material-checkbox-content">
                  <a-checkbox-group
                    v-model="selectedMaterials"
                    class="material-checkbox-group"
                  >
                    <a-row :gutter="[12, 12]">
                      <a-col
                        v-for="material in materialOptions"
                        :key="material"
                        :span="8"
                      >
                        <a-checkbox
                          :value="material"
                          class="material-checkbox"
                          disabled
                        >
                          <span class="material-label">{{ material }}</span>
                        </a-checkbox>
                      </a-col>
                    </a-row>
                  </a-checkbox-group>
                </div>
              </div>
            </a-col>
          </a-row>
        </div>
      </a-card>
    </div>

    <!-- 图片管理区域 -->
    <div class="section image-management-section">
      <a-row :gutter="24">
        <a-col :xs="24" :lg="12">
          <a-card title="图片目录管理" class="glow-card">
            <div class="image-directory-content">
              <div class="input-group">
                <a-input
                  v-model="imgConfig.temp_img_dir"
                  placeholder="请输入图片目录路径"
                  class="directory-input"
                  size="large"
                  allow-clear
                />
                <a-button
                  type="primary"
                  class="read-image-btn"
                  @click="handleReadImages"
                  size="large"
                >
                  <template #icon>
                    <FolderOpenOutlined />
                  </template>
                  读取图片
                </a-button>
              </div>

              <!-- 图片缩略图展示 -->

              <div v-if="getImagesByCategory('').length" class="thumbnail-grid">
                <a-image-preview-group>
                  <div
                    v-for="img in getImagesByCategory('')"
                    :key="img.path"
                    class="thumbnail-item"
                  >
                    <div class="thumbnail-wrapper">
                      <a-image
                        :src="img.url"
                        class="thumbnail-image"
                        fit="contain"
                        show-loader
                        width="100"
                      />

                      <div class="thumbnail-overlay">
                        <span class="image-name">{{ img.name }}</span>
                      </div>
                    </div>
                  </div>
                </a-image-preview-group>
              </div>
              <div v-else class="empty-thumbnail">
                <div class="empty-content">
                  <folder-open-outlined class="empty-icon" />
                  <p>暂无图片</p>
                </div>
              </div>
            </div>
          </a-card>
        </a-col>

        <a-col :xs="24" :lg="12">
          <a-card title="材料分类区域" class="glow-card">
            <div class="classification-content">
              <!-- 响应式栅格布局：根据屏幕尺寸调整每行分类数量 -->
              <a-row
                :gutter="[16, 16]"
                class="classification-areas"
                justify="start"
              >
                <a-col
                  v-for="category in materialCategories"
                  :key="category.label"
                  :span="11"
                >
                  <a-card class="category-card">
                    <template #title>
                      {{ category.label }} 
                    </template>
                    <template #actions>
                        <a-button
                            type="text"
                            size="small"
                            @click="handleAddImage(category)"
                            class="action-btn"
                          >
                            <template #icon>
                              <PlusOutlined />
                            </template>
                            增加
                          </a-button>
                          <a-button
                            type="text"
                            size="small"
                            @click="handleClearCategory(category)"
                            class="action-btn"
                          >
                            <template #icon>
                              <DeleteOutlined />
                            </template>
                            清空
                          </a-button>
                    </template>
                    <!-- 材料分类图片缩略图区 -->
                    <div class="category-images">
                      <a-image-preview-group>
                        <div
                          v-for="(img, index) in getImagesByCategory(
                            category.label
                          )"
                          :key="img.path"
                          class="category-image-item"
                          :style="{ '--animation-delay': `${index * 0.1}s` }"
                        >
                          <div class="image-card">
                            <!-- 图片容器 -->
                            <div class="image-container">
                              <a-image
                                :src="img.url"
                                fit="contain"
                                show-loader
                                class="thumbnail-image"
                                :preview-src-list="[img.url]"
                                width="100"
                              >
                                <template #loader>
                                  <div class="image-loader">
                                    <a-spin />
                                    <span>加载中...</span>
                                  </div>
                                </template>
                              </a-image>

                              <!-- 悬浮操作层 -->
                              
                                  <a-button
                                    class="delete-btn"
                                    @click="handleRemoveImage(img)"
                                  >
                                    <template #icon>
                                      <CloseOutlined />
                                    </template>
                                  </a-button>
                               
                            </div>

                            <!-- 图片信息 -->
                            <div class="image-info">
                              <span class="image-name" :title="img.name">{{
                                img.name
                              }}</span>
                            </div>
                          </div>
                        </div>
                      </a-image-preview-group>

                      <!-- 空状态 -->
                      <div
                        v-if="getImagesByCategory(category.label).length === 0"
                        class="empty-category"
                        @click="handleAddImage(category)"
                      >
                        
                        <div class="empty-content">
                          <div class="empty-icon">
                            <FolderOpenOutlined />
                          </div>
                          <p class="empty-text">暂无图片</p>
                        </div>
                      </div>
                    </div>
                  </a-card>
                </a-col>
              </a-row>
            </div>
          </a-card>
        </a-col>
      </a-row>
    </div>

    <!-- 归档操作区域 -->
    <div class="section archive-section">
      <div class="archive-content">
        <a-button
          type="primary"
          size="large"
          class="archive-btn"
          @click="handleNext"
        >
          <template #icon>
            <SaveOutlined />
          </template>
          下一步
        </a-button>
        
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import {
  FolderOpenOutlined,
  SaveOutlined,
  PlusOutlined,
  DeleteOutlined,
  CloseOutlined,
} from "@ant-design/icons-vue";
import { message } from "ant-design-vue";

import axios from "axios";
import { PageConfig } from "../store/config";
import { ImgConfig,type ImgItem } from "../store/ImgConfig";
import { BusinessConfig } from "../store/BusinessConfig";

const pageConfig = PageConfig();
const imgConfig = ImgConfig();
const businessConfig = BusinessConfig();

// 业务类型数据
const businessTypes = computed(() => {
  return pageConfig.business_config_colums.map((item) => item["title"]).slice(1);
})
// 材料选项数据
const materialOptions = computed(() => {
  return pageConfig.business_config_data.map((item) => item["0"]);
})

onMounted(() => {
  //初始化图片设置的目录
  imgConfig.getImgConfig();
});
const selectedBusinessType = ref<string>("");

const selectedMaterials = computed(() => {
  if (selectedBusinessType.value == "") {
    return [];
  } else {
    let index_colum: string = (
      pageConfig.business_config_colums as {
        dataIndex: string;
        title: string;
      }[]
    ).find((item) => item.title === selectedBusinessType.value)!.dataIndex;
    return pageConfig.business_config_data
      .filter((item) => item[index_colum] == "1")
      .map((item) => item["0"]);
  }
});


//图片分类的接口
interface ImgCategories {
  label: string;
}

// 材料分类数据
const materialCategories = ref([] as ImgCategories[]);
watch(selectedMaterials, async () => {
  //增加分类
  selectedMaterials.value.forEach((item) => {
    const findImgCategories = materialCategories.value.find(
      (imgCategories) => imgCategories.label == item
    );
    if (!findImgCategories) {
      materialCategories.value.push({ label: item });
    }
  });
  //删除没有的分类
  for (let index = materialCategories.value.length - 1; index >= 0; index--) {
    const element = selectedMaterials.value.find(
      (item) => item == materialCategories.value[index]!.label
    );
    if (!element) {
      materialCategories.value.splice(index, 1);
    }
  }
  //排序
  const sortId: string[] = pageConfig.business_config_data.map(
    (item) => item["0"]
  );
  materialCategories.value.sort(
    (a, b) => sortId.indexOf(a.label) - sortId.indexOf(b.label)
  );
  //类型同步本地目录
  if (imgConfig.temp_img_dir !== "") {
      axios
    .post(imgConfig.sync_img_category_url, {
      path: imgConfig.temp_img_dir,
      category_list: materialCategories.value.map((item) => item.label),
    })
    .catch((error) => {
      message.error("服务器错误：" + error.message);
    });
  }
  else{
    message.warning("请输入图片目录路径");
  }

  //给业务数据赋值
  businessConfig.business_type=selectedBusinessType.value;
  businessConfig.business_materials=materialCategories.value.map((item) => item.label);
});

// 图片目录相关数据 imgConfig.temp_img_dir
const imageThumbnails = ref([] as ImgItem[]);

// 读取图片
const handleReadImages = () => {
  if (imgConfig.temp_img_dir !== "") {

    axios
      .post(imgConfig.temp_img_url, { path: imgConfig.temp_img_dir })
      .then((res) => {
        imageThumbnails.value.length = 0; // 清空现有图片
        imgConfig.images.length=0;
        res.data.forEach((item: any) => {
          imageThumbnails.value.push({
            name: item.name,
            path: item.path,
            categories: item.categories,
            url: imgConfig.get_img_url + encodeURIComponent(item.path),
          });
        });
        //message.success(`成功读取 ${res.data.length} 张图片`);
      })
      .catch((error) => {
        message.error("读取图片失败：" + error.message);
      });

      imgConfig.images=imageThumbnails.value;
  } else {
    message.warning("请输入图片目录路径");
  }
};

// 根据分类获取图片
const getImagesByCategory = (categoryLabel: string) => {
  return imageThumbnails.value.filter(
    (img) => img.categories === categoryLabel
  );
};

// 处理添加图片到分类
const handleAddImage = (category: ImgCategories) => {
  axios
    .post(imgConfig.set_img_category_url, {
      path: imgConfig.temp_img_dir,
      category: category.label,
    })
    .then(() => handleReadImages())
    .catch((erro) => {
      message.error("服务器错误：" + erro.message);
    });

  //message.info(`向 ${category.label} 添加图片`);
};

// 清空分类中的图片
const handleClearCategory = (category: ImgCategories) => {
  imageThumbnails.value.forEach((img) => {
    if (img.categories === category.label) {
      img.categories = "";
    }
  });
  axios.post(imgConfig.clear_category_url,{'path':imgConfig.temp_img_dir+'\\'+category.label})
  .then(() =>{handleReadImages();message.success(`已清空 ${category.label} 分类`);})
  .catch((erro) => {
      message.error("服务器错误：" + erro.message);
    });
  
};

// 从分类中移除单张图片
const handleRemoveImage = (img: ImgItem) => {
  axios.post(imgConfig.del_img_category_url,{'file_list':[img.path]})
    .then(() =>{handleReadImages();})
  .catch((erro) => {
      message.error("服务器错误：" + erro.message);
    });
};

const changeTab_emit=defineEmits<{(e:'tab-change',key:string):void}>();
const handleNext = () => {
  handleReadImages();
  changeTab_emit('tab-change','3');
};
</script>

<style lang="less" scoped>
// 精简后的配色方案
@primary-color: #3ebdf8;
@secondary-color: #95b7fa;
@accent-color: #ffd2af;
@text-color: #314659;
@border-color: #d9d9d9;
@shadow-color: rgba(0, 0, 0, 0.1);
@transition-duration:0.3s;

.business-material-container {
  min-height: 100vh;
  padding: 20px;
  background: #f5f5f5;
}

.main-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px @shadow-color;
}

.section {
  margin-bottom: 20px;
}

.glow-card {
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 8px @shadow-color;
  max-height: 500px;
  overflow-y: auto;

  :deep(.ant-card-head) {
    border-bottom: 1px solid @border-color;
    padding: 16px 24px;

    .ant-card-head-title {
      font-weight: 600;
      color: @text-color;
    }
  }

  :deep(.ant-card-body) {
    padding: 20px;
  }
}

.combined-info-content {
  .info-row {
    align-items: stretch;
  }

  .info-item {
    height: 100%;

    .info-label {
      display: block;
      margin-bottom: 12px;
      font-weight: 600;
      color: @text-color;
    }
  }

  .business-select {
    width: 100%;

    :deep(.ant-select-selector) {
      border-radius: 6px;
    }
  }
}

.material-checkbox-content {
  .material-checkbox-group {
    width: 100%;
  }

  .material-checkbox {
    margin: 4px 0;

    :deep(.ant-checkbox-wrapper) {
      align-items: center;
      padding: 8px 12px;
      border: 1px solid @border-color;
      border-radius: 6px;
      background: #fff;
      width: 100%;
      margin: 0;
    }

    .material-label {
      color: @text-color;
    }
  }
}

.image-management-section {
  .image-directory-content {
    .input-group {
      display: flex;
      gap: 12px;
      margin-bottom: 16px;

      .directory-input {
        flex: 1;
      }

      .read-image-btn {
        border-radius: 6px;
        white-space: nowrap;
        min-width: 120px;
      }
    }

    // 缩略图网格容器
    .thumbnail-grid {
      display: grid;
      grid-template-columns: repeat(
        auto-fill,
        minmax(100px, 1fr)
      ); /* 增加最小宽度 */
      gap: 16px; /* 增加间距 */
      max-height: 400px; /* 增加最大高度 */
      overflow-y: auto;
      padding: 12px;
      border: 1px solid #f0f0f0;
      border-radius: 8px;
      background: rgba(149, 183, 250, 0.02);

      .thumbnail-item {
        cursor: grab;
        transition: all 0.3s ease;
        aspect-ratio: 1; /* 保持正方形比例 */

        &:hover {
          transform: scale(1.05);

          .thumbnail-wrapper {
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
          }
        }

        .thumbnail-wrapper {
          position: relative;
          border-radius: 6px;
          overflow: hidden;
          box-shadow: 0 2px 8px @shadow-color;
          transition: all 0.3s ease;
          width: 100%;
          height: 100%;

          .thumbnail-image {
            width: 100%;
            height: 100%;

            display: block;
          }

          .thumbnail-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
            padding: 6px;
            color: white;

            .image-name {
              font-size: 0.75rem; /* 稍微增大字体 */
              display: block;
              white-space: nowrap;
              overflow: hidden;
              text-overflow: ellipsis;
            }
          }
        }
      }
    }
  }
}

// 材料分类区域样式优化
// 材料分类区域网格布局优化
.classification-content {
  .classification-areas {
    // 启用 Flex 布局并设置换行，确保分类项均匀分布
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
  }

  .category-card {
    border: 1px solid #d9d9d9;
    border-radius: 8px;
    padding: 16px;
    background: #fff;
    // 使用 Flex 列布局确保内容均匀填充高度
    display: flex;
    flex-direction: column;
    height: 100%;
    transition: all 0.3s ease;

    &:hover {
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .category-header {
      display: grid;
      grid-template-columns: 1fr auto; // 标题居左，按钮居右
      align-items: center;
      margin-bottom: 12px;
      gap: 8px;

      .category-title {
        margin: 0;
        font-size: 14px;
        font-weight: bold;
        .text-ellipsis(); // 文本溢出显示省略号
      }

      .category-actions {
        display: flex;
        gap: 4px;
      }
    }

    .category-images {
      // 网格布局：自动调整列数，最小列宽 100px
      display: grid;
      grid-template-columns: repeat(
        auto-fill,
        minmax(100px, 1fr)
      ); /* 增加最小宽度 */
      gap: 16px; /* 增加间距 */
      max-height: 150px; /* 增加最大高度 */
      overflow-y: auto;
      padding: 12px;
      border: 1px solid #f0f0f0;
      border-radius: 8px;
      background: rgba(149, 183, 250, 0.02);
      overflow-y: auto;
      //flex-grow: 1;  // 填充剩余空间

      // 材料分类图片缩略图区样式
      .category-images {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        gap: 16px;
        padding: 12px;
        min-height: 200px;
        border-radius: 8px;
        background: rgba(149, 183, 250, 0.02);
        transition: all 0.3s ease;

        // 悬停效果增强
        &:hover {
          background: rgba(149, 183, 250, 0.05);
        }

        .category-image-item {
          animation: slideInUp 0.5s ease var(--animation-delay) both;
          .image-card {
            position: relative;
            border-radius: 8px;
            overflow: hidden;
            background: #fff;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid #f0f0f0;

            // 悬浮效果
            &:hover {
              transform: translateY(-4px);
              box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
              border-color: @primary-color;

              .image-overlay {
                opacity: 1;
                transform: translateY(0);
              }

              .thumbnail-image {
                transform: scale(1.05);
              }
            }

            .image-container {
              position: relative;
              aspect-ratio: 1; // 保持正方形比例
              overflow: hidden;

              .thumbnail-image {
                width: 100%;
                height: 100%;
                object-fit: cover;
                transition: transform 0.3s ease;
              }

              .image-loader {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                color: #8c8c8c;
                font-size: 12px;

                span {
                  display: block;
                  margin-top: 4px;
                }
              }

              .image-overlay {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(
                  to bottom,
                  rgba(0, 0, 0, 0.3) 0%,
                  transparent 30%,
                  transparent 70%,
                  rgba(0, 0, 0, 0.3) 100%
                );
                opacity: 0;
                transform: translateY(10px);
                transition: all 0.3s ease;
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                padding: 8px;

                .action-buttons {
                  display: flex;
                  gap: 4px;

                  .delete-btn{
                    position: absolute;
                    top: 4px;
                    right: 4px;
                    width: 24px;
                    height: 24px;
                    border: none;
                    border-radius: 50%;
                    background-color: rgba(0, 0, 0, 0.6);
                    color: white;
                    font-size: 16px;
                    cursor: pointer;
                    opacity: 0;
                    transform: scale(0.8);
                    transition: all @transition-duration ease;
                    
                    // 悬浮时按钮显示效果
                    &.show-btn {
                      opacity: 1;
                      transform: scale(1);
                    }
                    
                    // 按钮悬浮效果
                    &:hover {
                      background-color: rgba(255, 0, 0, 0.8);
                      transform: scale(1.1);
                    }
                  }
                  .preview-btn {
                    backdrop-filter: blur(8px);
                    background: rgba(255, 255, 255, 0.9);
                    border: none;
                    border-radius: 6px;

                    &:hover {
                      transform: scale(1.1);
                    }
                  }
                }
              }

              .selection-indicator {
                position: absolute;
                top: 8px;
                right: 8px;
                //color: @success-color;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 50%;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;

                .selected-icon {
                  font-size: 14px;
                }
              }
            }

            .image-info {
              padding: 8px;
              background: #fff;

              .image-name {
                display: block;
                font-size: 12px;
                font-weight: 500;
                color: @text-color;
                .text-ellipsis();
                margin-bottom: 2px;
              }

              .image-size {
                font-size: 10px;
                color: #8c8c8c;
              }
            }
          }
        }

        .empty-category {
          grid-column: 1 / -1;
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: 200px;
          border: 2px dashed #d9d9d9;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.3s ease;

          &:hover {
            border-color: @primary-color;
            background: rgba(62, 189, 248, 0.05);

            .empty-content {
              transform: scale(1.05);
            }
          }

          .empty-content {
            text-align: center;
            transition: transform 0.3s ease;

            .empty-icon {
              font-size: 48px;
              color: #d9d9d9;
              margin-bottom: 12px;
              transition: color 0.3s ease;
            }

            .empty-text {
              color: #8c8c8c;
              margin-bottom: 4px;
              font-weight: 500;
            }

            .empty-hint {
              color: #bfbfbf;
              font-size: 12px;
            }
          }
        }
      }

      // 动画定义
      @keyframes slideInUp {
        from {
          opacity: 0;
          transform: translateY(20px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      // 响应式调整
      @media (max-width: 768px) {
        .category-images {
          grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
          gap: 12px;

          .category-image-item .image-card {
            .image-info {
              padding: 6px;

              .image-name {
                font-size: 11px;
              }
            }
          }
        }
      }

      @media (min-width: 1200px) {
        .category-images {
          grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        }
      }

      .empty-category {
        grid-column: 1 / -1;
        text-align: center;
        color: #bfbfbf;
        padding: 20px;
      }
    }
  }
}

.archive-section {
  .archive-content {
    text-align: center;
    padding: 20px 0;

    .archive-btn {
      border-radius: 6px;
      padding: 0 40px;
      height: 40px;
    }

    .archive-tips {
      margin-top: 8px;
      color: #8c8c8c;
      font-size: 12px;
    }
  }
}

.empty-thumbnail {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  color: #8c8c8c;

  .empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
    color: #d9d9d9;
  }
}
// 关键帧动画定义
@keyframes gentlePulse {
  0%,
  100% {
    opacity: 0.6;
    transform: scale(0.98);
  }
  50% {
    opacity: 1;
    transform: scale(1.02);
  }
}
// 文本溢出处理混入
.text-ellipsis() {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
// 响应式设计
@media (max-width: 768px) {
  .classification-content .category-card .category-images {
    grid-template-columns: repeat(
      auto-fill,
      minmax(80px, 1fr)
    ); // 移动端缩小缩略图
  }

  .business-material-container {
    padding: 12px;
  }

  .classification-areas {
    .ant-col {
      margin-bottom: 16px;
    }
  }

  .image-directory-content {
    .input-group {
      flex-direction: column;

      .directory-input {
        width: 100%;
      }

      .read-image-btn {
        width: 100%;
      }
    }
  }
}

// 大屏幕优化
@media (min-width: 1200px) {
  .classification-content {
    .category-card {
      .category-images {
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
      }

      .category-image-item {
        .image-wrapper {
          height: 120px;
        }
      }
    }
  }
}
</style>
