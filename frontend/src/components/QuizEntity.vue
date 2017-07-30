<template>
  <section id="entity">
    <img name="entityImg" :src="imageUrl">
  </section>
</template>

<script>
export default {
    props: ["imageUrl"]
}
</script>

<style scoped>
#entity {
    margin-top: 1.5vh;
}
#entity > img {
    height: 69vh;
    max-width: 95vw;
    border-radius: 5px;
}
</style>
