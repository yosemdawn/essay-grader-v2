<template>
  <div class="students">
    <h2 class="page-title">👨‍🎓 学生管理</h2>

    <!-- 操作栏 -->
    <el-card class="toolbar-card" shadow="hover">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-button type="primary" @click="showImportDialog">
            批量导入学生
          </el-button>
          <el-button type="warning" @click="showResetPasswordDialog">
            重置密码
          </el-button>
        </el-col>
        <el-col :span="12">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索学生姓名或用户名"
            clearable
            @clear="loadStudents"
            @keyup.enter="loadStudents"
          >
            <template #append>
              <el-button :icon="Search" @click="loadStudents" />
            </template>
          </el-input>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 15px;">
        <el-col :span="6">
          <el-select v-model="filterClass" placeholder="筛选班级" clearable @change="loadStudents">
            <el-option label="全部班级" value="" />
            <el-option v-for="cls in classList" :key="cls" :label="cls" :value="cls" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="filterActive" placeholder="筛选状态" clearable @change="loadStudents">
            <el-option label="全部状态" value="" />
            <el-option label="活跃" :value="true" />
            <el-option label="禁用" :value="false" />
          </el-select>
        </el-col>
      </el-row>
    </el-card>

    <!-- 学生列表 -->
    <el-card class="table-card" shadow="hover">
      <el-table
        v-loading="loading"
        :data="students"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="email" label="邮箱" width="200" />
        <el-table-column prop="class_name" label="班级" width="120" />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '活跃' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewRecords(row.username)">
              查看记录
            </el-button>
            <el-button type="danger" link @click="deleteStudent(row)">
              删除
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
        @size-change="loadStudents"
        @current-change="loadStudents"
        style="margin-top: 20px; justify-content: center;"
      />
    </el-card>

    <!-- 批量导入对话框 -->
    <el-dialog v-model="importDialogVisible" title="批量导入学生" width="600px">
      <el-form :model="importForm" label-width="120px">
        <el-form-item label="默认密码">
          <el-input v-model="importForm.default_password" placeholder="默认密码，如: 123456" />
        </el-form-item>
        <el-form-item label="学生信息">
          <el-input
            v-model="importForm.studentsText"
            type="textarea"
            :rows="10"
            placeholder="每行一个学生，格式: 用户名,邮箱,班级&#10;例如:&#10;zhangsan,zhangsan@example.com,一班&#10;lisi,lisi@example.com,二班"
          />
        </el-form-item>
        <el-alert
          title="导入后会自动分配学生账号：用户名使用第一列，密码使用上方默认密码。作文图片里识别出的姓名需要和用户名一致。"
          type="info"
          show-icon
          :closable="false"
        />
      </el-form>
      <el-table
        v-if="importResultDetails.length"
        :data="importResultDetails"
        size="small"
        style="margin-top: 16px;"
      >
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'success' ? 'success' : 'warning'">
              {{ row.status === 'success' ? '已创建' : '未创建' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="初始密码" width="120">
          <template #default="{ row }">
            {{ row.status === 'success' ? importForm.default_password : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="reason" label="说明" />
      </el-table>
      <template #footer>
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="importing" @click="handleImport">
          导入
        </el-button>
      </template>
    </el-dialog>

    <!-- 重置密码对话框 -->
    <el-dialog v-model="resetPasswordDialogVisible" title="重置密码" width="500px">
      <el-form :model="resetPasswordForm" label-width="120px">
        <el-form-item label="重置范围">
          <el-radio-group v-model="resetPasswordForm.resetType">
            <el-radio label="all">所有学生</el-radio>
            <el-radio label="selected">选中的学生</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="resetPasswordForm.new_password" placeholder="输入新密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="resetPasswordDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="resetting" @click="handleResetPassword">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getUserList, batchImportStudents, resetPassword, deleteUser } from '@/api/users'
import type { User, StudentImportItem } from '@/types'

const router = useRouter()

const loading = ref(false)
const importing = ref(false)
const resetting = ref(false)

const students = ref<User[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)

const searchKeyword = ref('')
const filterClass = ref('')
const filterActive = ref<boolean | ''>('')

const importDialogVisible = ref(false)
const resetPasswordDialogVisible = ref(false)
const importResultDetails = ref<any[]>([])

const importForm = ref({
  default_password: '123456',
  studentsText: ''
})

const resetPasswordForm = ref({
  resetType: 'all',
  new_password: ''
})

const classList = computed(() => {
  const classes = new Set(students.value.map(s => s.class_name).filter(Boolean))
  return Array.from(classes)
})

const loadStudents = async () => {
  loading.value = true
  try {
    const params: any = {
      role: 'student',
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }

    if (filterClass.value) {
      params.class_name = filterClass.value
    }

    if (filterActive.value !== '') {
      params.is_active = filterActive.value
    }

    const res = await getUserList(params)
    
    // 如果有搜索关键词，在前端过滤
    if (searchKeyword.value) {
      students.value = res.users.filter(u => 
        u.username.includes(searchKeyword.value) || 
        (u.email && u.email.includes(searchKeyword.value))
      )
      total.value = students.value.length
    } else {
      students.value = res.users
      total.value = res.total
    }
  } catch (error: any) {
    ElMessage.error(error.message || '加载学生列表失败')
  } finally {
    loading.value = false
  }
}

const showImportDialog = () => {
  importForm.value = {
    default_password: '123456',
    studentsText: ''
  }
  importResultDetails.value = []
  importDialogVisible.value = true
}

const handleImport = async () => {
  if (!importForm.value.studentsText.trim()) {
    ElMessage.warning('请输入学生信息')
    return
  }

  importing.value = true
  try {
    const lines = importForm.value.studentsText.trim().split('\n')
    const students: StudentImportItem[] = []

    for (const line of lines) {
      const parts = line.split(',').map(p => p.trim())
      if (parts.length >= 1) {
        students.push({
          username: parts[0],
          email: parts[1] || undefined,
          class_name: parts[2] || undefined
        })
      }
    }

    const res = await batchImportStudents({
      students,
      default_password: importForm.value.default_password
    })

    importResultDetails.value = res.details
    ElMessage.success(`成功导入 ${res.success_count} 个学生，默认密码：${importForm.value.default_password}`)
    if (res.failed_count > 0) {
      ElMessage.warning(`失败 ${res.failed_count} 个`)
    }

    loadStudents()
  } catch (error: any) {
    ElMessage.error(error.message || '导入失败')
  } finally {
    importing.value = false
  }
}

const showResetPasswordDialog = () => {
  resetPasswordForm.value = {
    resetType: 'all',
    new_password: ''
  }
  resetPasswordDialogVisible.value = true
}

const handleResetPassword = async () => {
  if (!resetPasswordForm.value.new_password) {
    ElMessage.warning('请输入新密码')
    return
  }

  resetting.value = true
  try {
    const data: any = {
      new_password: resetPasswordForm.value.new_password
    }

    if (resetPasswordForm.value.resetType === 'all') {
      data.reset_all_students = true
    }

    const res = await resetPassword(data)
    ElMessage.success(`成功重置 ${res.affected_count} 个用户的密码`)
    resetPasswordDialogVisible.value = false
  } catch (error: any) {
    ElMessage.error(error.message || '重置密码失败')
  } finally {
    resetting.value = false
  }
}

const viewRecords = (username: string) => {
  router.push(`/admin/records?username=${username}`)
}

const deleteStudent = async (student: User) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除学生 ${student.username} 吗？此操作不可恢复！`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteUser(student.id)
    ElMessage.success('删除成功')
    loadStudents()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

onMounted(() => {
  loadStudents()
})
</script>

<style scoped>
.students {
  padding: 20px;
}

.page-title {
  margin: 0 0 20px 0;
  font-size: 24px;
  color: #303133;
}

.toolbar-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}
</style>
