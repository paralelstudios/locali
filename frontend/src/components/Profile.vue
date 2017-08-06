<template>
  <section class="elementView" id="profile">
    <article>
      <h2>Profile</h2>
      <hr>
      <p>You're a dipshit</p>
    </article>
  </section>
</template>

<script>

import RequireLogin from './mixins/RequireLogin.vue';

export default {
    name: "profile",
    mixins: [RequireLogin]
}

</script>


<style scoped>
#profileBtn {
    margin-top: 2vh;
    font-size: 5vh;
}
</style>
