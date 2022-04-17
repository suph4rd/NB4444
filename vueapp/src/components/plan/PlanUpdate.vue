<template>
  <div>
    <v-dialog
      v-model="dialogUpdate"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
          <v-btn icon @click="showUpdateDialog">
            <v-icon
              class="mr-2"
            >
              mdi-pencil
            </v-icon>
          </v-btn>
      </template>

      <v-card>
        <h2 class="grey lighten-2 text-center">Обновление плана</h2>
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
                Отправить
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
                @click="dialogUpdate = false"
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
  import updateMixin from "../../mixins/updateMixin";

  export default {
    name: "PlanUpdate",
    mixins: [header, updateMixin],
    props: ['objId'],

    data () {
      return {
        users: [],
        object: {
          name: '',
          user: ''
        },
        updatePath: '/api/v1/plan/',
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
      getFormParams() {
        return {
            "name": this.object.name,
            "user": this.object.user
          }
      },
      resetForm() {
        this.reset();
      },
      getUpdatePath() {
        return `${this.$apiHost}${this.updatePath}${this.$props.objId}/`
      },
      showUpdateDialog() {
        this.dialogUpdate = true;
        this.getObject();
        this.getUsers();
      },
    },
  }
</script>