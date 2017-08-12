<template>
  <button class="element" :value="element.name" @click="select">
    <h4>{{ element.name }}</h4>
    <slot></slot>
  </button>
</template>

<script>

export default {
    name: "item-element",
    props: ["element"],
    methods: {
	select () {
	    this.$emit("select", this.element);
	}
    }
};
</script>

<style>
</style>
