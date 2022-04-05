<template>
  <div :style="{'display': 'flex', 'justify-content': 'center'}">
  <v-form
    ref="form"
    v-model="valid"
    lazy-validation
    :style="{'width': '500px'}"
  >
    <v-text-field
      v-model="username"
      :counter="255"
      :rules="nameRules"
      label="Username"
      required
    ></v-text-field>

    <v-text-field
      v-model="password"
      label="Password"
      type="password"
      required
    ></v-text-field>


    <v-btn
      :disabled="!valid"
      color="success"
      class="mr-4"
      @click="login"
    >
      Login
    </v-btn>

    <v-btn
      color="error"
      class="mr-4"
      @click="reset"
    >
      Reset Form
    </v-btn>
  </v-form>
  </div>
</template>

<script>
  export default {
    name: 'Login',

    data: () => ({
      valid: true,
      username: '',
      password: '',
      nameRules: [
        v => !!v || 'Username is required',
        v => (v && v.length <= 255) || 'Name must be less than 255 characters',
      ],
    }),

    methods: {
      validate () {
        this.$refs.form.validate()
      },
      login() {
          this.axios.post( `${this.$apiHost}auth/jwt/create/`, {
            "username": this.username,
            "password": this.password
          }).then((result) =>{
            console.log(result.data)
            if (result.status === 200) {
              localStorage.setItem('user', JSON.stringify(result.data));
              this.$router.push('/')
            } else {
              alert("Ошибка отправки запроса!")
            }
        })
      },

      reset () {
        this.$refs.form.reset()
      },
    },
  }
</script>

<!--headers: {-->
<!--      Authorization: 'Bearer ' + token,-->
<!--   }-->
