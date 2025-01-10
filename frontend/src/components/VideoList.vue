<template>
  <div>
    <div v-for="(video, index) in videos" :key="index" class="row videodiv">
      <div class="video-card-head">
        <input :disabled="true" type="text" :value="video.name" />
        <div>
          <i @click="() => {}" class="bi bi-pencil" style="font-size: 30px; color: green; cursor: pointer;"></i>
          <i @click="$emit('remove-video', index)" class="bi bi-trash" style="font-size: 30px; color: red; cursor: pointer; margin-left: 1rem;"></i>
        </div>
      </div>

      <div class="video-controls" style="margin-top: 1rem;">
        <button @click="$emit('set-render-video', index)" class="btn btn-success video-ctrl-btn">Render/Preview</button>
        <button class="btn btn-primary btn-sm video-ctrl-btn" @click="$emit('reload-original-video', index)">Reload Original Video</button>
      </div>

      <div class="align-center" style="margin-top: 50px;">
        <h4>Video Effects</h4>
        <b>Trim</b>
        <div class="form-group">
          <div class="col-sm-4">
            <label for="start">Start:</label>
            <input min="0" max="120" type="number" :id="`trim_start` + index" value="0">
          </div>
          <div class="col-sm-4">
            <label for="end">End:</label>
            <input min="0" max="120" type="number" :id="`trim_end` + index" value="0">
          </div>
          <div class="col-sm-3">
            <button class="btn btn-warning" @click="$emit('edit-video-submit', index, 'trim')">Trim</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'VideoList',
    props: {
      videos: Array,
    },
  };
</script>
