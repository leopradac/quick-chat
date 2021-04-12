import Vue from 'vue'
export function newMessage (state, payload) {
    console.log('mutation newMessage')
    const roomMessages = state.chats[payload.roomCode]
    roomMessages.push(payload)
    if (roomMessages.length > 50) {
        roomMessages.shift()
    }
}
export function updateActiveRoomCode (state, roomCode) {
    state.activeRoomCode = roomCode
}
export function cleanAll (state) {
    state.chats = {}
    state.conversations = []
    state.activeRoomCode = 'general_room'
}
export function cleanChat (state, roomCode) {
    state.chats[roomCode] = []
}
export function removeChat (state, roomCode) {
    if (!roomCode) { return }
    const index = state.conversations.findIndex(i => i.roomCode === roomCode)
    if (index >= 0) {
        state.conversations.splice(index - 1, 1)
    }
    delete state.chats[roomCode]
    state.activeRoomCode = ''
}
export function addConversation (state, conversation) {
    state.conversations.push(conversation)
    const roomCode = conversation.roomCode
    Vue.set(state.chats, roomCode, [])
    // state.chats[roomCode] = []
}
