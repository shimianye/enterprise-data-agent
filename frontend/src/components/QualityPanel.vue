<script setup>
const props = defineProps({
  result: { type: Object, required: true },
  feedbackState: { type: String, default: 'idle' },
  selectedRating: { type: String, default: '' }
})
const emit = defineEmits(['rate'])

const labels = {
  high: { title: '基础检查通过', tone: 'quality-high' },
  medium: { title: '存在需要核对的项目', tone: 'quality-medium' },
  low: { title: '建议人工复核', tone: 'quality-low' }
}
</script>

<template>
  <section class="quality-panel mt-6" :class="labels[result.confidence]?.tone || 'quality-sample'">
    <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
      <div>
        <p class="text-xs tracking-[0.18em] uppercase opacity-60">Query quality</p>
        <h3 class="text-lg mt-1">
          {{ labels[result.confidence]?.title || '内置演示样例' }}
        </h3>
        <p class="text-xs opacity-60 mt-1">
          这是规则化检查等级，不是统计意义上的正确率概率。
        </p>
      </div>
      <span v-if="result.attempt_count" class="badge shrink-0">
        SQL 尝试 {{ result.attempt_count }} 次
      </span>
    </div>

    <div v-if="result.quality_checks?.length" class="quality-checks mt-4">
      <div v-for="check in result.quality_checks" :key="check.code" class="quality-check">
        <span :class="check.passed ? 'check-pass' : 'check-review'">
          {{ check.passed ? '✓' : '!' }}
        </span>
        <span>{{ check.message }}</span>
      </div>
    </div>

    <div v-if="result.query_id" class="feedback-row mt-5 pt-4 border-t border-brand-dark/10">
      <span class="text-sm text-brand-dark/65">这个结果对吗？</span>
      <button
        class="feedback-button"
        :class="{ selected: selectedRating === 'correct' }"
        :disabled="feedbackState === 'saving'"
        @click="emit('rate', 'correct')"
      >结果正确</button>
      <button
        class="feedback-button"
        :class="{ selected: selectedRating === 'incorrect' }"
        :disabled="feedbackState === 'saving'"
        @click="emit('rate', 'incorrect')"
      >需要改进</button>
      <span v-if="feedbackState === 'saved'" class="text-xs text-brand-green">已记录，将进入人工审核队列</span>
      <span v-else-if="feedbackState === 'error'" class="text-xs text-red-700">反馈未保存，请稍后重试</span>
    </div>
  </section>
</template>
