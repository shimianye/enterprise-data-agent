/**
 * chart_data -> ECharts option 的纯函数映射。
 * 不依赖 Vue / DOM，便于单独调试；kpi 与 table 返回 null（前端不画图）。
 */
// 森林系配色，与 cream / forest 视觉一致
export const PALETTE = ['#3d5a3e', '#6f8f70', '#2d3a2e', '#8aa68b', '#a9bfa9', '#54714f', '#c2d2c1']

export function fmt(v) {
  if (v === null || v === undefined || v === '') return '-'
  if (typeof v !== 'number') return String(v)
  return Number.isInteger(v)
    ? v.toLocaleString('zh-CN')
    : v.toLocaleString('zh-CN', { maximumFractionDigits: 2 })
}

const isNum = v => typeof v === 'number' || (typeof v === 'string' && v !== '' && !isNaN(Number(v)))

export { isNum }

export function buildOption(result) {
  const cd = result.chart_data
  if (!cd || result.chart_type === 'kpi' || result.chart_type === 'table') return null

  const cats = (cd.categories || []).map(String)
  const series = cd.series || []
  const unit = cd.unit || ''
  const dimLabel = cd.dimension_label || ''

  const axisFormatter = v =>
    unit === '元' && Math.abs(v) >= 10000 ? `${(v / 10000).toFixed(0)}万` : fmt(v)

  const base = {
    color: PALETTE,
    grid: { left: 16, right: 24, top: 28, bottom: 16, containLabel: true },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      valueFormatter: v => `${fmt(v)}${unit}`
    },
    legend: { show: series.length > 1, top: 0, textStyle: { color: '#5f6f5f' } }
  }

  if (result.chart_type === 'pie') {
    return {
      ...base,
      tooltip: {
        trigger: 'item',
        formatter: p => `${p.name}<br/>${p.seriesName}：${fmt(p.value)}${unit}（${p.percent}%）`
      },
      legend: { show: true, bottom: 0, textStyle: { color: '#5f6f5f' } },
      series: [{
        name: series[0]?.name || '指标',
        type: 'pie',
        radius: ['42%', '68%'],
        itemStyle: { borderColor: '#fff', borderWidth: 2 },
        label: { formatter: '{b}\n{d}%' },
        data: cats.map((c, i) => ({ name: c, value: series[0]?.data[i] }))
      }]
    }
  }

  // 类目过多时转横向条形，否则 X 轴标签会挤成一团
  const horizontal = cats.length > 8
  const catAxis = {
    type: 'category',
    data: cats,
    name: dimLabel,
    nameLocation: 'middle',
    nameGap: horizontal ? 28 : 34,
    nameTextStyle: { color: '#93a193' },
    axisLabel: {
      color: '#5f6f5f',
      interval: horizontal ? 0 : 'auto',
      rotate: horizontal ? 0 : (cats.length > 12 ? 35 : 0)
    },
    axisLine: { lineStyle: { color: '#e2e7e0' } },
    axisTick: { show: false }
  }
  const valAxis = {
    type: 'value',
    name: series.length === 1 ? `${series[0].name}${unit ? `(${unit})` : ''}` : '',
    nameTextStyle: { color: '#93a193' },
    splitLine: { lineStyle: { color: '#eef1ec' } },
    axisLabel: { color: '#93a193', formatter: axisFormatter }
  }

  const isLine = result.chart_type === 'line'
  return {
    ...base,
    xAxis: horizontal ? valAxis : catAxis,
    yAxis: horizontal ? { ...catAxis, inverse: true } : valAxis,
    series: series.map(s => ({
      name: s.name,
      type: isLine ? 'line' : 'bar',
      data: s.data,
      smooth: isLine,
      symbol: 'circle',
      symbolSize: 6,
      barMaxWidth: 28,
      itemStyle: { borderRadius: isLine ? 0 : [4, 4, 0, 0] },
      areaStyle: isLine ? { opacity: 0.12 } : undefined
    }))
  }
}
