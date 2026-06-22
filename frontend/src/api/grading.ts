import request from '@/utils/request'

export interface UploadPromptResponse {
  success: boolean
  message: string
  session_id: string
  file_id: string
}

export interface UploadEssaysResponse {
  success: boolean
  message: string
  uploaded_count: number
  file_ids: string[]
}

export interface ProcessBatchResponse {
  success: boolean
  message: string
  task_id: string
}

export interface TaskStatus {
  task_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  progress: number
  total: number
  current: number
  message: string
  current_step?: string
  summary?: {
    total_essays: number
    successful_grades: number
    failed_grades: number
    saved_to_db: number
    email_sent?: number
    average_score: number
  }
  details?: Array<{
    student_name: string
    student_id?: number | null
    essay_id?: number
    grading_record_id?: number
    saved_to_db: boolean
    email_sent?: boolean
    email_error?: string | null
    grading_result?: {
      score: number
      advantages: any
      disadvantages: any
      suggestions: any[] | string
      summary_comment: any
      [key: string]: any
    } | null
    error?: string
  }>
  overall_analysis?: {
    overview?: any
    score_distribution?: any
    common_strengths?: any[]
    common_issues?: any[]
    teaching_focus?: any[]
    student_groups?: Array<{
      group: string
      students: string[]
      reason: string
    }>
  } | null
}

export interface GradingSuggestion {
        original_sentence: string
        revised_sentence: string
        reason: string
}

/**
 * 上传作文要求图片
 */
export function uploadPrompt(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  return request.post<UploadPromptResponse>('/grading/upload-prompt', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 批量上传学生作文图片
 */
export function uploadEssays(sessionId: string, files: File[]) {
  const formData = new FormData()
  files.forEach(file => {
    formData.append('files', file)
  })
  return request.post<UploadEssaysResponse>(`/grading/upload-essays/${sessionId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 开始批量处理任务
 */
export function processBatch(sessionId: string) {
  return request.post<ProcessBatchResponse>(`/grading/process-batch/${sessionId}`)
}

/**
 * 查询任务状态
 */
export function getTaskStatus(taskId: string) {
  return request.get<TaskStatus>(`/grading/status/${taskId}`)
}
