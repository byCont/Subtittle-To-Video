//frontend/src/components/VideoUploadForm.vue

<template>
  <div>
    <div class="form-group">
      <label for="fileinput">Add Video Clip:</label>
      <input type="file" id="fileinput" accept="video/*">
      <label for="subtitleinput">Add Subtitles:</label>
      <input type="file" id="subtitleinput" accept=".srt,.ass">
      <div class="col-sm-4" style="padding-left: 0">
        <input type="text" class="form-control" placeholder="Clip Name" id="clipname">
      </div>
      <button class="btn btn-secondary" @click="$emit('addSubtitles')">Add Subtitles</button>
      <br />
      <button class="btn btn-primary" @click="$emit('uploadVideo')">Upload</button>
    </div>
    <div class="progress" v-if="uploadprogress > 0">
      <div id="uploadprogress" class="progress-bar progress-bar-success" role="progressbar"
        :aria-valuenow="uploadprogress" aria-valuemin="0" aria-valuemax="100" :style="{ width: uploadprogress + '%' }">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['uploadprogress'],
};
</script>
