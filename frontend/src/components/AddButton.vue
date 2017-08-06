<template>
  <button @click="add" class="addBtn">+</button>
</template>

<script>

export default {
    name: "addbtn",
    methods: {
	add () { this.$emit("add") }
    }
}
</script>

<style scoped>
.addBtn {
    width: 75px;
    height: 75px;
    font-size: 3vh;
    text-align: center;
    vertical-align: middle;
    border-radius: 100%;
    position: absolute;
    bottom: 5vh;
    z-index: 10001;
    transition: all .5s ease;
    background-color: #43A047;
}

.addBtn:enabled:hover {
    background-color: #2E7D32;
}

</style>
