<script setup>
// 真实技术栈（wordmark 用文字 + 展示字体，不引 SVG 品牌文件）
const stack = [
  { name: 'FastAPI',  class: 'font-playfair' },
  { name: 'SQLite',   class: 'font-oswald uppercase' },
  { name: 'sqlglot',  class: 'font-montserrat' },
  { name: 'DeepSeek', class: 'font-roboto-slab uppercase' },
  { name: 'ECharts',  class: 'font-raleway' }
]
</script>

<template>
  <div id="stack" class="w-full mt-10 md:mt-14 animate-fade-up stagger-5">
    <div class="text-left text-xs tracking-[0.25em] uppercase text-brand-dark/50 mb-6 md:mb-8 font-helvetica-neue">
      Built with
    </div>
    <div class="flex flex-wrap items-center justify-start gap-6 md:gap-12 lg:gap-16 animate-fade-up stagger-6">
      <span
        v-for="s in stack"
        :key="s.name"
        class="text-lg md:text-xl lg:text-2xl text-brand-dark/80 whitespace-nowrap"
        :class="s.class"
      >{{ s.name }}</span>
    </div>
  </div>
</template>
