import axios from 'axios'

export const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
})

export interface Employee {
  id: number
  name: string
  email: string
  department_id: number
  hire_date: string
  status: string
}

export interface Department {
  id: number
  name: string
}
