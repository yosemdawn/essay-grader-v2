<template>
  <div class="grading">
    <div class="page-head">
      <div>
        <h2>批阅作文</h2>
        <p>上传题目图片和学生作文图片，系统会用已配置的豆包模型完成图片识别、批改、邮件发送和总体分析。</p>
      </div>
      <el-button text type="primary" @click="router.push('/admin/settings')">检查系统配置</el-button>
    </div>

    <el-card class="steps-card" shadow="never">
      <el-steps :active="currentStep" align-center finish-status="success">
        <el-step title="上传题目" />
        <el-step title="上传作文" />
        <el-step title="开始批阅" />
        <el-step title="查看结果" />
      </el-steps>
    </el-card>

    <el-card v-if="currentStep === 0" class="step-card" shadow="never">
      <template #header>第一步：上传作文题目图片</template>
      <el-upload
        v-model:file-list="promptFileList"
        drag
        :auto-upload="false"
        :limit="1"
        accept="image/*"
        :on-change="handlePromptChange"
        :on-remove="handlePromptRemove"
        list-type="picture"
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">拖入题目图片，或 <em>点击选择</em></div>
        <template #tip>
          <div class="el-upload__tip">AI 会直接识别图片中的题目和写作要求，不再调用独立 OCR。</div>
        </template>
      </el-upload>

      <div v-if="promptPreviewUrl" class="image-preview">
        <el-image :src="promptPreviewUrl" fit="contain" />
      </div>

      <div class="step-actions">
        <el-button type="primary" :loading="uploading" :disabled="!promptFileList.length" @click="handleUploadPrompt">
          下一步
        </el-button>
      </div>
    </el-card>

    <el-card v-if="currentStep === 1" class="step-card" shadow="never">
      <template #header>第二步：批量上传学生作文图片</template>
      <el-alert
        title="请确保作文图片里能看清学生姓名。学生姓名需要和“学生管理”里的用户名一致，结果才能保存到学生账号。"
        type="info"
        :closable="false"
        show-icon
      />

      <el-upload
        v-model:file-list="essayFileList"
        class="essay-upload"
        drag
        multiple
        :auto-upload="false"
        :limit="50"
        accept="image/*"
        :on-change="handleEssaysChange"
        list-type="picture-card"
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">拖入作文图片，或 <em>点击选择</em></div>
        <template #tip>
          <div class="el-upload__tip">已选择 {{ essayFileList.length }} 份作文，最多 50 份。</div>
        </template>
      </el-upload>

      <div class="step-actions">
        <el-button @click="currentStep = 0">上一步</el-button>
        <el-button type="primary" :loading="uploading" :disabled="!essayFileList.length" @click="handleUploadEssays">
          下一步
        </el-button>
      </div>
    </el-card>

    <el-card v-if="currentStep === 2" class="step-card" shadow="never">
      <template #header>第三步：确认并开始批阅</template>
      <div class="confirm-grid">
        <div class="confirm-item">
          <span>作文题目</span>
          <strong>已上传</strong>
        </div>
        <div class="confirm-item">
          <span>学生作文</span>
          <strong>{{ essayFileList.length }} 份</strong>
        </div>
      </div>
      <el-alert
        title="批阅完成后会显示每个学生情况和总体分析；学生资料里有邮箱且已开启邮件配置时，会自动发送批阅报告。"
        type="warning"
        :closable="false"
        show-icon
      />
      <div class="step-actions">
        <el-button @click="currentStep = 1">上一步</el-button>
        <el-button type="primary" size="large" :loading="processing" @click="startProcessing">
          {{ processing ? '任务启动中...' : '开始 AI 批阅' }}
        </el-button>
      </div>
    </el-card>

    <el-card v-if="currentStep === 3" class="step-card" shadow="never">
      <template #header>第四步：批阅进度与结果</template>

      <el-progress :percentage="taskProgress" :status="taskProgressStatus" :stroke-width="18" striped striped-flow />
      <div class="progress-line">
        <el-tag :type="taskTagType">{{ taskStatusText }}</el-tag>
        <span>{{ taskMessage }}</span>
        <span v-if="taskStatus === 'processing'">第 {{ taskCurrent }} / {{ taskTotal }} 份</span>
      </div>

      <div v-if="summary" class="summary-grid">
        <div class="metric"><span>总数</span><strong>{{ summary.total_essays }}</strong></div>
        <div class="metric"><span>批改成功</span><strong>{{ summary.successful_grades }}</strong></div>
        <div class="metric"><span>已保存</span><strong>{{ summary.saved_to_db }}</strong></div>
        <div class="metric"><span>邮件发送</span><strong>{{ summary.email_sent ?? 0 }}</strong></div>
        <div class="metric"><span>平均分</span><strong>{{ summary.average_score }}</strong></div>
      </div>

      <section v-if="overallAnalysis" class="analysis-section">
        <h3>学生总体写作情况</h3>
        <p class="overview">{{ formatText(overallAnalysis.overview || '暂无总体概述') }}</p>
        <p v-if="overallAnalysis.score_distribution" class="score-distribution">
          {{ formatText(overallAnalysis.score_distribution) }}
        </p>
        <div class="analysis-columns">
          <div>
            <h4>共性优点</h4>
            <ul><li v-for="item in asList(overallAnalysis.common_strengths)" :key="formatText(item)">{{ formatText(item) }}</li></ul>
          </div>
          <div>
            <h4>共性问题</h4>
            <ul><li v-for="item in asList(overallAnalysis.common_issues)" :key="formatText(item)">{{ formatText(item) }}</li></ul>
          </div>
          <div>
            <h4>教学重点</h4>
            <ul><li v-for="item in asList(overallAnalysis.teaching_focus)" :key="formatText(item)">{{ formatText(item) }}</li></ul>
          </div>
        </div>
      </section>

      <section v-if="taskResults.length" class="results-section">
        <div class="results-header">
          <h3>每位学生情况</h3>
          <el-button type="primary" plain @click="viewRecords">查看记录页</el-button>
        </div>

        <div class="results-grid">
          <el-card v-for="(result, index) in taskResults" :key="resultKey(result, index)" shadow="never" class="result-card">
            <div class="result-top">
              <el-avatar>{{ getInitial(result.student_name) }}</el-avatar>
              <div>
                <h4>{{ result.student_name || '未知学生' }}</h4>
                <div class="tag-row">
                  <el-tag :type="result.saved_to_db ? 'success' : 'warning'" size="small">
                    {{ result.saved_to_db ? '已保存' : '未保存' }}
                  </el-tag>
                  <el-tag v-if="result.email_sent" type="success" size="small">邮件已发送</el-tag>
                  <el-tag v-else-if="result.email_error" type="info" size="small">邮件未发送</el-tag>
                </div>
              </div>
              <strong class="score">{{ result.grading_result?.score ?? '-' }}</strong>
            </div>

            <template v-if="result.grading_result">
              <div class="result-field">
                <b>优点</b>
                <p>{{ formatText(result.grading_result.advantages) }}</p>
              </div>
              <div class="result-field">
                <b>不足</b>
                <p>{{ formatText(result.grading_result.disadvantages) }}</p>
              </div>
              <div class="result-field">
                <b>修改建议</b>
                <ol v-if="asList(result.grading_result.suggestions).length">
                  <li v-for="(item, itemIndex) in asList(result.grading_result.suggestions)" :key="itemIndex">
                    {{ formatSuggestion(item) }}
                  </li>
                </ol>
                <p v-else>暂无</p>
              </div>
              <div class="result-field">
                <b>总评</b>
                <p>{{ formatText(result.grading_result.summary_comment) }}</p>
              </div>
            </template>

            <el-alert v-if="result.error" :title="formatText(result.error)" type="warning" :closable="false" show-icon />
            <el-alert v-if="result.email_error" :title="result.email_error" type="info" :closable="false" show-icon />
            <el-button
              v-if="result.grading_record_id"
              type="primary"
              link
              @click="viewRecordDetail(result.grading_record_id)"
            >
              查看保存的详情
            </el-button>
          </el-card>
        </div>
      </section>

      <div class="step-actions" v-if="taskStatus !== 'processing'">
        <el-button @click="resetForm">重新批阅</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import type { UploadFile } from 'element-plus'
import {
  uploadPrompt as uploadPromptApi,
  uploadEssays as uploadEssaysApi,
  processBatch,
  getTaskStatus,
  type TaskStatus
} from '@/api/grading'

const router = useRouter()

const currentStep = ref(0)
const uploading = ref(false)
const processing = ref(false)

const promptFileList = ref<UploadFile[]>([])
const essayFileList = ref<UploadFile[]>([])
const promptPreviewUrl = ref('')

const sessionId = ref('')
const taskId = ref('')
const taskStatus = ref<TaskStatus['status']>('pending')
const taskProgress = ref(0)
const taskMessage = ref('正在准备批阅...')
const taskCurrent = ref(0)
const taskTotal = ref(0)
const taskResults = ref<NonNullable<TaskStatus['details']>>([])
const summary = ref<TaskStatus['summary'] | null>(null)
const overallAnalysis = ref<TaskStatus['overall_analysis'] | null>(null)

let pollTimer: number | null = null

const taskProgressStatus = computed(() => {
  if (taskStatus.value === 'completed') return 'success'
  if (taskStatus.value === 'failed') return 'exception'
  return ''
})

const taskStatusText = computed(() => {
  const map = {
    pending: '等待开始',
    processing: '批阅中',
    completed: '批阅完成',
    failed: '批阅失败'
  }
  return map[taskStatus.value]
})

const taskTagType = computed(() => {
  if (taskStatus.value === 'completed') return 'success'
  if (taskStatus.value === 'failed') return 'danger'
  if (taskStatus.value === 'processing') return 'warning'
  return 'info'
})

const asList = (value: any): any[] => {
  if (!value) return []
  if (Array.isArray(value)) return value
  if (typeof value === 'string') {
    try {
      const parsed = JSON.parse(value)
      return Array.isArray(parsed) ? parsed : [parsed]
    } catch {
      return value.trim() ? [value] : []
    }
  }
  return [value]
}

const formatText = (value: any): string => {
  if (value === null || value === undefined || value === '') return '暂无'
  if (Array.isArray(value)) return value.map(formatText).join('；')
  if (typeof value === 'object') {
    if ('original_sentence' in value || 'revised_sentence' in value || 'reason' in value) {
      return formatSuggestion(value)
    }
    return Object.entries(value)
      .map(([key, val]) => `${key}：${formatText(val)}`)
      .join('；')
  }
  return String(value)
}

const formatSuggestion = (item: any): string => {
  if (!item) return '暂无'
  if (typeof item === 'string') return item
  const original = item.original_sentence || item.original || item.problem || item.issue
  const revised = item.revised_sentence || item.revised || item.suggestion || item.fixed
  const reason = item.reason || item.explanation || item.comment
  const parts = []
  if (original) parts.push(`原句/问题：${formatText(original)}`)
  if (revised) parts.push(`修改：${formatText(revised)}`)
  if (reason) parts.push(`原因：${formatText(reason)}`)
  return parts.length ? parts.join('；') : formatText(item)
}

const getInitial = (name?: string) => (name || '未').trim().charAt(0) || '未'

const resultKey = (result: NonNullable<TaskStatus['details']>[number], index: number) => (
  `${result.student_name || 'unknown'}-${result.grading_record_id || result.essay_id || index}`
)

const handlePromptChange = (file: UploadFile) => {
  promptFileList.value = [file]
  if (promptPreviewUrl.value) URL.revokeObjectURL(promptPreviewUrl.value)
  promptPreviewUrl.value = file.raw ? URL.createObjectURL(file.raw) : ''
}

const handlePromptRemove = () => {
  promptFileList.value = []
  if (promptPreviewUrl.value) URL.revokeObjectURL(promptPreviewUrl.value)
  promptPreviewUrl.value = ''
}

const handleEssaysChange = (_file: UploadFile, fileList: UploadFile[]) => {
  essayFileList.value = fileList
}

const handleUploadPrompt = async () => {
  if (!promptFileList.value.length) return
  uploading.value = true
  try {
    const res = await uploadPromptApi(promptFileList.value[0].raw as File)
    sessionId.value = res.session_id
    ElMessage.success('题目图片已上传')
    currentStep.value = 1
  } catch (error: any) {
    ElMessage.error(error.message || '上传题目失败')
  } finally {
    uploading.value = false
  }
}

const handleUploadEssays = async () => {
  if (!sessionId.value || !essayFileList.value.length) return
  uploading.value = true
  try {
    const files = essayFileList.value.map(file => file.raw as File)
    const res = await uploadEssaysApi(sessionId.value, files)
    ElMessage.success(`已上传 ${res.uploaded_count} 份作文`)
    currentStep.value = 2
  } catch (error: any) {
    ElMessage.error(error.message || '上传作文失败')
  } finally {
    uploading.value = false
  }
}

const startProcessing = async () => {
  if (!sessionId.value) return
  processing.value = true
  try {
    const res = await processBatch(sessionId.value)
    taskId.value = res.task_id
    taskTotal.value = essayFileList.value.length
    taskStatus.value = 'processing'
    taskMessage.value = 'AI 批阅任务已启动...'
    taskProgress.value = 0
    currentStep.value = 3
    startPolling()
  } catch (error: any) {
    taskStatus.value = 'failed'
    taskMessage.value = '批阅启动失败'
    ElMessage.error(error.message || '启动批阅失败')
  } finally {
    processing.value = false
  }
}

const startPolling = () => {
  stopPolling()
  pollTimer = window.setInterval(async () => {
    try {
      const status = await getTaskStatus(taskId.value)
      taskStatus.value = status.status
      taskMessage.value = status.message || status.current_step || getDefaultMessage(status.status)
      taskCurrent.value = status.current || 0
      taskTotal.value = status.total || essayFileList.value.length
      taskProgress.value = status.progress || 0
      summary.value = status.summary || null
      overallAnalysis.value = status.overall_analysis || null
      taskResults.value = status.details || []

      if (status.status === 'completed' || status.status === 'failed') {
        stopPolling()
      }
    } catch (error) {
      console.error('轮询任务状态失败', error)
    }
  }, 2000)
}

const getDefaultMessage = (status: string) => {
  if (status === 'processing') return 'AI 正在批阅...'
  if (status === 'completed') return '批阅完成'
  if (status === 'failed') return '批阅失败'
  return '准备中...'
}

const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

const viewRecords = () => router.push('/admin/records')

const viewRecordDetail = (recordId: number) => {
  router.push({ path: '/admin/records', query: { recordId } })
}

const resetForm = () => {
  stopPolling()
  handlePromptRemove()
  currentStep.value = 0
  essayFileList.value = []
  sessionId.value = ''
  taskId.value = ''
  taskStatus.value = 'pending'
  taskProgress.value = 0
  taskMessage.value = '正在准备批阅...'
  taskCurrent.value = 0
  taskTotal.value = 0
  taskResults.value = []
  summary.value = null
  overallAnalysis.value = null
}

onUnmounted(() => {
  stopPolling()
  if (promptPreviewUrl.value) URL.revokeObjectURL(promptPreviewUrl.value)
})
</script>

<style scoped>
.grading {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-head {
  display: flex;
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

.steps-card,
.step-card {
  margin-bottom: 24px;
  border-radius: 8px;
}

.essay-upload {
  margin-top: 16px;
}

.image-preview {
  margin-top: 20px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
  text-align: center;
}

.image-preview .el-image {
  max-width: 100%;
  max-height: 420px;
}

.step-actions {
  margin-top: 24px;
  text-align: center;
}

.confirm-grid,
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-bottom: 18px;
}

.confirm-item,
.metric {
  padding: 18px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background: #fff;
}

.confirm-item span,
.metric span {
  display: block;
  margin-bottom: 8px;
  color: #909399;
}

.confirm-item strong,
.metric strong {
  font-size: 26px;
  color: #303133;
}

.progress-line {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 18px 0 24px;
  color: #606266;
}

.analysis-section {
  padding: 18px;
  margin: 24px 0;
  border-radius: 8px;
  background: #f8fafc;
}

.analysis-section h3,
.results-header h3 {
  margin: 0 0 12px;
  color: #303133;
}

.overview {
  margin: 0 0 8px;
  font-size: 16px;
  color: #303133;
}

.score-distribution {
  margin: 0 0 16px;
  color: #606266;
}

.analysis-columns {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.analysis-columns h4 {
  margin: 0 0 8px;
}

.analysis-columns ul {
  margin: 0;
  padding-left: 20px;
  line-height: 1.8;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
}

.result-card {
  border-radius: 8px;
}

.result-top {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 12px;
  align-items: center;
  margin-bottom: 14px;
}

.result-top h4 {
  margin: 0 0 6px;
  color: #303133;
}

.tag-row {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.score {
  font-size: 32px;
  color: #409eff;
}

.result-field {
  margin: 10px 0;
}

.result-field b {
  display: block;
  margin-bottom: 4px;
  color: #303133;
}

.result-field p,
.result-field ol {
  margin: 0;
  color: #606266;
  line-height: 1.65;
}

.result-field ol {
  padding-left: 20px;
}

@media (max-width: 768px) {
  .grading {
    padding: 10px;
  }

  .page-head,
  .progress-line,
  .results-header {
    display: block;
  }
}
</style>
