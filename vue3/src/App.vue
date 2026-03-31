<template>
  <div id="app">
    <!-- 顶部导航栏：仅在非登录/注册页且已登录时显示 -->
    <el-header v-if="showHeader" class="header-container">
      <div class="header-left">
        <h1>学生信息管理系统</h1>
      </div>
      <div class="header-right">
        <span class="welcome-text">欢迎：{{ username }}</span>
        <el-button type="danger" text @click="handleLogout">
          退出登录
        </el-button>
      </div>
    </el-header>

    <!-- 主内容区 -->
    <el-main class="main-container">
      <router-view />
    </el-main>
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { ElMessage } from 'element-plus';

// 1. 正确获取路由实例（在setup顶层获取，保证注入完成）
const router = useRouter();
const route = useRoute();

// 2. 正确获取Pinia store（setup顶层获取，避免时机问题）
const userStore = useUserStore();
  const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');

// 3. 计算属性：是否显示顶部导航栏（排除登录/注册页，且已登录）
const showHeader = computed(() => {
  const excludePaths = ['/login', '/register'];
  return !excludePaths.includes(route.path) && !!userInfo.token;
});

// 4. 用户名计算属性
const username = computed(() => {
  return userInfo?.username || '';
});

// 5. 退出登录逻辑
const handleLogout = () => {
  userStore.logout(); // 清空token和用户名
  ElMessage.success('退出登录成功');
  router.push('/login'); // 跳回登录页
};

// 6. 监听路由变化（正确使用router.afterEach，而非route.afterEach）
// 方案一：使用watch监听route.path，替代afterEach（更简单、无报错）
watch(
  () => route.path,
  (newPath) => {
    console.log('路由变化:', newPath);
    // 可在这里添加路由变化后的逻辑，如页面埋点、权限校验等
  }
);


</script>

<style>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

/* 顶部导航栏样式 */
.header-container {
  background-color: #1989fa;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-left h1 {
  font-size: 18px;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.welcome-text {
  font-size: 14px;
}

/* 主内容区样式 */
.main-container {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: calc(100% - 60px);
}

/* Element Plus 全局样式适配 */
:root {
  --el-color-primary: #1989fa;
}

.el-header, .el-main {
  padding: 0;
}
</style>