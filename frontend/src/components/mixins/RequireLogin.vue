<script>

export default {
    beforeCreate () {
	if (!this.$store.state.loggedIn) {
	    this.$router.push("/login")
	}
    }
}
</script>
