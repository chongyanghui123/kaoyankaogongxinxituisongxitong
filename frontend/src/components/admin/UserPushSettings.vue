<template>
  <div class="user-push-settings">
    <h2 class="text-2xl font-bold mb-6">用户推送设置</h2>

    <!-- 用户选择 -->
    <div class="bg-white p-6 rounded-lg shadow mb-8">
      <h3 class="text-lg font-semibold mb-4">选择用户</h3>
      <div class="flex gap-4">
        <select v-model="selectedUserId" class="border border-gray-300 rounded px-3 py-2 flex-1">
          <option value="">请选择用户</option>
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.username }} ({{ user.email }})
          </option>
        </select>
        <button @click="loadUserSettings" class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded">
          加载设置
        </button>
      </div>
    </div>

    <!-- 推送设置 -->
    <div v-if="selectedUser" class="bg-white p-6 rounded-lg shadow">
      <h3 class="text-lg font-semibold mb-4">
        {{ selectedUser.username }} 的推送设置
      </h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 推送渠道设置 -->
        <div>
          <h4 class="font-medium mb-3">推送渠道</h4>
          <div class="space-y-2">
            <label class="flex items-center">
              <input v-model="pushSettings.channels.email" type="checkbox" class="mr-2">
              <span>邮件</span>
            </label>
            <label class="flex items-center">
              <input v-model="pushSettings.channels.wechat" type="checkbox" class="mr-2">
              <span>微信</span>
            </label>
            <label class="flex items-center">
              <input v-model="pushSettings.channels.enterprise_wechat" type="checkbox" class="mr-2">
              <span>企业微信</span>
            </label>
          </div>
        </div>

        <!-- 推送频率设置 -->
        <div>
          <h4 class="font-medium mb-3">推送频率</h4>
          <div class="space-y-2">
            <label class="flex items-center">
              <input v-model="pushSettings.frequency" type="radio" value="daily" class="mr-2">
              <span>每日推送</span>
            </label>
            <label class="flex items-center">
              <input v-model="pushSettings.frequency" type="radio" value="weekly" class="mr-2">
              <span>每周推送</span>
            </label>
            <label class="flex items-center">
              <input v-model="pushSettings.frequency" type="radio" value="realtime" class="mr-2">
              <span>实时推送</span>
            </label>
          </div>
        </div>

        <!-- 推送内容类型 -->
        <div>
          <h4 class="font-medium mb-3">推送内容类型</h4>
          <div class="space-y-2">
            <label class="flex items-center">
              <input v-model="pushSettings.content_types.policy" type="checkbox" class="mr-2">
              <span>政策变化</span>
            </label>
            <label class="flex items-center">
              <input v-model="pushSettings.content_types.school" type="checkbox" class="mr-2">
              <span>院校动态</span>
            </label>
            <label class="flex items-center">
              <input v-model="pushSettings.content_types.exam" type="checkbox" class="mr-2">
              <span>考试时间</span>
            </label>
            <label class="flex items-center">
              <input v-model="pushSettings.content_types.recommend" type="checkbox" class="mr-2">
              <span>个性化推荐</span>
            </label>
            <label class="flex items-center">
              <input v-model="pushSettings.content_types.system" type="checkbox" class="mr-2">
              <span>系统通知</span>
            </label>
          </div>
        </div>

        <!-- 推送时间设置 -->
        <div>
          <h4 class="font-medium mb-3">推送时间</h4>
          <div class="space-y-2">
            <div>
              <label class="block text-sm text-gray-600 mb-1">选择时间</label>
              <input v-model="pushSettings.push_time" type="time" class="border border-gray-300 rounded px-3 py-2">
            </div>
            <div>
              <label class="block text-sm text-gray-600 mb-1">推送日期（每周推送时生效）</label>
              <div class="flex flex-wrap gap-2">
                <label v-for="(day, index) in weekDays" :key="index" class="flex items-center">
                  <input v-model="pushSettings.weekdays" type="checkbox" :value="day.value" class="mr-1">
                  <span>{{ day.label }}</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 保存按钮 -->
      <div class="mt-6">
        <button @click="saveSettings" class="bg-green-500 hover:bg-green-600 text-white py-2 px-6 rounded">
          保存设置
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      selectedUserId: '',
      selectedUser: null,
      pushSettings: {
        channels: {
          email: true,
          wechat: false,
          enterprise_wechat: false
        },
        frequency: 'daily',
        content_types: {
          policy: true,
          school: true,
          exam: true,
          recommend: true,
          system: true
        },
        push_time: '09:00',
        weekdays: ['1', '3', '5'] // 默认周一、三、五
      },
      weekDays: [
        { label: '周一', value: '1' },
        { label: '周二', value: '2' },
        { label: '周三', value: '3' },
        { label: '周四', value: '4' },
        { label: '周五', value: '5' },
        { label: '周六', value: '6' },
        { label: '周日', value: '0' }
      ]
    }
  },
  mounted() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await fetch('/api/users', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        const data = await response.json()
        if (data.success) {
          this.users = data.data.items
        }
      } catch (error) {
        console.error('获取用户列表失败:', error)
      }
    },

    async loadUserSettings() {
      if (!this.selectedUserId) {
        alert('请选择用户')
        return
      }

      try {
        // 这里应该调用API获取用户的推送设置
        // 暂时使用模拟数据
        const user = this.users.find(u => u.id == this.selectedUserId)
        this.selectedUser = user

        // 模拟加载设置
        this.pushSettings = {
          channels: {
            email: true,
            wechat: false,
            enterprise_wechat: false
          },
          frequency: 'daily',
          content_types: {
            policy: true,
            school: true,
            exam: true,
            recommend: true,
            system: true
          },
          push_time: '09:00',
          weekdays: ['1', '3', '5']
        }
      } catch (error) {
        console.error('加载用户设置失败:', error)
      }
    },

    async saveSettings() {
      if (!this.selectedUserId) {
        alert('请选择用户')
        return
      }

      try {
        // 这里应该调用API保存用户的推送设置
        // 暂时模拟保存
        console.log('保存用户推送设置:', this.pushSettings)
        alert('设置保存成功')
      } catch (error) {
        console.error('保存用户设置失败:', error)
        alert('保存设置失败')
      }
    }
  }
}
</script>

<style scoped>
.user-push-settings {
  padding: 20px;
}
</style>
