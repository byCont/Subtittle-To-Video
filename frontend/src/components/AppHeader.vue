<template>
  <div class="app-header">
    <div class="header-content">
      <h1>Video Lyric Generator</h1>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppHeader',
};
</script>

<style scoped>
.app-header {
  padding: 1rem 0;
  text-align: center;
  width: 100%;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (min-width: 992px) {
  .app-header {
    margin-bottom: 1rem;
  }
}
</style>
