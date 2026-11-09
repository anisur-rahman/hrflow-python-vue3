<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api, type Employee, type Department } from '../services/api'

const employees = ref<Employee[]>([])
const departments = ref<Department[]>([])
const error = ref('')
const message = ref('')

const form = ref({
  name: '',
  email: '',
  department_id: 0,
  hire_date: new Date().toISOString().slice(0, 10),
})

async function load() {
  try {
    const [e, d] = await Promise.all([api.get('/employees'), api.get('/departments')])
    employees.value = Array.isArray(e.data) ? e.data : (e.data.items ?? [])
    departments.value = Array.isArray(d.data) ? d.data : (d.data.items ?? [])
  } catch {
    error.value = 'Could not load HR data.'
  }
}

async function addEmployee() {
  error.value = ''
  message.value = ''
  try {
    await api.post('/employees', form.value)
    message.value = 'Employee added.'
    form.value.name = ''
    form.value.email = ''
    await load()
  } catch {
    error.value = 'Could not add employee. Check the form and department.'
  }
}

onMounted(load)
</script>

<template>
  <header>
    <h2>Employees</h2>
    <p>Manage employee records</p>
  </header>

  <section class="card">
    <h3>Add employee</h3>
    <form @submit.prevent="addEmployee">
      <label>
        Full name
        <input v-model="form.name" required minlength="2" />
      </label>
      <label>
        Email
        <input v-model="form.email" type="email" required />
      </label>
      <label>
        Department
        <select v-model.number="form.department_id" required>
          <option :value="0" disabled>Select department</option>
          <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
        </select>
      </label>
      <label>
        Hire date
        <input v-model="form.hire_date" type="date" required />
      </label>
      <button type="submit">Add employee</button>
    </form>
    <p v-if="error" role="alert">{{ error }}</p>
    <p v-if="message" role="status">{{ message }}</p>
    <p v-if="!departments.length">
      Create a department through
      <a href="http://localhost:8000/docs" target="_blank" rel="noopener">API docs</a> first.
    </p>
  </section>

  <section class="card">
    <h3>Employee directory</h3>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="e in employees" :key="e.id">
          <td>{{ e.name }}</td>
          <td>{{ e.email }}</td>
          <td>{{ e.status }}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="!employees.length">No employees yet.</p>
  </section>
</template>
