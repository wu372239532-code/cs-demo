<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="brand">风控管理系统</div>
      <div class="meta">Vue3 + Element Plus</div>
    </header>

    <main class="app-main">
      <!-- 使用路由视图，根据路由显示不同组件 -->
      <router-view />
    </main>
  </div>
</template>

<script setup>
// 不再需要直接导入组件，路由会自动处理
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: #f5f7fa;
  color: #303133;
}
.app-header {
  height: 56px;
  background: #ffffff;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
}
.brand {
  font-weight: 700;
  letter-spacing: 0.5px;
}
.meta {
  font-size: 12px;
  color: #909399;
}
.app-main {
  padding: 16px;
  max-width: 1280px;
  margin: 0 auto;
}
</style>


