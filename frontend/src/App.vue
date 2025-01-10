/frontend/src/App.vue
//main component

<template>
  <div class="app-container">
    <AppHeader />
    <div class="container-fluid">
      <br><br>
      <CustomLoader v-if="loading" />
      <div class="row">
        <VideoUpload 
          @upload="uploadVideoFile"
          @add-subtitles="addSubtitles"
          :upload-progress="uploadprogress" 
        />
        <VideoPreview 
          :video-to-render="videoToRender" 
          :original-videos="originalvideos" 
        />        
      </div>
      <VideoList 
        :videos="videos"
        @remove-video="removeVideo"
        @set-render-video="setRenderVideo"
        @reload-original-video="reloadOriginalVideo"
        @edit-video-submit="editVideoSubmit"
      />
      <MergeClipsButton 
        v-if="videos.length > 0"
        @final-render="finalrender" 
      />
    </div>
  </div>
</template>

<script>
  import logic from './scripts/AppLogic.js';
  import CustomLoader from './components/CustomLoader.vue';
  import AppHeader from './components/AppHeader.vue';
  import VideoPreview from './components/VideoPreview.vue';
  import VideoUpload from './components/VideoUpload.vue';
  import VideoList from './components/VideoList.vue';
  import MergeClipsButton from './components/MergeClipsButton.vue';
  import './App.css';

  export default {
    mixins: [logic],
    components: { 
      CustomLoader, 
      AppHeader, 
      VideoPreview, 
      VideoUpload, 
      VideoList, 
      MergeClipsButton 
    },
  };
</script>