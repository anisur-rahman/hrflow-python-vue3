<template>
  <div class="shell">
    <aside>
      <h1>HRFlow</h1>
      <p>HR Management</p>
      <nav>
        <RouterLink to="/">Dashboard</RouterLink>
        <RouterLink to="/employees">Employees</RouterLink>
      </nav>
    </aside>
    <main>
      <RouterView />
    </main>
  </div>
</template>
