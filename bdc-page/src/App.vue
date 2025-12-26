<script setup lang="ts">
import InformationOCR from './components/InformationOCR.vue'

import Config from './components/Config.vue';
import ImageProcessing from './components/ImageProcessing.vue';
import PushTask from './components/PushTask.vue';
import { ref } from 'vue';
const active_tabs_index=ref('2');

function changeTab(tabs:string)
{
  active_tabs_index.value=tabs;
}
</script>

<template>
  <a-tabs default-active-key="2" v-model:activeKey="active_tabs_index" animation>
    <a-tab-pane key="1"  title="配置信息">
      <Config></Config>
    </a-tab-pane>
    <a-tab-pane key="2" title="影像处理">
      <ImageProcessing @tab-change="changeTab"></ImageProcessing>
    </a-tab-pane>
    <a-tab-pane key="3" title="整理信息">
      <keep-alive>
      <InformationOCR @tab-change="changeTab"></InformationOCR></keep-alive>
    </a-tab-pane>
    <a-tab-pane key="4" title="提交任务">
      <PushTask @tab-change="changeTab"> </PushTask>
    </a-tab-pane>
  </a-tabs>
</template>

<style scoped>

</style>
