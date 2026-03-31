<template>
  <div class="register-container">
    <el-card class="register-card" shadow="hover">
      <h2 class="register-title">学生信息管理系统</h2>
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="80px"
        class="register-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名（3-20位）"
            prefix-icon="User"
            clearable
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码（6-20位）"
            prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>

        <el-form-item class="register-btn-group">
          <el-button
            type="primary"
            @click="handleRegister"
            :loading="loading"
            class="register-btn"
          >
            注册
          </el-button>
          <el-button link @click="goToLogin">已有账号？去登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage, ElForm } from 'element-plus';
import { useRouter } from 'vue-router';
import { register } from '@/api/user';

const router = useRouter();
const loading = ref(false);
const registerFormRef = ref<InstanceType<typeof ElForm>>();

// 注册表单数据（保留confirmPassword仅用于前端校验）
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: ''
});

// 表单验证规则
const registerRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { 
      validator: (rule: any, value: string) => value === registerForm.password, 
      message: '两次输入的密码不一致', 
      trigger: 'blur' 
    }
  ]
});

// 注册处理（核心修复：过滤confirmPassword，只传username和password）
const handleRegister = async () => {
  if (!registerFormRef.value) return;
  try {
    const valid = await registerFormRef.value.validate();
    if (!valid) return;

    loading.value = true;
    // 关键：只传后端需要的字段，过滤掉confirmPassword
    const reqData = {
      username: registerForm.username,
      password: registerForm.password
    };
    const res = await register(reqData);
    const { data } = res;
    if (data.code === 200) {
      ElMessage.success(data.message || '注册成功，请登录');
      router.push('/login');
    } else {
      ElMessage.error(data.message || '注册失败');
    }
  } catch (error) {
    console.error('注册失败:', error);
    ElMessage.error('注册异常，请重试');
  } finally {
    loading.value = false;
  }
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
}

.register-card {
  width: 450px;
  padding: 20px;
  box-sizing: border-box;
}

.register-title {
  text-align: center;
  margin-bottom: 20px;
  color: #1989fa;
  font-weight: 600;
}

.register-form {
  margin-top: 10px;
}

.register-btn-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.register-btn {
  width: 180px;
}
</style>