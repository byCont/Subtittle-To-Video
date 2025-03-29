<template>
  <div class="app-container">
    <AppHeader />
    <div class="main-content">
      <CustomLoader v-if="loading" />
      <div class="content-grid">
        <VideoUpload 
          @upload="uploadVideoFile"
          @generate-video="generateVideo"
          :upload-progress="uploadprogress" 
          class="upload-section"
        />
        <VideoPreview 
          :video-to-render="videoToRender" 
          :original-videos="originalvideos" 
        />        
      </div>
    </div>
  </div>
</template>

<script>
  import logic from './scripts/AppLogic.js';
  import CustomLoader from './components/CustomLoader.vue';
  import AppHeader from './components/AppHeader.vue';
  import VideoPreview from './components/VideoPreview.vue';
  import VideoUpload from './components/VideoUpload.vue';
  import './App.css';

  export default {
    mixins: [logic],
    components: { 
      CustomLoader, 
      AppHeader, 
      VideoPreview, 
      VideoUpload
    },
  };
</script>

<style scoped>
.main-content {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 1rem;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

/* Ajuste para pantallas grandes */
@media (min-width: 992px) {
  .content-grid {
    grid-template-columns: 350px 1fr;
  }
  
  .upload-section {
    width: 100%;
  }
  
  .preview-section {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>