<template>
  <section class="addPage" id="addPlace">
    <form @submit.prevent="submit" :class="{spinning: sending}">
      <user-message v-if="userMessage" :message="userMessage"></user-message>
      <div class="form-block">
	<label for="name">What's the area called? *</label>
	<input type="text" name="name"
	       placeholder="Santurce" v-model="name" required>
      </div>
      <div v-if="placesReady" class="form-block">
	<label for="places">Where is it?</label>
	<multiselect v-model="superplace" :options="possiblePlaces"
		     select-label=""
		     :loading="!placesReady" name="places"
		     placeholder="Pick a place" label="name" track-by="name"
		     deselect-label="Remove"></multiselect>
      </div>
      <photo-drop ref="photos" name="placePhotos" drop-label="Any photos?"></photo-drop>
      <div class="form-block">
	<label for="description">What is it like? *</label>
	<textarea required v-model="description" name="description" placeholder="Dark green shell with a delicious orange pulp.">
	</textarea>
      </div>
      <div class="form-block">
	<button>Add Place</button>
      </div>
    </form>
  </section>
</template>

<script>

import Multiselect from 'vue-multiselect'
import PhotoDrop from './PhotoDrop.vue'
import RequireLogin from './mixins/RequireLogin.vue'
import UserMessage from "./base/UserMessage.vue"

export default {
    name: "add-place",
    mixins: [RequireLogin],
    components: {
	Multiselect,
	PhotoDrop,
	UserMessage
    },
    computed: {
	placesReady () { return !!this.possiblePlaces.length }
    },
    created () {
	this.getPlaces();
    },
    data () {
	return {
	    sending: false,
	    name: null,
	    description: null,
	    userMessage: null,
	    possiblePlaces: [],
	    photos: [],
	    superplace: null
	}
    },
    methods: {
	submit () {
	    this.sending = true
	    const formData = new FormData()
	    formData.append('name', this.name)
	    if (this.superplace) {
		formData.append('superplace', this.superplace.name)
	    }
	    formData.append('description', this.description)
	    for (const photo of this.$refs.photos.photos) {
		formData.append(photo.name, photo.file)
	    }
	    let vm = this;
	    this.$http.post("/api/places", formData, {
		headers: {
		    'Authorization': "JWT " + localStorage.getItem('access_token'),
		    'Content-Type': 'multipart/form-data'
		}})
		.then(function (r) {
		    vm.sending = false;
		    vm.$router.push("/places/" + vm.name)
		})
		.catch(function (err) {
		    vm.sending = false;
		    vm.userMessage = {isError: true,
				      text: err.response.data.description ||
				      err.response.statusText};
		})
	},
	getPlaces () {
	    let vm = this;
	    this.$http.get("/api/places/names")
		.then(function (resp) {
		    vm.possiblePlaces = resp.data
		}).catch(function (err) {
		    console.log(err)
		})
	}
    }
}
</script>
<style src="vue-multiselect.min.css"></style>
<style>
.multiselect__option > span {
    color: #33691E;
}
.multiselect__option--highlight {
    background-color: #4CAF50;
}
.multiselect__option--highlight > span {
    color: #fff;
}

</style>
