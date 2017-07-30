<template>
  <button class="headerBtn" id="infoBtn" @mouseenter="mouseenter" @mouseleave="mouseleave"><span>{{ mouseOver ? "?" : "&#xbf;" }}</span></button>
</template>

<script>

export default {
    name: "info-button",
    data () {
	return { mouseOver: false };
    },
    methods: {
        mouseenter () { this.mouseOver = true; },
	mouseleave () { this.mouseOver = false; }
   }
}

</script>


<style scoped>

#infoBtn {
    margin-bottom: 1vh;
    font-size: 7vh;
    font-weight: 500;
}

</style>
