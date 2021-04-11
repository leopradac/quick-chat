export function getConversation(state) {
    return roomCode => {
        return state.chats[roomCode] || []
    }
}
