<template>
    <el-dialog v-model="dialogVisible" :title="title" :width="width" :fullscreen="fullscreen" :draggable="draggable"
        :close-on-click-modal="closeOnClickModal" :append-to-body="appendToBody" :before-close="handleBeforeClose"
        destroy-on-close>
        <!-- 表单区域 -->
        <el-scrollbar :max-height="maxHeight">
            <el-form ref="formRef" :model="formData" :rules="computedRules" :label-width="labelWidth"
                :label-position="labelPosition" :size="size" :disabled="disabled">
                <!-- 动态渲染表单项 -->
                <template v-for="field in fields" :key="field.prop">
                    <el-form-item :label="field.label" :prop="field.prop" :rules="field.rules"
                        :required="field.required">
                        <!-- 输入框 -->
                        <el-input v-if="field.type === 'input'" v-model="formData[field.prop]"
                            :type="field.inputType || 'text'" :placeholder="field.placeholder || `请输入${field.label}`"
                            :clearable="field.clearable !== false" :disabled="field.disabled"
                            :maxlength="field.maxlength" :minlength="field.minlength"
                            :show-word-limit="field.showWordLimit" :autosize="field.autosize" :rows="field.rows"
                            @change="handleFieldChange(field, $event)">
                            <template v-if="field.prefix" #prefix>
                                <span>{{ field.prefix }}</span>
                            </template>
                            <template v-if="field.suffix" #suffix>
                                <span>{{ field.suffix }}</span>
                            </template>
                        </el-input>

                        <!-- 文本域 -->
                        <el-input v-else-if="field.type === 'textarea'" v-model="formData[field.prop]" type="textarea"
                            :placeholder="field.placeholder || `请输入${field.label}`"
                            :clearable="field.clearable !== false" :disabled="field.disabled"
                            :maxlength="field.maxlength" :minlength="field.minlength"
                            :show-word-limit="field.showWordLimit"
                            :autosize="field.autosize || { minRows: 3, maxRows: 6 }" :rows="field.rows"
                            @change="handleFieldChange(field, $event)" />

                        <!-- 数字输入框 -->
                        <el-input-number v-else-if="field.type === 'number'" v-model="formData[field.prop]"
                            :placeholder="field.placeholder || `请输入${field.label}`" :disabled="field.disabled"
                            :min="field.min" :max="field.max" :step="field.step || 1" :precision="field.precision"
                            :controls-position="field.controlsPosition" @change="handleFieldChange(field, $event)" />

                        <!-- 下拉选择器 -->
                        <el-select v-else-if="field.type === 'select'" v-model="formData[field.prop]"
                            :placeholder="field.placeholder || `请选择${field.label}`"
                            :clearable="field.clearable !== false" :disabled="field.disabled"
                            :filterable="field.filterable" :multiple="field.multiple"
                            :collapse-tags="field.collapseTags" @change="handleFieldChange(field, $event)">
                            <el-option v-for="option in field.options" :key="option.value" :label="option.label"
                                :value="option.value" :disabled="option.disabled" />
                        </el-select>

                        <!-- 单选框组 -->
                        <el-radio-group v-else-if="field.type === 'radio'" v-model="formData[field.prop]"
                            :disabled="field.disabled" @change="handleFieldChange(field, $event)">
                            <el-radio v-for="option in field.options" :key="option.value" :value="option.value"
                                :disabled="option.disabled">
                                {{ option.label }}
                            </el-radio>
                        </el-radio-group>

                        <!-- 复选框组 -->
                        <el-checkbox-group v-else-if="field.type === 'checkbox'" v-model="formData[field.prop]"
                            :disabled="field.disabled" @change="handleFieldChange(field, $event)">
                            <el-checkbox v-for="option in field.options" :key="option.value" :value="option.value"
                                :disabled="option.disabled">
                                {{ option.label }}
                            </el-checkbox>
                        </el-checkbox-group>

                        <!-- 开关 -->
                        <el-switch v-else-if="field.type === 'switch'" v-model="formData[field.prop]"
                            :disabled="field.disabled" :active-text="field.activeText"
                            :inactive-text="field.inactiveText"
                            :active-value="field.activeValue !== undefined ? field.activeValue : true"
                            :inactive-value="field.inactiveValue !== undefined ? field.inactiveValue : false"
                            @change="handleFieldChange(field, $event)" />

                        <!-- 日期选择器 -->
                        <el-date-picker v-else-if="field.type === 'date'" v-model="formData[field.prop]"
                            :type="field.dateType || 'date'" :placeholder="field.placeholder || `请选择${field.label}`"
                            :clearable="field.clearable !== false" :disabled="field.disabled" :format="field.format"
                            :value-format="field.valueFormat" @change="handleFieldChange(field, $event)" />

                        <!-- 时间选择器 -->
                        <el-time-picker v-else-if="field.type === 'time'" v-model="formData[field.prop]"
                            :placeholder="field.placeholder || `请选择${field.label}`"
                            :clearable="field.clearable !== false" :disabled="field.disabled" :format="field.format"
                            :value-format="field.valueFormat" @change="handleFieldChange(field, $event)" />

                        <!-- 级联选择器 -->
                        <el-cascader v-else-if="field.type === 'cascader'" v-model="formData[field.prop]"
                            :options="field.options" :placeholder="field.placeholder || `请选择${field.label}`"
                            :clearable="field.clearable !== false" :disabled="field.disabled"
                            :props="field.cascaderProps" @change="handleFieldChange(field, $event)" />

                        <!-- 默认输入框 -->
                        <el-input v-else v-model="formData[field.prop]"
                            :placeholder="field.placeholder || `请输入${field.label}`"
                            :clearable="field.clearable !== false" :disabled="field.disabled"
                            @change="handleFieldChange(field, $event)" />

                        <!-- 字段提示信息 -->
                        <div v-if="field.tip" class="field-tip">
                            <el-text size="small" type="info">{{ field.tip }}</el-text>
                        </div>
                    </el-form-item>
                </template>

                <!-- 自定义表单内容插槽 -->
                <slot name="form" :form-data="formData" />
            </el-form>
        </el-scrollbar>

        <!-- 底部按钮区域 -->
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="handleCancel" :disabled="loading">
                    {{ cancelText }}
                </el-button>
                <el-button type="primary" @click="handleSubmit" :loading="loading">
                    {{ submitText }}
                </el-button>
                <!-- 自定义按钮插槽 -->
                <slot name="footer" :loading="loading" :submit="handleSubmit" :cancel="handleCancel" />
            </div>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, nextTick } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'

// 字段配置类型
export interface FormField {
    prop: string                    // 字段名
    label: string                   // 标签
    type?: string                   // 类型: input/textarea/number/select/radio/checkbox/switch/date/time/cascader
    required?: boolean              // 是否必填
    placeholder?: string            // 占位符
    disabled?: boolean              // 是否禁用
    clearable?: boolean             // 是否可清空
    rules?: any[]                   // 自定义验证规则
    options?: Array<{               // 选项（用于select/radio/checkbox）
        label: string
        value: any
        disabled?: boolean
    }>
    // input 相关
    inputType?: string              // input 原生类型
    maxlength?: number
    minlength?: number
    showWordLimit?: boolean
    autosize?: boolean | { minRows: number, maxRows: number }
    rows?: number
    prefix?: string
    suffix?: string
    // number 相关
    min?: number
    max?: number
    step?: number
    precision?: number
    controlsPosition?: string
    // select 相关
    filterable?: boolean
    multiple?: boolean
    collapseTags?: boolean
    // switch 相关
    activeText?: string
    inactiveText?: string
    activeValue?: any
    inactiveValue?: any
    // date/time 相关
    dateType?: string
    format?: string
    valueFormat?: string
    // cascader 相关
    cascaderProps?: object
    // 提示信息
    tip?: string
    // 事件回调
    onChange?: (value: any, formData: any) => void
}

// 组件 Props
interface Props {
    // 弹窗相关
    visible?: boolean
    title?: string
    width?: string | number
    fullscreen?: boolean
    draggable?: boolean
    closeOnClickModal?: boolean
    appendToBody?: boolean
    maxHeight?: string | number
    // 表单相关
    fields?: FormField[]
    initialData?: Record<string, any>
    rules?: FormRules
    labelWidth?: string | number
    labelPosition?: 'left' | 'right' | 'top'
    size?: 'large' | 'default' | 'small'
    disabled?: boolean
    // 按钮相关
    submitText?: string
    cancelText?: string
    // 提交前钩子
    beforeSubmit?: (data: Record<string, any>) => boolean | Promise<boolean>
}

const props = withDefaults(defineProps < Props > (), {
    visible: false,
    title: '表单',
    width: '500px',
    fullscreen: false,
    draggable: false,
    closeOnClickModal: true,
    appendToBody: true,
    maxHeight: '60vh',
    fields: () => [],
    initialData: () => ({}),
    rules: () => ({}),
    labelWidth: '100px',
    labelPosition: 'right',
    size: 'default',
    disabled: false,
    submitText: '确定',
    cancelText: '取消',
})

// Emits
const emit = defineEmits < {
    'update:visible': [value: boolean]
  'submit': [data: Record < string, any >]
  'cancel': []
  'open': []
  'close': []
} > ()

// 表单引用
const formRef = ref < FormInstance > ()

// 弹窗显示状态（内部双向绑定）
const dialogVisible = computed({
    get: () => props.visible,
    set: (val) => emit('update:visible', val)
})

// 表单数据
const formData = reactive < Record < string, any>> ({})

// 加载状态
const loading = ref(false)

// 合并验证规则
const computedRules = computed(() => {
    const mergedRules: FormRules = { ...props.rules }

    // 从 fields 中提取 required 规则
    props.fields.forEach(field => {
        if (field.required && !mergedRules[field.prop]) {
            mergedRules[field.prop] = [
                { required: true, message: `请输入${field.label}`, trigger: 'blur' }
            ]
        } else if (field.required && mergedRules[field.prop]) {
            // 如果已有规则，添加 required 规则
            const existingRules = mergedRules[field.prop] as any[]
            if (!existingRules.some(rule => rule.required)) {
                existingRules.unshift({ required: true, message: `请输入${field.label}`, trigger: 'blur' })
            }
        }
    })

    return mergedRules
})

// 初始化表单数据
const initFormData = () => {
    // 先清空
    Object.keys(formData).forEach(key => {
        delete formData[key]
    })

    // 从 fields 中获取默认值
    props.fields.forEach(field => {
        if (props.initialData[field.prop] !== undefined) {
            formData[field.prop] = props.initialData[field.prop]
        } else {
            // 根据类型设置默认值
            if (field.type === 'checkbox' && field.multiple !== false) {
                formData[field.prop] = []
            } else if (field.type === 'switch') {
                formData[field.prop] = field.activeValue !== undefined ? field.activeValue : false
            } else {
                formData[field.prop] = ''
            }
        }
    })

    // 合并 initialData 中的额外字段
    Object.keys(props.initialData).forEach(key => {
        if (formData[key] === undefined) {
            formData[key] = props.initialData[key]
        }
    })
}

// 监听弹窗打开，重置表单
watch(() => props.visible, (newVal) => {
    if (newVal) {
        initFormData()
        // 清空验证
        nextTick(() => {
            formRef.value?.clearValidate()
            emit('open')
        })
    } else {
        emit('close')
    }
}, { immediate: true })

// 监听 initialData 变化
watch(() => props.initialData, () => {
    if (props.visible) {
        initFormData()
    }
}, { deep: true })

// 字段变化回调
const handleFieldChange = (field: FormField, value: any) => {
    if (field.onChange) {
        field.onChange(value, formData)
    }
}

// 关闭前回调
const handleBeforeClose = (done: () => void) => {
    // 如果有加载中，不允许关闭
    if (loading.value) return
    done()
}

// 取消
const handleCancel = () => {
    if (loading.value) return
    dialogVisible.value = false
    emit('cancel')
}

// 提交
const handleSubmit = async () => {
    if (loading.value) return

    // 表单验证
    try {
        await formRef.value?.validate()
    } catch {
        return
    }

    // 执行前置钩子
    if (props.beforeSubmit) {
        try {
            const result = await props.beforeSubmit({ ...formData })
            if (result === false) return
        } catch (error) {
            console.error('beforeSubmit error:', error)
            return
        }
    }

    loading.value = true

    try {
        await emit('submit', { ...formData })
        // 提交成功后默认关闭弹窗（如果父组件没有手动处理）
        dialogVisible.value = false
    } catch (error) {
        console.error('提交失败:', error)
        // 不关闭弹窗，让父组件处理
    } finally {
        loading.value = false
    }
}

// 暴露方法给父组件
defineExpose({
    // 表单验证
    validate: () => formRef.value?.validate(),
    // 重置表单
    reset: () => {
        initFormData()
        nextTick(() => {
            formRef.value?.clearValidate()
        })
    },
    // 设置字段值
    setFieldValue: (prop: string, value: any) => {
        formData[prop] = value
    },
    // 获取表单数据
    getFormData: () => ({ ...formData }),
    // 设置加载状态
    setLoading: (status: boolean) => {
        loading.value = status
    }
})
</script>

<style scoped>
.dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
}

.field-tip {
    margin-top: 4px;
    line-height: 1.2;
}

/* 滚动条样式优化 */
:deep(.el-scrollbar__view) {
    padding-right: 8px;
}
</style>