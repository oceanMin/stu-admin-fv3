<template>
  <div class="toolbar">
    <!-- 🔥 关键：用 :value 绑定 prop，@input 触发 update:searchValue 事件 -->
    <el-input
      :value="searchValue"
      placeholder="学号/姓名"
      style="width: 280px;height: 34px;"
      @input="(val) => $emit('update:searchValue', val)"
    />
    <el-button type="primary" @click="$emit('search')">搜索</el-button>
    <el-button @click="$emit('reset')">重置</el-button>
    <el-button type="success" @click="$emit('add')">新增</el-button>
    <el-button type="danger" :disabled="selectedDisabled" @click="$emit('batch-delete')">批量删除</el-button>
    <el-button type="primary" @click="$emit('export')">导出 Excel</el-button>

    <el-upload :auto-upload="false" @change="(f) => $emit('import', f)">
      <el-button type="warning">导入 Excel</el-button>
    </el-upload>

    <el-button @click="$emit('download-template')">导入模板</el-button>
  </div>
</template>

<script setup>
defineProps({
  searchValue: String,
  selectedDisabled: Boolean
})
defineEmits(['update:searchValue', 'search', 'reset', 'add', 'batch-delete', 'export', 'import', 'download-template'])
</script>

<style scoped>
.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}
</style>