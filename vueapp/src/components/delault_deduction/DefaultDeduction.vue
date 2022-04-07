<template>
  <v-container>
    <div class="deductions">
      <div v-if="deduction">
        <div>Дом:</div>
        <div>{{ deduction.house }}</div>
      </div>
      <div v-if="deduction">
        <div>Путешествия:</div>
        <div>{{ deduction.travel }}</div>
      </div>
      <div v-if="deduction">
        <div>Телефон:</div>
        <div>{{ deduction.phone }}</div>
      </div>
      <div v-if="deduction">
        <div>Еда:</div>
        <div>{{ deduction.food }}</div>
      </div>
    </div>
  </v-container>
</template>

<script>
  import header from "../../mixins/header";

  export default {
    name: 'DefaultDeduction',
    mixins: [header],

    data: function () {
      return {
        deduction: null,
        apiHost: location.origin,
      }
    },
    mounted() {
        this.getDefaultDeductions()
    },
    methods: {
      getDefaultDeductions() {
            let headers = this.getHeaders();
            this.axios.get(`${this.$apiHost}/api/v1/default-deduction/user_last/`, {
              headers: headers
            }).then((result) =>{
            this.deduction = result.data;
        }).catch((res) => {
          this.dropSession();
        })
      }
    }
  }
</script>

<style scoped>
  .deductions {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  .deductions div {
    display: flex;
  }
  .deductions div > div {
    margin-right: 10px;
  }
</style>
