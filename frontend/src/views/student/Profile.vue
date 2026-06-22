<template>
  <div class="profile">
    <h2 class="page-title">👤 个人信息</h2>

    <el-row :gutter="20">
      <!-- 个人信息卡片 -->
      <el-col :xs="24" :md="12">
        <el-card class="info-card" shadow="hover">
          <template #header>
            <span>基本信息</span>
          </template>

          <div class="avatar-section">
            <el-avatar :size="100" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <span style="font-size: 48px;">{{ userStore.username?.charAt(0).toUpperCase() }}</span>
            </el-avatar>
          </div>

          <el-descriptions :column="1" border style="margin-top: 20px;">
            <el-descriptions-item label="用户名">
              <el-tag type="primary">{{ userStore.userInfo?.username }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="角色">
              <el-tag type="success">👨‍🎓 学生</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="邮箱">
              {{ userStore.userInfo?.email || '未设置' }}
            </el-descriptions-item>
            <el-descriptions-item label="班级">
              {{ userStore.userInfo?.class_name || '未设置' }}
            </el-descriptions-item>
            <el-descriptions-item label="账号状态">
              <el-tag :type="userStore.userInfo?.is_active ? 'success' : 'danger'">
                {{ userStore.userInfo?.is_active ? '活跃' : '禁用' }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <!-- 学习统计卡片 -->
      <el-col :xs="24" :md="12">
        <el-card class="stats-card" shadow="hover">
          <template #header>
            <span>学习统计</span>
          </template>

          <div class="stat-item">
            <div class="stat-icon">📚</div>
            <div class="stat-content">
              <div class="stat-label">总批阅数</div>
              <div class="stat-value">{{ stats.totalRecords }}</div>
            </div>
          </div>

          <el-divider />

          <div class="stat-item">
            <div class="stat-icon">⭐</div>
            <div class="stat-content">
              <div class="stat-label">平均分数</div>
              <div class="stat-value">{{ stats.avgScore }}</div>
            </div>
          </div>

          <el-divider />

          <div class="stat-item">
            <div class="stat-icon">🏆</div>
            <div class="stat-content">
              <div class="stat-label">最高分数</div>
              <div class="stat-value">{{ stats.highestScore }}</div>
            </div>
          </div>

          <el-divider />

          <div class="stat-item">
            <div class="stat-icon">📈</div>
            <div class="stat-content">
              <div class="stat-label">最近批阅</div>
              <div class="stat-value">{{ stats.lastGradedAt }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 提示信息 -->
    <el-card class="tips-card" shadow="hover" style="margin-top: 20px;">
      <template #header>
        <span>💡 温馨提示</span>
      </template>
      <el-alert
        title="如需修改个人信息，请联系管理员"
        type="info"
        :closable="false"
        show-icon
      />
      <el-alert
        title="如需查看批阅记录，请前往我的记录页面"
        type="success"
        :closable="false"
        show-icon
        style="margin-top: 10px;"
      >
        <template #default>
          <el-button type="primary" link @click="goToRecords">
            前往我的记录 →
          </el-button>
        </template>
      </el-alert>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getMyRecords } from '@/api/records'

const router = useRouter()
const userStore = useUserStore()

const stats = ref({
  totalRecords: 0,
  avgScore: '0',
  highestScore: '0',
  lastGradedAt: '暂无记录'
})

const loadStats = async () => {
  try {
    const res = await getMyRecords(0, 100)
    stats.value.totalRecords = res.total

    if (res.records.length > 0) {
      // 计算平均分
      const sum = res.records.reduce((acc, r) => acc + r.score, 0)
      stats.value.avgScore = (sum / res.records.length).toFixed(1)

      // 最高分
      stats.value.highestScore = Math.max(...res.records.map(r => r.score)).toString()

      // 最近批阅时间
      const latestRecord = res.records.sort((a, b) => 
        new Date(b.graded_at).getTime() - new Date(a.graded_at).getTime()
      )[0]
      stats.value.lastGradedAt = new Date(latestRecord.graded_at).toLocaleString('zh-CN')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '加载统计数据失败')
  }
}

const goToRecords = () => {
  router.push('/student/records')
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.profile {
  padding: 20px;
}

.page-title {
  margin: 0 0 20px 0;
  font-size: 24px;
  color: #303133;
}

.info-card,
.stats-card,
.tips-card {
  margin-bottom: 20px;
}

.avatar-section {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.stat-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin-right: 15px;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}
</style>
