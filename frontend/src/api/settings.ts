import request from '@/utils/request'

export interface LLMConfig {
  model_id: string
  api_key_configured: boolean
  api_key_masked: string
}

export interface LLMConfigUpdate {
  model_id: string
  api_key: string
}

export interface EmailConfig {
  enabled: boolean
  smtp_host: string
  smtp_port: number
  smtp_username: string
  smtp_password_configured: boolean
  smtp_password_masked: string
}

export interface EmailConfigUpdate {
  enabled: boolean
  smtp_host: string
  smtp_port: number
  smtp_username: string
  smtp_password: string
}

export function getLLMConfig() {
  return request.get<LLMConfig>('/settings/llm')
}

export function updateLLMConfig(data: LLMConfigUpdate) {
  return request.put<LLMConfig>('/settings/llm', data)
}

export function getEmailConfig() {
  return request.get<EmailConfig>('/settings/email')
}

export function updateEmailConfig(data: EmailConfigUpdate) {
  return request.put<EmailConfig>('/settings/email', data)
}
