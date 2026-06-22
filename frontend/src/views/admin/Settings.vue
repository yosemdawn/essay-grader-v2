<template>
  <div class="settings-page">
    <div class="page-head">
      <div>
        <h2>系统配置</h2>
        <p>配置 AI 批阅模型和学生结果邮件发送。配置保存在本机 data/teacher_config.json，不写入源码。</p>
      </div>
      <div class="status-tags">
        <el-tag v-if="llmConfig?.api_key_configured" type="success" size="large">
          AI 已配置 {{ llmConfig.api_key_masked }}
        </el-tag>
        <el-tag v-else type="danger" size="large">AI 未配置</el-tag>
        <el-tag v-if="emailConfig?.enabled && emailConfig.smtp_password_configured" type="success" size="large">
          邮件已开启
        </el-tag>
        <el-tag v-else type="info" size="large">邮件未开启</el-tag>
      </div>
    </div>

    <el-card class="settings-card" shadow="never">
      <template #header>AI 批阅配置</template>
      <el-form label-width="120px">
        <el-form-item label="模型 ID">
          <el-input v-model="llmForm.model_id" placeholder="doubao-seed-2-0-lite-260428" />
        </el-form-item>
        <el-form-item label="API Key">
          <el-input
            v-model="llmForm.api_key"
            type="password"
            show-password
            placeholder="填写火山方舟 API Key"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="savingLLM" @click="saveLLMConfig">保存 AI 配置</el-button>
          <el-button :loading="loading" @click="loadConfig">刷新</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="settings-card" shadow="never">
      <template #header>学生邮件发送配置</template>
      <el-form label-width="120px">
        <el-form-item label="发送邮件">
          <el-switch
            v-model="emailForm.enabled"
            active-text="开启"
            inactive-text="关闭"
          />
        </el-form-item>
        <el-form-item label="SMTP 服务器">
          <el-input v-model="emailForm.smtp_host" placeholder="smtp.qq.com" />
        </el-form-item>
        <el-form-item label="SMTP 端口">
          <el-input-number v-model="emailForm.smtp_port" :min="1" :max="65535" />
        </el-form-item>
        <el-form-item label="发件 QQ 邮箱">
          <el-input v-model="emailForm.smtp_username" placeholder="例如：123456@qq.com" />
        </el-form-item>
        <el-form-item label="邮箱授权码">
          <el-input
            v-model="emailForm.smtp_password"
            type="password"
            show-password
            :placeholder="emailConfig?.smtp_password_configured ? `已保存 ${emailConfig.smtp_password_masked}，不改可留空` : '填写 QQ 邮箱 SMTP 授权码'"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="savingEmail" @click="saveEmailConfig">保存邮件配置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="guide-card" shadow="never">
      <template #header>简要说明</template>
      <ol>
        <li>火山引擎：进入火山方舟/Ark 控制台，开通服务并创建 API Key，模型 ID 使用 <code>doubao-seed-2-0-lite-260428</code>。</li>
        <li>QQ 邮箱：进入 QQ 邮箱设置，开启 SMTP 服务，按提示生成“授权码”。这里填写授权码，不是 QQ 登录密码。</li>
        <li>导入学生时填写邮箱，例如 <code>张三,zhangsan@qq.com,一班</code>。批改保存成功后，系统会自动把结果发到该学生邮箱。</li>
        <li>如果学校集中部署，只需要在运行程序的那台电脑上配置一次。</li>
      </ol>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  getEmailConfig,
  getLLMConfig,
  updateEmailConfig,
  updateLLMConfig,
  type EmailConfig,
  type LLMConfig
} from '@/api/settings'

const loading = ref(false)
const savingLLM = ref(false)
const savingEmail = ref(false)
const llmConfig = ref<LLMConfig | null>(null)
const emailConfig = ref<EmailConfig | null>(null)

const llmForm = reactive({
  model_id: 'doubao-seed-2-0-lite-260428',
  api_key: ''
})

const emailForm = reactive({
  enabled: false,
  smtp_host: 'smtp.qq.com',
  smtp_port: 465,
  smtp_username: '',
  smtp_password: ''
})

const loadConfig = async () => {
  loading.value = true
  try {
    const [llm, email] = await Promise.all([getLLMConfig(), getEmailConfig()])
    llmConfig.value = llm
    emailConfig.value = email
    llmForm.model_id = llm.model_id || 'doubao-seed-2-0-lite-260428'
    llmForm.api_key = ''
    emailForm.enabled = email.enabled
    emailForm.smtp_host = email.smtp_host || 'smtp.qq.com'
    emailForm.smtp_port = email.smtp_port || 465
    emailForm.smtp_username = email.smtp_username || ''
    emailForm.smtp_password = ''
  } catch (error: any) {
    ElMessage.error(error.message || '读取配置失败')
  } finally {
    loading.value = false
  }
}

const saveLLMConfig = async () => {
  if (!llmForm.model_id.trim()) {
    ElMessage.warning('请填写模型 ID')
    return
  }
  if (!llmForm.api_key.trim()) {
    ElMessage.warning('请填写 API Key')
    return
  }

  savingLLM.value = true
  try {
    llmConfig.value = await updateLLMConfig({
      model_id: llmForm.model_id.trim(),
      api_key: llmForm.api_key.trim()
    })
    llmForm.api_key = ''
    ElMessage.success('AI 配置已保存')
  } catch (error: any) {
    ElMessage.error(error.message || '保存 AI 配置失败')
  } finally {
    savingLLM.value = false
  }
}

const saveEmailConfig = async () => {
  if (emailForm.enabled && !emailForm.smtp_username.trim()) {
    ElMessage.warning('开启邮件发送时，请填写发件 QQ 邮箱')
    return
  }
  if (emailForm.enabled && !emailForm.smtp_password.trim() && !emailConfig.value?.smtp_password_configured) {
    ElMessage.warning('开启邮件发送时，请填写 QQ 邮箱授权码')
    return
  }

  savingEmail.value = true
  try {
    emailConfig.value = await updateEmailConfig({
      enabled: emailForm.enabled,
      smtp_host: emailForm.smtp_host.trim() || 'smtp.qq.com',
      smtp_port: emailForm.smtp_port,
      smtp_username: emailForm.smtp_username.trim(),
      smtp_password: emailForm.smtp_password.trim()
    })
    emailForm.smtp_password = ''
    ElMessage.success('邮件配置已保存')
  } catch (error: any) {
    ElMessage.error(error.message || '保存邮件配置失败')
  } finally {
    savingEmail.value = false
  }
}

onMounted(loadConfig)
</script>

<style scoped>
.settings-page {
  padding: 20px;
}

.page-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}

.page-head h2 {
  margin: 0 0 8px;
  font-size: 24px;
  color: #303133;
}

.page-head p {
  margin: 0;
  color: #606266;
}

.status-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.settings-card,
.guide-card {
  margin-bottom: 20px;
  border-radius: 8px;
}

.guide-card ol {
  margin: 0;
  padding-left: 22px;
  color: #303133;
  line-height: 1.9;
}

code {
  padding: 2px 6px;
  border-radius: 4px;
  background: #f5f7fa;
  color: #c45656;
}
</style>
