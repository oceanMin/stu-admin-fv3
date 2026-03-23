<template>
    <div class="pro-table-container">
        <!-- 工具栏 -->
        <div class="toolbar" v-if="$slots.toolbar || showToolbar">
            <div class="left">
                <slot name="toolbar-left"></slot>
            </div>
            <div class="right">
                <slot name="toolbar-right">
                    <el-button type="primary" @click="handleRefresh">
                        <el-icon>
                            <refresh />
                        </el-icon>
                        刷新
                    </el-button>
                </slot>
            </div>
        </div>

        <!-- 表格部分 -->
        <el-table v-bind="$attrs" :data="tableData" :border="border" :stripe="stripe" v-loading="loading"
            element-loading-text="加载中..." element-loading-spinner="el-icon-loading"
            element-loading-background="rgba(0, 0, 0, 0.1)" @selection-change="handleSelectionChange"
            @sort-change="handleSortChange">
            <template v-for="item in columns" :key="item.prop">
                <!-- 选择列 -->
                <el-table-column v-if="item.type === 'selection'" type="selection" width="55" />

                <!-- 序号列 -->
                <el-table-column v-else-if="item.type === 'index'" type="index" :width="item.width || '80'"
                    :label="item.label || '序号'" />

                <!-- 普通列 -->
                <el-table-column v-else :prop="item.prop" :label="item.label" :width="item.width"
                    :min-width="item.minWidth" :align="item.align || 'center'" :sortable="item.sortable || false">
                    <!-- 自定义列内容 -->
                    <template #default="scope" v-if="item.slot">
                        <slot :name="item.slot" :row="scope.row"></slot>
                    </template>
                </el-table-column>
            </template>
        </el-table>
    </div>
</template>

<script setup>
import { Refresh } from '@element-plus/icons-vue'

const props = defineProps({
    columns: {
        type: Array,
        required: true
    },
    tableData: {
        type: Array,
        required: true
    },
    border: {
        type: Boolean,
        default: true
    },
    stripe: {
        type: Boolean,
        default: true
    },
    loading: {
        type: Boolean,
        default: false
    },
    
    showToolbar: {
        type: Boolean,
        default: true
    }
})

const emit = defineEmits([
    'selection-change',
    'sort-change',
    'update:pageSize',
    'update:currentPage',
    'pagination-change',
    'refresh'
])

const handleSelectionChange = (val) => {
    emit('selection-change', val)
}

const handleSortChange = (val) => {
    emit('sort-change', val)
}


const handleRefresh = () => {
    emit('refresh')
}
</script>

<style scoped>
.pro-table-container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 16px;
}
</style>
