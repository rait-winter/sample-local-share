<!--
SettingsDialog.vue
统一设置弹窗组件，集中管理消息/文件/视频最大保留数量。
props: modelValue 控制弹窗显示
emit: update:modelValue 控制父组件弹窗开关，saved 通知设置已保存
主要逻辑：表单校验、API交互、保存后自动刷新
-->

<template>
  <el-dialog v-model="visible" title="系统设置" width="400px" @close="onClose">
    <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
      <el-form-item label="消息最大条数" prop="maxMessages">
        <el-input v-model.number="form.maxMessages" type="number" :min="1" :max="100" />
      </el-form-item>
      <el-form-item label="文件最大数量" prop="maxFiles">
        <el-input v-model.number="form.maxFiles" type="number" :min="1" :max="100" />
      </el-form-item>
      <el-form-item label="视频最大数量" prop="maxVideos">
        <el-input v-model.number="form.maxVideos" type="number" :min="1" :max="100" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="onClose">取消</el-button>
      <el-button type="primary" :loading="loading" @click="onSave">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, watch, defineEmits, defineProps } from 'vue';
import { ElMessage } from 'element-plus';

const props = defineProps<{ modelValue: boolean }>();
const emit = defineEmits(['update:modelValue', 'saved']);

const visible = ref(props.modelValue);
watch(() => props.modelValue, v => visible.value = v);
watch(visible, v => emit('update:modelValue', v));

const formRef = ref();
const form = reactive({
  maxMessages: 20,
  maxFiles: 10,
  maxVideos: 10
});
const rules = {
  maxMessages: [
    { required: true, type: 'number', min: 1, max: 100, message: '1-100之间', trigger: 'blur' }
  ],
  maxFiles: [
    { required: true, type: 'number', min: 1, max: 100, message: '1-100之间', trigger: 'blur' }
  ],
  maxVideos: [
    { required: true, type: 'number', min: 1, max: 100, message: '1-100之间', trigger: 'blur' }
  ]
};
const loading = ref(false);

// fetchSettings: 获取当前设置，弹窗打开时自动调用
async function fetchSettings() {
  loading.value = true;
  try {
    const [msg, file, video] = await Promise.all([
      fetch('/api/message/max_count').then(r => r.json()),
      fetch('/api/file/max_count').then(r => r.json()),
      fetch('/api/video/max_count').then(r => r.json())
    ]);
    form.maxMessages = msg.max_count || 20;
    form.maxFiles = file.max_count || 10;
    form.maxVideos = video.max_count || 10;
  } catch (e) {
    ElMessage.error('获取设置失败');
  } finally {
    loading.value = false;
  }
}

watch(visible, v => { if (v) fetchSettings(); });

function onClose() {
  visible.value = false;
}

// onSave: 校验表单并依次调用后端API保存设置，成功后emit('saved')
async function onSave() {
  await formRef.value.validate();
  loading.value = true;
  try {
    await Promise.all([
      fetch('/api/message/max_count', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ max_count: form.maxMessages })
      }),
      fetch('/api/file/max_count', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ max_count: form.maxFiles })
      }),
      fetch('/api/video/max_count', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ max_count: form.maxVideos })
      })
    ]);
    ElMessage.success('设置已保存');
    visible.value = false;
    emit('saved');
  } catch (e) {
    ElMessage.error('保存失败');
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.el-dialog {
  border-radius: 10px;
}
.el-form-item {
  margin-bottom: 18px;
}
</style> 