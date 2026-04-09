<template>
  <div class="student-admin-container">
    <h1 class="page-title">学生信息管理页面（增删查改）</h1>

    <!-- 统计 + 图表 -->
    <StudentStatistics :total="total" :college-count="collegeCount" :clazz-count="clazzCount"
      :major-count="majorCount" />

    <!-- 表格 + 工具栏 + 分页 -->
    <StudentTable v-model:selected-ids="selectedIds" :search-value="searchValue" :table-data="tableData"
      :loading="loading" :pagination="pagination" @search="handleSearch" @reset="handleReset" @add="handleAdd"
      @batch-delete="handleBatchDelete" @export="handleExport" @import="handleImport"
      @download-template="handleDownloadTemplate" @view="handleView" @edit="handleEdit" @delete="handleDelete"
      @page-change="handlePageChange" />

    <!-- 新增/编辑/查看弹窗 -->
    <StudentDialog v-model:visible="showDialog" v-model:form-data="formData" :title="dialogTitle" :rules="customRules"
      @submit="handleSubmit" />
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import StudentStatistics from './components/StudentStatistics.vue'
import StudentTable from './components/StudentTable.vue'
import StudentDialog from './components/StudentDialog.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getStudentInfo,
  addStudentInfo,
  updateStudentInfo,
  deleteStudentInfo,
  exportStudents,
  importStudents,
  batchDeleteStudents,
  downloadStudentTemplate,
  getStatistics
} from '@/api/student'

// 选中ID
const selectedIds = ref<number[]>([])
// 搜索
const searchValue = ref('')
// 表格
const tableData = ref<any[]>([])
const loading = ref(false)
// 分页
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})
// 弹窗
const showDialog = ref(false)
const dialogTitle = ref('新增')
const formData = ref<any>({})
// 统计数字
const total = ref(0)
const collegeCount = ref(0)
const clazzCount = ref(0)
const majorCount = ref(0)
// 导入文件
const selectedFile = ref<File | null>(null)

// 校验规则
const customRules = ref({
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3456789]\d{9}$/, message: '手机号格式错误' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式错误' }
  ]
})

// ==================== 数据加载 ====================
const fetchStudents = async (query?: any) => {
  loading.value = true
  try {
    const data = await getStudentInfo(query || {
      page: pagination.value.currentPage,
      size: pagination.value.pageSize,
      search: searchValue.value
    })
    if (data.code === 200) {
      tableData.value = data.data || []
      pagination.value.total = data.pages?.total || 0
    }
  } catch (err) {
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

// ==================== 统计 ====================
const loadStatistics = async () => {
  const res = await getStatistics()
  total.value = res.data.total
  collegeCount.value = res.data.collegeCount
  clazzCount.value = res.data.clazzCount
  majorCount.value = res.data.majorCount
}

// ==================== 搜索 / 重置 ====================
const handleSearch = () => {
  fetchStudents()
}
const handleReset = () => {
  searchValue.value = ''
  fetchStudents()
}

// ==================== 分页 ====================
const handlePageChange = (page: number, size: number) => {
  pagination.value.currentPage = page
  pagination.value.pageSize = size
  fetchStudents()
}

// ==================== 弹窗 ====================
const handleAdd = () => {
  dialogTitle.value = '新增'
  formData.value = {}
  showDialog.value = true
}
const handleView = (row: any) => {
  dialogTitle.value = '查看'
  formData.value = { ...row }
  showDialog.value = true
}
const handleEdit = (row: any) => {
  dialogTitle.value = '编辑'
  formData.value = { ...row }
  showDialog.value = true
}

// ==================== 提交 ====================
const handleSubmit = async (data: any) => {
  try {
    if (dialogTitle.value === '新增') {
      await addStudentInfo(data)
    } else {
      await updateStudentInfo(data)
    }
    ElMessage.success('操作成功')
    showDialog.value = false
    fetchStudents()
  } catch (err) {
    ElMessage.error('操作失败')
  }
}

// ==================== 删除 ====================
const handleDelete = async (row: any) => {
  await ElMessageBox.confirm('确定删除？')
  await deleteStudentInfo(row.id)
  ElMessage.success('删除成功')
  fetchStudents()
}

// ==================== 批量删除 ====================
const handleBatchDelete = async () => {
  if (selectedIds.value.length === 0) return ElMessage.warning('请选择数据')
  await ElMessageBox.confirm(`确定删除 ${selectedIds.value.length} 条？`)
  await batchDeleteStudents({ ids: selectedIds.value })
  ElMessage.success('批量删除成功')
  selectedIds.value = []
  fetchStudents()
}

// ==================== 导出 ====================
const handleExport = async () => {
  await ElMessageBox.confirm('确定导出？')
  const res = await exportStudents({ search: searchValue.value })
  const blob = new Blob([res], { type: 'application/vnd.openxmlformats' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = '学生信息.xlsx'
  a.click()
  URL.revokeObjectURL(url)
  ElMessage.success('导出成功')
}

// ==================== 下载模板 ====================
const handleDownloadTemplate = async () => {
  const res = await downloadStudentTemplate()
  const blob = new Blob([res], { type: 'application/vnd.openxmlformats' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = '学生信息导入模板.xlsx'
  a.click()
  URL.revokeObjectURL(url)
  ElMessage.success('模板下载成功')
}

// ==================== 导入 ====================
const handleImport = async (file: any) => {
  selectedFile.value = file.raw
  if (!selectedFile.value) return ElMessage.warning('请选择文件')
  await ElMessageBox.confirm('确定导入？')
  const res = await importStudents(selectedFile.value)
  ElMessage.success(res.message)
  fetchStudents()
}

// ==================== 生命周期 ====================
onMounted(() => {
  fetchStudents()
  loadStatistics()
})
</script>

<style scoped>
.page-title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 28px;
}

.student-admin-container {
  padding: 20px 30px;
  background: #f5f7fa;
  min-height: 100vh;
}
</style>