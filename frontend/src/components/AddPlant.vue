<template>
  <section class="addPage" id="addPlant">
    <form @submit.prevent="submit" :class="{spinning: sending}">
      <user-message v-if="userMessage" :message="userMessage"></user-message>
      <div class="form-block">
	<label for="name">What it called? *</label>
	<input type="text" name="name"
	       placeholder="Quenepa" v-model="name" required>
      </div>
      <div class="form-block">
	<label for="common-names">What else do people call it?</label>
	<input name="common-names"
	       placeholder="Manoncillo, ..." v-model="rawCommonNames">
      </div>
      <div class="form-block">
	<label for="scientific-names">What do scientists call it?</label>
	<input type="text" name="scientific-name"
	       placeholder="Melicoccus bijugatus, ..."
	       v-model="rawScientificNames">
      </div>
      <photo-drop name="flowerPhotos" ref="flowerPhotos"
		  drop-label="Any photos of its flowers?"></photo-drop>
      <photo-drop name="seedPhotos" ref="seedPhotos"
		  drop-label="Any photos of its seeds?"></photo-drop>
      <photo-drop name="leafPhotos" ref="leafPhotos"
		  drop-label="Any photos of its leaves?"></photo-drop>
      <photo-drop name="otherPhotos" ref="otherPhotos"
		  drop-label="Any other photos?"></photo-drop>
      <div class="form-block">
	<label for="plantType">What type is it?</label>
	<multiselect v-model="plantType" :options="plantTypes"
		     select-label="" name="plantType"
		     placeholder="Pick a type"
		     deselect-label="Remove"></multiselect>
      </div>
      <div v-if="placesReady" class="form-block">
	<label for="places">Where does it grow?</label>
	<multiselect v-model="rawPlaces" :options="possiblePlaces"
		     select-label="" :multiple="true"
		     :loading="!placesReady" name="places"
		     placeholder="Pick a place" label="name" track-by="name"
		     deselect-label="Remove"></multiselect>
      </div>
      <div class="form-block">
	<label for="uses">What uses does it have?</label>
	<multiselect v-model="uses" :options="possibleUses"
		     select-label="" name="uses"
		     placeholder="Pick uses" :multiple="true"
		     deselect-label="Remove"></multiselect>
      </div>
      <div class="form-block">
	<label for="substrates">On what does it grow?</label>
	<multiselect v-model="substrates" :options="possibleSubstrates"
		     select-label="" name="substrates"
		     placeholder="Pick substrates" :multiple="true"
		     deselect-label="Remove"></multiselect>
      </div>
      <div class="form-block">
	<label for="monthsAvailable">When is it in season?</label>
	<multiselect v-model="monthsAvailable" :options="possibleMonths"
		     :multiple="true" select-label=""
		     name="monthsAvailable"
		     placeholder="Pick months"
		     deselect-label="Remove"></multiselect>
      </div>
      <div class="form-block">
	<label for="description">What is it like?</label>
	<textarea name="description" placeholder="Dark green shell with a delicious orange pulp." required v-model="description">
	</textarea>
      </div>
      <div class="form-block">
	<button>Add Plant</button>
      </div>
    </form>
  </section>
</template>

<script>

import Multiselect from 'vue-multiselect'
import PhotoDrop from './PhotoDrop.vue'
import RequireLogin from './mixins/RequireLogin.vue'
import UserMessage from './UserMessage.vue'

export default {
    name: "add-plant",
    mixins: [RequireLogin],
    components: {
	Multiselect,
	PhotoDrop,
	UserMessage
    },
    computed: {
	placesReady () { return !!this.possiblePlaces.length },
	scientificNames () { return this.rawScientificNames.split(',').filter((x) => !!x).map((x) => x.trim()) },
	commonNames () { return this.rawCommonNames.split(',').filter((x) => !!x).map((x) => x.trim()) },
	places () { return this.rawPlaces.map((x) => x.name) }
    },
    data () {
	return {
	    sending: false,
	    userMessage: null,
	    uses: [],
	    monthsAvailable: [],
	    possibleUses: ["Medicine", "Food", "Other"],
	    plantTypes: ["Herb", "Shrub", "Tree", "Vine"],
	    possibleMonths: [
		"January", "February", "March", "April",
		"May", "June", "July", "August", "September",
		"October", "November", "December"],
	    plantType: '',
	    rawCommonNames: '',
	    rawScientificNames: '',
	    substrates: [],
	    possibleSubstrates: ["Marine", "Freshwater",
			 "Terrestial", "Lithophyte",
			 "Epiphyte", "Saprophyte",
			 "Parasite"],
	    possiblePlaces: [],
	    rawPlaces: [],
	    description: '',
	    name: '',
	};
    },
    created () {
	this.getPlaces();
    },
    methods: {
	addToData (property, form, transform) {
	    if (this[property]) {
		form.append('items[' + property + ']', transform ?
			    transform(this[property]) : this[property])
	    }
	},
	postData () {
	    const payload = {
		name: this.name,
		description :this.description,
		commonNames: this.commonNames,
		scientificNames: this.scientificNames,
		places: this.places,
		substrates: this.substrates,
		monthsAvailable: this.monthsAvailable,
		plantType: this.plantType,
		uses: this.uses
	    }
	    return this.$http.post("/api/plants", payload, {
		headers: {
		    'Authorization': "JWT " + localStorage.getItem('access_token'),
		    'Content-Type': 'application/json'
		}})

	},
	postPhotos () {
	    const formData = new FormData()

	    this.$refs.leafPhotos.photos.forEach(
		(photo) => formData.append('leafPhotos[]', photo.file, photo.name))
	    this.$refs.seedPhotos.photos.forEach(
		(photo) => formData.append('seedPhotos[]', photo.file, photo.name))
	    this.$refs.flowerPhotos.photos.forEach(
		(photo) => formData.append('flowerPhotos[]', photo.file, photo.name))
	    this.$refs.otherPhotos.photos.forEach(
		(photo) => formData.append('otherPhotos[]', photo.file, photo.name))
	    return this.$http.post(
		"/api/plants/" + this.name.replace(' ', '_') + "/photos", formData, {
		    headers: {
			'Authorization': "JWT " + localStorage.getItem('access_token'),
			'Content-Type': 'multipart/form-data'
		    }})
	},
	submit () {
	    let vm = this;
	    this.sending = true;
	    this.postData()
		.then(function (r) {
		    console.log("getting photos")
		    return vm.postPhotos()
		}).then(function(r) {
		    vm.sending = false;
		    vm.$router.push("/plants/" + vm.name)
		}).catch(function (err) {
		    vm.sending = false;
		    console.log(err.response)
		    vm.userMessage = {isError: true,
				      text: err.response.data.description ||
				      err.response.data.message ||
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
		});

	}
    }
}
</script>
<style src="vue-multiselect.min.css"></style>

<style scoped>

.multiselect__option--highlight {
    background-color: #4CAF50;
}
.multiselect__option--highlight > span {
    color: #fff;
}
.multiselect__option > span {
    color: #33691E;
}
</style>
