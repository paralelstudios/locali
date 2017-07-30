import Vue from 'vue';
import VueRouter from 'vue-router';
import QuizService from "./components/QuizService.vue";
import Menu from "./components/Menu.vue";
import Info from "./components/Information.vue";
import Login from "./components/Login.vue";
import Profile from "./components/Profile.vue";
import { Element, List, Item, PlaceItem } from "./helpers";

Vue.use(VueRouter);

const router = new VueRouter({
    mode: process.env.NODE_ENV === "production" ? 'history': '',
    routes: [
	{path: "/season",
	 name: "season",
	 component: List("plants", "plant", "/season")},
	{path: "/places",
	 name: "places",
	 component: List("places", "place", "/places")},
	{path: "/practice",
	 name: "practice",
	 component: QuizService},
	{path: "/plants",
	 name: "plants",
	 component: List("plants", "plant", "/plants")},
	{path: "/places/:name",
	 name: "place",
	 component: PlaceItem()},
	{path: "/plants/:name",
	 name: "plant",
	 component: Item("plant", "/plants")},
	{path: "/info",
	 name: "info",
	 component: Info},
	{path: "/profile",
	 name: "profile",
	 component: Profile},
	{path: "/login",
	 name: "login",
	 component: Login},
	{path: "*", name: "menu", component: Menu},
    ]
});


export default router;
