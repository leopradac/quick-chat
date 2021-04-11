export function newMessage (state, payload) {
    const roomMessages = state.chats[payload.roomCode]
    roomMessages.push(payload)
    if (roomMessages.length > 50) {
        roomMessages.shift()
    }
}
export function updateActiveRoomCode (state, roomCode) {
    state.activeRoomCode = roomCode
}
// export function updateConversations (state, conversations) {
//     state.conversations = conversations
// }
export function addConversation (state, conversation) {
    state.conversations.push(conversation)
    const roomCode = conversation.roomCode
    state.chats[roomCode] = []
}
