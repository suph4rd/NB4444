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
          this.axios.post( `${this.$apiHost}/auth/jwt/create/`, {
            "username": this.username,
            "password": this.password
          }).then((result) =>{
            if (result.status === 200) {
              let user = result.data
              sessionStorage.setItem('user', JSON.stringify(user));
              this.$router.push('/')
            } else {
              sessionStorage.removeItem('user');
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

