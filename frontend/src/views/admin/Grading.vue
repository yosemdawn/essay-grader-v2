<template>
  <div class="grading">
    <h2 class="page-title">✍️ 批阅作文</h2>

    <!-- 步骤条 -->
    <el-card class="steps-card" shadow="hover">
      <el-steps :active="currentStep" align-center finish-status="success">
        <el-step title="上传作文要求" description="上传作文题目图片" />
        <el-step title="上传学生作文" description="批量上传学生作文图片" />
        <el-step title="开始批阅" description="AI自动批阅并生成记录" />
        <el-step title="查看结果" description="查看批阅结果" />
      </el-steps>
    </el-card>

    <!-- 步骤1: 上传作文要求 -->
    <el-card v-if="currentStep === 0" class="step-card" shadow="hover">
      <template #header>
        <span>📄 步骤1: 上传作文要求图片</span>
      </template>
      
      <el-upload
        class="upload-demo"
        drag
        :auto-upload="false"
        :limit="1"
        accept="image/*"
        :on-change="handlePromptChange"
        :file-list="promptFileList"
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          将作文要求图片拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">只能上传jpg/png文件，且不超过10MB</div>
        </template>
      </el-upload>

      <div class="step-actions">
        <el-button type="primary" :loading="uploading" @click="handleUploadPrompt" :disabled="promptFileList.length === 0">
          下一步
        </el-button>
      </div>
    </el-card>

    <!-- 步骤2: 上传学生作文 -->
    <el-card v-if="currentStep === 1" class="step-card" shadow="hover">
      <template #header>
        <span>📚 步骤2: 批量上传学生作文图片 (最多50张)</span>
      </template>
      
      <el-upload
        class="upload-demo"
        drag
        multiple
        :auto-upload="false"
        :limit="50"
        accept="image/*"
        :on-change="handleEssaysChange"
        :file-list="essayFileList"
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          将学生作文图片拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            可以一次选择多个文件，最多50张。已选择: {{ essayFileList.length }} 张
          </div>
        </template>
      </el-upload>

      <div class="step-actions">
        <el-button @click="currentStep = 0">上一步</el-button>
        <el-button type="primary" :loading="uploading" @click="handleUploadEssays" :disabled="essayFileList.length === 0">
          下一步
        </el-button>
      </div>
    </el-card>

    <!-- 步骤3: 开始批阅 -->
    <el-card v-if="currentStep === 2" class="step-card" shadow="hover">
      <template #header>
        <span>🚀 步骤3: 开始批阅</span>
      </template>
      
      <el-result
        icon="success"
        title="文件上传完成"
        :sub-title="`已上传 ${essayFileList.length} 份学生作文，点击下方按钮开始AI批阅`"
      >
        <template #extra>
          <el-button type="primary" size="large" :loading="processing" @click="startProcessing">
            开始批阅
          </el-button>
        </template>
      </el-result>
    </el-card>

    <!-- 步骤4: 查看结果 -->
    <el-card v-if="currentStep === 3" class="step-card" shadow="hover">
      <template #header>
        <span>📊 步骤4: 批阅进度</span>
      </template>
      
      <div class="progress-section">
        <el-progress
          :percentage="taskProgress"
          :status="taskStatus === 'completed' ? 'success' : taskStatus === 'failed' ? 'exception' : undefined"
        />
        <div class="progress-info">
          <p>{{ taskMessage }}</p>
          <p v-if="taskStatus === 'processing'">
            进度: {{ taskCurrent }} / {{ taskTotal }}
          </p>
        </div>

        <!-- 批阅结果 -->
        <div v-if="taskStatus === 'completed' && taskResults.length > 0" class="results-section">
          <el-divider>批阅结果</el-divider>
          <el-table :data="taskResults" stripe>
            <el-table-column prop="student_name" label="学生姓名" width="150" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'success' ? 'success' : 'danger'">
                  {{ row.status === 'success' ? '成功' : '失败' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="record_id" label="记录ID" width="100" />
            <el-table-column prop="error" label="错误信息" show-overflow-tooltip />
          </el-table>
        </div>
      </div>

      <div class="step-actions">
        <el-button type="primary" @click="viewRecords">查看批阅记录</el-button>
        <el-button @click="resetForm">重新批阅</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import type { UploadFile } from 'element-plus'
import { uploadPrompt as uploadPromptApi, uploadEssays as uploadEssaysApi, processBatch, getTaskStatus } from '@/api/grading'

const router = useRouter()

const currentStep = ref(0)
const uploading = ref(false)
const processing = ref(false)

const promptFileList = ref<UploadFile[]>([])
const essayFileList = ref<UploadFile[]>([])

const sessionId = ref('')
const taskId = ref('')
const taskStatus = ref<'pending' | 'processing' | 'completed' | 'failed'>('pending')
const taskProgress = ref(0)
const taskMessage = ref('')
const taskCurrent = ref(0)
const taskTotal = ref(0)
const taskResults = ref<any[]>([])

let pollTimer: number | null = null

const handlePromptChange = (file: UploadFile) => {
  promptFileList.value = [file]
}

const handleEssaysChange = (file: UploadFile, fileList: UploadFile[]) => {
  essayFileList.value = fileList
}

const handleUploadPrompt = async () => {
  if (promptFileList.value.length === 0) {
    ElMessage.warning('请先选择作文要求图片')
    return
  }

  uploading.value = true
  try {
    const file = promptFileList.value[0].raw as File
    const res = await uploadPromptApi(file)
    sessionId.value = res.session_id
    ElMessage.success('作文要求上传成功')
    currentStep.value = 1
  } catch (error: any) {
    ElMessage.error(error.message || '上传失败')
  } finally {
    uploading.value = false
  }
}

const handleUploadEssays = async () => {
  if (essayFileList.value.length === 0) {
    ElMessage.warning('请先选择学生作文图片')
    return
  }

  uploading.value = true
  try {
    const files = essayFileList.value.map(f => f.raw as File)
    const res = await uploadEssaysApi(sessionId.value, files)
    ElMessage.success(`成功上传 ${res.uploaded_count} 份作文`)
    currentStep.value = 2
  } catch (error: any) {
    ElMessage.error(error.message || '上传失败')
  } finally {
    uploading.value = false
  }
}

const startProcessing = async () => {
  processing.value = true
  try {
    const res = await processBatch(sessionId.value)
    taskId.value = res.task_id
    ElMessage.success('批阅任务已启动')
    currentStep.value = 3
    startPolling()
  } catch (error: any) {
    ElMessage.error(error.message || '启动批阅失败')
  } finally {
    processing.value = false
  }
}

const startPolling = () => {
  pollTimer = window.setInterval(async () => {
    try {
      const status = await getTaskStatus(taskId.value)
      taskStatus.value = status.status
      taskMessage.value = status.message
      taskCurrent.value = status.current
      taskTotal.value = status.total
      taskProgress.value = status.progress
      
      if (status.results) {
        taskResults.value = status.results
      }

      if (status.status === 'completed' || status.status === 'failed') {
        stopPolling()
        if (status.status === 'completed') {
          ElMessage.success('批阅完成！')
        } else {
          ElMessage.error('批阅失败')
        }
      }
    } catch (error) {
      console.error('轮询任务状态失败:', error)
    }
  }, 2000)
}

const stopPolling = () => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

const viewRecords = () => {
  router.push('/admin/records')
}

const resetForm = () => {
  stopPolling()
  currentStep.value = 0
  promptFileList.value = []
  essayFileList.value = []
  sessionId.value = ''
  taskId.value = ''
  taskStatus.value = 'pending'
  taskProgress.value = 0
  taskMessage.value = ''
  taskResults.value = []
}
</script>

<style scoped>
.grading {
  padding: 20px;
}

.page-title {
  margin: 0 0 20px 0;
  font-size: 24px;
  color: #303133;
}

.steps-card {
  margin-bottom: 20px;
}

.step-card {
  margin-bottom: 20px;
}

.upload-demo {
  margin-bottom: 20px;
}

.step-actions {
  margin-top: 20px;
  text-align: center;
}

.step-actions .el-button {
  margin: 0 10px;
}

.progress-section {
  padding: 20px;
}

.progress-info {
  margin-top: 20px;
  text-align: center;
  color: #606266;
}

.results-section {
  margin-top: 30px;
}
</style>

