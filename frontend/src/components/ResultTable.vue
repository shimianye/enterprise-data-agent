<script setup>
import { computed } from 'vue'
import { fmt } from '../chartOption.js'

const props = defineProps({
  result: { type: Object, required: true },
  limit: { type: Number, default: 100 }
})

// 优先用后端 columns（中文表头 + 数值列标记），缺失时再从 rows 的 key 推断
const columns = computed(() => {
  if (props.result.columns && props.result.columns.length) return props.result.columns
  const row = (props.result.rows || [])[0]
  if (!row) return []
  return Object.keys(row).map(name => ({
    name,
    label: name,
    is_numeric: (props.result.rows || []).some(r => typeof r[name] === 'number')
  }))
})

const rows = computed(() => (props.result.rows || []).slice(0, props.limit))
const total = computed(() => (props.result.rows || []).length)

const cell = (row, col) =>
  col.is_numeric && typeof row[col.name] === 'number' ? fmt(row[col.name]) : (row[col.name] ?? '-')
</script>

<template>
  <div class="overflow-auto">
    <table>
      <thead>
        <tr>
          <th v-for="c in columns" :key="c.name" :class="{ num: c.is_numeric }">{{ c.label }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(r, i) in rows" :key="i">
          <td v-for="c in columns" :key="c.name" :class="{ num: c.is_numeric }">{{ cell(r, c) }}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="total > limit" class="text-xs text-brand-dark/45 mt-2">仅显示前 {{ limit }} 行，共 {{ total }} 行</p>
  </div>
</template>
