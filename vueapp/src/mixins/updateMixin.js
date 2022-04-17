export default {
  data () {
    return {
      object: null,
      updatePath: null,
      dialogUpdate: false,
    };
  },

  methods: {
    getUpdatePath() {
        throw "Not implemented";
    },
    getFormParams() {
        throw "Not implemented";
    },
    resetForm() {
        throw "Not implemented";
    },
    showUpdateDialog() {
        this.dialogUpdate = true;
        this.getObject();
    },
    getObject() {
      let headers = this.getHeaders();
      this.axios.get(this.getUpdatePath(), {
        headers: headers
      }).then((result) =>{
        console.log(result.data);
        this.object = result.data;
      }).catch((res) => {
          this.dropSession(res);
      });
    },
    sendForm(e) {
      e.preventDefault();
      let headers = this.getHeaders();
      let data = this.getFormParams();
        this.axios.patch(this.getUpdatePath(), data, {
            headers: headers
          }).then((res) => {
              this.resetForm();
              this.dialogUpdate = false;
              this.$emit('onUpdate');
          }).catch((res) => {
          this.dropSession(res);
        });
    },
  },
}