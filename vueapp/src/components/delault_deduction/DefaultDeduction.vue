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
  export default {
    name: 'DefaultDeduction',
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
            let user = JSON.parse(sessionStorage.getItem('user'));
            let headers = user ? {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${user.access}`,
            } : {};
            this.axios.get(`${this.$apiHost}/api/v1/default-deduction/user_last/`, {
              headers: headers
            }).then((result) =>{
            this.deduction = result.data;
        }).catch((res) => {
            sessionStorage.removeItem('user');
            this.$router.push('login');
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
