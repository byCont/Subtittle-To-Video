//frontend/src/App.vue
//main component
<template>
  <div class="app-container">
    <AppHeader />
    <div class="container-fluid">
      <CustomLoader v-if="loading" />
      <div class="row">
        <VideoPreview 
          :videoToRender="videoToRender" 
          :originalvideos="originalvideos" 
        />
        <div class="col-lg-6">
          <VideoUploadForm 
            @uploadVideo="uploadVideoFile"
            @addSubtitles="addSubtitles"
            :uploadprogress="uploadprogress" 
          />
          <VideoList 
            :videos="videos" 
            :originalvideos="originalvideos" 
            @setRenderVideo="setRenderVideo"
            @removeVideo="removeVideo"
            @reloadOriginalVideo="reloadOriginalVideo"
            @editVideoSubmit="editVideoSubmit"
            @finalrender="finalrender"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from './components/main/AppHeader.vue';
import CustomLoader from './components/main/CustomLoader.vue';
import VideoPreview from './components/main/VideoPreview.vue';
import VideoUploadForm from './components/main/VideoUploadForm.vue';
import VideoList from './components/main/VideoList.vue';

export default {
  data() {
    return {
      originalvideos: [],
      videos: [],
      loading: false,
      videoToRender: null,
      uploadprogress: 0,
    };
  },
  methods: {
    // Métodos existentes
  },
  components: {
    AppHeader,
    CustomLoader,
    VideoPreview,
    VideoUploadForm,
    VideoList,
  },
};
</script>
