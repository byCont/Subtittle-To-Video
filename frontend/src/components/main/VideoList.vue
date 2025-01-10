//frontend/src/components/VideoList.vue

<template>
  <div>
    <div v-for="(video, index) in videos" :key="index" class="videodiv">
      <div class="video-card-head">
        <input :disabled="true" type="text" :value="video.name" />
        <div>
          <i @click="$emit('removeVideo', index)" class="bi bi-trash" style="font-size: 30px; color: red; cursor: pointer; margin-left: 1rem;"></i>
        </div>
      </div>
      <div class="video-controls">
        <button class="btn btn-success video-ctrl-btn" @click="$emit('setRenderVideo', index)">Render/Preview</button>
        <button class="btn btn-primary btn-sm video-ctrl-btn" @click="$emit('reloadOriginalVideo', index)">Reload Original Video</button>
      </div>
      <VideoEffects :index="index" @editVideoSubmit="$emit('editVideoSubmit', index, 'trim')" />
    </div>
    <div v-if="videos.length > 0" class="col-sm-3">
      <button class="btn btn-success" @click="$emit('finalrender')">Merge Clips</button>
    </div>
  </div>
</template>

<script>
import VideoEffects from './VideoEffects.vue';

export default {
  props: ['videos'],
  components: { VideoEffects },
};
</script>
