<template>
  <v-container>
    <v-row v-if="deduction">
      <v-col cols="2" offset="4">Дом:</v-col>
      <v-col>{{ deduction.house }}</v-col>
    </v-row>
    <v-row v-if="deduction">
      <v-col cols="2" offset="4">Путешествия:</v-col>
      <v-col>{{ deduction.travel }}</v-col>
    </v-row>
    <v-row v-if="deduction">
      <v-col cols="2" offset="4">Телефон:</v-col>
      <v-col>{{ deduction.phone }}</v-col>
    </v-row>
    <v-row v-if="deduction">
      <v-col cols="2" offset="4">Еда:</v-col>
      <v-col>{{ deduction.food }}</v-col>
    </v-row>
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
            this.axios.get(`${this.apiHost}/api/v1/default-deduction/user_last/`, {
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
