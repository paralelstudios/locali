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
		items: [{name: "",
			      description: ""}],
		selectedItem: null
	    };
	},
	computed: {
	    parameter () {
		return parameter ? "/" + parameter + "/" + this.$route.params.name : "";
	    }
	},
	components: {
	    itemElement: Element(item)
	},
	template: '<section id="categories"">' +
	    '<item-element v-for="item in items" :key="item.name" :' + item + '="item" @select="select"></item-element>' +
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
			console.log(err);
 			vm.userMessage = {isError: true, text: err.message };
		    });
	    }
	}
    };
};


function Item (item, endpoint) {
    return  {
	data () {
	    return {
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
	    '<h2 class="' + item + 'Title">{{ item.name }}</h2><hr>' +
	    '<img class="' + item + 'Photo" :src="item.photo" :alt="item.name"/>' +
	    '<p class="' + item + 'Description">{{ item.description }}</p>' +
	    '</article>',
	methods: {
	    getItem () {
		var vm = this;
		this.$http.get("/api" + endpoint + "/" + this.$route.params.name)
		    .then(function (resp) {
			vm.item = resp.data;
		    })
		    .catch(function (err) {
			console.log(err);
 			vm.userMessage = {isError: true, text: err.message };
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
		   plants: [
		       // {name: ""}
		   ]}};
    };
    if (item.components) {
	item.components["itemElement"] = Element("plant");
    } else {
	item.components = {itemElement: Element("plant")};
    }
    item.methods.select = function (plant) {
	this.$router.push(
	    {name: 'plant',
	     params: {
		 name: plant.name.toLowerCase().replace(" ", "_")
	     }}
	);
    };
    item.template = '<article class="place">' +
	'<h2 class="placeTitle">{{ item.name }}</h2><hr>' +
	'<img class="placePhoto" :src="item.primary_image" :alt="item.name"/>' +
	'<p class="placeDescription">{{ item.description }}</p>' +
	'<hr><h4 v-if="item.plants.length" >Local Plants</h4><hr>' +
	'<menu class="cityPlantList"><item-element v-for="plant in item.plants" :key="plant.name" :plant="plant" @select="select"></item-element></menu>' +
	'</article>';
    return item;
};


export { Element, List, Item, PlaceItem }
