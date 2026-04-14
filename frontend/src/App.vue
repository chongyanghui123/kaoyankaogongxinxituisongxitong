<template>
  <router-view />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #333;
  background-color: #fff;
}

.container {
  width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 通用样式 */
a {
  color: #409eff;
  text-decoration: none;
}

a:hover {
  color: #66b1ff;
}

/* 清除浮动 */
.clearfix::after {
  content: '';
  display: table;
  clear: both;
}
</style>
