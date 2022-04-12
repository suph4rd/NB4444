<template>
  <v-container>
    <div class="main-content">
    <v-form
      ref="form"
      v-model="valid"
      lazy-validation
      :style="{'width': '95%'}"
      @submit="sendDefaultDeductions"
    >
    <v-text-field
      type="number"
      v-model="deduction.house"
      label="Дом"
      required
    ></v-text-field>
      <v-text-field
      type="number"
      v-model="deduction.travel"
      label="Путешествия"
      required
    ></v-text-field>
      <v-text-field
      type="number"
      v-model="deduction.phone"
      label="Телефон"
      required
    ></v-text-field>
      <v-text-field
      type="number"
      v-model="deduction.food"
      label="Еда"
      required
    ></v-text-field>

    <v-btn
      color="success"
      class="mr-4"
      type="submit"
    >Отправить</v-btn>
  </v-form>
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
        deduction: {
            "house": 0,
            "travel": 0,
            "phone": 0,
            "food": 0,
            "user": 0
          },
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
          this.dropSession(res);
        })
      },
      sendDefaultDeductions(e) {
            e.preventDefault();
            let headers = this.getHeaders();
            let data = {
              "house": this.deduction.house,
              "travel": this.deduction.travel,
              "phone": this.deduction.phone,
              "food": this.deduction.food,
              "user": this.deduction.user
            }
            this.axios.post(`${this.$apiHost}/api/v1/default-deduction/`, data, {
              headers: headers
            }).then((res) =>{
              this.getDefaultDeductions();
        }).catch((res) => {
          this.dropSession(res);
        })
      },
    }
  }
</script>

