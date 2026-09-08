<script setup>
import { ArrowRight } from 'lucide-vue-next'
import TrustedBy from './TrustedBy.vue'

defineProps({
  question: { type: String, default: '' },
  samples: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  activeIndex: { type: Number, default: -1 },
  backend: { type: String, default: '' }
})
const emit = defineEmits(['update:question', 'submit', 'pick'])
</script>

<template>
  <section id="hero" class="relative w-full bg-brand-cream">
    <div class="max-w-7xl mx-auto flex flex-col items-start pt-28 md:pt-36 pb-6 px-6 lg:px-8">
      <!-- 公告 pill -->
      <a
        href="#result"
        class="pill-link mb-5 md:mb-6 animate-fade-up stagger-3"
      >
        <span class="text-sm text-brand-dark">80 题真实评测正确率 64.0% · 安全端到端 25/25</span>
        <ArrowRight class="w-3.5 h-3.5 text-brand-dark" />
      </a>

      <!-- 标题 -->
      <h1
        class="text-left text-3xl sm:text-4xl md:text-5xl lg:text-6xl text-brand-dark leading-[1.05] tracking-tight max-w-4xl font-helvetica-neue animate-fade-up stagger-4"
      >
        把经营问题翻译成 SQL，<br class="hidden sm:block" /> 直接给出图表与结论
      </h1>

      <!-- 提问区 -->
      <div class="w-full max-w-3xl mt-8 md:mt-10 animate-fade-up stagger-5">
        <div class="flex gap-3 flex-wrap">
          <input
            type="text"
            :value="question"
            placeholder="例如：2026 年 8 月各渠道销售额对比"
            class="flex-1 min-w-[240px] bg-white border border-brand-dark/15 rounded-full px-5 py-3 text-sm text-brand-dark outline-none placeholder:text-brand-dark/35 focus:border-brand-green transition-colors"
            @input="emit('update:question', $event.target.value)"
            @keyup.enter="emit('submit')"
          />
          <button
            class="px-6 py-3 bg-brand-dark text-white text-sm tracking-wide uppercase rounded-full hover:bg-brand-green transition-colors disabled:opacity-60"
            :disabled="loading"
            @click="emit('submit')"
          >{{ loading ? '查询中…' : '提问' }}</button>
          <button
            class="px-5 py-3 border border-brand-dark/15 text-brand-dark text-sm rounded-full hover:border-brand-green hover:text-brand-green transition-colors disabled:opacity-60"
            :disabled="loading"
            @click="emit('pick', Math.floor(Math.random() * samples.length))"
          >随机样例</button>
        </div>

        <div id="samples" class="flex flex-wrap gap-2 mt-4">
          <button
            v-for="(s, i) in samples"
            :key="s.id"
            class="chip"
            :class="{ 'chip-on': i === activeIndex }"
            @click="emit('pick', i)"
          >{{ s.question }}</button>
        </div>

        <p class="mt-3 text-xs text-brand-dark/45">后端 {{ backend }} · 示例问题点击即用内置真实响应渲染</p>
      </div>

      <TrustedBy />
    </div>
  </section>
</template>
