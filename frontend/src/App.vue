<script setup>
import { onMounted, ref } from 'vue'
import Navbar from './components/Navbar.vue'
import Hero from './components/Hero.vue'
import Conclusion from './components/Conclusion.vue'
import KpiCard from './components/KpiCard.vue'
import ChartPanel from './components/ChartPanel.vue'
import ResultTable from './components/ResultTable.vue'
import SqlPanel from './components/SqlPanel.vue'
import { fetchHealth, postQuery } from './api.js'
import samples from './mock/querySamples.json'

const links = [
  { id: 'hero', label: '提问' },
  { id: 'samples', label: '示例问题' },
  { id: 'stack', label: '技术栈' }
]

const question = ref(samples[0].question)
const result = ref(null)
const status = ref('idle')          // idle | loading | success | empty | error
const error = ref(null)
const activeIndex = ref(0)
const backend = ref('检测中…')
const backendOnline = ref(false)

async function detectBackend() {
  const h = await fetchHealth()
  backendOnline.value = !!h
  backend.value = h ? `已连接（${h.status}）` : '未连接（使用内置样例）'
}

function render(data) {
  result.value = data
  status.value = (data.rows || []).length ? 'success' : 'empty'
}

async function ask(q) {
  const text = (q ?? question.value).trim()
  if (!text) return
  error.value = null
  status.value = 'loading'
  if (!backendOnline.value) {
    const hit = samples.findIndex(s => s.question === text)
    if (hit >= 0) { activeIndex.value = hit; render(samples[hit]); return }
    status.value = 'error'
    error.value = { kind: 'network', message: '后端未连接，且该问题不在内置样例中。请启动后端或点击示例问题。' }
    return
  }
  try {
    render(await postQuery(text))
    activeIndex.value = samples.findIndex(s => s.question === text)
  } catch (e) {
    status.value = 'error'
    error.value = { kind: e.kind, message: e.message, detail: e.detail }
    result.value = null
  }
}

function pick(i) {
  if (i == null || i < 0) return
  question.value = samples[i].question
  activeIndex.value = i
  ask(samples[i].question)
}

function focusHero() {
  document.getElementById('hero')?.scrollIntoView({ behavior: 'smooth' })
  setTimeout(() => document.querySelector('#hero input')?.focus(), 350)
}

onMounted(detectBackend)
</script>

<template>
  <div class="font-helvetica-neue min-h-screen bg-brand-cream text-brand-dark">
    <Navbar :links="links" @ask="focusHero" />

    <Hero
      v-model:question="question"
      :samples="samples"
      :loading="status === 'loading'"
      :active-index="activeIndex"
      :backend="backend"
      @submit="ask()"
      @pick="pick"
    />

    <main id="result" class="max-w-7xl mx-auto px-6 lg:px-8 pb-24">
      <section v-if="status === 'error'" class="card p-6 md:p-8 border-l-4 border-l-brand-green">
        <div class="text-sm tracking-[0.2em] uppercase text-brand-dark/50 mb-2">
          {{ error.kind === 'sql_invalid' ? '安全校验拦截' : '查询失败' }}
        </div>
        <p class="text-lg text-brand-dark">{{ error.message }}</p>
        <pre v-if="error.detail" class="sql">{{ JSON.stringify(error.detail, null, 2) }}</pre>
        <p v-if="error.kind === 'sql_invalid'" class="text-xs text-brand-dark/55 mt-3">
          这是防御生效（不是缺陷）：请求被 sqlglot AST 校验器拦下，未进入数据库。
        </p>
      </section>

      <section v-else-if="status === 'loading'" class="card p-6 md:p-8">
        <div class="skeleton"></div>
        <p class="text-center text-sm text-brand-dark/50 mt-4">正在生成 SQL 并查询…</p>
      </section>

      <section v-else-if="status === 'empty'" class="card p-6 md:p-8">
        <p class="text-center text-brand-dark/60 py-10">{{ result?.nl_explanation || '未查询到符合条件的数据。' }}</p>
      </section>

      <section v-else-if="result" class="card p-6 md:p-8">
        <Conclusion :result="result" />
        <div class="mt-6">
          <KpiCard v-if="result.chart_type === 'kpi'" :key="result.question" :result="result" />
          <ChartPanel v-else-if="result.chart_data" :key="result.question" :result="result" />
        </div>
        <details class="fold mt-8 pt-4 border-t border-brand-dark/10" open>
          <summary>明细数据</summary>
          <ResultTable :result="result" />
        </details>
        <SqlPanel :sql="result.sql" />
      </section>

      <section v-else class="card p-6 md:p-8">
        <p class="text-center text-brand-dark/50 py-10">输入问题或点击上方示例开始</p>
      </section>
    </main>

    <p class="text-center text-xs text-brand-dark/40 pb-10">
      第一版范围：查询结果页（提问 → 结论 + 图表 + 明细 + SQL）
    </p>
  </div>
</template>
