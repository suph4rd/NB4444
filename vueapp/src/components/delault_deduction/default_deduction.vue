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
      <v-col>{{ deduction.food }}</v-col>>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'default_deduction',
    data: function () {
      return {
        deduction: null
      }
    },
    mounted() {
        this.getDefaultDeductions()
    },
    methods: {
      getDefaultDeductions() {
          this.axios.get(`${this.$apiHost}api/v1/get-default-deduction/`).then((result) =>{
            console.log(result.data)
            if (result.status === 200) {
              this.deduction = result.data
            } else {
              alert("Ошибка отправки запроса!")
            }
        })
      }
    }
  }
</script>
