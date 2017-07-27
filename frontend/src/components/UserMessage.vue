<template>
  <div class="choice message" :class="{error: message.isError}">{{ message.text }}</div>
</template>

<script>
export default {
    name: "user-message",
    props: ["message"]
}
</script>
