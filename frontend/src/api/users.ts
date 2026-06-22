import request from '@/utils/request'
import type { User, BatchImportRequest } from '@/types'

export interface BatchImportResponse {
  success_count: number
  failed_count: number
  total_count: number
  details: Array<{
    username: string
    status: 'success' | 'skipped' | 'failed'
    user_id?: number
    reason?: string
  }>
}

export interface PasswordResetRequest {
  user_ids?: number[]
  usernames?: string[]
  reset_all_students?: boolean
  new_password: string
}

export interface UserListParams {
  role?: 'admin' | 'student'
  class_name?: string
  is_active?: boolean
  skip?: number
  limit?: number
}

export interface UserListResponse {
  total: number
  users: User[]
}

/**
 * 批量导入学生
 */
export function batchImportStudents(data: BatchImportRequest) {
  return request.post<BatchImportResponse>('/users/batch-import', data)
}

/**
 * 重置用户密码
 */
export function resetPassword(data: PasswordResetRequest) {
  return request.put<{ success: boolean; message: string; affected_count: number }>('/users/reset-password', data)
}

/**
 * 获取用户列表
 */
export function getUserList(params: UserListParams = {}) {
  return request.get<UserListResponse>('/users/list', { params })
}

/**
 * 获取用户详情
 */
export function getUserDetail(userId: number) {
  return request.get<User>(`/users/${userId}`)
}

/**
 * 删除用户
 */
export function deleteUser(userId: number) {
  return request.delete<{ success: boolean; message: string }>(`/users/${userId}`)
}
