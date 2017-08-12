<template>
    <section class="elementView">
    <article>
      <user-message v-if="userMessage" :message="userMessage"></user-message>
      <h2>{{ item.primary_name }}</h2>

      <span class="alternativeNames">{{ item.scientific_names | commaJoin}}</span>
      <span class="alternativeNames" >{{ item.common_names | commaJoin }}</span>

      <hr>
      <section class="images" v-if="item.leaf_image_urls.length">
	<h3>Leaves</h3>
	<div class="image-gallery">
	  <img v-for="image in item.leaf_image_urls" v-img:leaf
	       :src="image" :alt="item.name" />
	</div>
      </section>
      <section class="images" v-if="item.flower_image_urls.length">
	<h3>Flowers</h3>
	<div class="image-gallery">
	  <img v-for="image in item.flower_image_urls" v-img:flower
	       :src="image" :alt="item.name" />
	</div>
      </section>
      <section class="images" v-if="item.seed_image_urls.length">
	<h3>Seeds</h3>
	<div class="image-gallery">
	  <img v-for="image in item.seed_image_urls" v-img:seed
	       :src="image" :alt="item.name" />
	</div>
      </section>
      <section class="images" v-if="item.other_image_urls.length">
	<h3>Other</h3>
	<div class="image-gallery">
	  <img v-for="image in item.other_image_urls" v-img:other
	       :src="image" :alt="item.name" />
	</div>
      </section>
      <hr>
      <section class="information">
	<ul class="attributes">
	  <li v-if="item.substrates.length"><span>Substrate:</span> {{ item.substrates | commaJoin }} </li>
	  <li v-if="item.uses.length"><span>Uses:</span> {{ item.uses | commaJoin }} </li>
	  <li v-if="item.months_available.length"><span>In Season:</span> {{ this.in_season ? "Yes!" : "No"}} </li>
	  <li v-if="item.months_available.length"><span>Months Available:</span> {{ item.months_available | toMonths | commaJoin }} </li>
	</ul>
      </section><hr>
      <p>{{ item.description }}</p><hr>
      <!-- related plants -->
      <section v-if="item.places.length" class="subelementList">
	<h3>Places</h3>
	<menu><item-element :element="place" v-for="place in item.places" :key="place.name" @select="selectPlace"></item-element></menu></section>
      <!-- farms with available supply -->
    </article>
  </section>

</template>


<script>

import Item from "./base/Item.vue";
import Element from "./base/Element.vue";


export default {
    extends: Item,
    name: "plant-item",
    components: {
	itemElement: Element,
    },
    filters: {
	commaJoin (val) {
	    if (!val || !val.length) return ''
	    return val.join(', ')
	},
	toMonths (val) {
	    if (!val || !val.length) return ''
	    return val.slice().sort().map((v) =>
			   new Date(v.toString())
			   .toLocaleString("en-us", {month: "long"}))
	},

    },
    computed: {
	in_season () {
	    return this.item.months_available.includes(
		new Date().getMonth() + 1
	    )
	}
    },
    data () {
     	return {
	    userMessage: null,
	    item_name: "plant",
	    endpoint: "/plants",
	    item: {
		primary_name: "",
		common_names: null,
		scientific_names: null,
		seed_image_urls: [],
		flower_image_urls: [],
		leaf_image_urls: [],
		other_image_urls: [],
		months_available: [],
		substrates: [],
		uses: [],
		description: "",
		places: [
		    // {name: ""}
		]
	    }
	}
    },
    methods: {
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

<style lang="scss" type="text/scss">
h2 {
    margin-bottom: 1vh;
}

.images > h3  {
    margin-bottom: 2vh;
    padding-left: 2.5%;
    font-weight: 500;
    font-size: 3.5vh;
}

.images ~ .images {
    margin-top: 2vh;
}
.alternativeNames {
    font-style: italic;
    padding-left: 2.5%;
}

.information {
    padding-left: 2.5%;
    .attributes {
	li  {
	    line-height: 125%;
	}
	li > span {
	    font-weight: 500;
	}
    }
}
</style>
