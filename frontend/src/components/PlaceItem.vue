<template>
  <section class="elementView">
    <article>
      <user-message v-if="userMessage" :message="userMessage"></user-message>
      <h2>{{ item.name }}</h2><hr>
      <div class="image-gallery">
	<img v-for="image in item.image_urls" v-img:group
	     :src="image" :alt="item.name" />
      </div><hr>
      <p>{{ item.description }}</p><hr>
      <section v-if="item.plants.length" class="subelementList">
	<h3>Local Plants</h3>
	<menu><item-element :element="plant" v-for="plant in item.plants" :key="plant.name" :plant="plant" @select="selectPlant"></item-element></menu><hr></section>
      <section v-if="item.subplaces.length" class="subelementList">
	<h3>Subplaces</h3>
	<menu><item-element :element="place" v-for="place in item.subplaces" :key="place.name" @select="selectPlace"></item-element></menu></section>
    </article>
  </section>
</template>

<script>

import Item from "./base/Item.vue";
import Element from "./base/Element.vue";

export default {
    extends: Item,
    name: "place-item",
    components: {
	itemElement: Element
    },
    data () {
     	return {
	    userMessage: null,
	    item_name: "place",
	    endpoint: "/places",
	    item: {name: "",
		   image_urls: "",
		   description: "",
		   subplaces: [
		       // {name: ""}
		   ],
		   plants: [
		       // {name: ""}
		   ]}};
    },
    methods: {
	selectPlant (plant) {
	    this.$router.push(
		{name: 'plant',
		 params: {
		     name: plant.name.toLowerCase().replace(" ", "_")
		 }}
	    );
	},
	selectPlace (place) {
	    this.$router.push(
		{name: 'place',
		 params: {
		     name: place.name.toLowerCase().replace(" ", "_")}
		}
	    );
	    this.getItem();
	}
    }
}
</script>

<style>

</style>
