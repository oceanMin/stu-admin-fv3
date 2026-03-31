<template>
  <div class="login-container">
    <el-card class="login-card" shadow="hover">
      <h2 class="login-title">学生信息管理系统</h2>
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="80px" class="login-form">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" prefix-icon="User" clearable />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" prefix-icon="Lock" show-password
            clearable />
        </el-form-item>

        <el-form-item class="login-btn-group">
          <el-button type="primary" @click="handleLogin" :loading="loading" class="login-btn">
            登录
          </el-button>
          <el-button link @click="goToRegister">还没有账号？去注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage, ElForm, ElFormItem } from 'element-plus';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { login } from '@/api/user';

// 路由实例
const router = useRouter();
// 用户状态管理
const userStore = useUserStore();
// 加载状态
const loading = ref(false);
// 表单引用
const loginFormRef = ref<InstanceType<typeof ElForm>>();

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
});

// 表单验证规则
const loginRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
});

// 登录处理
const handleLogin = async () => {
  // 表单验证
  if (!loginFormRef.value) return;
  try {
    const valid = await loginFormRef.value.validate();
    if (!valid) return;

    loading.value = true;
    // 调用登录接口
   const res = await login({
      username: loginForm.username,
      password: loginForm.password
    })

    console.log('登录接口返回数据:', res) 
    if (res.code === 200) {
      // 存储用户信息
      const userInfo = JSON.stringify({
        token: res.token,
        username: res.username
      });
      localStorage.setItem('userInfo', userInfo);
      console.log(11111111,res,res)
      ElMessage.success(res.message || '登录成功');
      // 跳转到学生列表页
      await router.push('/');
    } else {
      ElMessage.error(res.message || '登录失败');
    }
  } catch (error) {
    ElMessage.error('登录异常，请重试');
  } finally {
    loading.value = false;
  }
};

// 跳转到注册页面
const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
}

.login-card {
  width: 450px;
  padding: 20px;
  box-sizing: border-box;
}

.login-title {
  text-align: center;
  margin-bottom: 20px;
  color: #1989fa;
  font-weight: 600;
}

.login-form {
  margin-top: 10px;
}

.login-btn-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.login-btn {
  width: 180px;
}
</style>