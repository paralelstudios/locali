import UserMessage from "./components/UserMessage.vue";

function Element (element) {
    return {
	name: "item-element",
	props: [element],
	template: '<button class="' + element + 'Element" :value="' + element + '.name" @click="select">' +
	    '<h4 class="' + element + 'Name">{{ ' + element + '.name }}</h4>' +
	    '<p class="' + element + 'Description">{{ ' + element + '.description }}</p>' +
	    '</button>',
	methods: {
	    select () {
		this.$emit("select", this[element]);
	    }
	}
    };
};

function List(items, item, endpoint, parameter) {
    return {
	data () {
	    return {
		userMessage: null,
		items: [ // {name: "", description: ""}
		],
		selectedItem: null
	    };
	},
	computed: {
	    parameter () {
		return parameter ? "/" + parameter + "/" + this.$route.params.name : "";
	    }
	},
	components: {
	    itemElement: Element(item),
	    UserMessage
	},
	template: '<section id="' + items + '"">' +
	    '<user-message v-if="userMessage" :message="userMessage"></user-message>' +
	    '<item-element v-else v-for="item in items" :key="item.name" :' + item + '="item" @select="select"></item-element>' +
	    '</section>',
	created () {
	    this.getItems();
	},
	methods: {
	    select (selectedItem) {
		this.$router.push(
		    {name: item,
		     params: {
			 name: selectedItem.name.toLowerCase().replace(" ", "_")
		     }}
		);
	    },
	    getItems () {
		var vm = this;
		this.$http.get("/api" + endpoint + this.parameter)
		    .then(function (resp) {
			vm.items = resp.data;
		    })
		    .catch(function (err) {
			vm.userMessage = {isError: true,
					  text: err.response.data.description ||
					  err.response.statusText};
		    });
	    }
	}
    };
};


function Item (item, endpoint) {
    return  {
	data () {
	    return {
		userMessage: null,
		item: {name: "",
			photo: "resources/imgs/paralel-logo.png",
			description: ""}
	    };
	},
	created () {
	    console.log("Creating " + item + " page");
	    this.getItem();
	},
	template: '<article class=' + item + '>' +
	    '<user-message v-if="userMessage" :message="userMessage"></user-message>' +
	    '<h2 class="' + item + 'Title">{{ item.name }}</h2><hr>' +
	    '<img class="' + item + 'Photo" :src="item.photo" :alt="item.name"/>' +
	    '<p class="' + item + 'Description">{{ item.description }}</p>' +
	    '</article>',
	methods: {
	    getItem () {
		console.log("get");
		var vm = this;
		this.$http.get("/api" + endpoint + "/" + this.$route.params.name)
		    .then(function (resp) {
			console.log("got");
			vm.item = resp.data;
		    })
		    .catch(function (err) {
			vm.userMessage = {isError: true,
					  text: err.response.data.description ||
					  err.response.statusText};
		    });
	    }
	}

    };
}

function PlaceItem () {
    var item = Item("place", "/places");
    item.data = function () {
	return {
	    item: {name: "",
		    primary_image: "",
		    description: "",
		    subplaces: [
			// {name: ""}
		    ],
		    plants: [
			// {name: ""}
		    ]}};
    };

    if (item.components) {
	item.components["plantElement"] = Element("plant");
	item.components["placeElement"] = Element("place");
    } else {
	item.components = {plantElement: Element("plant"),
			   placeElement: Element("place")};
    }
    item.methods.selectPlant = function (plant) {
	this.$router.push(
	    {name: 'plant',
	     params: {
		 name: plant.name.toLowerCase().replace(" ", "_")
	     }}
	);
    };
    item.methods.selectPlace = function (place) {
	this.$router.push(
	    {name: 'place',
	     params: {
		 name: place.name.toLowerCase().replace(" ", "_")}
	    }
	);
	this.getItem();

    };

    item.template = '<article class="place">' +
	'<h2 class="placeTitle">{{ item.name }}</h2><hr>' +
	'<img class="placePhoto" :src="item.primary_image" :alt="item.name"/>' +
	'<p class="placeDescription">{{ item.description }}</p>' +
	'<hr><h4 v-if="item.plants.length" >Local Plants</h4><hr>' +
	'<menu class="cityPlantList"><plant-element v-for="plant in item.plants" :key="plant.name" :plant="plant" @select="selectPlant"></plant-element></menu>' +
	'<hr><h4 v-if="item.subplaces.length" >Subplaces</h4><hr>' +
	'<menu class="cityPlaceList"><place-element v-for="place in item.subplaces" :key="place.name" :place="place" @select="selectPlace"></place-element></menu>' +
	'</article>';
    return item;
};


export { Element, List, Item, PlaceItem }
