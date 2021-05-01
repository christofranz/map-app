<template>
  <div class="row justify-content-center mb-3 text-center">
    <b-alert variant="danger" show>{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
  props: ['message'],
};
</script>