<template>
  <div class="statistics-card">
    <div class="stat-row">
      <el-card flex="1"><div>总学生：{{ total }}</div></el-card>
      <el-card flex="1"><div>班级数：{{ clazzCount }}</div></el-card>
      <el-card flex="1"><div>专业数：{{ majorCount }}</div></el-card>
      <el-card flex="1"><div>学院数：{{ collegeCount }}</div></el-card>
    </div>

    <div class="chart-row">
      <div ref="chartCollege" class="chart-box"></div>
      <div ref="chartClazz" class="chart-box"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import { getStatsByCollege, getStatsByClazz } from '@/api/student'

const props = defineProps(['total', 'collegeCount', 'clazzCount', 'majorCount'])
const chartCollege = ref(null)
const chartClazz = ref(null)

const loadCharts = async () => {
  const collegeChart = echarts.init(chartCollege.value)
  const clazzChart = echarts.init(chartClazz.value)

  const resCollege = await getStatsByCollege()
  collegeChart.setOption({
    title: { text: '学院人数统计' },
    series: [{ type: 'pie', data: resCollege.data.map(i => ({ name: i.college, value: i.count })) }]
  })

  const resClazz = await getStatsByClazz()
  clazzChart.setOption({
    title: { text: '班级人数统计' },
    series: [{ type: 'pie', data: resClazz.data.map(i => ({ name: i.clazz, value: i.count })) }]
  })
}

onMounted(() => loadCharts())
watch(() => props.total, () => loadCharts())
</script>

<style scoped>
.statistics-card { background:#fff; border-radius:12px; padding:20px; margin-bottom:20px; }
.stat-row { display:flex; gap:20px; margin-bottom:20px; }
.chart-row { display:flex; gap:20px; }
.chart-box { flex:1; height:320px; }
</style>