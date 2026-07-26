import api from './api'

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest extends LoginRequest {
  full_name?: string
}

export const authService = {
  login: async (data: LoginRequest) => {
    const resp = await api.post('/api/v1/auth/login', data)
    return resp.data
  },
  register: async (data: RegisterRequest) => {
    const resp = await api.post('/api/v1/auth/register', data)
    return resp.data
  },
  refresh: async (refreshToken: string) => {
    const resp = await api.post('/api/v1/auth/refresh', { refresh_token: refreshToken })
    return resp.data
  },
  getMe: async () => {
    const resp = await api.get('/api/v1/users/me')
    return resp.data
  },
}