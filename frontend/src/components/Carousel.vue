<template>
  <div class="carousel-container">
    <el-carousel 
      :interval="5000" 
      :autoplay="true" 
      indicator-position="outside"
      height="400px"
    >
      <el-carousel-item 
        v-for="item in carousels" 
        :key="item.id"
        @click="handleCarouselClick(item)"
      >
        <div class="carousel-item">
          <img 
            :src="item.image_url || '/default-carousel.png'" 
            :alt="item.title"
            class="carousel-image"
          />
          <div class="carousel-content">
            <h3 class="carousel-title">{{ item.title }}</h3>
            <p class="carousel-subtitle" v-if="item.subtitle">{{ item.subtitle }}</p>
            <el-button 
              v-if="item.link_url" 
              type="primary" 
              size="large"
              @click="handleButtonClick($event, item)"
            >
              <span>查看详情</span>
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRight } from '@element-plus/icons-vue'
import axios from '@/utils/axios'

const carousels = ref([])

// 获取轮播图数据
const getCarousels = async () => {
  try {
    const response = await axios.get('/api/v1/learning_materials/carousels/active')
    if (response.success) {
      carousels.value = response.data
    }
  } catch (error) {
    console.error('获取轮播图数据失败:', error)
  }
}

// 处理轮播图点击
const handleCarouselClick = (item) => {
  if (item.link_url) {
    navigateToLink(item.link_url)
  }
}

// 处理按钮点击
const handleButtonClick = (event, item) => {
  event.stopPropagation()
  if (item.link_url) {
    navigateToLink(item.link_url)
  }
}

// 导航到链接
const navigateToLink = (url) => {
  if (url.startsWith('http')) {
    window.open(url, '_blank')
  } else {
    // 如果是内部链接，使用路由跳转
    const router = useRouter()
    router.push(url)
  }
}

onMounted(() => {
  getCarousels()
})
</script>

<style scoped>
.carousel-container {
  margin-bottom: 30px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.el-carousel {
  height: 400px;
}

.el-carousel__container {
  height: 100%;
}

.carousel-item {
  position: relative;
  height: 100%;
  cursor: pointer;
  transition: all 0.3s ease;
}

.carousel-item:hover {
  transform: scale(1.05);
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.3s ease;
}

.carousel-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 30px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.3), transparent);
  color: #fff;
}

.carousel-title {
  margin: 0 0 10px 0;
  font-size: 24px;
  font-weight: 600;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  line-height: 1.3;
}

.carousel-subtitle {
  margin: 0 0 20px 0;
  font-size: 14px;
  line-height: 1.5;
  opacity: 0.9;
  max-height: 42px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.carousel-content .el-button {
  background: rgba(64, 158, 255, 0.9);
  border: none;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.carousel-content .el-button:hover {
  background: rgba(64, 158, 255, 1);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

/* 指示器样式 */
:deep(.el-carousel__indicator) {
  background: rgba(255, 255, 255, 0.5);
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin: 0 5px;
  transition: all 0.3s ease;
}

:deep(.el-carousel__indicator:hover) {
  background: rgba(255, 255, 255, 0.8);
}

:deep(.el-carousel__indicator.is-active) {
  background: #fff;
  width: 25px;
  border-radius: 5px;
}

/* 控制面板样式 */
:deep(.el-carousel__arrow) {
  background: rgba(0, 0, 0, 0.3);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

:deep(.el-carousel__arrow:hover) {
  background: rgba(0, 0, 0, 0.5);
  transform: scale(1.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .el-carousel {
    height: 250px;
  }
  
  .carousel-content {
    padding: 20px;
  }
  
  .carousel-title {
    font-size: 18px;
  }
  
  .carousel-subtitle {
    font-size: 12px;
    margin-bottom: 15px;
  }
  
  .carousel-content .el-button {
    padding: 8px 16px;
    font-size: 12px;
  }
  
  :deep(.el-carousel__indicator) {
    width: 8px;
    height: 8px;
    margin: 0 3px;
  }
  
  :deep(.el-carousel__indicator.is-active) {
    width: 20px;
  }
}

@media (max-width: 480px) {
  .el-carousel {
    height: 200px;
  }
  
  .carousel-content {
    padding: 15px;
  }
  
  .carousel-title {
    font-size: 16px;
  }
  
  .carousel-subtitle {
    font-size: 11px;
    margin-bottom: 12px;
  }
  
  .carousel-content .el-button {
    padding: 6px 12px;
    font-size: 11px;
  }
}
</style>
