<template>
  <!-- 🔥 关键：用 :model-value 绑定 prop，@update:model-value 触发事件 -->
  <el-dialog
    :model-value="visible"
    :title="title"
    width="600px"
    @update:model-value="$emit('update:visible', $event)"
  >
    <el-form :model="formData" :rules="rules" label-width="80px">
      <el-form-item label="学号" prop="no">
        <el-input
          v-model="formData.no"
          :disabled="title === '查看'"
          @input="$emit('update:formData', { ...formData, no: $event })"
        />
      </el-form-item>
      <el-form-item label="姓名" prop="name">
        <el-input
          v-model="formData.name"
          :disabled="title === '查看'"
          @input="$emit('update:formData', { ...formData, name: $event })"
        />
      </el-form-item>
      <el-form-item label="班级" prop="clazz">
        <el-input
          v-model="formData.clazz"
          :disabled="title === '查看'"
          @input="$emit('update:formData', { ...formData, clazz: $event })"
        />
      </el-form-item>
      <el-form-item label="专业" prop="major">
        <el-input
          v-model="formData.major"
          :disabled="title === '查看'"
          @input="$emit('update:formData', { ...formData, major: $event })"
        />
      </el-form-item>
      <el-form-item label="学院" prop="college">
        <el-input
          v-model="formData.college"
          :disabled="title === '查看'"
          @input="$emit('update:formData', { ...formData, college: $event })"
        />
      </el-form-item>
      <el-form-item label="手机号" prop="phone">
        <el-input
          v-model="formData.phone"
          :disabled="title === '查看'"
          @input="$emit('update:formData', { ...formData, phone: $event })"
        />
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input
          v-model="formData.email"
          :disabled="title === '查看'"
          @input="$emit('update:formData', { ...formData, email: $event })"
        />
      </el-form-item>
      <el-form-item label="地址" prop="address">
        <el-input
          v-model="formData.address"
          type="textarea"
          :disabled="title === '查看'"
          @input="$emit('update:formData', { ...formData, address: $event })"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="$emit('update:visible', false)">取消</el-button>
      <el-button
        type="primary"
        v-if="title !== '查看'"
        @click="$emit('submit', formData)"
      >
        确认
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
defineProps({
  visible: Boolean,
  title: String,
  formData: Object,
  rules: Object
})
defineEmits(['update:visible', 'update:formData', 'submit'])
</script>