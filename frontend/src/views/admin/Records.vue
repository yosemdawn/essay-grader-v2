<template>
  <div class="records">
    <h2 class="page-title">📝 批阅记录</h2>

    <!-- 筛选栏 -->
    <el-card class="filter-card" shadow="hover">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="filterUsername"
            placeholder="按学生用户名筛选"
            clearable
            @clear="loadRecords"
            @keyup.enter="loadRecords"
          >
            <template #append>
              <el-button :icon="Search" @click="loadRecords" />
            </template>
          </el-input>
        </el-col>
        <el-col :span="8">
          <el-input
            v-model="filterStudentName"
            placeholder="按学生姓名筛选"
            clearable
            @clear="filterByStudentName"
            @keyup.enter="filterByStudentName"
          >
            <template #append>
              <el-button :icon="Search" @click="filterByStudentName" />
            </template>
          </el-input>
        </el-col>
        <el-col :span="8">
          <el-button type="primary" @click="loadRecords">刷新</el-button>
          <el-button @click="clearFilters">清除筛选</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 记录列表 -->
    <el-card class="table-card" shadow="hover">
      <el-table
        v-loading="loading"
        :data="records"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="essay_id" label="作文ID" width="120" />
        <el-table-column prop="student_name" label="学生姓名" width="120" />
        <el-table-column prop="score" label="分数" width="100">
          <template #default="{ row }">
            <el-tag :type="getScoreType(row.score)" size="large">
              {{ row.score }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="advantages" label="优点" show-overflow-tooltip min-width="150">
          <template #default="{ row }">
            {{ formatField(row.advantages) }}
          </template>
        </el-table-column>
        <el-table-column prop="disadvantages" label="不足" show-overflow-tooltip min-width="150">
          <template #default="{ row }">
            {{ formatField(row.disadvantages) }}
          </template>
        </el-table-column>
        <el-table-column prop="suggestions" label="建议" show-overflow-tooltip min-width="150">
          <template #default="{ row }">
            {{ formatSuggestions(row.suggestions) }}
          </template>
        </el-table-column>
        <el-table-column prop="graded_at" label="批阅时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.graded_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewDetail(row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadRecords"
        @current-change="loadRecords"
        style="margin-top: 20px; justify-content: center;"
      />
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="批阅详情" width="800px">
      <el-descriptions v-if="currentRecord" :column="2" border>
        <el-descriptions-item label="记录ID">{{ currentRecord.id }}</el-descriptions-item>
        <el-descriptions-item label="作文ID">{{ currentRecord.essay_id }}</el-descriptions-item>
        <el-descriptions-item label="学生姓名">{{ currentRecord.student?.username || '-' }}</el-descriptions-item>
        <el-descriptions-item label="分数">
          <el-tag :type="getScoreType(currentRecord.score)" size="large">
            {{ currentRecord.score }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="优点" :span="2">
          <div v-html="formatFieldHTML(currentRecord.advantages)"></div>
        </el-descriptions-item>
        <el-descriptions-item label="不足" :span="2">
          <div v-html="formatFieldHTML(currentRecord.disadvantages)"></div>
        </el-descriptions-item>
        <el-descriptions-item label="建议" :span="2">
          <div v-if="isSuggestionsArray(currentRecord.suggestions)">
            <div v-for="(item, index) in parseSuggestions(currentRecord.suggestions)" :key="index" style="margin-bottom: 15px; padding: 10px; background: #f5f7fa; border-radius: 4px;">
              <div style="margin-bottom: 5px;"><strong>{{ index + 1 }}. 原句：</strong>{{ item.original_sentence }}</div>
              <div style="margin-bottom: 5px; color: #67c23a;"><strong>修改建议：</strong>{{ item.revised_sentence }}</div>
              <div style="color: #909399;"><strong>原因：</strong>{{ item.reason }}</div>
            </div>
          </div>
          <div v-else>{{ currentRecord.suggestions }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="批阅人">{{ currentRecord.graded_by }}</el-descriptions-item>
        <el-descriptions-item label="批阅时间">
          {{ formatDate(currentRecord.graded_at) }}
        </el-descriptions-item>
      </el-descriptions>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getAllRecords, getStudentRecords, getRecordDetail } from '@/api/records'
import type { GradingRecord } from '@/types'

const route = useRoute()

const loading = ref(false)
const records = ref<GradingRecord[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)

const filterUsername = ref('')
const filterStudentName = ref('')

const detailDialogVisible = ref(false)
const currentRecord = ref<GradingRecord | null>(null)

const loadRecords = async () => {
  loading.value = true
  try {
    const skip = (currentPage.value - 1) * pageSize.value
    const limit = pageSize.value

    let res
    if (filterUsername.value) {
      res = await getStudentRecords(filterUsername.value)
      // 手动分页
      records.value = res.records.slice(skip, skip + limit)
      total.value = res.records.length
    } else {
      res = await getAllRecords(skip, limit)
      records.value = res.records
      total.value = res.total
    }
  } catch (error: any) {
    ElMessage.error(error.message || '加载记录失败')
  } finally {
    loading.value = false
  }
}

const filterByStudentName = () => {
  if (!filterStudentName.value) {
    loadRecords()
    return
  }

  // 前端过滤
  const filtered = records.value.filter(r => 
    r.student_name.includes(filterStudentName.value)
  )
  records.value = filtered
  total.value = filtered.length
}

const clearFilters = () => {
  filterUsername.value = ''
  filterStudentName.value = ''
  currentPage.value = 1
  loadRecords()
}

const getScoreType = (score: number) => {
  if (score >= 90) return 'success'
  if (score >= 80) return 'primary'
  if (score >= 60) return 'warning'
  return 'danger'
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  try {
    return new Date(dateStr).toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch {
    return dateStr
  }
}

// 格式化字段（简单文本或JSON）
const formatField = (field: any) => {
  if (!field) return '-'
  if (typeof field === 'string') {
    try {
      const parsed = JSON.parse(field)
      if (Array.isArray(parsed)) {
        return parsed.join('; ')
      }
      return field
    } catch {
      return field
    }
  }
  return String(field)
}

// 格式化字段为HTML（用于详情页）
const formatFieldHTML = (field: any) => {
  if (!field) return '-'
  if (typeof field === 'string') {
    try {
      const parsed = JSON.parse(field)
      if (Array.isArray(parsed)) {
        return parsed.map((item, index) => `<div style="margin-bottom: 5px;">${index + 1}. ${item}</div>`).join('')
      }
      return field.replace(/\n/g, '<br>')
    } catch {
      return field.replace(/\n/g, '<br>')
    }
  }
  return String(field)
}

// 格式化建议（简短显示）
const formatSuggestions = (suggestions: any) => {
  if (!suggestions) return '-'
  if (typeof suggestions === 'string') {
    try {
      const parsed = JSON.parse(suggestions)
      if (Array.isArray(parsed)) {
        return `共 ${parsed.length} 条建议`
      }
      return suggestions
    } catch {
      return suggestions
    }
  }
  return String(suggestions)
}

// 检查建议是否为数组格式
const isSuggestionsArray = (suggestions: any) => {
  if (!suggestions) return false
  if (typeof suggestions === 'string') {
    try {
      const parsed = JSON.parse(suggestions)
      return Array.isArray(parsed) && parsed.length > 0 && parsed[0].original_sentence
    } catch {
      return false
    }
  }
  return false
}

// 解析建议数组
const parseSuggestions = (suggestions: any) => {
  if (!suggestions) return []
  if (typeof suggestions === 'string') {
    try {
      return JSON.parse(suggestions)
    } catch {
      return []
    }
  }
  return suggestions
}

const viewDetail = async (record: GradingRecord) => {
  try {
    const response = await getRecordDetail(record.id)
    // 后端返回的是 { record: {...} } 格式
    currentRecord.value = (response as any).record || response
    detailDialogVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '加载详情失败')
  }
}

onMounted(() => {
  // 从URL参数获取筛选条件
  const username = route.query.username as string
  const recordId = route.query.id as string

  if (username) {
    filterUsername.value = username
  }

  loadRecords()

  // 如果有recordId，直接打开详情
  if (recordId) {
    getRecordDetail(Number(recordId)).then(response => {
      // 后端返回的是 { record: {...} } 格式
      currentRecord.value = (response as any).record || response
      detailDialogVisible.value = true
    }).catch(error => {
      ElMessage.error(error.message || '加载详情失败')
    })
  }
})
</script>

<style scoped>
.records {
  padding: 20px;
}

.page-title {
  margin: 0 0 20px 0;
  font-size: 24px;
  color: #303133;
}

.filter-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}
</style>

