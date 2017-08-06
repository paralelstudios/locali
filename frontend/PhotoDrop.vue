<template>
  <div class="form-block">
    <label for="name">Any photos?</label>
    <file-upload class="dropzone" v-model="name" multiple="multiple"
		 accept="image/*"
		 @input-file="inputFile"
		 name="name"
		 drop="drop"
		 ref="ref">
      <div >
	<img v-for="photo in name" :src="photo.blob" />
	<label v-if="!(!!name.length)"><span class="primary">Drop or click</span> to add photos</label>
      </div>
    </file-upload>
  </div>
</template>

<script>

export default {
    name: "photo-drop",
    data () {
	return {
	    name: null,
	    multiple: false
	    drop: true
	    ref: "upload"
	};
    },
    inputFile (newFile, oldFile) {
	if (newFile && !oldFile) {
	    console.log('add', newFile)
	    var URL = window.URL || window.webkitURL
	    if (URL && URL.createObjectURL) {
		this.$refs.upload.update(newFile,
					 {blob: URL.createObjectURL(newFile.file)})
	    }
	}
    }
}
</script>

<style scoped>
.dropzone {
    display: flex;
    color: #33691E;
    border: 1px dashed #33691E;
    height: 15vh;
    width: 50vw;
    background-color: #C8E6C9;
    transition: all 0.5s ease;
}
.dropzone > div {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: scroll;
}
.dropzone img {
    max-height: 50%;
    max-width: 50%;
    margin-right: 1vw;
}

</style>
