// frontend/src/components/VideoUpload.vue

<template>
  <div class="col-lg-3 video-upload-container">
    <div class="form-group">
     
      <div class="form-control-group">
        <label for="subtitleinput">Add Subtitles:</label>
        <input type="file" id="subtitleinput" accept=".srt,.ass, .lrc" @change="handleFileSelect" />
      </div>

      <div class="form-control-group">
        <label for="audioinput">Add Audio:</label>
        <input type="file" id="audioinput" accept="audio/*" />
      </div>
      <div class="form-buttons">
        <button class="btn btn-primary" @click="$emit('generate-video')">Generate Video</button>
      </div>

    </div>

    <!-- Progress Bar -->
    <div class="progress-container" v-if="uploadProgress > 0">
      <div class="progress">
        <div
          id="uploadprogress"
          class="progress-bar"
          role="progressbar"
          :aria-valuenow="uploadProgress"
          aria-valuemin="0"
          aria-valuemax="100"
          :style="{ width: uploadProgress + '%' }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
  import '../App.css';
  export default {
    name: 'VideoUpload',
    props: {
      uploadProgress: Number,
    },
    methods: {
      handleDrop(event) {
        const files = event.dataTransfer.files;
        this.processFiles(files);
      },
      handleFileSelect(event) {
        const files = event.target.files;
        this.processFiles(files);
      },
      processFiles(files) {
        // Emit files to the parent component for further handling
        this.$emit('files-selected', files);
      },
    },
  };
</script>


