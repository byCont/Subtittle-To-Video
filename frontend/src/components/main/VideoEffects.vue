//frontend/src/components/VideoEffects.vue

<template>
  <div class="align-center">
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
        <button class="btn btn-warning" @click="$emit('editVideoSubmit')">Trim</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['index'],
};
</script>
