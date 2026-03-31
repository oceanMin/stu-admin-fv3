// src/main.ts
import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'  // 1. 先导入Pinia
import router from './router'       // 2. 再导入路由
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 3. 先创建Pinia实例
const pinia = createPinia()
// 4. 再创建Vue应用
const app = createApp(App)

// 5. 先注册Pinia（绝对不能晚于app.mount）
app.use(pinia)
// 6. 再注册路由
app.use(router)
// 7. 最后注册ElementPlus，挂载应用
app.use(ElementPlus)
app.mount('#app')