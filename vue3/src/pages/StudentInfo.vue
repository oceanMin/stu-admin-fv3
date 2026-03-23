<template>
  <div>
    <h1 style="text-align: center;margin-bottom: 50; font-size: 28px;">学生信息管理页面（增删查改）</h1>
    <!-- 搜索框 -->
    <div style="width: 70%;margin: 30px auto;">
      <ProTable :columns="columns" :table-data="tableData" :loading="loading" @refresh="handleSearch">
        <template #toolbar-left>
          <div style="margin-bottom: 20px;">
            <el-input v-model="searchValue" placeholder="请输入学号/姓名" style="width: 300px; margin-right: 20px;" />
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button type="default" @click="handleReset">重置</el-button>
            <el-button type="success" @click="handleAdd">新增</el-button>
          </div>
        </template>
        <!-- 自定义操作列 -->
        <template #action="{ row }">
          <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </ProTable>
      <div style="display: flex;justify-content: end; margin-top: 20px;">
        <el-pagination background layout="prev, pager, next" @current-change="handleCurrentChange"
          @size-change="handleSizeChange" :current-page="pagination.currentPage" :page-size="pagination.pageSize"
          :total="pagination.total"></el-pagination>
      </div>
    </div>
    <FormDialog v-model:visible="showDialog" :title="dialogTitle" :fields="formFields" :initial-data="formData"
      :rules="customRules" @submit="handleSubmit" />
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { getStudentInfo, addStudentInfo, updateStudentInfo, deleteStudentInfo } from '@/api/student'
import ProTable from '@/components/ProTable.vue'
import FormDialog from '@/components/FormDialog.vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const columns = [
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
  pageSize: 100,
  pageSizes: [10, 20, 50, 100],
  total: 0
})
const searchValue = ref('')
const dialogTitle = ref('新增')
const tableData = ref<any[]>([])
const loading = ref(false)
const showDialog = ref(false)
const formData = ref<any>({})
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
  console.log('current change', val)
  fetchStudents({
    page: val,
    size: pagination.value.pageSize,
    search: searchValue.value
  })
}
// 改变每页显示数量
const handleSizeChange = (val: number) => {
  console.log('size change', val)
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

// 获取学生列表
const fetchStudents = async (query?: any) => {
  loading.value = true;
  try {
    // 使用配置好的 request 实例
    const data = !!query ? await getStudentInfo(query) : await getStudentInfo();
    tableData.value = data.data;
  } catch (error) {
    console.error('获取学生列表失败:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchStudents()
})
</script>
