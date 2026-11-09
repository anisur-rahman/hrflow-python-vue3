<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../services/api'

const count = ref<number | null>(null)
const error = ref('')

onMounted(async () => {
  try {
    const { data } = await api.get('/employees')
    count.value = Array.isArray(data) ? data.length : (data.total ?? data.items?.length ?? 0)
  } catch {
    error.value = 'Unable to load headcount.'
  }
})
</script>

<template>
  <header>
    <h2>HR Dashboard</h2>
    <p>Welcome to HRFlow</p>
  </header>

  <section class="card">
    <h3>Total employees</h3>
    <strong>{{ count ?? '—' }}</strong>
    <p v-if="error" role="alert">{{ error }}</p>
  </section>

  <p>Start by creating a department, then add employees.</p>
</template>
