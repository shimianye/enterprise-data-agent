<script setup>
defineProps({ sql: { type: String, default: '' } })
</script>

<template>
  <details v-if="sql" class="fold mt-8 pt-4 border-t border-brand-dark/10">
    <summary>生成 SQL</summary>
    <pre class="sql">{{ sql }}</pre>
  </details>
</template>
