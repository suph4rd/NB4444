<template>
  <div>
    <v-dialog
      v-model="dialogUpdate"
      width="800"
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
        <h2 class="grey lighten-2 text-center">Обновление задачи</h2>
          <v-form
            ref="form"
            @submit="validForm"
            :style="{'margin': '15px'}"
          >
            <v-checkbox
              v-model="object.is_ready"
              label="Готово"
              color="success"
            ></v-checkbox>

            <v-text-field
              type="text"
              v-model="object.plan.name"
              label="Название плана"
              disabled
            ></v-text-field>

            <v-textarea
              outlined
              v-model="object.description"
              rows="4"
              label="Описание"
              :rules="[v => !!v] || 'Обязательное поле!'"
              required
            ></v-textarea>

            <v-select
              v-model="object.section"
              :items="sections"
              label="Секция"
              item-text="name"
              item-value="id"
              :rules="[v => !!v] || 'Обязательное поле!'"
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
    name: "TaskUpdate",
    mixins: [header, updateMixin],
    props: ['objId'],

    data () {
      return {
        sections: [],
        object: {
          plan:'',
          section: '',
          description: '',
          is_ready: false
        },
        updatePath: '/api/v1/task/',
      }
    },
    methods: {
      reset () {
        this.$refs.form.reset()
      },
      getSections() {
        let headers = this.getHeaders();
        this.axios.get(`${this.$apiHost}/api/v1/section-list/`, {
          headers: headers
        }).then((result) =>{
          console.log(result.data)
          this.sections = result.data;
        }).catch((res) => {
            this.dropSession(res);
        })
      },
      getFormParams() {
        return {
            "plan": this.object.plan.id,
            "section": this.object.section.hasOwnProperty('id') ? this.object.section.id : this.object.section,
            "description": this.object.description,
            "is_ready": this.object.is_ready,
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
        this.getSections();
      },
      validForm(e) {
        e.preventDefault();
        if (this.$refs.form.validate()){
          this.sendForm(e);
        }
      },
    },
  }
</script>