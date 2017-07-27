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
