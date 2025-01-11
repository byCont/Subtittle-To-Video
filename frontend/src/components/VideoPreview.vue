// frontend/src/components/VideoPreview.vue

<template>
  <div class="col-lg-6">
    <div class="align-center row">
      <b>Video Render Preview</b><br />
      <div v-if="videoToRender" style="width: 100%; max-width: 100%;">
        <video :src="'http://localhost:5000/' + videoToRender" class="rounded-4" controls></video>
      </div>
      <div v-else>
        <div class="alert alert-warning">No video loaded</div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'VideoPreview',
    props: {
      videoToRender: String,
      originalVideos: Array,
    },
  };
</script>
