<template>
  <div class="WAL position-relative bg-grey-4" :style="style">
    <q-layout view="lHh Lpr lFf" class="WAL__layout shadow-3" container>
      <q-header elevated>
        <q-toolbar class="bg-grey-3 text-black">
          <q-btn
            round
            flat
            icon="keyboard_arrow_left"
            class="WAL__drawer-open q-mr-sm"
            @click="leftDrawerOpen = true"
          />

          <q-btn round flat>
            <q-avatar color="primary" text-color="white">
              {{ currentConversation.roomName[0] }}
            </q-avatar>
          </q-btn>

          <span class="q-subtitle-1 q-pl-md">
            {{ currentConversation.roomName }}
          </span>

          <q-space/>

          <q-btn round flat icon="search" />
          <q-btn round flat>
            <q-icon name="attachment" class="rotate-135" />
          </q-btn>
          <q-btn round flat icon="more_vert">
            <q-menu auto-close :offset="[110, 0]">
              <q-list style="min-width: 150px">
                <q-item clickable>
                  <q-item-section>Contact data</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Block</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Select messages</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Silence</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Clear messages</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Erase messages</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </q-toolbar>
      </q-header>

      <q-drawer
        v-model="leftDrawerOpen"
        show-if-above
        bordered
        :breakpoint="690"
      >
        <q-toolbar class="bg-grey-3">
          <q-avatar class="cursor-pointer">
            <img src="https://cdn.quasar.dev/app-icons/icon-128x128.png" />
          </q-avatar>

          <q-space />

          <q-btn round flat icon="message" />
          <q-btn round flat icon="more_vert">
            <q-menu auto-close :offset="[110, 8]">
              <q-list style="min-width: 150px">
                <q-item clickable>
                  <q-item-section>New group</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Profile</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Archived</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Favorites</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Settings</q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Logout</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>

          <q-btn
            round
            flat
            icon="close"
            class="WAL__drawer-close"
            @click="leftDrawerOpen = false"
          />
        </q-toolbar>

        <q-toolbar class="bg-grey-2">
          <q-input
            rounded
            outlined
            dense
            class="WAL__field full-width"
            bg-color="white"
            v-model="search"
            placeholder="Join or start a new chat"
            @keyup.enter="addChannel(search)"
          >
            <template slot="append">
              <q-icon name="login" class="cursor-pointer" @click="addChannel(search)"/>
            </template>
          </q-input>
        </q-toolbar>

        <q-scroll-area style="height: calc(100% - 100px)" ref="scrollArea">
          <q-list>
            <q-item
              v-for="(conversation, index) in conversations"
              :key="index"
              :class="conversation.roomCode === activeRoomCode ? 'bg-green-2' : ''"
              clickable
              v-ripple
              @click="activeConversation(index)"
            >
              <q-item-section avatar>
                <q-avatar color="primary" text-color="white">
                  {{ conversation.roomName[0] }}
                </q-avatar>
              </q-item-section>

              <q-item-section>
                <q-item-label lines="1">
                  {{ conversation.roomName }}
                </q-item-label>
                <q-item-label class="conversation__summary" caption>
                  #
                  {{conversation.roomCode}}
                </q-item-label>
              </q-item-section>

              <q-item-section side>
                <q-item-label caption>
                  <!-- {{ conversation.time }} -->
                </q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>
      </q-drawer>

      <q-page-container class="bg-grey-2">
        <router-view @scrollAllDown="scrollAllDown" />
      </q-page-container>

      <q-footer>
        <q-toolbar class="bg-grey-3 text-black row">
          <q-btn round flat icon="insert_emoticon" class="q-mr-sm" />
          <q-input rounded outlined dense class="WAL__field col-grow q-mr-sm" bg-color="white" v-model="message" placeholder="Type a message" @keyup.enter="sendMessage(message)"/>
          <q-btn round flat icon="mic" />
        </q-toolbar>
      </q-footer>
    </q-layout>
  </div>
</template>

<script>
export default {
  name: 'WhatsappLayout',
  data () {
    return {
      username: 'realLeo',
      leftDrawerOpen: false,
      search: '',
      message: '',
      currentConversation: { roomName: '' },
      // currentConversationIndex: 0,
      sockets: {}
      // conversations: []
    }
  },
  methods: {
    scrollAllDown() {
      console.log('EMITED scrollAllDown', this.$refs.scrollArea)
      this.$refs.scrollArea.setScrollPercentage('1')
    },
    sendMessage(message) {
      const CHAT_SOCKET = this.sockets[this.activeRoomCode]
      CHAT_SOCKET.send(JSON.stringify({
        name: this.username,
        text: message,
        createdAt: Date.now()
      }))
      // Limpiamos el campo donde hemos escrito
      this.message = ''
    },
    activeConversation (index) {
      this.currentConversation = this.conversations[index]
      // this.currentConversationIndex = index
      this.activeRoomCode = this.conversations[index].roomCode
    },
    initSocket(roomCode) {
      const ROOM_SOCKET = new WebSocket('ws://localhost:9000/ws/chat/' + roomCode + '/');
        // Conectado
        ROOM_SOCKET.addEventListener('open', () => {
            console.log('Conectado');
        });
        // Desconectado
        ROOM_SOCKET.addEventListener('close', () => {
            console.log('Desconectado');
        });
        // Recibir mensaje
        ROOM_SOCKET.addEventListener('message', (event) => {
            this.addMessage(event, roomCode)
        })
        this.sockets[roomCode] = ROOM_SOCKET
    },
    addChannel(roomName) {
      if (roomName == '') return
      const roomCode = roomName.replaceAll(' ', '_').toLowerCase()
      const index = this.conversations.findIndex(conv => conv.roomCode == roomCode)
      console.log('roomName :', roomName)
      console.log('index :', index)
      if (index === -1) {
        this.initSocket(roomCode)
        const conv = {
            // id: 1,
            // ROOM_SOCKET: ROOM_SOCKET,
            roomName: roomName,
            roomCode: roomCode,
            // time: '15:00',
            sent: true
        }
        
        // this.conversations.push(conv)
        this.$store.commit('chat/addConversation', conv)
        this.activeConversation(this.conversations.length - 1)
      }
      else {
        console.log('room already exists')
      }
      this.search = ''
    },
    addMessage(event, roomCode) {
      console.log('Recibido nuevo mensaje');
          const newMessage = JSON.parse(event.data);
          const payload = {
            roomCode: roomCode,
            name: newMessage.name,
            message: newMessage.text,
            date: newMessage.createdAt,
            sent: newMessage.name === this.username
          }
          this.$store.commit('chat/newMessage', payload)
    }
  },
  computed: {
    // currentConversation () {
    //   return this.conversations.find(x => x.roomCode = this.activeRoomCode) || { roomName: '' }
    // },
    conversations: {
      get () {
        return this.$store.state.chat.conversations
      }
    },
    activeRoomCode: {
      get () {
        return this.$store.state.chat.activeRoomCode
      },
      set (value) {
        this.$store.commit('chat/updateActiveRoomCode', value)
      }
    },
    style () {
      return {
        height: this.$q.screen.height + 'px'
      }
    }
  },
  beforeMount () {
    this.addChannel('General Room')
  },
  mounted () {
    this.currentConversation = this.conversations.find(x => x.roomCode === this.activeRoomCode)
    for (const item of this.conversations) {
      this.initSocket(item.roomCode)
    }
    // this.sockets
  },
}
</script>

<style lang="sass">
.WAL
  width: 100%
  height: 100%
  padding-top: 20px
  padding-bottom: 20px
  &:before
    content: ''
    height: 127px
    position: fixed
    top: 0
    width: 100%
    background-color: #009688
  &__layout
    margin: 0 auto
    z-index: 4000
    height: 100%
    width: 90%
    max-width: 950px
    border-radius: 5px
  &__field.q-field--outlined .q-field__control:before
    border: none
  .q-drawer--standard
    .WAL__drawer-close
      display: none
@media (max-width: 850px)
  .WAL
    padding: 0
    &__layout
      width: 100%
      border-radius: 0
@media (min-width: 691px)
  .WAL
    &__drawer-open
      display: none
.conversation__summary
  margin-top: 4px
.conversation__more
  margin-top: 0!important
  font-size: 1.4rem
</style>