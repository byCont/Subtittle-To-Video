<template>
  <div class="col-sm-3">
    <button class="btn btn-success" @click="$emit('final-render')">Merge Clips</button>
  </div>
</template>

<script>
  export default {
    name: 'MergeClipsButton',
  };
</script>
