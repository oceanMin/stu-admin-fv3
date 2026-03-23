<template>
  <div>
    <h1 style="text-align: center;margin-bottom: 50; font-size: 18px;">学生信息管理页面（增删查改）</h1>
    <!-- 搜索框 -->
    <div style="width: 70%;margin: 30px auto;">
      <div style="margin-bottom: 20px;">
        <el-input v-model="searchValue" placeholder="请输入内容" style="width: 300px; margin-right: 20px;" />
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button type="default" @click="handleReset">重置</el-button>
        <el-button type="primary" @click="handleAdd">新增</el-button>
      </div>
      <el-table :data="tableData" style="width: 100%" stripe  v-loading="loading">
        <template v-for="item in columns" :key="item.prop">
          <!-- 选择列 -->
          <el-table-column v-if="item.type === 'selection'" type="selection" width="55" />
          <el-table-column v-else-if="item.type === 'index'" type="index" :width="item.width || '80'"
            :label="item.label || '序号'" />
          <el-table-column v-else :prop="item.prop" :label="item.label" :width="item.width" :min-width="item.minWidth"
            :align="item.align || 'center'">
            <!-- 自定义列内容 -->
            <template #default="scope" v-if="item.slot">
              <el-button size="small" type="primary" @click="updateStudents(scope.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </template>
      </el-table>
      <div style="display: flex;justify-content: end; margin-top: 20px;">
        <el-pagination
          background
          layout="prev, pager, next"
          @current-change="pager.page = $event"
          @size-change="pager.size = $event"
          :current-page="pager.page"
          :page-size="pager.size"
          :total="pager.total"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { getStudentInfo } from '@/api/student'

const columns = [
  { type: 'index', width: 60, align: 'center' },
  { label: 'ID', prop: 'id'},
  { label: '学号', prop: 'no' ,width:120},
  { label: '姓名', prop: 'name' },
  { label: '班级', prop: 'clazz' },
  { label: '专业', prop: 'major' },
  { label: '学院', prop: 'college' },
  { label: '手机号', prop: 'phone' },
  { label: '邮箱', prop: 'email', width: 160 },
  { label: '地址', prop: 'address' },
  { label: '操作', slot: 'action', width: 200, align: 'center' },
]

const pager = ref({
  page: 1,
  size: 10,
  total: 0
})
const searchValue = ref('')
const tableData = ref<any[]>([])
const loading = ref(false)

// 搜索
const handleSearch = () => {
  console.log('search', searchValue.value)
}

// 重置
const handleReset = () => {
  searchValue.value = ''
}

// 新增学生信息
const handleAdd = () => {
  console.log('add')
}

// 编辑学生信息
const updateStudents = (row: any) => {
  console.log('click', row)
}

// 删除学生信息
const handleDelete = (row: any) => {
  console.log('delete', row)
}

// 获取学生列表
const fetchStudents = async () => {
  loading.value = true;
  try {
    // 使用配置好的 request 实例
    const data = await getStudentInfo();
    tableData.value = data;
    console.log('获取到学生数据:', data);
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
