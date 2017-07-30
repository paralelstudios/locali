<template>
  <div class="message" :class="{error: message.isError}">{{ message.text }}</div>
</template>

<script>
export default {
    name: "user-message",
    props: ["message"]
}
</script>

<style scoped>

.message {
    font-size: 5vh;
    justify-self: center;
    align-self: center;
    padding: 1vh;
    text-transform: capitalize;
    text-align: center;
    background-color: #43A047;
    border-radius: 10px;
    transition: all 0.5s ease;
}

.error {
    background-color: #F44336;
}

</style>
