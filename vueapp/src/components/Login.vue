<template>
  <div :style="{'display': 'flex', 'justify-content': 'center'}">
  <v-form
    ref="form"
    v-model="valid"
    lazy-validation
    :style="{'width': '500px'}"
    @submit="login"
  >
    <v-text-field
      v-model="username"
      :rules="nameRules"
      label="Логин"
      required
    ></v-text-field>

    <v-text-field
      v-model="password"
      label="Пароль"
      type="password"
      required
    ></v-text-field>

    <v-btn
      :disabled="!valid"
      color="success"
      class="mr-4"
      type="submit"
    >Вход</v-btn>

    <v-btn
      color="error"
      class="mr-4"
      @click="reset"
    >Сброс</v-btn>
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
      login(e) {
          e.preventDefault();
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

