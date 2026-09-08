<script setup>
import { computed } from 'vue'
import { fmt } from '../chartOption.js'

const props = defineProps({ result: { type: Object, required: true } })

const series = computed(() => props.result.chart_data?.series?.[0] || { name: '指标', data: ['-'] })
const unit = computed(() => props.result.chart_data?.unit || '')
</script>

<template>
  <div class="py-10 flex flex-col items-center gap-2">
    <div class="text-xs tracking-[0.25em] uppercase text-brand-dark/45">{{ series.name }}</div>
    <div class="text-5xl md:text-6xl text-brand-dark tracking-tight">
      {{ fmt(series.data[0]) }}<span class="text-xl text-brand-dark/50 ml-1">{{ unit }}</span>
    </div>
    <div class="text-xs text-brand-dark/40">单值指标 · 无需图表</div>
  </div>
</template>
