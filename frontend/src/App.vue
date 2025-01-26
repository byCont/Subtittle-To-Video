// frontend/src/App.vue, Main component

<template>
  <div class="app-container">
    <AppHeader />
    <div class="container-fluid">
      <br><br>
      <CustomLoader v-if="loading" />
      <div class="row">
        <VideoUpload 
          @upload="uploadVideoFile"
          @generate-video="generateVideo"
          :upload-progress="uploadprogress" 
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