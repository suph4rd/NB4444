<template>
  <v-app>

    <v-app-bar color="green accent-3" app>
      <v-app-bar-nav-icon v-if="this.$route.name !== 'Login' " @click="onLeftMenu"></v-app-bar-nav-icon>
      <v-col
      class="text-center"
    >
      <h1>БЧ</h1>
    </v-col>
    <v-col v-if="this.$route.name !== 'Login' " cols="2" class="text-end">
      <button @click="logout">Выход</button>
    </v-col>
    </v-app-bar>

    <v-navigation-drawer v-if="this.$route.name !== 'Login' " class="green accent-1" width="300px" v-model=leftMenu app>
      <router-link :to="{name: 'Main'}">
        <img src="../../media/ss.jpg" width="100%" height="65px" alt="">
      </router-link>

      <v-list>
        <v-list-item :href="this.$apiHost">
          <v-list-item-content>1.Старая версия
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-list>
        <v-list-item :to="{name: 'DefaultDeduction'}">
          <v-list-item-content>2.Стандартные вычеты
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-list>
        <v-list-item :to="{name: 'Note'}">
          <v-list-item-content>3.Заметки
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-list>
        <v-list-item :to="{name: 'PlanList'}">
          <v-list-item-content>4.Планы
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-list>
        <v-list-item @click="updateBotMessages">
          <v-list-item-content>5.Подгрузить заметки из телеграмм бота
          </v-list-item-content>
        </v-list-item>
      </v-list>

    </v-navigation-drawer>

    <!-- Sizes your content based upon application components -->
    <v-main class="blue-grey lighten-5">

      <!-- Provides the application the proper gutter -->
      <v-container fluid>

        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer padless class="green accent-4">
    <v-col
      class="text-center"
      cols="12"
    >
      <strong>© 2021 Andrey Bernyak</strong>
    </v-col>
  </v-footer>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: function () {
    return {
      leftMenu: false,
      apiHost: location.origin
    }
  },
  methods: {
    onLeftMenu(){
      this.leftMenu = !this.leftMenu
    },
    updateBotMessages(){
      this.axios.get(`${this.$apiHost}/api/v1/bot-response/`).then((result) =>{
        if (result.status === 200) {
          alert("Запрос на подгрузку записей успешно получен!")
        } else {
          alert("Ошибка отправки запроса!")
        }
      })
    },
    logout() {
      sessionStorage.removeItem('user');
      this.$router.push('login')
    }
  }
};
</script>

<style>
.main-content {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
</style>
