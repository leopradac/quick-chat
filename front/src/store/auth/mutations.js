export function signedIn (state, payload) {
    state.user = payload
}
export function signOut (state, payload) {
    state.user = false
}
