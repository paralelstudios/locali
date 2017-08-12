import Vue from 'vue';
import VueRouter from 'vue-router';
import QuizService from "./components/QuizService.vue";
import Menu from "./components/Menu.vue";
import Info from "./components/Information.vue";
import Login from "./components/Login.vue";
import Profile from "./components/Profile.vue";
import AddPlant from "./components/AddPlant.vue";
import AddPlace from "./components/AddPlace.vue";
import PlaceList from "./components/PlaceList.vue";
import List from "./components/base/List.vue";
import PlaceItem from "./components/PlaceItem.vue";
import PlantItem from "./components/PlantItem.vue";

Vue.use(VueRouter);

const router = new VueRouter({
    mode: process.env.NODE_ENV === "production" ? 'history': '',
    routes: [
	{path: "/",
	 name: "menu",
	 component: Menu},
	{path: "/season",
	 name: "season",
	 component: List,
	 props: {name: "plants", endpoint: "/season",
		 select_route: "plant"}},
	{path: "/places",
	 name: "places",
	 component: List,
	 props: {name: "places", endpoint: "/places",
		 select_route: "place"}},
	{path: "/practice",
	 name: "practice",
	 component: QuizService},
	{path: "/plants",
	 name: "plants",
	 component: List,
	 props: {
	     name: "plants", endpoint: "/plants",
	     select_route: "plant"}},
	{path: "/places/:name",
	 name: "place",
	 component: PlaceItem},
	{path: "/plants/:name",
	 name: "plant",
	 component: PlantItem},
	{path: "/info",
	 name: "info",
	 component: Info},
	{path: "/profile",
	 name: "profile",
	 component: Profile},
	{path: "/login",
	 name: "login",
	 component: Login},
	{path: "/add/plants",
	 name: "add-plant",
	 component: AddPlant},
	{path: "/add/places",
	 name: "add-place",
	 component: AddPlace},
	{path: "*", redirect: "/"}
    ]
});


export default router;
