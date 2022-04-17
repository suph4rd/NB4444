<template>
  <div>
    <v-dialog
      v-model="dialogCreate"
      width="800"
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
        <h2 class="grey lighten-2 text-center">Создание задачи</h2>
          <v-form
            ref="form"
            @submit="validForm"
            :style="{'margin': '15px'}"
          >
            <v-text-field
              type="text"
              v-model="plan.name"
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
  import createMixin from "../../mixins/createMixin";

  export default {
    name: "TaskCreate",
    mixins: [header, createMixin],
    props: ['plan'],

    data () {
      return {
        sections: [],
        object: {
          plan:'',
          section: '',
          description: ''
        },
        createPath: '/api/v1/task/',
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
            "plan": this.$props.plan.id,
            "section": this.object.section,
            "description": this.object.description,
          }
      },
      resetForm() {
        this.reset();
      },
      validForm(e) {
        e.preventDefault();
        if (this.$refs.form.validate()){
          this.sendForm(e);
        }
      },
    },
    mounted() {
      this.getSections();
    }
  }
</script>