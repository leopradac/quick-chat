<template>
  <q-page padding class="row">
    <div class="col-12 row justify-center">
      <div style="width: 100%; max-width: 400px">
        <!-- {{activeRoomCode}}   -->
        <q-chat-message
          v-for="(msg, index) in messages" :key="index"
          :name="msg.name"
          :text="[msg.message]"
          :sent="msg.sent"
          :stamp="msg.date | timeAgo"
          :bg-color="msg.name == 'BOT' ? 'blue' : ''"

        />
      </div>
    </div>
  </q-page>
</template>

<script>
import formatDistance from 'date-fns/formatDistance'
export default {
  name: 'PageIndex',
  data() {
    return {
      messages: []
    }
  },
  computed: {
    activeRoomCode: {
      get () {
        return this.$store.state.chat.activeRoomCode
      },
      set (value) {
        this.$store.commit('chat/updateActiveRoomCode', value)
      }
    }
  },
  filters: {
    timeAgo: function(value) {
      return formatDistance(new Date(value), Date.now())
    }
  },
  watch: {
    activeRoomCode: {
      immediate: true,
      deep: true,
      handler(newValue, oldValue) {
        console.log('newValue :', newValue)
        this.messages = this.$store.getters['chat/getConversation'](newValue)
        this.$nextTick(() => {
          this.$emit('scrollAllDown')
        })
      }
    }
  },
}
</script>
