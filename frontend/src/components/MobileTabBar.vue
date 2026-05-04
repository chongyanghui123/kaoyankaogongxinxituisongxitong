<template>
  <div class="mobile-tab-bar">
    <div
      v-for="item in tabs"
      :key="item.path"
      class="tab-item"
      :class="{ active: currentPath === item.path }"
      @click="navigateTo(item.path)"
    >
      <el-icon :size="24" :color="currentPath === item.path ? '#409eff' : '#999'">
        <component :is="item.icon" />
      </el-icon>
      <span :style="{ color: currentPath === item.path ? '#409eff' : '#999' }">{{ item.label }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Home, FileText, Message, User } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const currentPath = ref(route.path)

const tabs = [
  { path: '/', label: '首页', icon: Home },
  { path: '/kaoyan', label: '情报', icon: FileText },
  { path: '/user', label: '消息', icon: Message },
  { path: '/user', label: '我的', icon: User }
]

const navigateTo = (path) => {
  if (path !== currentPath.value) {
    router.push(path)
  }
}

const handleRouteChange = () => {
  currentPath.value = route.path
}

onMounted(() => {
  router.afterEach(handleRouteChange)
})

onUnmounted(() => {
  router.afterEach(() => {})
})
</script>

<style scoped>
.mobile-tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 56px;
  background-color: #fff;
  border-top: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-around;
  align-items: center;
  z-index: 1000;
  padding-bottom: env(safe-area-inset-bottom);
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  height: 100%;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-item span {
  font-size: 12px;
  margin-top: 4px;
}

.tab-item.active {
  background-color: #f5f7fa;
}

.tab-item:hover {
  background-color: #f5f7fa;
}
</style>