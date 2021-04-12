<template>
  <q-page padding class="flex flex-center">
    <div class="row items-center">
      <div class="q-px-md">
        <q-card class="q-pa-lg">
          <q-card-section>
            <div class="text-h6 text-center">Existing account</div>
          </q-card-section>
          <q-card-section>
            <q-input v-model="loginUser" label="Username" outlined dense
            ></q-input>
          </q-card-section>
          <q-card-section>
            <q-input v-model="loginPassword" type="password" label="Password" outlined dense
            ></q-input>
          </q-card-section>
          <q-card-section class="text-center">
              <q-btn color="primary" @click="signin">Log in</q-btn>
          </q-card-section>
        </q-card >
      </div>
      <div class="q-px-md">
        <q-card class="q-pa-lg">
          <q-card-section>
            <div class="text-h6 text-center">New account</div>
          </q-card-section>
          <q-card-section>
            <q-input v-model="signupUser" label="Username" outlined dense
            ></q-input>
          </q-card-section>
          <q-card-section>
            <q-input v-model="signupPassword" type="password" label="Password" outlined dense
            ></q-input>
          </q-card-section>
          <q-card-section>
            <q-input v-model="signupPassword2" type="password" label="Repeat Password" outlined dense
            ></q-input>
          </q-card-section>
          <q-card-section class="text-center">
            <q-btn color="primary" @click="signup">Create account</q-btn>
          </q-card-section>
        </q-card >
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  // name: 'PageName',
  data() {
    return {
      loginUser: 'leoprada',
      loginPassword: '123456',
      signupUser: '',
      signupPassword: '',
      signupPassword2: ''
    }
  },
  computed: {
    username() {
      return this.$store.getters['auth/username'] 
    }
  },
  methods: {
    signin() {
      console.log('signin')
      const params = {
        username: this.loginUser,
        password: this.loginPassword
      }
      this.$api.post('/api/user/token/', JSON.stringify(params))
      .then(res => {
        console.log(res)
        const data = res.data
        data['username'] = this.loginUser
        this.$store.commit('auth/signedIn', data)
        this.$router.push({ name: 'chat' })
      }).catch(err => {
        console.log(err)
      })
    },
    signup() {
      console.log('signup')
      if (this.signupPassword !== this.signupPassword2) {
        console.log('Password does not match')
        return
      }
      const params = {
        username: this.signupUser,
        password: this.signupPassword,
        password2: this.signupPassword2
      }
      this.$api.post('/api/user/register/', JSON.stringify(params))
      .then(res => {
        console.log(res)
        const data = res.data
        data['username'] = this.signupUser
        this.$store.commit('auth/signedIn', data)
        this.$router.push({ name: 'chat' })
      }).catch(err => {
        console.log(err)
      })
    }
  },
}
</script>
