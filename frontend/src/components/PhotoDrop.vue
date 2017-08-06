<template>
  <div class="form-block">
    <label :for="name">{{ dropLabel }}</label>
    <file-upload class="dropzone" v-model="photos" :multiple="multiple"
		 accept="image/*"
		 @input-file="inputFile"
		 :name="name"
		 drop="Element"
		 :ref="ref">
      <div>
	<img v-for="photo in photos" :src="photo.blob" />
	<h4 v-if="!(!!photos.length)"><span class="primary">Drop or click</span> to add photos</h4>
      </div>
    </file-upload>
  </div>
</template>

<script>

import FileUpload from 'vue-upload-component'
export default {
    name: "photo-drop",
    props: ["name", "dropLabel"],
    data () {
	return {
	    photos: [],
	    multiple: true,
	    drop: true,
	    ref: "upload",
	};
    },
    components: {
	FileUpload
    },
    methods: {
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
}
</script>

<style scoped>
.dropzone {
    display: flex;
    border: 1px dashed #33691E;
    height: 15vh;
    width: 50vw;
    background-color: #C8E6C9;
    transition: all 0.5s ease;
    cursor: pointer;
    align-self: center;

}

.dropzone > div {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: scroll;
}
.dropzone h4, .dropzone span.primary {
    display: block;
    color: #33691E;
}
.dropzone span.primary {
    font-size: 3.5vh;
    margin-bottom: 1vh;
}
.dropzone img {
    max-height: 50%;
    max-width: 50%;
    margin-right: 1vw;
}

</style>
