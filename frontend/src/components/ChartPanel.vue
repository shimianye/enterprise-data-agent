<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
// 按需引入：只打包 line / bar / pie + 用到的组件，避免整包 1.1MB
import * as echarts from 'echarts/core'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import {
  AxisPointerComponent,
  GridComponent,
  LegendComponent,
  TooltipComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { buildOption } from '../chartOption.js'

echarts.use([
  BarChart, LineChart, PieChart,
  GridComponent, TooltipComponent, LegendComponent, AxisPointerComponent,
  CanvasRenderer
])

const props = defineProps({ result: { type: Object, required: true } })

const el = ref(null)
let chart = null

function draw() {
  if (!el.value) return
  const option = buildOption(props.result)
  if (!option) return
  if (!chart) chart = echarts.init(el.value)
  chart.setOption(option, true)
}

function resize() { chart && chart.resize() }

onMounted(() => { draw(); window.addEventListener('resize', resize) })
watch(() => props.result, () => draw(), { deep: false })
onBeforeUnmount(() => {
  window.removeEventListener('resize', resize)
  chart && chart.dispose()
  chart = null
})
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-2">
      <div class="text-sm text-brand-dark">
        {{ result.chart_data?.series?.[0]?.name || '指标' }}
        <span v-if="result.chart_data?.unit" class="text-brand-dark/50">（{{ result.chart_data.unit }}）</span>
      </div>
      <div class="text-xs text-brand-dark/45">维度：{{ result.chart_data?.dimension_label || '-' }}</div>
    </div>
    <div ref="el" class="w-full h-[360px]"></div>
  </div>
</template>

