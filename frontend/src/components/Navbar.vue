<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { ChevronDown, Triangle } from 'lucide-vue-next'

defineProps({
  links: { type: Array, default: () => [] }   // [{ id, label }]
})
const emit = defineEmits(['ask'])

const scrolled = ref(false)
const open = ref(false)

const onScroll = () => { scrolled.value = window.scrollY > 20 }

onMounted(() => {
  window.addEventListener('scroll', onScroll)
  onScroll()
})
onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
  document.body.style.overflow = ''
})

// 展开移动端菜单时锁定滚动
watch(open, v => { document.body.style.overflow = v ? 'hidden' : '' })

function go(id) {
  open.value = false
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <header
    class="fixed top-0 left-0 right-0 z-50 transition-all duration-300"
    :class="scrolled ? 'bg-brand-cream/90 backdrop-blur-md shadow-sm' : 'bg-transparent'"
  >
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <div class="relative flex items-center h-16 md:h-20">
        <!-- 桌面左侧链接 -->
        <nav class="hidden md:flex items-center gap-8 animate-fade-down stagger-1">
          <button
            v-for="(l, i) in links"
            :key="l.id"
            class="text-sm text-brand-dark tracking-wide uppercase hover:opacity-70 transition-opacity flex items-center gap-1"
            @click="go(l.id)"
          >
            {{ l.label }}
            <ChevronDown v-if="i === 0" class="w-3.5 h-3.5" />
          </button>
        </nav>

        <!-- 居中标志 -->
        <a
          href="#hero"
          class="absolute left-1/2 -translate-x-1/2 flex items-center gap-2 animate-fade-down stagger-2"
          @click.prevent="go('hero')"
        >
          <Triangle class="w-5 h-5 text-brand-dark fill-brand-dark" />
          <span class="text-xl text-brand-dark tracking-tight font-helvetica-neue">数据分析 Agent</span>
        </a>

        <!-- 桌面右侧 CTA -->
        <button
          class="hidden md:inline-flex items-center ml-auto px-5 py-2.5 bg-brand-dark text-white text-sm tracking-wide uppercase rounded-full hover:bg-brand-green transition-colors animate-fade-down stagger-3"
          @click="emit('ask')"
        >
          开始提问
        </button>

        <!-- 移动端汉堡 -->
        <button
          class="md:hidden ml-auto z-50 relative w-10 h-10"
          aria-label="Toggle menu"
          @click="open = !open"
        >
          <span
            class="absolute left-2 w-6 h-[2px] bg-brand-dark rounded transition-all duration-300 ease-[cubic-bezier(0.68,-0.6,0.32,1.6)] top-[6px]"
            :class="open ? 'rotate-45 translate-y-[5px]' : ''"
          ></span>
          <span
            class="absolute left-2 w-6 h-[2px] bg-brand-dark rounded transition-all duration-300 ease-[cubic-bezier(0.68,-0.6,0.32,1.6)] top-[13px]"
            :class="open ? '-rotate-45' : ''"
          ></span>
        </button>
      </div>
    </div>

    <!-- 移动端全屏遮罩 -->
    <div
      class="md:hidden fixed inset-0 bg-brand-cream z-40 transition-all duration-500 ease-[cubic-bezier(0.22,1,0.36,1)]"
      :class="open ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'"
    >
      <div
        class="flex flex-col items-center justify-center h-full gap-8 transition-all duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] delay-100"
        :class="open ? 'translate-y-0 opacity-100' : '-translate-y-8 opacity-0'"
      >
        <button
          v-for="l in links"
          :key="l.id"
          class="text-3xl text-brand-dark tracking-tight"
          @click="go(l.id)"
        >{{ l.label }}</button>
        <button
          class="mt-4 inline-flex items-center px-8 py-3.5 bg-brand-dark text-white text-lg tracking-wide rounded-full"
          @click="open = false; emit('ask')"
        >开始提问</button>
      </div>
    </div>
  </header>
</template>
