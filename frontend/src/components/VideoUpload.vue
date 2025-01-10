<template>
  <div class="col-lg-6 video-upload-container">
    <div class="form-group">
      <!-- Drag and Drop Area -->
      <div
        class="drag-and-drop-area"
        @dragover.prevent
        @dragenter.prevent
        @drop.prevent="handleDrop"
      >
        <p>Drag & Drop your video files here</p>
        <span>or </span>
        <label class="upload-label">
          Add Video Clip
          <input type="file" id="fileinput" accept="video/*" hidden @change="handleFileSelect" />
        </label>
      </div>

      <div class="form-control-group">
        <label for="subtitleinput">Add Subtitles:</label>
        <input type="file" id="subtitleinput" accept=".srt,.ass" @change="handleFileSelect" />
      </div>

      <div class="form-control-group">
        <input type="text" class="form-control" placeholder="Clip Name" id="clipname" />
      </div>

      <div class="form-buttons">
        <button class="btn btn-secondary" @click="$emit('add-subtitles')">Add Subtitles</button>
        <button class="btn btn-primary" @click="$emit('upload')">Upload</button>
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


