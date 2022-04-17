export default {
  data: function () {
      return {
          createPath: null,
          dialogCreate: false,
          // обязательные параметры! this.$apiHost this.apiPath
      };
  },
  methods: {
    getFormParams() {
        throw "Not implemented";
      },
      resetForm() {
        throw "Not implemented";
      },
      sendForm(e) {
        e.preventDefault();
        let headers = this.getHeaders();
        let data = this.getFormParams();
          this.axios.post( `${this.$apiHost}${this.createPath}`, data, {
              headers: headers
            }).then((res) => {
                this.resetForm();
                this.dialogCreate = false;
                this.$emit('onCreate');
            }).catch((res) => {
            this.dropSession(res);
          });
      },
  }
}