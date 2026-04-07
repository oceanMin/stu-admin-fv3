<template>
  <div>
    <h1 style="text-align: center;margin-bottom: 50; font-size: 28px;">学生信息管理页面（增删查改）</h1>
    <!-- 🔥 统计图表区域 -->
    <div style="width: 90%;margin: 0 auto; display: flex; gap: 20px; margin: 20px auto;">
      <div ref="chartCollegeRef"
        style="flex: 1; height: 320px; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px #00000005;">
      </div>
      <div ref="chartClazzRef"
        style="flex: 1; height: 320px; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px #00000005;">
      </div>
    </div>
    <!-- 搜索框 + 导入导出按钮 -->
    <div style="width: 90%;margin: 30px auto;">
      <ProTable :columns="columns" :table-data="tableData" :loading="loading" @refresh="handleSearch"
        @selection-change="handleSelectionChange">
        <template #toolbar-left>
          <div style="display: flex; align-items: center; gap: 10px;">
            <el-input v-model="searchValue" placeholder="请输入学号/姓名" style="width: 300px;" />
            <el-button type="primary" @click="handleSearch" :icon="Search">搜索</el-button>
            <el-button type="default" @click="handleReset" :icon="Refresh">重置</el-button>
            <el-button type="success" @click="handleAdd" :icon="Plus">新增</el-button>
            <!-- Excel 导出按钮 -->
            <el-button type="primary" :icon="Download" @click="handleExport">导出 Excel</el-button>
            <el-button type="danger" :icon="Delete" @click="handleBatchDelete" :disabled="selectedIds.length === 0">
              批量删除
            </el-button>
            <!-- Excel 导入按钮 -->
            <el-upload class="upload-btn" action="#" :auto-upload="false" :on-change="handleFileChange"
              :show-file-list="false" accept=".xlsx,.xls">
              <el-button type="warning" :icon="Upload">导入 Excel</el-button>
            </el-upload>
          </div>
        </template>
        <!-- 自定义操作列 -->
        <template #action="{ row }">
          <el-button size="small" type="primary" @click="handleView(row)">查看</el-button>
          <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </ProTable>
      <div style="display: flex;justify-content: end; margin-top: 20px;">
        <el-pagination background layout="total,prev, pager, next" @current-change="handleCurrentChange"
          @size-change="handleSizeChange" :current-page="pagination.currentPage" :page-size="pagination.pageSize"
          :total="pagination.total"></el-pagination>
      </div>
    </div>
    <FormDialog v-model:visible="showDialog" :title="dialogTitle" :fields="formFields" :initial-data="formData"
      :rules="customRules" @submit="handleSubmit" />
  </div>
</template>

<script lang="ts" setup>
import { nextTick, onMounted, ref } from 'vue'
import {
  getStudentInfo, addStudentInfo, updateStudentInfo,
  deleteStudentInfo, exportStudents, importStudents, batchDeleteStudents,
  getStatsByCollege,
  getStatsByClazz
} from '@/api/student'
import ProTable from '@/components/ProTable.vue'
import FormDialog from '@/components/FormDialog.vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Download, Upload, Delete, Search, Refresh, Plus } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

type StudentQueryParams = {
  page: number,
  size: number,
  search: string
}

const columns = [
  {
    type: "selection",
    width: 60,
    align: "center"
  },
  { type: 'index', width: 60, align: 'center' },
  { label: 'ID', prop: 'id' },
  { label: '学号', prop: 'no', width: 120 },
  { label: '姓名', prop: 'name' },
  { label: '班级', prop: 'clazz' },
  { label: '专业', prop: 'major' },
  { label: '学院', prop: 'college' },
  { label: '手机号', prop: 'phone' },
  { label: '邮箱', prop: 'email', width: 160 },
  { label: '地址', prop: 'address' },
  { label: '操作', slot: 'action', width: 200, align: 'center' },
]

const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  pageSizes: [10, 20, 50, 100],
  total: 0
})
const searchValue = ref('')
const dialogTitle = ref('新增')
const tableData = ref<any[]>([])
const loading = ref(false)
const showDialog = ref(false)
const formData = ref<any>({})
// 存储选中的导入文件
const selectedFile = ref<File | null>(null)

const customRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

const formFields = [
  { label: '学号', prop: 'no', required: true },
  { label: '姓名', prop: 'name', required: true },
  { label: '班级', prop: 'clazz' },
  { label: '专业', prop: 'major' },
  { label: '学院', prop: 'college' },
  { label: '手机号', prop: 'phone' },
  { label: '邮箱', prop: 'email', required: true },
  { label: '地址', prop: 'address' },
]
// 多选事件
const selectedIds = ref<number[]>([])

// 图表
const chartCollegeRef = ref(null)
const chartClazzRef = ref(null)
let collegeChart: any = null
let clazzChart: any = null

// ==================== 统计图表 ====================
async function loadCharts() {
  await nextTick()
  collegeChart = echarts.init(chartCollegeRef.value)
  clazzChart = echarts.init(chartClazzRef.value)

  // 学院统计
  const resCollege = await getStatsByCollege()
  const collegeData = resCollege.data.map((item: any) => ({
    name: item.college || '未知学院',
    value: item.count
  }))

  collegeChart.setOption({
    title: { text: '各学院人数统计', left: 'center' },
    tooltip: { trigger: 'item' },
    series: [{
      name: '人数',
      type: 'pie',
      radius: ['40%', '70%'],
      data: collegeData
    }]
  })

  // 班级统计
  const resClazz = await getStatsByClazz()
  const clazzData = resClazz.data.map((item: any) => ({
    name: item.clazz || '未知班级',
    value: item.count
  }))

  clazzChart.setOption({
    title: { text: '各班级人数统计', left: 'center' },
    tooltip: { trigger: 'item' },
    series: [{
      name: '人数',
      type: 'pie',
      radius: ['40%', '70%'],
      data: clazzData
    }]
  })
}


const handleSelectionChange = (val: any[]) => {
  selectedIds.value = val.map(item => item.id)
}
// 搜索
const handleSearch = () => {
  fetchStudents({
    page: pagination.value.currentPage,
    size: pagination.value.pageSize,
    search: searchValue.value
  })
}

// 重置
const handleReset = () => {
  searchValue.value = ''
  fetchStudents()
}

// 切换页码
const handleCurrentChange = (val: number) => {
  pagination.value.currentPage = val
  fetchStudents({
    page: val,
    size: pagination.value.pageSize,
    search: searchValue.value
  })
}
// 改变每页显示数量
const handleSizeChange = (val: number) => {
  pagination.value.pageSize = val
  fetchStudents({
    page: pagination.value.currentPage,
    size: val,
    search: searchValue.value
  })
}

// 提交表单
const handleSubmit = async (data: any) => {
  try {
    const res = dialogTitle.value === '新增' ? await addStudentInfo(data) : await updateStudentInfo(data)
    if (res?.code === 200) {
      showDialog.value = false
      fetchStudents()
      ElMessage.success(dialogTitle.value === '新增' ? '添加成功!' : '修改成功!');
    } else {
      ElMessage.error(res.message);
      return false
    }
  } catch (error) {
    ElMessage.error('提交表单失败!');
    console.error('提交表单失败:', error);
  }
}

// 新增学生信息
const handleAdd = () => {
  dialogTitle.value = '新增'
  showDialog.value = true
  console.log('add')
}

// 获取学生信息
const handleView = (row: any) => {
  dialogTitle.value = '查看'
  showDialog.value = true
  formData.value = row
}

// 编辑学生信息
const handleEdit = (row: any) => {
  dialogTitle.value = '编辑'
  showDialog.value = true
  formData.value = row
}

// 删除学生信息
const handleDelete = async (row: any) => {
  ElMessageBox.confirm('此操作将永久删除该学生信息, 是否继续?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 确定删除
    deleteStudentInfo(row.id).then(() => {
      ElMessage({
        type: 'success',
        message: '删除成功!'
      })
      fetchStudents()
    })
  }).catch((e) => {
    console.log(e)
  })
}
// 🔥 批量删除
const handleBatchDelete = async () => {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请选择要删除的学生')
    return
  }

  ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 条数据吗？`, '批量删除', {
    type: 'warning',
    confirmButtonText: '确定删除',
    cancelButtonText: '取消'
  }).then(async () => {
    const res: any = await batchDeleteStudents({ ids: selectedIds.value })
    if (res.code === 200) {
      ElMessage.success('批量删除成功！')
      selectedIds.value = []
      fetchStudents()
    }
  }).catch(() => { })
}
// 获取学生列表
const fetchStudents = async (query?: StudentQueryParams) => {
  loading.value = true;
  try {
    const data = query ? await getStudentInfo(query) : await getStudentInfo();
    if (data && data.code === 200) {
      tableData.value = data.data || []; // 兜底空数组
      // 分页数据兜底
      pagination.value = {
        ...pagination.value,
        total: data.pages?.total || 0,
        currentPage: data.pages?.current || 1,
        pageSize: data.pages?.size || 10,
        pageSizes: data.pages?.pages || 0
      };
      loadCharts() // 🔥 删除后刷新图表
    } else {
      ElMessage.error(data?.message || "获取学生列表失败");
      tableData.value = []; // 失败时清空列表
    }
  } catch (error) {
    // 捕获请求异常（如网络错误、401/500等）
    console.error('获取学生列表失败:', error);
    ElMessage.error("网络异常或接口未响应，请检查后端服务");
    tableData.value = []; // 异常时清空列表
    loadCharts() // 🔥 删除后刷新图表
  } finally {
    loading.value = false;
  }
};

// Excel 导出功能
const handleExport = async () => {
  try {
    ElMessageBox.confirm('确定要导出当前筛选的学生数据吗？', '导出提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    }).then(async () => {
      loading.value = true

      // 🔥 关键：把当前搜索值一起传给后端
      const res: any = await exportStudents({
        search: searchValue.value
      })

      const blob = new Blob([res], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `学生信息表_${new Date().getTime()}.xlsx`
      a.click()
      window.URL.revokeObjectURL(url)
      ElMessage.success('导出成功！')
      loading.value = false
    })
  } catch (error) {
    loading.value = false
    ElMessage.error('导出失败')
  }
}

// 选择 Excel 文件
const handleFileChange = (file: any) => {
  selectedFile.value = file.raw
  // 选择文件后触发导入确认
  handleImport()
}

// Excel 导入功能
const handleImport = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请选择要导入的 Excel 文件（仅支持 .xlsx/.xls 格式）')
    return
  }

  try {
    ElMessageBox.confirm('确定要导入该 Excel 文件吗？导入后会批量新增学生数据', '导入提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      loading.value = true
      const res: any = await importStudents(selectedFile.value!)
      if (res.code === 200) {
        ElMessage.success(res.message || 'Excel 导入成功！')
        // 导入成功后刷新列表
        fetchStudents()
      } else {
        ElMessage.error(res.message || 'Excel 导入失败！')
      }
      loading.value = false
    })
  } catch (error) {
    loading.value = false
    console.error('Excel 导入失败:', error)
    ElMessage.error('Excel 导入失败，请检查文件格式！')
  }
}

onMounted(() => {
  fetchStudents()
})
</script>

<style scoped>
/* 导入按钮样式适配 */
.upload-btn {
  display: inline-block;
}
</style>