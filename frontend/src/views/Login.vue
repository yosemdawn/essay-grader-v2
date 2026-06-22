<template>
  <div class="login-container">
    <div class="login-box">
      <!-- 标题区域 -->
      <div class="login-header">
        <h1 class="title">🎓 AI作文批阅系统</h1>
        <p class="subtitle">✨ V2.0 智能批阅 · 高效便捷 ✨</p>
      </div>

      <!-- 登录表单 -->
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @keyup.enter="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="👤 请输入用户名"
            size="large"
            prefix-icon="User"
            clearable
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="🔑 请输入密码"
            size="large"
            prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            class="login-button"
            @click="handleLogin"
          >
            <span v-if="!loading">🚀 登录</span>
            <span v-else>⏳ 登录中...</span>
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 提示信息 -->
      <div class="login-tips">
        <el-alert type="info" :closable="false" show-icon>
          <template #title>
            <div>💡 登录提示</div>
          </template>
          <div class="tips-content">
            <p>👨‍💼 <strong>管理员</strong>：admin / admin123</p>
            <p>👨‍🎓 <strong>学生</strong>：学生姓名 / 123456</p>
          </div>
        </el-alert>
      </div>

      <!-- 页脚 -->
      <div class="login-footer">
        <p>© 2024 牛逼格拉斯yosem AI作文批阅系统 🎉</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { FormInstance, FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'
import type { LoginRequest } from '@/types'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 表单引用
const loginFormRef = ref<FormInstance>()

// 登录表单数据
const loginForm = reactive<LoginRequest>({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '用户名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 4, max: 20, message: '密码长度在 4 到 20 个字符', trigger: 'blur' }
  ]
}

// 加载状态
const loading = ref(false)

/**
 * 处理登录
 */
const handleLogin = async () => {
  if (!loginFormRef.value) return

  // 验证表单
  const valid = await loginFormRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true

  try {
    // 调用登录API
    await userStore.login(loginForm)

    // 登录成功，根据角色跳转
    const redirect = (route.query.redirect as string) || 
                    (userStore.isAdmin ? '/dashboard' : '/student/records')
    
    router.push(redirect)
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-box {
  background: white;
  border-radius: 16px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  padding: 40px;
  width: 100%;
  max-width: 450px;
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 35px;
}

.title {
  font-size: 32px;
  font-weight: bold;
  color: #333;
  margin: 0 0 12px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 16px;
  color: #999;
  margin: 0;
}

.login-form {
  margin-bottom: 25px;
}

.login-button {
  width: 100%;
  font-size: 16px;
  font-weight: 600;
  height: 45px;
}

.login-tips {
  margin-bottom: 25px;
}

.tips-content {
  font-size: 14px;
  line-height: 1.8;
}

.tips-content p {
  margin: 6px 0;
}

.login-footer {
  text-align: center;
  color: #999;
  font-size: 13px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.login-footer p {
  margin: 0;
}

/* 移动端适配 */
@media (max-width: 500px) {
  .login-box {
    padding: 30px 25px;
  }

  .title {
    font-size: 26px;
  }

  .subtitle {
    font-size: 14px;
  }
}
</style>
