<script setup>
defineProps({ result: { type: Object, required: true } })
</script>

<template>
  <div>
    <div class="flex gap-4 items-start">
      <div class="w-[3px] self-stretch rounded-full bg-brand-green shrink-0"></div>
      <div>
        <p class="text-xl md:text-2xl text-brand-dark leading-snug tracking-tight">
          {{ result.nl_explanation }}
        </p>
        <p class="text-sm text-brand-dark/45 mt-2">{{ result.question }}</p>
      </div>
    </div>

    <div v-if="result.warnings && result.warnings.length" class="mt-4 px-3 py-2 rounded-lg bg-brand-light text-xs text-brand-dark/70">
      ⚠ {{ result.warnings.join('；') }}
    </div>

    <div class="flex flex-wrap gap-2 mt-5">
      <span class="badge">意图 {{ result.intent }}</span>
      <span class="badge">图表 {{ result.chart_type }}</span>
      <span class="badge">行数 {{ result.row_count ?? (result.rows || []).length }}</span>
      <span class="badge">耗时 {{ result.duration_ms ?? 0 }} ms</span>
      <span v-for="k in result.metric_keys || []" :key="k" class="badge">指标 {{ k }}</span>
    </div>
  </div>
</template>
