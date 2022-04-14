<template>
  <div>
    <v-dialog
      v-model="dialogCreate"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <div class="text-end" style="margin: 15px">
        <v-btn
          color="red lighten-2"
          dark
          v-bind="attrs"
          v-on="on"
          style="{'position': 'absolute', 'right': '17%', 'top': '12%'}"
        >
          Создать
        </v-btn>
        </div>
      </template>

      <v-card>
        <h2 class="grey lighten-2 text-center">Создание плана</h2>
          <v-form
            ref="form"
            @submit="sendForm"
            :style="{'margin': '15px'}"
          >
            <v-text-field
              type="text"
              v-model="object.name"
              label="Название плана"
              required
            ></v-text-field>
            <v-select
              v-model="object.user"
              :items="users"
              label="Пользователь"
              item-text="username"
              item-value="id"
              required
            ></v-select>

            <v-divider></v-divider>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                text
                type="submit"
              >
                Создать
              </v-btn>
              <v-btn
                color="danger"
                text
                @click="reset"
              >
                Сбросить
              </v-btn>
              <v-btn
                color="secondary"
                text
                @click="dialogCreate = false"
              >
                Отмена
              </v-btn>
            </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import header from "../../mixins/header";

  export default {
    name: "PlanCreate",
    mixins: [header],

    data () {
      return {
        dialogCreate: false,
        users: [],
        object: {
          name: '',
          user: ''
        }
      }
    },
    methods: {
      reset () {
        this.$refs.form.reset()
      },
      getUsers() {
        let headers = this.getHeaders();
        this.axios.get(`${this.$apiHost}/api/v1/user/get_for_plan/`, {
          headers: headers
        }).then((result) =>{
          console.log(result.data)
          this.users = result.data;
        }).catch((res) => {
            this.dropSession(res);
        })
      },
      sendForm(e) {
        e.preventDefault();
        let headers = this.getHeaders();
        let data = {
            "name": this.object.name,
            "user": this.object.user
          }
          this.axios.post( `${this.$apiHost}/api/v1/plan/`, data, {
              headers: headers
            }).then((res) =>{
                this.object = {
                  name: '',
                  user: ''
                };
                this.dialogCreate = false;
                this.$emit('onCreate')
            }).catch((res) => {
            this.dropSession(res);
          })
      },
    },
    mounted() {
      this.getUsers();
    }
  }
</script>