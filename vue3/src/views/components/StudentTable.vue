<template>
  <div class="table-wrapper">
    <StudentToolbar
      :search-value="searchValue"
      :selected-disabled="!selectedIds.length"
      @update:search-value="(val) => searchValue = val"
      @search="$emit('search')"
      @reset="$emit('reset')"
      @add="$emit('add')"
      @batch-delete="$emit('batch-delete')"
      @export="$emit('export')"
      @import="$emit('import', $event)"
      @download-template="$emit('download-template')"
    />

    <el-table
      :data="tableData"
      :loading="loading"
      @selection-change="(val) => $emit('update:selectedIds', val.map(v => v.id))"
      border
    >
      <el-table-column type="selection" width="60" />
      <el-table-column label="ID" prop="id" width="70" />
      <el-table-column label="学号" prop="no" width="130" />
      <el-table-column label="姓名" prop="name" />
      <el-table-column label="班级" prop="clazz" />
      <el-table-column label="专业" prop="major" />
      <el-table-column label="学院" prop="college" />
      <el-table-column label="操作" width="220">
        <template #default="{ row }">
          <el-button size="small" type="primary" @click="$emit('view', row)">查看</el-button>
          <el-button size="small" type="primary" @click="$emit('edit', row)">编辑</el-button>
          <el-button size="small" type="danger" @click="$emit('delete', row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-box">
      <el-pagination
        background
        layout="total, prev, pager, next"
        :current-page="pagination.currentPage"
        :page-size="pagination.pageSize"
        :total="pagination.total"
        @current-change="p => $emit('page-change', p, pagination.pageSize)"
        @size-change="s => $emit('page-change', pagination.currentPage, s)"
      />
    </div>
  </div>
</template>

<script setup>
import StudentToolbar from './StudentToolbar.vue'
defineProps({
  searchValue: String,
  tableData: Array,
  loading: Boolean,
  pagination: Object,
  selectedIds: Array
})
defineEmits([
  'update:selectedIds',
  'search', 'reset', 'add', 'batch-delete',
  'export', 'import', 'download-template',
  'view', 'edit', 'delete', 'page-change'
])
</script>

<style scoped>
.table-wrapper {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
}
.pagination-box {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>