import UserMessage from "./components/UserMessage.vue";
import AddButton from "./components/AddButton.vue";
import router from "./router";

function Element (element) {
    return {
	name: "item-element",
	props: [element],
	template: '<button class="element" :value="' + element + '.name" @click="select">' +
	    '<h4>{{ ' + element + '.name }}</h4>' +
	    '<slot></slot>' +
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
	    UserMessage,
	    AddButton
	},
	template: '<section class="elementList">' +
	    '<user-message v-if="userMessage" :message="userMessage"></user-message>' +
	    '<item-element v-else v-for="item in items" :key="item.name" :' + item + '="item" @select="select"><p>{{ item.description }} </p></item-element>' +
	    '<add-button v-if="$store.state.loggedIn" @add="add"></add-button>' +
	    '</section>',
	created () {
	    this.getItems();
	},
	methods: {
	    add () { this.$router.push("/add/" + item); },
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
		item: {primary_name: "",
			photo: "resources/imgs/paralel-logo.png",
			description: ""}
	    };
	},
	created () {
	    console.log("Creating " + item + " page");
	    this.getItem();
	},
	template: '<section class="elementView">' +
	    '<article>' +
	    '<user-message v-if="userMessage" :message="userMessage"></user-message>' +
	    '<h2>{{ item.primary_name }}</h2><hr>' +
	    '<img :src="item.photo" :alt="item.name"/>' +
	    '<p>{{ item.description }}</p>' +
	    '</article>' +
	    '</section>',
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
		    image_urls: "",
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
			   placeElement: Element("place")}
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

    item.template = '<section class="elementView">' +
	'<article>' +
	'<h2>{{ item.name }}</h2><hr>' +
	'<div class="image-gallery">' +
	'<img v-for="image in item.image_urls" v-img:group  :src="image" :alt="item.name"/>' +
	'</div><hr>' +
	'<p>{{ item.description }}</p><hr>' +
	'<section v-if="item.plants.length" class="subelementList">' +
	'<h3>Local Plants</h3>' +
	'<menu ><plant-element v-for="plant in item.plants" :key="plant.name" :plant="plant" @select="selectPlant"></plant-element></menu><hr></section>' +
	'<section v-if="item.subplaces.length" class="subelementList">' +
	'<h3>Subplaces</h3>' +
	'<menu><place-element v-for="place in item.subplaces" :key="place.name" :place="place" @select="selectPlace"></place-element></menu></section>' +
	'</article>' +
	'</section>';
    return item;
};


export { Element, List, Item, PlaceItem }
